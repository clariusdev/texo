# Capture Output and Reading the Data

This page describes what Texo 13.1 writes to disk and how to load it in Python. For the
capture controls themselves, see [Capture data](getting-started.md#6-capture-data).

Texo saves two kinds of output:

| Capture Selection | Where it goes | What it holds |
|-------------------|---------------|---------------|
| **Images** / **Prescan** | A capture folder under the Storage Folder | PNG frames, metadata, and the four scripts |
| **Download Raw** | A single `.zip` in the Storage Folder | Raw data buffered on the probe, with a metadata file per data type |

## Images and prescan

### Folder layout

```
<Storage Folder>/
  [<prefix>_]<folder name>/
    investigation.yml
    workflow/
      script.yml
      sequences.yml
      probe.yml
      parameters.yml
    {<cine uuid>}/
      cine.yml
      <frames>
```

- **Folder name** follows **Folder Naming**: a local timestamp (`2026-10-15_14-03-22`) or a
  UUID in braces. The **Capture Prefix**, if set, is added in front with an underscore.
- **`investigation.yml`**: the **Capture Notes**, the capture date and time, and the
  connected probe: model, element count, pitch (µm), radius (mm), and capabilities.
- **`workflow/`**: the four scripts in use when you captured. When a window has several
  tabs, their contents are joined into one file.
- **`{<cine uuid>}/`**: the frames and `cine.yml`. Each capture gets its own cine folder,
  even when two captures land in the same capture folder.

### Frames

**Images** are scan-converted to the width × height set in Data Storage and saved as
8-bit RGBA PNGs. **Prescan** frames are saved before scan conversion, in line and sample
coordinates, as 8-bit grayscale PNGs (or as JPEG when the script's
`compress` stage has already compressed them).

**File Naming** sets each frame's name:

| File Naming | Name |
|-------------|------|
| Timestamp | `<stream>.<timestamp ns>.png` |
| Indexed | `<stream>.<frame id>.png` |
| UUID | `<TIMESTAMP>.<FRAME ID>.<STREAM>.png`, in hexadecimal |

`<stream>` is `0` for B mode. With **Separate Doppler Overlays** on, a Color or Power
Doppler capture saves each frame twice: stream `0` is the B image and stream `1` is the
Doppler overlay, at the same size, so they can be composited or analyzed separately.

### `cine.yml`

One entry per frame under `sections[].files[]`, with `filename`, `timestamp` (ns),
`hardware id`, and, where available, `frameRate` and inertial (IMU) readings.
`sections[].info` describes the image: `size` (samples per line, number of lines),
`sampling rate` (MHz), `delay samples`, `vsound` (m/s), the per-line `lines[]` (element,
angle), and the transmit `focus[]`.

## Raw data

### Turning raw storage on

The probe only buffers raw data for processing chains that contain an enabled `rawdata`
stage. In the examples it is enabled by `storeRaw`, which defaults to `false`. Set
`storeRaw: true` in the Parameters window, **Program Probe**, and image.

Each script's `rawdata` section names the data type and the buffer size on the probe:

```yaml
rawdata:
 ch:
  dataType: channel
  size: 128MB
  freq: "{txFreq}"
  depth: "{endDepth}"
  focus: "{txFocus}"
```

Where the stage sits in `imageprocessing` decides what is captured: before `envlog` you
get RF, IQ or channel data; after it, envelope data. The examples store:

| Example script | Raw data stored |
|----------------|-----------------|
| `env_ll`, `env_hl` (B mode) | IQ and envelope |
| `rf` | RF |
| `channels` | Per-channel RF |
| `pw` | PW Doppler |
| `ce` | Contrast |

### The package

**Download Raw** with **Capture Image** saves the current frame; with **Capture Cine** it
saves everything buffered. The package is a `.zip` saved directly in the Storage Folder,
named by **File Naming** (timestamp, index, or UUID) with the **Capture Prefix** in front.

Downloading empties the probe's buffer, so a second download reports *No Raw Data
Buffered* until you image again.

> **Compression:** entries in the zip are compressed with Zstandard (zip method 93). Many
> unzip tools can't extract these. Python 3.14 and later reads them with the standard
> `zipfile` module (see below).

Inside the zip, every file starts with the probe's local time of the capture, e.g.
`2026-10-15T14-03-22+0000`. For each data type that has frames there is:

| File | Contents |
|------|----------|
| `<time>_<type>.raw` | The data (see below) |
| `<time>_<type>.yml` | Acquisition metadata |
| `<time>_<type>.tgc.yml` | Per-frame TGC, only when auto gain was on |

`<type>` is one of:

| `<type>` | Data | Sample format | `id` in header |
|----------|------|---------------|----------------|
| `iq` | IQ (baseband) | interleaved int16 I, Q | 0 |
| `env` | Envelope (log compressed) | uint8 | 1 |
| `env_sc` | Envelope, Spatial Compounding | uint8 | 2 |
| `env_m` | M mode envelope | uint8 | 3 |
| `rf` | RF | int16 | 4 |
| `ch` | Per-channel RF (Channels Sequence) | int16 | 5 |
| `cfi` | Color Doppler | | 6 |
| `pw` | PW Doppler | | 7 |
| `ce` | Contrast | | 9 |

If the script sets `storeImu: true`, the package also holds `<time>_imu.yml` with the
probe's inertial readings, timestamped in ns.

### `.raw` format

A 20-byte header of five little-endian `uint32` values:

| Field | Meaning |
|-------|---------|
| `id` | Data type (table above; numbering differs in other releases) |
| `frames` | Number of frames |
| `lines` | Lines per frame |
| `samples` | Samples per line |
| `sampleSize` | Bytes per sample |

Then, for each frame, a `uint64` timestamp in ns followed by
`lines × samples × sampleSize` bytes. Samples are contiguous within each line. This is the
same layout described in
[raw-data-format.md](https://github.com/clariusdev/research/blob/master/docs/raw-data-format.md)
in clariusdev/research, so its readers work on the extracted `.raw` files; only the
packaging differs.

### `.yml` metadata

Read the start of the file as `key: value` text:

```yaml
# raw data parameters

software version: 13.1.0...
iso time/date: 2026-10-15T14-03-22+0000
probe:
  version: ...
  elements: 192
  pitch: 260
frames: 120
frame rate: 30.00 Hz
transmit frequency: 7.50 MHz
imaging depth: 40.00 mm
focal depth: 20.00 mm
auto gain: off
tgc:
  - { 7.00mm, 15.70dB }
  ...
```

`pitch` is in µm and `radius` (curved probes only) in mm. Below the TGC comes the full
image description, as in `cine.yml`: `size`, `sampling rate` (MHz), `delay samples`,
`vsound`, `lines[]`, and `focus[]`. PW files also give `speed of sound`, `velocity per
sample`, and `angle correction`.

## Reading raw data in Python

Requires Python 3.14 or later and NumPy. The reader picks the sample format from
`sampleSize` (1 = envelope, 2 = RF or channel, 4 = IQ), since `id` numbering has changed
between releases.

```python
import zipfile
import numpy as np

DTYPES = {1: np.uint8, 2: np.int16, 4: np.int16}  # by sampleSize

def read_raw(buf):
    """Return (header, timestamps, data[frames, lines, samples]) from a .raw file's bytes."""
    names = ("id", "frames", "lines", "samples", "sampleSize")
    hdr = dict(zip(names, np.frombuffer(buf, "<u4", 5).tolist()))
    frame_bytes = hdr["lines"] * hdr["samples"] * hdr["sampleSize"]
    rec = np.dtype([("ts", "<u8"), ("data", "u1", frame_bytes)])
    frames = np.frombuffer(buf, rec, hdr["frames"], offset=20)
    dtype = np.dtype(DTYPES[hdr["sampleSize"]]).newbyteorder("<")
    data = frames["data"].copy().view(dtype)
    if hdr["sampleSize"] == 4:  # IQ: split interleaved I and Q into complex samples
        data = data[..., 0::2] + 1j * data[..., 1::2]
    return hdr, frames["ts"], data.reshape(hdr["frames"], hdr["lines"], -1)

def load_package(path):
    """Read every .raw in a Download Raw package, keyed by type (env, rf, ch, ...)."""
    out = {}
    with zipfile.ZipFile(path) as z:
        for name in z.namelist():
            if name.endswith(".raw"):
                kind = name.split("_", 1)[1].removesuffix(".raw")
                meta = z.read(name.removesuffix(".raw") + ".yml").decode()
                out[kind] = (*read_raw(z.read(name)), meta)
    return out
```

### Envelope

```python
import matplotlib.pyplot as plt

hdr, ts, env, meta = load_package("capture.zip")["env"]
plt.imshow(env[0].T, cmap="gray", aspect="auto")  # samples down, lines across
plt.xlabel("line"); plt.ylabel("sample")
plt.show()
```

The envelope is log compressed but not scan converted. For a curved probe the lines fan
out; use `lines[]` and `sampling rate` from the metadata to place them.

### RF

```python
from scipy.signal import hilbert

hdr, ts, rf, meta = load_package("capture.zip")["rf"]
env = np.abs(hilbert(rf[0].astype(float), axis=-1))
bmode = 20 * np.log10(env / env.max() + 1e-6)
plt.imshow(bmode.T, cmap="gray", vmin=-60, vmax=0, aspect="auto")
plt.show()
```

### Channels

Each event in the Channels Sequence receives on one channel, so a frame holds one line
per receive channel. On HD3 the example runs `channelWalk32Alt`, which visits channels in
the order 0, 16, 1, 17, …, 15, 31. Put them back in channel order before use:

```python
hdr, ts, ch, meta = load_package("capture.zip")["ch"]
order = np.ravel(np.column_stack((np.arange(16), np.arange(16, 32))))  # 0,16,1,17,...
channels = np.empty_like(ch)
channels[:, order] = ch          # channels[frame, channel, sample]
```

The channels are stored as received: the example sets `focusType: none`, so no receive
delays or apodization are applied, and you can beamform them yourself. With
`focusType: dynamic`, each channel is instead pre-delayed to focus on the centre beam.

Channel *k* is element `element − 16 + k`, where `element` (in the parameters) is the
middle of the array by default. In the example, the transmit is focused at half the
imaging depth. Element count and pitch are in the metadata's `probe:` block, and
`sampling rate`, `delay samples`, and `vsound` give the time axis.

## Other readers

[clariusdev/research](https://github.com/clariusdev/research) has Python, MATLAB, and
Jupyter readers and viewers for `.raw` files (`common/python/rdataread.py`,
`common/matlab/rdataread.m`, `viewer/`). Extract the zip with Python first, then point
them at the `.raw` files.
