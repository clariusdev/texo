"""Reading and writing Texo raw data packages and probe definitions."""

import re
import zipfile
from dataclasses import dataclass

import numpy as np

# header id for each raw type in 13.1; readers should decide the format from sampleSize
RAW_IDS = {"iq": 0, "env": 1, "env_sc": 2, "env_m": 3, "rf": 4, "ch": 5}


@dataclass
class Geometry:
    elements: int
    pitch: float  # m
    lens: float  # m, lens thickness
    rx_channels: int = 32
    tx_channels: int = 64
    kind: str = "linear"
    radius: float = 0.0  # m, curved probes
    width: float | None = None  # m, element width (kerf = pitch - width); None if unknown
    lens_c: float | None = None  # m/s, speed of sound in the lens; None if unknown
    height: float | None = None  # m, element height (elevation)
    elevation_focus: float | None = None  # m
    low_freq: float | None = None  # Hz
    centre_freq: float | None = None  # Hz
    upper_freq: float | None = None  # Hz
    measured_freq: float | None = None  # Hz, measured -6 dB pulse-echo centre frequency
    bandwidth: float | None = None  # measured -6 dB fractional bandwidth (0.8 = 80%)

    def x(self, element):
        """Lateral position of an element on a linear array, the array centre at 0."""
        return (np.asarray(element, float) - (self.elements - 1) / 2) * self.pitch

    def lens_time(self, c):
        """One-way travel time through the lens; tissue speed if the lens speed is unknown."""
        return self.lens / (self.lens_c or c)

    @property
    def kerf(self):
        return None if self.width is None else self.pitch - self.width


@dataclass
class Acquisition:
    fs: float  # Hz
    delay: float  # samples before the first stored sample
    c: float  # m/s
    f0: float  # Hz, transmit frequency
    focus: float  # m, transmit focal depth
    platform: str = "v3"


def number(text, key, default=None):
    """First number following `key:` in a metadata or definition file (commented lines skipped)."""
    m = re.search(rf"^[ \t]*{re.escape(key)}:[ \t]*([-+\d.eE]+)", text, re.M)
    if m:
        return float(m.group(1))
    if default is None:
        raise KeyError(f"'{key}' not found")
    return default


def optional(text, key, scale):
    value = number(text, key, float("nan"))
    return None if np.isnan(value) else value * scale


def read_raw(buf, dtype="<i2"):
    """Return (header, timestamps, data[frames, lines, samples]) from a .raw file's bytes."""
    names = ("id", "frames", "lines", "samples", "sampleSize")
    hdr = dict(zip(names, np.frombuffer(buf, "<u4", 5).tolist()))
    frame_bytes = hdr["lines"] * hdr["samples"] * hdr["sampleSize"]
    rec = np.dtype([("ts", "<u8"), ("data", "u1", frame_bytes)])
    frames = np.frombuffer(buf, rec, hdr["frames"], offset=20)
    data = frames["data"].copy().view(dtype)
    return hdr, frames["ts"], data.reshape(hdr["frames"], hdr["lines"], -1)


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
    """Geometry and transducer properties from a Texo probe definition."""
    text = open(path).read()
    kind = re.search(r"^\s*type:\s*(\w+)", text, re.M)
    return Geometry(
        elements=int(number(text, "elements")),
        pitch=number(text, "pitch") * 1e-6,
        lens=number(text, "lensThickness", 0.0) * 1e-3,
        rx_channels=int(number(text, "rx", 32)),
        tx_channels=int(number(text, "tx", 64)),
        kind=kind.group(1) if kind else "linear",
        radius=number(text, "radius", 0.0) * 1e-3,
        width=optional(text, "elementWidth", 1e-6),
        lens_c=optional(text, "lensSpeedOfSound", 1.0),
        height=optional(text, "elevationHeight", 1e-3),
        elevation_focus=optional(text, "elevationFocus", 1e-3),
        low_freq=optional(text, "lowFreq", 1e6),
        centre_freq=optional(text, "centerFreq", 1e6),
        upper_freq=optional(text, "upperFreq", 1e6),
        measured_freq=optional(text, "measuredCenterFreq", 1e6),
        bandwidth=optional(text, "bandwidth", 0.01),
    )


def write_capture(path, data, geo, acq, kind="ch", depth=None, timestamps=None, time="2026-01-01T00-00-00+0000",
                  line_elements=None):
    """Write data[frames, lines, samples] (or one [lines, samples] frame) as a Download Raw package.

    Use it to save simulated or processed data in the same format Texo captures, so the
    same readers apply. `acq.delay` is the number of samples between the transmit and the
    first sample in `data`. Values are stored as int16, so scale them first. `line_elements`
    gives each line's transmit element, as a scan's metadata lists them.
    """
    data = np.asarray(data)
    if data.ndim == 2:
        data = data[None]
    frames = np.clip(np.round(data), -32768, 32767).astype("<i2")
    timestamps = np.arange(len(frames), dtype="<u8") if timestamps is None else np.asarray(timestamps, "<u8")
    header = np.array([RAW_IDS[kind], *frames.shape, 2], "<u4").tobytes()
    raw = header + b"".join(t.tobytes() + f.tobytes() for t, f in zip(timestamps, frames))
    depth = depth if depth is not None else (acq.delay + frames.shape[2]) / acq.fs * acq.c / 2 - geo.lens
    probe = f"\nprobe:\n  version: {acq.platform}\n  elements: {geo.elements}\n  pitch: {geo.pitch * 1e6:g}"
    if geo.radius:
        probe += f"\n  radius: {geo.radius * 1e3:g}"
    if geo.width is not None:
        probe += f"\n  element width: {geo.width * 1e6:g}"
    probe += f"\n  lens thickness: {geo.lens * 1e3:g}"
    if geo.lens_c is not None:
        probe += f"\n  lens speed of sound: {geo.lens_c:g}"
    meta = (
        "# raw data parameters\n"
        f"\nsoftware version: simulated\niso time/date: {time}{probe}"
        f"\nframes: {len(frames)}\nframe rate: 10.00 Hz"
        f"\ntransmit frequency: {acq.f0 / 1e6:.2f} MHz"
        f"\nimaging depth: {depth * 1e3:.2f} mm\nfocal depth: {acq.focus * 1e3:.2f} mm"
        "\nauto gain: off\ntgc: \n"
        f"size: {{samples per line: {frames.shape[2]}, number of lines: {frames.shape[1]}, sample size: 2 bytes}}\n"
        f"sampling rate: {acq.fs / 1e6:g} MHz\ndelay samples: {acq.delay:g}\nvsound: {acq.c:g} m/s\n"
    )
    if line_elements is not None:
        meta += "lines:\n" + "".join(f"  - {{rx element: {e},tx element: {e},angle: 0 °}}\n" for e in line_elements)
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr(f"{time}_{kind}.raw", raw)
        z.writestr(f"{time}_{kind}.yml", meta)
