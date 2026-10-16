"""Delay-and-sum beamforming of Texo channel data.

Reads a Texo Download Raw package (.zip) holding per-channel RF (`_ch.raw`) and forms
an image from one of the two example sequences:

- Channels Sequence (`singleElement: false`): one focused transmit from the centre
  element, received on every channel of the aperture. Beamforms the region around
  the transmit beam.
- Single element (`singleElement: true`): every element transmits and receives on its
  own. Beamforms the full width of the array (synthetic aperture).

Both need `focusType: none` (the example default), so channels are stored as received,
and `storeRaw: true`. Linear probes only.

    python beamform.py capture.zip --probe ../examples/probe/L15HD3/definition.yml
"""

import argparse
import re
import zipfile
from dataclasses import dataclass

import numpy as np


@dataclass
class Geometry:
    elements: int
    pitch: float  # m
    lens: float  # m, lens thickness (adds to every path at the speed of sound)
    rx_channels: int = 32
    tx_channels: int = 64

    def x(self, element):
        """Lateral position of an element, the array centre at 0."""
        return (np.asarray(element, float) - (self.elements - 1) / 2) * self.pitch


@dataclass
class Acquisition:
    fs: float  # Hz
    delay: float  # samples before the first stored sample
    c: float  # m/s
    f0: float  # Hz, transmit frequency
    focus: float  # m, transmit focal depth
    platform: str


def read_raw(buf):
    """Return (header, timestamps, data[frames, lines, samples]) from a .raw file's bytes."""
    names = ("id", "frames", "lines", "samples", "sampleSize")
    hdr = dict(zip(names, np.frombuffer(buf, "<u4", 5).tolist()))
    frame_bytes = hdr["lines"] * hdr["samples"] * hdr["sampleSize"]
    rec = np.dtype([("ts", "<u8"), ("data", "u1", frame_bytes)])
    frames = np.frombuffer(buf, rec, hdr["frames"], offset=20)
    data = frames["data"].copy().view("<i2")
    return hdr, frames["ts"], data.reshape(hdr["frames"], hdr["lines"], hdr["samples"])


def number(text, key, default=None):
    """First number following `key:` in a metadata file."""
    m = re.search(rf"^\s*{re.escape(key)}:\s*([-+\d.eE]+)", text, re.M)
    if m:
        return float(m.group(1))
    if default is None:
        raise KeyError(f"'{key}' not found in metadata")
    return default


def read_channels(path):
    """Read the channel data and its metadata from a Download Raw package."""
    with zipfile.ZipFile(path) as z:
        raw = next(n for n in z.namelist() if n.endswith("_ch.raw"))
        meta = z.read(raw.removesuffix(".raw") + ".yml").decode()
        hdr, ts, data = read_raw(z.read(raw))
    platform = re.search(r"^\s*version:\s*(\S+)", meta, re.M)
    acq = Acquisition(
        fs=number(meta, "sampling rate") * 1e6,
        delay=number(meta, "delay samples", 0.0),
        c=number(meta, "vsound", 1540.0),
        f0=number(meta, "transmit frequency") * 1e6,
        focus=number(meta, "focal depth") * 1e-3,
        platform=platform.group(1) if platform else "v3",
    )
    return data, acq, meta


def read_probe(path):
    """Element count, pitch and lens thickness from a Texo probe definition."""
    text = open(path).read()
    return Geometry(
        elements=int(number(text, "elements")),
        pitch=number(text, "pitch") * 1e-6,
        lens=number(text, "lensThickness", 0.0) * 1e-3,
        rx_channels=int(number(text, "rx", 32)),
        tx_channels=int(number(text, "tx", 64)),
    )


