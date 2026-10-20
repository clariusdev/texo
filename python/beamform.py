"""Delay-and-sum beamforming of Texo channel data.

Reads a Texo Download Raw package (.zip) holding per-channel RF (`_ch.raw`) and forms
an image from one of the example Channels Sequence captures:

- Channel walk (the default): one focused transmit from the centre element, received on
  every channel of the aperture. Beamforms the region around the transmit beam.
- Scan (`scan: true`): 24 adjacent scan lines, each a focused transmit received on all 32
  channels. Beamforms each line with dynamic receive focusing, like a B-mode image.
- Single element (`singleElement: true`): every element transmits and receives on its
  own. Beamforms the full width of the array (synthetic aperture).

All need `focusType: none` (the example default), so channels are stored as received,
and `storeRaw: true`. HD3 linear probes only.

    python beamform.py capture.zip --probe ../examples/probe/L15HD3/definition.yml
"""

import argparse
import re

import numpy as np

from capture import read_channels, read_probe


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


# receive channel of each event in the HD3 channel walk: 0, 16, 1, 17, ..., 15, 31
WALK_CHANNELS = np.ravel(np.column_stack((np.arange(16), np.arange(16, 32))))


def rx_channel(element):
    """HD3 receive channel of an element; the assignment repeats every 32 elements."""
    e = np.asarray(element)
    return 16 * (e % 2) + (e // 2) % 16


def line_elements(element, n=32):
    """Element held by each stored line of a channel walk centred on `element`.

    The walk's events receive channels 0, 16, 1, 17, ... of the 32 elements from
    element - 16, so the lines hold those elements in ascending order, rotated to start at
    the one on channel 0. Near the ends of the array the window runs past it; those
    elements fall outside 0 .. elements - 1 and their lines hold no echo.
    """
    window = element - n // 2 + np.arange(n)
    by_channel = dict(zip(rx_channel(window).tolist(), window.tolist()))
    return np.array([by_channel[c] for c in WALK_CHANNELS[:n]])


def scan_elements(meta, lines, n=32):
    """Transmit element of each scan line, from the `rx element` the metadata gives every line."""
    found = [int(v) for v in re.findall(r"rx element:\s*(-?\d+)", meta)]
    if len(found) != lines:
        raise ValueError(f"metadata lists {len(found)} line elements for {lines} lines")
    return np.array(found[::n])


def directivity(geo, dx, r, f0, c):
    """Element response at angle asin(dx / r); 1 everywhere if the element width is unknown."""
    if geo.width is None:
        return np.ones_like(r)
    sin = np.abs(dx) / np.maximum(r, 1e-12)
    return np.abs(np.sinc(geo.width * sin * f0 / c)) * np.sqrt(1 - sin ** 2)


def beamform_focused(frame, geo, acq, x, z, centre=None, fnumber=1.0, tx_fnumber=1.0):
    """Channels Sequence: focused transmit from `centre`, receive on each channel.

    The transmit is modelled as a virtual source at the focus: a pixel's transmit path is
    the focal depth plus (beyond the focus) or minus (before it) its distance to the focus.
    That model breaks down at the focus itself, so within the transmit depth of field the
    wavefront is treated as plane instead.
    """
    centre = geo.elements // 2 if centre is None else centre
    elements = line_elements(centre, frame.shape[0])

    X, Z = np.meshgrid(x, z)
    xs = geo.x(centre)
    to_focus = np.hypot(X - xs, Z - acq.focus)
    tx = acq.focus + np.where(Z >= acq.focus, to_focus, -to_focus)
    tx_fnumber = max(acq.focus / (geo.tx_channels * geo.pitch), tx_fnumber)
    depth_of_field = 7 * acq.c / acq.f0 * tx_fnumber ** 2
    tx = np.where(np.abs(Z - acq.focus) < depth_of_field / 2, Z, tx)

    image = np.zeros(X.shape, complex)
    for trace, element in zip(analytic(frame.astype(float)), elements):
        if not 0 <= element < geo.elements:
            continue
        dx = X - geo.x(element)
        rx = np.hypot(dx, Z)
        t = (tx + rx) / acq.c + 2 * geo.lens_time(acq.c)
        image += apodization(dx, Z, fnumber) * sample(trace, t, acq)
    return image


def beamform_synthetic(frame, geo, acq, x, z, fnumber=1.0):
    """Single element: every element transmits and receives alone (monostatic SAFT)."""
    X, Z = np.meshgrid(x, z)
    image = np.zeros(X.shape, complex)
    for element, trace in enumerate(analytic(frame.astype(float))):
        dx = X - geo.x(element)
        r = np.hypot(dx, Z)
        t = 2 * r / acq.c + 2 * geo.lens_time(acq.c)
        image += apodization(dx, Z, fnumber) * sample(trace, t, acq)
    return image


def beamform_scan(frame, geo, acq, elements, z, fnumber=1.0):
    """Scan: one image line per scan line, on its transmit axis, with dynamic receive focusing.

    Each pixel at depth z under scan line `el` sums every channel at its own two-way time,
    the transmit taken along the axis, weighted by a Hann window over the f-number aperture
    and the element directivity. Returns image[z, line].
    """
    n = geo.rx_channels
    image = np.zeros((len(z), len(elements)), complex)
    for i, el in enumerate(elements):
        block = analytic(frame[n * i:n * (i + 1)].astype(float))
        for trace, element in zip(block, line_elements(el, n)):
            if not 0 <= element < geo.elements:
                continue
            dx = geo.x(el) - geo.x(element)
            rx = np.hypot(dx, z)
            t = (z + rx) / acq.c + 2 * geo.lens_time(acq.c)
            weight = apodization(dx, z, fnumber) * directivity(geo, dx, rx, acq.f0, acq.c)
            image[:, i] += weight * sample(trace, t, acq)
    return image


def beamform(data, geo, acq, frame=0, depth=None, width=None, step=None, fnumber=1.0, meta=None):
    """Beamform one frame; picks the method from the number of stored lines.

    A scan (more lines than one walk) needs the package metadata, which gives each line's
    element; its image has one column per scan line, at the line positions returned in x.
    """
    lines = data.shape[1]
    single = lines == geo.elements
    scan = not single and lines > geo.rx_channels and lines % geo.rx_channels == 0
    if not (single or scan) and lines != geo.rx_channels:
        raise ValueError(f"{lines} lines matches neither the element count nor the receive channels")
    depth = depth or (acq.delay + data.shape[2]) / acq.fs * acq.c / 2 - geo.lens
    step = step or acq.c / acq.f0 / 4
    if scan:
        if meta is None:
            raise ValueError("a scan capture needs its metadata (meta=) for the line elements")
        elements = scan_elements(meta, lines, geo.rx_channels)
        z = np.arange(step, depth, step)
        return geo.x(elements), z, beamform_scan(data[frame], geo, acq, elements, z, fnumber)
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

    data, acq, meta = read_channels(args.package)
    geo = read_probe(args.probe)
    x, z, image = beamform(data, geo, acq, args.frame, fnumber=args.fnumber, meta=meta)
    half = (x[1] - x[0]) / 2 if len(x) > 1 else 0
    extent = [(x[0] - half) * 1e3, (x[-1] + half) * 1e3, z[-1] * 1e3, z[0] * 1e3]
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
