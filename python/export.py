"""Export a Texo probe and transmit to ultrasound simulators.

Gives the probe's transducer and the example sequences' transmits in the form Field II
and PyMUST (MUST) expect, so simulations use the same array, timing and focusing as a
capture. Simulated RF can be saved as a Texo capture with `capture.write_capture`, and
then read and beamformed like data from a probe.

    python export.py ../examples/probe/L15HD3/definition.yml --field2 l15.m
    python export.py ../examples/probe/L15HD3/definition.yml --pymust

Element width is needed for both simulators. Where the probe definition doesn't give it
yet, pass `--width` (µm) to state your own assumption.
"""

import argparse
import json

import numpy as np

from capture import read_probe


def transducer(geo, width=None):
    """The probe as plain numbers, in SI units."""
    width = width or geo.width
    if width is None:
        raise ValueError("element width unknown; set elementWidth in the probe definition or pass a width")
    # prefer the measured pulse-echo band; otherwise approximate it from the probe's frequency range
    centre = geo.measured_freq or geo.centre_freq
    bandwidth = geo.bandwidth
    if bandwidth is None and geo.low_freq and geo.upper_freq and centre:
        bandwidth = (geo.upper_freq - geo.low_freq) / centre
    return {
        "kind": geo.kind,
        "elements": geo.elements,
        "pitch": geo.pitch,
        "width": width,
        "kerf": geo.pitch - width,
        "height": geo.height,
        "elevation_focus": geo.elevation_focus,
        "radius": geo.radius,
        "centre_freq": centre,
        "fractional_bandwidth": bandwidth,
        "lens_thickness": geo.lens,
        "lens_speed_of_sound": geo.lens_c,
    }


def focused_delays(geo, focus, c=1540.0, element=None, fnumber=1.0):
    """Transmit delays (s) of the Channels Sequence: focused at `focus` from `element`.

    Returns (elements, delays); delay 0 is the centre element, outer elements fire earlier
    (negative), matching the time origin of Texo's stored samples.
    """
    element = geo.elements // 2 if element is None else element
    half = min(geo.tx_channels / 2, focus / fnumber / geo.pitch / 2)
    idx = np.arange(geo.elements)
    active = idx[np.abs(idx - element) <= half]
    xs = geo.x(element)
    return active, (focus - np.hypot(geo.x(active) - xs, focus)) / c


def pymust_param(geo, fs, c=1540.0, width=None):
    """A PyMUST `param` dictionary for a linear or convex array."""
    t = transducer(geo, width)
    param = {
        "fc": t["centre_freq"],
        "pitch": t["pitch"],
        "width": t["width"],
        "kerf": t["kerf"],
        "Nelements": t["elements"],
        "c": c,
        "fs": fs,
    }
    if t["fractional_bandwidth"]:
        param["bandwidth"] = 100 * t["fractional_bandwidth"]
    if t["height"]:
        param["height"] = t["height"]
    if t["elevation_focus"]:
        param["focus"] = t["elevation_focus"]
    if t["kind"] == "curved":
        param["radius"] = t["radius"]
    return param


def field2_script(geo, fs, c=1540.0, width=None, focus=None):
    """MATLAB lines that set up the Field II transducer, and the Channels Sequence transmit if `focus` is given."""
    t = transducer(geo, width)
    height = t["height"] or 5e-3
    rfocus = t["elevation_focus"] or 1e3
    lines = [
        f"% {geo.elements}-element {t['kind']} array from the Texo probe definition",
        f"fs = {fs:g}; c = {c:g}; f0 = {t['centre_freq'] or 5e6:g};",
        "set_sampling(fs); set_field('c', c);",
        f"N = {t['elements']}; width = {t['width']:g}; height = {height:g}; kerf = {t['kerf']:g};",
        f"rfocus = {rfocus:g};  % elevation focus",
    ]
    if t["kind"] == "curved":
        lines.append(f"rconvex = {t['radius']:g};")
        make = "xdc_convex_focused_array(N, width, height, kerf, rconvex, rfocus, 1, 5, [0 0 0])"
    else:
        make = "xdc_focused_array(N, width, height, kerf, rfocus, 1, 5, [0 0 0])"
    lines += [f"tx = {make};", f"rx = {make};"]
    bw = t["fractional_bandwidth"] or 0.6
    lines += [
        f"impulse = gauspuls(-2/f0:1/fs:2/f0, f0, {bw:g});",
        "xdc_impulse(tx, impulse); xdc_impulse(rx, impulse);",
        "xdc_excitation(tx, sin(2*pi*f0*(0:1/fs:1/f0)));",
    ]
    if focus is not None:
        active, delays = focused_delays(geo, focus, c)
        apod = np.zeros(geo.elements)
        apod[active] = 1
        lines += [
            f"% Channels Sequence transmit: focused at {focus * 1e3:g} mm from element {geo.elements // 2}",
            f"apod = [{' '.join(f'{a:g}' for a in apod)}];",
            "xdc_apodization(tx, 0, apod);",
            f"delays = zeros(1, N); delays([{' '.join(str(a + 1) for a in active)}]) = [{' '.join(f'{d:.6e}' for d in delays)}];",
            "xdc_times_focus(tx, 0, delays - min(delays));",
            f"% receive on channels {geo.elements // 2 - geo.rx_channels // 2}..{geo.elements // 2 + geo.rx_channels // 2 - 1} (0-based),"
            " one element each; no receive focusing",
            "xdc_focus_times(rx, 0, zeros(1, N));",
            "% calc_scat_multi(tx, rx, points, amplitudes) returns rf and its start time t0;",
            "% t0 + min(delays) is the time after the centre element fires, as in Texo captures",
            "% (Field II's t0 also includes the delay of the excitation and impulse responses)",
        ]
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("probe", help="probe definition.yml from examples/probe")
    parser.add_argument("--width", type=float, help="element width (µm) if the definition doesn't give it")
    parser.add_argument("--fs", type=float, default=60, help="sampling rate (MHz)")
    parser.add_argument("--focus", type=float, help="Channels Sequence transmit focus (mm), for --field2")
    parser.add_argument("--field2", help="write a Field II MATLAB setup script")
    parser.add_argument("--pymust", action="store_true", help="print a PyMUST param dictionary")
    args = parser.parse_args()

    geo = read_probe(args.probe)
    if geo.width is None and not args.width:
        parser.error("the probe definition has no elementWidth yet; pass --width (µm)")
    width = args.width * 1e-6 if args.width else None
    fs = args.fs * 1e6
    if args.field2:
        focus = args.focus * 1e-3 if args.focus else None
        with open(args.field2, "w") as f:
            f.write(field2_script(geo, fs, width=width, focus=focus))
        print(f"wrote {args.field2}")
    if args.pymust or not args.field2:
        print(json.dumps(pymust_param(geo, fs, width=width), indent=2))


if __name__ == "__main__":
    main()
