# Python tools

Examples for working with Texo captures. They need Python 3.14 or later (to read the
Zstandard-compressed raw packages) and NumPy; `beamform.py` also uses Matplotlib to show
its image.

| Script | What it does |
|--------|--------------|
| [`beamform.py`](beamform.py) | Delay-and-sum beamforming of channel data from the Channels Sequence: channel walk, scan or single element |
| [`simulate.py`](simulate.py) | Writes simulated point-target captures in the same format, and checks the beamformer against them |
| [`export.py`](export.py) | Exports a probe and the Channels Sequence transmit to Field II or PyMUST |
| [`capture.py`](capture.py) | Reads and writes raw data packages and probe definitions; `write_capture` saves simulated data as a Texo capture |

See [Capture Output and Reading the Data](../docs/capture-data.md#beamforming-channel-data).
[`../samples/pins.zip`](../samples/pins.zip) is a real scan of a pin phantom to try it on.

## Simulating with Field II or PyMUST

`export.py` gives the probe's array (element count, pitch, element width and kerf,
elevation height and focus, centre frequency) and the Channels Sequence's focused
transmit in the form each simulator takes:

```
python export.py ../examples/probe/L15HD3/definition.yml --field2 l15.m --focus 15
python export.py ../examples/probe/L15HD3/definition.yml --pymust
```

Save the simulated RF with `capture.write_capture`, giving the sample delay from the
transmit to the first sample, and it reads and beamforms like a probe capture.

Element width and the lens's speed of sound will be added to the probe definitions
(`elementWidth`, `lensSpeedOfSound`); until then, pass `--width` with your own value.
Without the lens's speed of sound, timing treats the lens as tissue, as the probe does.
