"""Simulated Texo channel data, for checking beamform.py without a probe.

Writes Download Raw packages in the Texo format holding point scatterers, as the two
example sequences would record them on a linear probe:

- channels.zip: focused transmit from the centre element (each element fired with its
  own focusing delay), received on 32 channels in channelWalk32Alt order.
- single.zip: every element transmits and receives alone.

    python simulate.py --probe ../examples/probe/L15HD3/definition.yml --check
"""

import argparse

import numpy as np

import beamform as bf
from capture import Acquisition, read_channels, read_probe, write_capture


def pulse(t, f0, cycles=2.0):
    """Gaussian-windowed tone burst centred on t = 0."""
    sigma = cycles / f0 / 2.355
    return np.exp(-0.5 * (t / sigma) ** 2) * np.cos(2 * np.pi * f0 * t)


def directivity(geo, dx, r, f0, c):
    """Element response at angle asin(dx / r); 1 everywhere if the element width is unknown."""
    if geo.width is None:
        return np.ones_like(r)
    sin = dx / r
    return np.sinc(geo.width * sin * f0 / c) * np.sqrt(1 - sin ** 2)


def timing(geo, acq_c, fs, depth):
    """Delay samples and stored sample count, as the probe sets them for a 0 cm start."""
    delay = round(2 * geo.lens / acq_c * fs)
    end = round(2 * (geo.lens + depth) / acq_c * fs)
    return delay, int(np.ceil((end - delay) / 16) * 16)


def simulate_focused(geo, acq, samples, points, tx_apt=64, fnumber=1.0):
    centre = geo.elements // 2
    t = (np.arange(samples) + acq.delay) / acq.fs
    half = min(tx_apt / 2, acq.focus / fnumber / geo.pitch / 2)
    tx_el = np.arange(geo.elements)[np.abs(np.arange(geo.elements) - centre) <= half]
    xs = geo.x(centre)
    fire = (acq.focus - np.hypot(geo.x(tx_el) - xs, acq.focus)) / acq.c
    rx_el = centre - geo.rx_channels // 2 + np.arange(geo.rx_channels)
    channels = np.zeros((geo.rx_channels, samples))
    for px, pz in points:
        to_tx = np.hypot(geo.x(tx_el) - px, pz)
        tx_gain = directivity(geo, px - geo.x(tx_el), to_tx, acq.f0, acq.c)
        for k, e in enumerate(rx_el):
            back = np.hypot(geo.x(e) - px, pz)
            rx_gain = directivity(geo, px - geo.x(e), back, acq.f0, acq.c)
            arrive = fire + (to_tx + back) / acq.c + 2 * geo.lens_time(acq.c)
            channels[k] += (tx_gain * pulse(t[:, None] - arrive, acq.f0)).sum(axis=1) * rx_gain / back
    return channels[bf.channel_order(geo.rx_channels, acq.platform)]


def simulate_single(geo, acq, samples, points):
    t = (np.arange(samples) + acq.delay) / acq.fs
    out = np.zeros((geo.elements, samples))
    for px, pz in points:
        dx = px - geo.x(np.arange(geo.elements))
        r = np.hypot(dx, pz)
        gain = directivity(geo, dx, r, acq.f0, acq.c) ** 2 / r
        out += gain[:, None] * pulse(t - 2 * r[:, None] / acq.c - 2 * geo.lens_time(acq.c), acq.f0)
    return out


def to_counts(lines, noise=0.01, seed=0):
    """Scale to the 14-bit range of channel data and add noise."""
    rng = np.random.default_rng(seed)
    lines = lines / np.abs(lines).max() + noise * rng.standard_normal(lines.shape)
    return np.clip(lines * 4000, -8192, 8191)


def peak_near(x, z, image, px, pz, window=1.5e-3):
    """Position of the brightest pixel within `window` of a target."""
    X, Z = np.meshgrid(x, z)
    env = np.where((np.abs(X - px) < window) & (np.abs(Z - pz) < window), np.abs(image), 0)
    iz, ix = np.unravel_index(env.argmax(), env.shape)
    return x[ix], z[iz]


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--probe", required=True, help="probe definition.yml from examples/probe")
    parser.add_argument("--depth", type=float, default=30, help="imaging depth (mm)")
    parser.add_argument("--check", action="store_true", help="beamform the packages and report target errors")
    args = parser.parse_args()

    geo = read_probe(args.probe)
    depth = args.depth * 1e-3
    c, fs = 1540.0, 60e6
    delay, samples = timing(geo, c, fs, depth)
    acq = Acquisition(fs=fs, delay=delay, c=c, f0=10e6, focus=depth / 2, platform="v3")

    focused_points = [(1.5e-3, 8e-3), (0.0, depth / 2), (-1.5e-3, 20e-3), (0.0, 25e-3)]
    single_points = [(-8e-3, 10e-3), (0.0, depth / 2), (6e-3, 20e-3), (-3e-3, 25e-3)]
    write_capture("channels.zip", to_counts(simulate_focused(geo, acq, samples, focused_points)), geo, acq, depth=depth)
    write_capture("single.zip", to_counts(simulate_single(geo, acq, samples, single_points)), geo, acq, depth=depth)
    print("wrote channels.zip and single.zip")

    if args.check:
        for path, points in (("channels.zip", focused_points), ("single.zip", single_points)):
            data, acq_read, _ = read_channels(path)
            x, z, image = bf.beamform(data, geo, acq_read, step=25e-6)
            for px, pz in points:
                fx, fz = peak_near(x, z, image, px, pz)
                print(f"{path}: target ({px * 1e3:+.2f}, {pz * 1e3:.2f}) mm -> "
                      f"error ({(fx - px) * 1e6:+.0f}, {(fz - pz) * 1e6:+.0f}) um")


if __name__ == "__main__":
    main()
