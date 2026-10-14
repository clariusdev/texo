# The Texo Workspace

![Texo imaging live with a research script applied: the four script windows, the image panel, probe connection, and presets](../blob/workspace.png)

Texo's window is organized into a few regions. The center holds the **four script windows**
(the heart of Texo); the left shows the live **image**; the right manages **probe
connection**, **presets**, and **firmware**. Every panel around the script windows is a
dock: toggle it from the toolbar, and drag or float it wherever suits you.

## Toolbar

Across the top, each button shows or hides a panel. Hover a button for its name.

| Panel | What it shows |
|-------|---------------|
| **Probe Connection** | Bluetooth and Wi-Fi connection to the probe (see below). |
| **Image** | The live scan-converted image and gain controls (see below). |
| **Raw Image** | Prescan data before scan conversion, with rotate/flip and histogram options. |
| **Contrast Image** | The contrast-mode image, when a contrast script is running. |
| **Spectrum** | The spectral Doppler display, when a PW script is running. |
| **RF Signal** | One RF line as a waveform, with a line selector and an optional FFT. |
| **Channel Scope** | Every receive channel as a stacked trace, for the Channels Sequence. |
| **Inertial** | The probe's motion sensor: orientation and calibration. |
| **Cine Control** | Scroll back through the buffered frames while frozen. |
| **Parameters** | Live view of the parameter values the probe is running with. |
| **Data Storage** | Capture settings and capture buttons (see below). |
| **Settings** | Account, cine buffer size, display calibration, and dark mode. |
| **Presets** | Loads a script set into the four windows (see below). |
| **Firmware Update** | Updates the probe software to match Texo. |

The last button signs out. The title bar shows the Texo version and build.

## Image panel (left)

The live ultrasound image produced by the applied script, with the current **frame rate**
shown in the corner and the gain controls beneath it:

- **Disable compounding** and **Smoothing** toggles.
- **Reset Gain**, which returns the sliders below to their defaults.
- **Overall**: overall gain.
- **DTGC (S)** / **DTGC (M)** / **DTGC (D)**: the digital TGC sliders for the **shallow**,
  **mid**, and **deep** portions of the image. Texo exposes *digital* TGC directly (see
  [how auto gain moved from analog to digital TGC](https://github.com/clariusdev/research/blob/master/docs/imaging-parameter-automation.md#auto-gain-and-tgc)).

Depth isn't a slider: it's the `endDepth` parameter in the Parameters window.

## The four script windows (center)

The same four parts every script is made of, in a 2×2 grid:

| Position | Window | Part |
|----------|--------|------|
| Top-left | **Processing** | Image processing pipeline |
| Top-right | **Probe** | Probe definition |
| Bottom-left | **Sequences** | Transmit/receive sequence |
| Bottom-right | **Parameters** | Named values/expressions |

Each window has:

- A **parse indicator** next to its title, which turns green once the window has parsed
  and resets when you edit it.
- **Tabs**: a window can hold more than one open file, e.g. the B-mode scripts plus those
  of an added mode. All tabs in a window are sent to the probe together.
- A **Path** field: the file backing the active tab.
- The **editor**, where you read and edit the YAML.
- **Open File** / **Save File** buttons, which open a file into the tab or write the tab to
  a file.

**Program Probe** (in the connection bar) parses all four windows and sends them to the
probe. Errors are reported in the log and the offending line is selected. See the
[Scripting Guide](scripting.md) for what belongs in each window and how they reference one
another through the `{...}` expression language.

## Probe Connection (right)

Lists nearby probes and manages the link:

- **Bluetooth** tab: discover and manage the probe over BLE: search, connect, power
  on/off, and trigger the locator alert. Once the probe reports its network, Texo connects
  over Wi-Fi automatically.
- **Wireless** tab: the probe's Wi-Fi network settings.

## Presets (right)

How you pull a research script set into the four windows.

- **Data folder** (**...**): where script sets live. Choose the
  [`examples/`](../examples) folder from this repository.
- **Filters**: the **V1**, **HD** and **HD3** buttons choose which probe platforms are
  listed. They start off, so turn on **HD3**.
- **Probes**, **Presets**, **Modes**, **Ranges**: pick a probe, a preset, optionally a mode
  to add on top of B mode, and a depth range.
- **Load** fills Processing, Sequences, Probe, and Parameters from that selection.
- **Save** writes every open tab back over the files it was loaded from. Copy `examples/`
  before editing if you want to keep the originals.
- **Reset** clears the four windows.

The **Preset** chooses the sequence style: **Research** (a concise high-level sequence,
available for all probes) or the event-by-event **Envelope Sequence** and **Channels
Sequence**. See [Sequences in the Scripting Guide](scripting.md#three-sequences-two-styles)
for how they differ.

## Connection bar & log (bottom)

- A **log console** showing script and probe activity, e.g. *Connected to Probe*, UDP
  port assignments, and the script apply cycle (*Parsing scripts...* → *Sent Scripts* →
  *Loaded Scripts*). Errors are shown in red.
- A **status** readout: battery and temperature.
- **IP address and ports** of the probe, filled in automatically when Texo connects over
  Bluetooth, or entered by hand.
- The **buffer fill** bar for the cine buffer.
- Action buttons:
  - **Connect**: connect to the IP address and port above.
  - **Program Probe**: parse the four windows and send them to the probe.
  - **Run**: start imaging; press again to freeze.
  - **Shut Down**: power off the probe.

## Data Storage (right)

Where and how captures are saved:

- **Storage Folder**, **Capture Prefix**, and **Capture Notes**.
- **Folder Naming** and **File Naming**: timestamp, index, or UUID.
- **Capture Selection**:
  - **Images**: scan-converted images at the width × height you set, optionally with
    Doppler overlays as separate frames.
  - **Prescan**: images before scan conversion.
  - **Download Raw**: raw data buffered on the probe (needs `storeRaw: true` in the
    parameters).
- **Capture Image** saves the current frame and **Capture Cine** the buffered loop.

Image and prescan captures save the four scripts in use alongside the images. See
[Capture data](getting-started.md#6-capture-data) for details.

## Firmware Update (right)

When the log reports that the probe software differs from the version bundled with Texo,
press **Send Firmware** to update the probe.
