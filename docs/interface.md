# The Texo Workspace

> 🚧 **Pre-release.** The screenshot below is from a development build; panels, paths, and
> styling will change before release.

![Texo imaging live with a research script applied: the four script windows, the image panel, probe connection, and presets](../blob/workspace.png)

Texo's window is organized into a few regions. The center holds the **four script windows**
(the heart of Texo); the left shows the live **image**; the right manages **probe
connection** and **presets**.

## Toolbar

Across the top: Bluetooth, imaging-mode toggles, save, capture, settings, and sign-out.
The title bar shows the build (e.g. *Texo II*).

## Image panel (left)

The live ultrasound image produced by the applied script, with the current **frame rate**
shown in the corner and the gain controls beneath it:

- **Disable compounding** and **Smoothing** toggles.
- **Overall** — overall gain.
- **DTGC (S)** / **DTGC (M)** / **DTGC (D)** — the digital TGC sliders for the **shallow**,
  **mid**, and **deep** portions of the image. Texo exposes *digital* TGC directly (see
  [how auto gain moved from analog to digital TGC](https://github.com/clariusdev/research/blob/master/docs/imaging-parameter-automation.md#auto-gain-and-tgc)).

## The four script windows (center)

The same four parts every script is made of, in a 2×2 grid:

| Position | Window | Part |
|----------|--------|------|
| Top-left | **Processing** | Image processing pipeline |
| Top-right | **Probe** | Probe definition |
| Bottom-left | **Sequences** | Transmit/receive sequence |
| Bottom-right | **Parameters** | Named values/expressions |

Each window has:

- **Tabs** — a window can hold more than one open file (e.g. several parameter files that
  layer together).
- A **Path** field — the file backing the active tab.
- The **editor** — where you read and edit the YAML.
- **Load / save** buttons — open a file into the tab, or write the tab back to a file.

Edit a window, then parse; errors are reported against the offending line. All four must
parse cleanly before the script is applied to the probe. See the
[Scripting Guide](scripting.md) for what belongs in each window and how they reference one
another through the `{...}` expression language.

> In a development build the paths point at a local data tree; in a research release you
> load a Clarius-provided script set through the **Presets** panel rather than browsing
> raw files.

## Probe Connection (right)

Lists the connected probe and manages the link:

- **Bluetooth** tab — discover and manage the probe over BLE: search, connect, power
  on/off, and trigger the locator alert.
- **Wireless** tab — the Wi-Fi/network connection used for imaging.

## Presets (right)

How you pull a research script set into the four windows. Select the **Probe**, **Preset**,
**Mode**, and depth **Range**, then load — Texo fills Processing, Sequences, Probe, and
Parameters from that set. Save and refresh controls let you store and re-pull your own
sets, and a data-folder selector points Texo at where script sets live.

The **Preset** chooses the sequence style: **Research** (a concise high-level sequence,
available for all probes) or the event-by-event **Envelope** and **Channels** sequences.
See [Sequences in the Scripting Guide](scripting.md#three-sequences-two-styles) for how
they differ.

## Connection bar & log (bottom)

- **IP address and ports** for connecting to the probe over the network.
- A **status** readout (battery, temperature).
- Imaging action buttons (connect/optimize, download data, freeze, power, sync).
- A **log console** showing script and probe activity — e.g. *Connected to Probe*,
  *Probe Ready*, UDP port assignments, and the script apply cycle (*Sent Scripts* →
  *Parsing scripts...* → *Loaded Scripts*), with a progress bar while scripts are sent and
  applied.

## Firmware Update (bottom-right)

Push a matching firmware build to the connected probe when prompted.
