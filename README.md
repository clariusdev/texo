# Clarius Texo

Texo is a research tool for driving Clarius scanners with **scripts** instead of the
clinical presets in the Clarius App. Where the App automatically derives imaging
parameters from a preset and depth (see
[how imaging parameters are automated](https://github.com/clariusdev/research/blob/master/docs/imaging-parameter-automation.md)),
Texo hands the transmit/receive sequence, parameters, processing, and probe definition to
the researcher to read, edit, apply to a connected probe, and capture data from.

Texo runs **research-targeted scripts that Clarius defines** for research use. It does not
load the clinical-grade scripts that ship in the Clarius App.

## Download

Get Texo for macOS, Windows, or Linux from
[Releases](https://github.com/clariusdev/texo/releases). Each release's notes cover setup
for your platform, and the [`examples/`](examples) folder at the same tag holds the
matching research script sets.

## What you can do

- Log in with a Clarius Cloud account and connect to an HD3 probe over Bluetooth and Wi-Fi
- Load a Clarius-provided research script set from [`examples/`](examples) into the editor
- Edit four script sections (**parameters**, **sequences**, **processing**, **probe**)
  and check each for errors
- Program a connected probe with your scripts and image live
- Capture images, prescan data, and raw data for offline analysis

## Documentation

- [Getting Started](docs/getting-started.md) — log in, connect, load a script set, program
  the probe, image, capture, and troubleshoot
- [The Texo Workspace](docs/interface.md) — a tour of the window: the four script windows,
  every panel, the image, probe connection, presets, and data storage
- [Capture Output and Reading the Data](docs/capture-data.md) — what a capture writes to
  disk, the raw package format, and Python examples
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