def analytic(rf):
    """Analytic signal along the last axis (equivalent to scipy.signal.hilbert)."""
    n = rf.shape[-1]
    spec = np.fft.fft(rf - rf.mean(axis=-1, keepdims=True), axis=-1)
    h = np.zeros(n)
    h[0] = 1
    h[1:(n + 1) // 2] = 2
    if n % 2 == 0:
        h[n // 2] = 1
    return np.fft.ifft(spec * h, axis=-1)


def sample(sig, t, acq):
    """Interpolate a complex trace at round-trip times t, zero outside the record."""
    idx = t * acq.fs - acq.delay
    i0 = np.floor(idx).astype(int)
    frac = idx - i0
    valid = (i0 >= 0) & (i0 < sig.size - 1)
    i0 = np.clip(i0, 0, sig.size - 2)
    return np.where(valid, sig[i0] * (1 - frac) + sig[i0 + 1] * frac, 0)


def apodization(dx, z, fnumber):
    """Hann window across the receive aperture allowed by the f-number at each depth."""
    half = z / (2 * fnumber)
    return np.where(np.abs(dx) <= half, np.cos(np.pi * dx / (2 * half)) ** 2, 0)


def channel_order(n, platform):
    """Channel received by each stored line of the Channels Sequence."""
    if platform != "v1" and n == 32:  # channelWalk32Alt: 0, 16, 1, 17, ...
        return np.ravel(np.column_stack((np.arange(16), np.arange(16, 32))))
    return np.arange(n)


def beamform_focused(frame, geo, acq, x, z, centre=None, fnumber=1.0, tx_fnumber=1.0):
    """Channels Sequence: focused transmit from `centre`, receive on each channel.

    The transmit is modelled as a virtual source at the focus: a pixel's transmit path is
    the focal depth plus (beyond the focus) or minus (before it) its distance to the focus.
    That model breaks down at the focus itself, so within the transmit depth of field the
    wavefront is treated as plane instead.
    """
    centre = geo.elements // 2 if centre is None else centre
    lines = frame.shape[0]
    channels = np.empty_like(frame)
    channels[channel_order(lines, acq.platform)] = frame
    elements = centre - geo.rx_channels // 2 + np.arange(lines)

    X, Z = np.meshgrid(x, z)
    xs = geo.x(centre)
    to_focus = np.hypot(X - xs, Z - acq.focus)
    tx = acq.focus + np.where(Z >= acq.focus, to_focus, -to_focus)
    tx_fnumber = max(acq.focus / (geo.tx_channels * geo.pitch), tx_fnumber)
    depth_of_field = 7 * acq.c / acq.f0 * tx_fnumber ** 2
    tx = np.where(np.abs(Z - acq.focus) < depth_of_field / 2, Z, tx)

    image = np.zeros(X.shape, complex)
    for trace, element in zip(analytic(channels.astype(float)), elements):
        dx = X - geo.x(element)
        rx = np.hypot(dx, Z)
        t = (tx + rx + 2 * geo.lens) / acq.c
        image += apodization(dx, Z, fnumber) * sample(trace, t, acq)
    return image


def beamform_synthetic(frame, geo, acq, x, z, fnumber=1.0):
    """Single element: every element transmits and receives alone (monostatic SAFT)."""
    X, Z = np.meshgrid(x, z)
    image = np.zeros(X.shape, complex)
    for element, trace in enumerate(analytic(frame.astype(float))):
        dx = X - geo.x(element)
        r = np.hypot(dx, Z)
        t = 2 * (r + geo.lens) / acq.c
        image += apodization(dx, Z, fnumber) * sample(trace, t, acq)
    return image


def beamform(data, geo, acq, frame=0, depth=None, width=None, step=None, fnumber=1.0):
    """Beamform one frame; picks the method from the number of stored lines."""
    single = data.shape[1] == geo.elements
    if not single and data.shape[1] != geo.rx_channels:
        raise ValueError(f"{data.shape[1]} lines matches neither the element count nor the receive channels")
    depth = depth or (acq.delay + data.shape[2]) / acq.fs * acq.c / 2 - geo.lens
    step = step or acq.c / acq.f0 / 4
    if width is None:
        width = geo.elements * geo.pitch if single else geo.rx_channels * geo.pitch
    half = int(width / 2 / step)
    x = np.arange(-half, half + 1) * step
    z = np.arange(step, depth, step)
    if single:
        image = beamform_synthetic(data[frame], geo, acq, x, z, fnumber)
    else:
        image = beamform_focused(data[frame], geo, acq, x, z, fnumber=fnumber)
    return x, z, image


def bmode(image, dynamic_range=50):
    """Log-compressed envelope in dB, 0 at the peak."""
    env = np.abs(image)
    return np.maximum(20 * np.log10(env / env.max() + 1e-12), -dynamic_range)


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("package", help="Download Raw .zip holding _ch.raw")
    parser.add_argument("--probe", required=True, help="probe definition.yml from examples/probe")
    parser.add_argument("--frame", type=int, default=0)
    parser.add_argument("--fnumber", type=float, default=1.0, help="receive f-number")
    parser.add_argument("--range", type=float, default=50, help="display dynamic range (dB)")
    parser.add_argument("--save", help="write the image to this file instead of showing it")
    args = parser.parse_args()

    import matplotlib.pyplot as plt

    data, acq, _ = read_channels(args.package)
    geo = read_probe(args.probe)
    x, z, image = beamform(data, geo, acq, args.frame, fnumber=args.fnumber)
    extent = [x[0] * 1e3, x[-1] * 1e3, z[-1] * 1e3, z[0] * 1e3]
    plt.imshow(bmode(image, args.range), cmap="gray", extent=extent, aspect="equal")
    plt.xlabel("lateral (mm)")
    plt.ylabel("depth (mm)")
    plt.colorbar(label="dB")
    if args.save:
        plt.savefig(args.save, dpi=150, bbox_inches="tight")
    else:
        plt.show()


if __name__ == "__main__":
    main()
