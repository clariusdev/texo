# Python tools

Examples for working with Texo captures. They need Python 3.14 or later (to read the
Zstandard-compressed raw packages) and NumPy; `beamform.py` also uses Matplotlib to show
its image.

| Script | What it does |
|--------|--------------|
| [`beamform.py`](beamform.py) | Delay-and-sum beamforming of channel data from the Channels Sequence or single-element capture |
| [`simulate.py`](simulate.py) | Writes simulated point-target captures in the same format, and checks the beamformer against them |

See [Capture Output and Reading the Data](../docs/capture-data.md#beamforming-channel-data).
