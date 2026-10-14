# Clarius Texo

> 🚧 **Pre-release.** Texo and this documentation are in preparation and not yet
> generally available. Details may change before release.

Texo is a research tool for driving Clarius scanners with **scripts** instead of the
clinical presets in the Clarius App. Where the App automatically derives imaging
parameters from a preset and depth (see
[how imaging parameters are automated](https://github.com/clariusdev/research/blob/master/docs/imaging-parameter-automation.md)),
Texo hands the transmit/receive sequence, parameters, processing, and probe definition to
the researcher to read, edit, apply to a connected probe, and capture data from.

Texo runs **research-targeted scripts that Clarius defines** for research use. It does not
load the clinical-grade scripts that ship in the Clarius App.

## What you can do

- Log in with a Clarius Cloud account and connect to a probe over the network
- Load a Clarius-provided research script set into the editor
- Edit four script sections — **parameters**, **sequences**, **processing**, **probe** —
  and parse each for errors
- Apply scripts to a connected probe and image live
- Freeze and capture raw data for offline analysis

## Documentation

- [Getting Started](docs/getting-started.md) — log in, connect, load a script set, apply
  it, image, and capture
- [The Texo Workspace](docs/interface.md) — a tour of the window: the four script windows,
  the image panel, probe connection, and presets
- [Scripting Guide](docs/scripting.md) — the four script sections and the parameter
  expression language

## Prerequisites

- A Clarius HD3 scanner with research access enabled on the probe
- A Clarius Cloud account with research/Texo permissions
- A probe and host machine on the same wireless network

## Related repositories

- [clariusdev/research](https://github.com/clariusdev/research) — raw-data formats,
  in-app research tools, and how clinical imaging parameters are automated
- [clariusdev/cast](https://github.com/clariusdev/cast) — real-time image streaming and
  raw-data download while the Clarius App is running
- [clariusdev/solum](https://github.com/clariusdev/solum) — OEM SDK for direct probe
  control
