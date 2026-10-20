# Recipes

Short how-tos that each change **one thing** in the example scripts. Every recipe starts
from a script set in [`examples/`](../examples), loaded as described in
[Getting Started](getting-started.md#3-load-a-research-script-set), and ends the same
way: edit, press **Program Probe**, then **Run**.

Each recipe gives:

- **Goal**: what you get.
- **Start from**: the preset, mode and window to edit.
- **Edit**: the YAML change, using the keys and file names from `examples/`.
- **What you should see**, and **pitfalls**.

File names below are the example files, e.g. `parameters/research/env.yml` is the
**Parameters** tab loaded by the Research preset. The Presets panel's **Save** overwrites
the loaded files, so copy `examples/` first or save edited tabs to files of your own. See
the [Scripting Guide](scripting.md) for how the four windows reference one another.

> **Safety:** recipes 1, 2, 3 and 4 change the transmit (frequency, angle, aperture or
> pulse shape). Texo does not hold you to the App's validated operating points. Read
> [Safety](getting-started.md#safety) before changing acoustic output, and stay within
> the probe's limits in the **Probe** window.

| # | Recipe | Start from |
|---|--------|------------|
| 1 | [Fixed transmit frequency](#1-fixed-transmit-frequency) | Research |
| 2 | [Steered frames](#2-steered-frames) | Research, Envelope Sequence |
| 3 | [Single-element acquisition](#3-single-element-acquisition) | Channels Sequence |
| 4 | [Pulse-inversion harmonics](#4-pulse-inversion-harmonics) | Research |
| 5 | [Flat TGC](#5-flat-tgc) | Research, Channels Sequence |
| 6 | [Raw storage for one data type](#6-raw-storage-for-one-data-type) | Research (+ RF mode) |
| 7 | [Channel data with or without receive focusing](#7-channel-data-with-or-without-receive-focusing) | Channels Sequence |
| 8 | [Channel data for every scan line](#8-channel-data-for-every-scan-line) | Channels Sequence |

---

## 1. Fixed transmit frequency

**Goal:** transmit at a frequency you choose instead of the probe's centre frequency.

**Start from:** Research preset, **Parameters** window (`parameters/research/env.yml`).

**Edit:** `txFreq` defaults to the probe's centre frequency. Pin it:

```diff
 params:
-  txFreq: "{probe::stackinfo::centerFreq}"
+  txFreq: 5MHz
```

In the Research sequence (`sequences/research/env_hl.yml`) both transmit nodes, `b` and
`binv`, use `freq: "{txFreq}"`, and the raw-data metadata (`rawdata` → `freq` in
`script/research/env_hl.yml`) follows it too.

**The receive side does not follow `txFreq`.** The receive node demodulates with a
frequency that slides from `shallow` at the surface to `deep` at `depth`, and in the
Research sequence those come from the probe:

```yaml
rx:
 b:
  shallow: "{probe::freq::upperFreq}"
  deep: "{probe::freq::lowFreq}"
  depth: "{probe::freq::end depth}"
```

To demodulate at your transmit frequency at every depth, as the Channels Sequence does,
edit the **Sequences** window:

```diff
 rx:
  b:
-  shallow: "{probe::freq::upperFreq}"
-  deep: "{probe::freq::lowFreq}"
+  shallow: "{txFreq}"
+  deep: "{txFreq}"
```

The decimation low-pass filter, `lpfid` in the parameters, is chosen from the probe's
centre frequency, not `txFreq`:

```yaml
  lpfid: "{probe::stackinfo::centerFreq} < 7 MHz ? 17 : 0"
```

Leave it unless you move far from the centre frequency.

**What you should see:** the **Parameters** panel and the raw-data metadata
(`transmit frequency:`) show your value. Lower frequencies give more penetration and
coarser axial resolution; higher frequencies the reverse.

**Pitfalls:**

- **Envelope Sequence:** `sequences/research/env_ll.yml` doesn't use `txFreq`. Its
  transmit node has `freq: "{probe::stackinfo::centerFreq}"`, and its `rawdata` entries
  in `script/research/env_ll.yml` do too. Change those to `"{txFreq}"` as well, or
  changing `txFreq` has no effect.
- **Frequency steps:** each `+` or `-` of the pulse lasts a whole number of transmit
  clock cycles. With the 120 MHz transmit clock in the HD3 probe definitions, the
  frequency you get is 60 MHz / *n* for a whole number *n*: 5, 6, 6.67, 7.5, 8.57, 10,
  12, 15, 20 MHz, … A request in between is rounded to the nearest step, while the
  metadata records the value you asked for.
- Stay inside the probe's `stackinfo` band (`lowFreq` to `upperFreq` in the **Probe**
  window). Transmit nodes accept 1 to 40 MHz, but the probe's band is the real limit.
- Modes added on top (Color, PW) have their own frequency parameters. This recipe only
  changes B mode.

---

## 2. Steered frames

**Goal:** steer every line of the B frame by a fixed angle.

**Start from:** Research preset (or Envelope Sequence), **Parameters** window
(`parameters/research/env.yml`).

**Edit:**

```diff
 params:
-  steer: 0 degrees
+  steer: 10 degrees
```

`steer` reaches the sequence in two different ways:

- **Research** (`sequences/research/env_hl.yml`): the block angle,
  `blocks: - { id: b, angle: "{steer}", frame: b }`. Each line's angle is the block
  angle plus the frame's `start angle` to `end angle`, which are both `0 degrees` in the
  example.
- **Envelope Sequence** (`sequences/research/env_ll.yml`) and **Channels Sequence**:
  every event carries its own `txAngle: "{steer}"` and `rxAngle: "{steer}"`.

To steer transmit and receive differently, edit the events in the Envelope Sequence,
e.g. transmit steered and receive straight:

```diff
-      - { el: "0", txAngle: "{steer}", rxAngle: "{steer}", lpf: "{lpfid}", tx: b, rx: [ { rx: b } ], tgc: b }
+      - { el: "0", txAngle: "{steer}", rxAngle: 0 degrees, lpf: "{lpfid}", tx: b, rx: [ { rx: b } ], tgc: b }
```

(and the same for every event). In the Research sequence, giving the frame different
`start angle` and `end angle` spreads the angle across the frame instead: line *i* gets
the block angle plus `start angle` + *i* × (`end angle` − `start angle`) / (`lines` − 1).

**What you should see:** the frame tilts by the steer angle. On a linear probe a
steered frame is a parallelogram.

**Pitfalls:**

- The scripts accept −90° to +90°, but useful angles are much smaller. The linear probe
  definitions list a `max steering angle` under `defaults` (L7HD3 25°, L15HD3 15°, L20HD3
  20°); beyond it, expect grating lobes and lost sensitivity. Curved probes don't list
  one.
- `steer` is also used by the RF mode (`sequences/research/rf.yml`) and by the Spatial
  Compounding frames (`sequences/research/sc.yml`, as their `start angle` / `end angle`),
  so it moves those too.
- With several angled blocks the sequence is treated as compounding. Use the **Spatial
  Compounding** mode (`scMode`) for that rather than building it from `steer`.

---

## 3. Single-element acquisition

**Goal:** every element transmits and receives on its own, one after another, giving
per-element RF for synthetic-aperture beamforming offline.

**Start from:** Channels Sequence preset, **Parameters** window
(`parameters/research/channels.yml`).

**Edit:**

```diff
 params:
-  singleElement: false
+  singleElement: true
   viewSingleElement: false
-  storeRaw: false
+  storeRaw: true
```

`singleElement: true` switches the `imaging` binding in `script/research/channels.yml`
from the channel walk to the `singleElement32` sequence:

```yaml
imaging:
  - { seq: singleElement32, imgpro: ch, enabled: "{singleElement} && {probe::capabilities::rx} == 32" }
```

`singleElement32` (in `sequences/research/channels.yml`) has **192 events**, one per
element: event *k* is centred on element *k*, transmits on that element alone and
receives on that element alone. Its output is `Channel`, so each frame holds 192 lines
of RF, **line *k* = element *k***, in ascending element order (unlike the channel walk,
whose lines [follow the receive channels](capture-data.md#channels)).

`viewSingleElement` switches the output to `IQ` and turns on `envlog` and `compress` in
the processing chain, so you can see the data as an image while positioning the probe:

```yaml
  output: "{viewSingleElement} ? IQ : Channel"
```

**What you should see:** a much lower frame rate than B mode (192 events per frame, and
`lineformation` caps it with `maxFrameRate: 10Hz`). **Download Raw** gives a `ch`
package; see [Capture Output and Reading the Data](capture-data.md) for the format.

To beamform the capture, [`python/beamform.py`](../python/beamform.py) forms an image
from a single-element package (linear probes):

```
python python/beamform.py capture.zip --probe examples/probe/L15HD3/definition.yml
```

**Pitfalls:**

- Set `viewSingleElement: false` before capturing. With it on, the frames are IQ rather
  than per-element RF.
- Keep `focusType: none` (the default), so each element is stored as received. See
  [recipe 7](#7-channel-data-with-or-without-receive-focusing).
- The event list covers elements 0 to 191, so it is written for the 192-element HD3
  probes. PA2HD3 has 80 elements.
- A single element transmits far less energy than a focused aperture, so the signal is
  weak at depth. Raise the TGC (see [recipe 5](#5-flat-tgc), or set `rampGain: true`).

---

## 4. Pulse-inversion harmonics

**Goal:** image with pulse inversion: each line is transmitted twice with opposite
polarity and the two echoes are summed, cancelling the fundamental and keeping the even
harmonics.

**Start from:** Research preset, **Parameters** window (`parameters/research/env.yml`).

**Edit:**

```diff
   # sequencing parameters
   rxc: 32
   mla: 1
-  pih: false
+  pih: true
```

This works through three pieces that are already in the example:

| Where | Key | Effect |
|-------|-----|--------|
| `parameters/research/env.yml` | `txPulse: +-`, `txPulseInv: -+` | The pulse and its inverse. |
| `parameters/research/env.yml` | `pihEnabled: "{pih} \|\| ({ceMode} && {ceType} == pih)"` | Turned on by `pih`. |
| `sequences/research/env_hl.yml` | `tx: binv` focus rules, `enabled: "... && {pihEnabled}"` | Adds an inverted-pulse event after each line's normal event. |
| `script/research/env_hl.yml` | `lineformation` → `accum: "{pihEnabled} ? ({rxc} / 32) * 2 : ({rxc} / 32)"` | Sums each pair. |

**What you should see:** half the frame rate (two transmits per line), and an image
built from the harmonic content: typically less clutter near the surface and less
penetration.

**Pitfalls:**

- Only the **Research** sequence has the `binv` transmit node and the accumulating line
  formation. The Envelope Sequence (`env_ll`) ignores `pih`.
- If you change the pulse shape, keep `txPulseInv` the exact inverse of `txPulse`, or the
  fundamental doesn't cancel. A pulse is a string of `+`, `-` and `0` (clamp to zero), each
  character half a cycle at `txFreq`, up to 31 characters on HD3. For a two-cycle pulse:

  ```yaml
    txPulse: +-+-
    txPulseInv: -+-+
  ```

- Pulse inversion doesn't change the receive band: `rx` → `b` still demodulates from the
  probe's `upperFreq` down to `lowFreq` (see [recipe 1](#1-fixed-transmit-frequency)).
  Lowering `txFreq` keeps the second harmonic inside the probe's band.
- Motion between the two transmits leaves residual fundamental. Hold the probe still.

---

## 5. Flat TGC

**Goal:** the same receive gain at every depth.

**Start from:** Research preset, **Processing** window (`script/research/env_hl.yml`).

**Edit:** the analog TGC `b` ramps from 5 dB at the surface to 40 dB at the probe's
`end depth`. Give both points the same value:

```diff
 tgc:
  b:
-  - { v: 5dB, d: 0mm }
-  - { v: 40dB, d: "{probe::freq::end depth}" }
+  - { v: 20dB, d: 0mm }
+  - { v: 20dB, d: "{probe::freq::end depth}" }
```

The digital TGC curves under `dtgc` are already flat (`b` and `d75` at 0 dB). Leave
`d25` at −6 dB: it weights the outer lines when `mla: 4`.

**What you should see:** the image darkens with depth as attenuation is no longer
compensated, and a homogeneous phantom shows its true attenuation.

**Pitfalls:**

- On HD3 the analog TGC covers **5 to 40 dB**. Values outside that range are clamped.
- The **Overall** and **DTGC (S/M/D)** sliders in the Image panel are added to the
  digital curves listed in `sliderTgcSel`. Press **Reset Gain** before capturing so the
  sliders don't reshape the curve.
- No auto gain runs in the examples: none of them set `autogain` or `autoGainSel`, so
  the TGC you write is the TGC you get.
- The **Channels Sequence** already has this as a switch: `rampGain: false` (the default)
  gives a flat 20 dB, and `true` ramps from 0 to 40 dB over the imaging depth:

  ```yaml
  tgc:
   ch:
    - { v: "{rampGain} ? 0dB : 20dB", d: 0mm }
    - { v: "{rampGain} ? 40dB : 20dB", d: "{endDepth}" }
  ```

- Added modes have their own curves (e.g. `pwTgc` in the PW script). This recipe only
  changes B mode.

---

## 6. Raw storage for one data type

**Goal:** buffer only the data you need, e.g. only RF, so the probe's raw buffer holds
more frames of it.

**Start from:** Research preset with the **RF** mode added. Edit the **Parameters**
window (`env` tab) and the **Processing** window (`env_hl` tab).

**How storage is switched:** each processing chain under `imageprocessing` can contain
`rawdata` stages. A stage stores whatever data is flowing at that point in the chain, and
in the examples each one is enabled by `storeRaw`:

```yaml
imageprocessing:
 b:
  - { type: lineformation , id: b }
  - { type: celf, id: b, enabled: "{ceMode}", forward: true }
  - { type: rawdata, id: iq, enabled: "{storeRaw}" }    # IQ, before detection
  - { type: envlog, id: b }
  - { type: rawdata, id: env, enabled: "{storeRaw}" }   # envelope, after detection
```

With the RF mode added, its own chain (`script/research/rf.yml`) stores RF the same way.

**Edit:** set `storeRaw: true` in the parameters, then turn off the stages you don't want
in `env_hl`:

```diff
-  - { type: rawdata, id: iq, enabled: "{storeRaw}" }
+  - { type: rawdata, id: iq, enabled: false }
   - { type: envlog, id: b }
-  - { type: rawdata, id: env, enabled: "{storeRaw}" }
+  - { type: rawdata, id: env, enabled: false }
```

For **envelope only**, use the Research preset without a mode and disable just the `iq`
stage.

**Buffer size:** each `rawdata` entry sets the size of its buffer on the probe, in MB:

```yaml
rawdata:
 rf:
  dataType: rf
  size: 128MB
```

The examples use 128 MB for IQ, RF and channel data, 64 MB for envelope and 16 MB for M
mode and PW. The scripts accept up to 512 MB per entry.

**What you should see:** **Download Raw** gives a package with only the `rf` files.

**Pitfalls:**

- `dataType` names what the stage stores; it doesn't convert the data. Keep each stage
  where that type is produced: before `envlog` for `iq`, `rf` and `channel`, after it for
  `env`.
- The probe's memory is shared by all enabled buffers. Raise `size` for the buffer you
  keep rather than for all of them.
- Downloading empties the buffer; image again before the next download.

---

## 7. Channel data with or without receive focusing

**Goal:** choose whether each channel is stored exactly as received or pre-delayed for
the centre beam.

**Start from:** Channels Sequence preset, **Parameters** window
(`parameters/research/channels.yml`).

**Edit:**

```diff
   # none: channels as received; dynamic: each channel pre-delayed for the centre beam
-  focusType: none
+  focusType: dynamic
```

`focusType` sets the receive `type` of every receive node in
`sequences/research/channels.yml` (`type: "{focusType}"`), and the apodization in
`script/research/channels.yml`:

```yaml
apod:
 ch:
  shape: "{focusType} == none ? ones : hamming"
```

| `focusType` | Receive delays | Apodization | Use it for |
|-------------|----------------|-------------|------------|
| `none` (default) | Constant: channels as received | Flat (`ones`) | Your own beamforming |
| `dynamic` | Dynamic: each channel delayed to focus on the centre beam | Hamming | Seeing the focused echoes line up across channels |

**What you should see:** in the **Channel Scope**, the transmit ring-down at the start of
each trace is a straight band across all channels with `none`, and bends into a chevron
(edge channels earliest) with `dynamic`, since each channel is shifted by its receive
delay. Echoes from a point target on the centre line line up across channels with
`dynamic` and form the usual hyperbola with `none`.

**Pitfalls:**

- Offline beamforming, including [`python/beamform.py`](../python/beamform.py), expects
  `none`. With `dynamic` the delays are already applied.

---

## 8. Channel data for every scan line

**Goal:** per-channel RF for a block of adjacent scan lines, each a focused transmit
received on all 32 channels, so you can beamform a B-mode image offline.

**Start from:** Channels Sequence preset, **Parameters** window
(`parameters/research/channels.yml`).

**Edit:**

```diff
-  scan: false
+  scan: true
-  storeRaw: false
+  storeRaw: true
```

`scan: true` switches the `imaging` binding in `script/research/channels.yml` to the
`channelScan32Alt` sequence:

```yaml
imaging:
  - { seq: channelScan32Alt, imgpro: ch, enabled: "{scan} && !{singleElement} && {probe::capabilities::rx} == 32 && {alt} == true" }
```

`channelScan32Alt` (in `sequences/research/channels.yml`) has **768 events**: 24 scan
lines, from element `scanStart` to `scanStart + 23`, each a focused transmit at
`txFocus` followed by the 32 channel-walk events. Each frame holds 768 lines of RF; lines
`32 × i` to `32 × i + 31` belong to scan line *i*, in the [channel order](capture-data.md#channels)
of a walk centred on its element. The metadata's `lines` list gives each line's element.

`scanStart` centres the 24 lines on the array by default. Move it to put the lines over
your target, or to `0` or `elements − 24` to look at the ends of the array:

```diff
-  scanStart: "{probe::geometry::elements} / 2 - 12"
+  scanStart: 60
```

**What you should see:** about 10 Hz at 4 cm, the same frame-rate limit as the walk. Beamform a
download with [`python/beamform.py`](../python/beamform.py), which recognises the scan
and forms one image column per scan line.

**Pitfalls:**

- The strip is only 24 lines wide (4.8 mm on L7HD3). Find your target on a B-mode
  image first and set `scanStart` so it sits under the lines.
- Keep the sequence at 768 events. Longer scans exceed what the probe can sequence.
- With `singleElement: true` the single-element sequence runs instead.
- The scan transmits 768 times per frame, so it pulses about as often as a B-mode image.
  See [Safety](getting-started.md#safety).

