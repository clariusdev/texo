# Texo Script Reference

> **Generated from the 13.1 schemas; do not edit by hand.**

This is the key-by-key reference for the four Texo script windows. For how the
windows fit together, the expression language, and worked examples, start with the
[Scripting Guide](scripting.md).

How to read the tables:

- **Key** is the YAML key exactly as written in a script (some contain spaces,
  e.g. `start element`).
- **Type** gives the value type. `map of id → X` means a block of named entries
  (e.g. `afe: { b: { ... } }`) that other sections refer to by id; `list of X` is a
  YAML sequence. Enumerated types link to their allowed values under
  [Enumerations](#enumerations).
- Any value may be written as an expression (`"{endDepth} / 2"`, `"{probe::geometry::elements}"`);
  it must evaluate to the listed type. Values with **Units** accept unit suffixes
  (`5MHz`, `40mm`); a bare number is taken in the listed unit.
- **Range** and **Default** are the limits and fallback values enforced by the parser,
  where the schema defines them. Descriptions are left blank where the schema has none.

## Processing

<a id="processing-script"></a>

### Top-level keys

The entire script which will run a sequence.

| Key | Type | Units | Range | Default | Description |
|-----|------|-------|-------|---------|-------------|
| `version` | integer |  |  |  | Version number |
| `setup` | [SetupInfo](#processing-setupinfo) |  |  |  | Setup information |
| `power` | [PowerSupplyInfo](#processing-powersupplyinfo) |  |  |  | Power supply settings |
| `ceus` | [CeusInfo](#processing-ceusinfo) (optional) |  |  |  | Ceus power settings |
| `network` | [NetworkInfo](#processing-networkinfo) |  |  |  | Network settings |
| `tgc` | map of id → list of [TGCInfo](#processing-tgcinfo) |  |  |  | Analog tgc curves |
| `dtgc` | map of id → list of [TGCInfo](#processing-tgcinfo) |  |  |  | Digital tgc curves |
| `lgc` | map of id → list of [LateralGainInfo](#processing-lateralgaininfo) |  |  |  | Lateral gain points |
| `egc` | map of id → list of [ElementGainInfo](#processing-elementgaininfo) |  |  |  | Element gain points |
| `afe` | map of id → [AfeInfo](#processing-afeinfo) |  |  |  | Analog front-end settings |
| `sliderTgcSel` | list of string |  |  |  | Digital tgc curve id(s) that will be combined with user sliders |
| `apod` | map of id → [ApodizationInfo](#processing-apodizationinfo) |  |  |  | Apodization settings |
| `lineformation` | map of id → [LineFormationInfo](#processing-lineformationinfo) |  |  |  | Line formation settings |
| `celf` | map of id → [CelfInfo](#processing-celfinfo) |  |  |  | Contrast enhance line formation settings |
| `envlog` | map of id → [EnvLogInfo](#processing-envloginfo) |  |  |  | Envelope detection/log compression settings |
| `enhance` | map of id → [EnhanceInfo](#processing-enhanceinfo) |  |  |  | Image enhancement settings |
| `edge` | map of id → [EdgeInfo](#processing-edgeinfo) |  |  |  | Edge enhancement settings |
| `gamma` | map of id → [GammaInfo](#processing-gammainfo) |  |  |  | Gamma filter settings |
| `scurve` | map of id → [SCurveInfo](#processing-scurveinfo) |  |  |  | S-curve filter settings |
| `scale` | map of id → [ScaleInfo](#processing-scaleinfo) |  |  |  | Scale filter settings |
| `persist` | map of id → [PersistInfo](#processing-persistinfo) |  |  |  | Persistence settings |
| `flowdepth` | map of id → [FlowDepthInfo](#processing-flowdepthinfo) |  |  |  | Flow depth settings |
| `compress` | map of id → [JpegInfo](#processing-jpeginfo) |  |  |  | Compression (jpeg) settings |
| `autogain` | map of id → [AutoGainInfo](#processing-autogaininfo) |  |  |  | Autogain settings |
| `flash` | map of id → [FlashSuppressInfo](#processing-flashsuppressinfo) |  |  |  | Flash suppression settings |
| `cfilf` | map of id → [CfiLfInfo](#processing-cfilfinfo) |  |  |  | Color line formation settings |
| `cfiwfac` | map of id → [CfiWfAcInfo](#processing-cfiwfacinfo) |  |  |  | Color wallfilter and autocorrelation settings |
| `cfiproc` | map of id → [CfiProcInfo](#processing-cfiprocinfo) |  |  |  | Color flow processing settings |
| `pwwf` | map of id → [PwWfInfo](#processing-pwwfinfo) |  |  |  | Pulsed Wave Doppler wallfilter settings |
| `pwfft` | map of id → [PwFftInfo](#processing-pwfftinfo) |  |  |  | Pulsed Wave Doppler FFT settings |
| `cfienhance` | map of id → [EnhanceInfo](#processing-enhanceinfo) |  |  |  | Color flow enhance |
| `strain` | map of id → [StrainProcInfo](#processing-strainprocinfo) |  |  |  | Strain imaging processing settings |
| `spatialfilter` | map of id → [SpatialProcInfo](#processing-spatialprocinfo) |  |  |  | Spatial filter processing settings |
| `rawdata` | map of id → [RawDataInfo](#processing-rawdatainfo) |  |  |  | Raw data buffering settings |
| `imagebuffer` | map of id → [ImageBufferInfo](#processing-imagebufferinfo) |  |  |  | Image buffering settings |
| `stream` | map of id → [SendStreamInfo](#processing-sendstreaminfo) |  |  |  | Stream settings |
| `imageprocessing` | map of id → list of [ProcessInfo](#processing-processinfo) |  |  |  | Image processing chains |
| `imaging` | list of [ImageConfig](#processing-imageconfig) |  |  |  | Image streams (sequence + processing chain) |
| `inertial` | [InertialInfo](#processing-inertialinfo) |  |  |  | Inertial module settings |

<a id="processing-setupinfo"></a>

### `setup`

Setup information.

| Key | Type | Units | Range | Default | Description |
|-----|------|-------|-------|---------|-------------|
| `vsound` | number | m/s |  | `1540` |  |

<a id="processing-powersupplyinfo"></a>

### `power`

Power supply settings.

| Key | Type | Units | Range | Default | Description |
|-----|------|-------|-------|---------|-------------|
| `vpp` | number | V | 5 – 60 | `10` |  |
| `vnn` | number | V | 5 – 60 | `10` |  |
| `disablePowerBuf` | boolean |  |  | `true` | Since powerbuf output enable can be unstable, don't use by default |
| `psSyncEnable` | boolean |  |  | `false` | Enables or disables the power sync of the hv |
| `psSyncFreqHD` | integer | kHz | 205 – 750 | `300` |  |

<a id="processing-ceusinfo"></a>

### `ceus`

Ceus power settings.

| Key | Type | Units | Range | Default | Description |
|-----|------|-------|-------|---------|-------------|
| `vpp` | number | V | 5 – 60 | `10` |  |
| `vnn` | number | V | 5 – 60 | `10` |  |
| `enabled` | boolean |  |  | `false` | Ceus mode enabled |

<a id="processing-networkinfo"></a>

### `network`

Network settings.

| Key | Type | Units | Range | Default | Description |
|-----|------|-------|-------|---------|-------------|
| `maxDataRate` | number | kbit/s | 1 – 1000000 | `40000` | Maximum network transmission rate for udp frame transfers |
| `packetSize` | integer | bytes | 128 – 65535 | `65000` | Udp packet size for frame transfers |

<a id="processing-tgcinfo"></a>

### `dtgc`, `tgc`

The TGC info.

| Key | Type | Units | Range | Default | Description |
|-----|------|-------|-------|---------|-------------|
| `v` | number | dB | -140 – 140 |  |  |
| `d` | number | mm | 0 – 500 |  |  |

<a id="processing-lateralgaininfo"></a>

### `lgc`

Lateral gain points.

| Key | Type | Units | Range | Default | Description |
|-----|------|-------|-------|---------|-------------|
| `v` | number | dB | -140 – 140 |  |  |
| `a` | number | degrees | -90 – 90 |  |  |

<a id="processing-elementgaininfo"></a>

### `egc`

Element gain points.

| Key | Type | Units | Range | Default | Description |
|-----|------|-------|-------|---------|-------------|
| `v` | number | dB | -140 – 140 |  |  |
| `e` | integer |  | 0 – 191 |  |  |

<a id="processing-afeinfo"></a>

### `afe`

Analog front-end settings.

| Key | Type | Units | Range | Default | Description |
|-----|------|-------|-------|---------|-------------|
| `vcapower` | [VcaPower](#enum-cus-afe-vcapower) |  |  |  |  |
| `pgaclamp` | [PgaClamp](#enum-cus-afe-pgaclamp) |  |  |  |  |
| `pgagain` | [PgaGain](#enum-cus-afe-pgagain) |  |  |  |  |
| `activeterm` | [AcTerm](#enum-cus-afe-acterm) |  |  |  |  |
| `lnaclamp` | [LnaClamp](#enum-cus-afe-lnaclamp) |  |  |  |  |
| `lnagain` | [LnaGain](#enum-cus-afe-lnagain) |  |  |  |  |
| `lnahpf` | [LnaHpf](#enum-cus-afe-lnahpf) |  |  |  |  |
| `lpf` | [Lpf](#enum-cus-afe-lpf) |  |  |  |  |
| `digihpf` | [DigiHpf](#enum-cus-afe-digihpf) |  |  |  |  |
| `chopper` | boolean |  |  | `false` |  |
| `dither` | boolean |  |  | `false` |  |
| `disableLna` | boolean |  |  | `false` |  |
| `disableVca` | boolean |  |  | `false` |  |
| `res12bits` | boolean |  |  | `false` |  |
| `averageChannels` | boolean |  |  | `false` |  |

<a id="processing-apodizationinfo"></a>

### `apod`

Apodization settings.

| Key | Type | Units | Range | Default | Description |
|-----|------|-------|-------|---------|-------------|
| `shape` | [ApodizationType](#enum-cus-sequence-apodizationtype) |  |  |  | The type of apodization curve to use. |
| `size` | number | cm | 0.01 – 100 |  | The width of the curve. |

<a id="processing-lineformationinfo"></a>

### `lineformation`

Line formation settings.

| Key | Type | Units | Range | Default | Description |
|-----|------|-------|-------|---------|-------------|
| `spectralLine` | boolean |  |  | `false` | Spectral line flag to bypass lineformation and use standard dma |
| `accum` | integer |  | 1 – 16 | `1` | Number of lines to accumulate for a given scanline |
| `send` | integer |  | 1 – 16 | `1` | Number of lines to send for mla |
| `firstLine` | integer |  | 0 – 16 | `0` | First line to send within the mla |
| `lastLine` | integer |  | 0 – 16 | `0` | Last line to send within the mla |
| `maxFrameRate` | number | Hz | 0 – 1000 | `0` | Maximum frame rate allowed |
| `ecoMode` | boolean |  |  | `false` |  |
| `usePrevTimestamp` | boolean |  |  | `false` | Use the previous stream timestamp to correlate separate acquisitions such as b and rf |
| `powerdown` | [PowerDownMode](#enum-cus-afe-powerdownmode) |  |  | `partial` |  |
| `forcedWaitTime` | integer | ms | 0 – 60 | `0` | Forced wait time after a block, overrides max frame rate if no wait time calculated |
| `ceMode` | boolean |  |  | `false` | Contrast mode flag |
| `scale` | number |  |  | `1` | Scale factor |

<a id="processing-celfinfo"></a>

### `celf`

Contrast enhance line formation settings.

| Key | Type | Units | Range | Default | Description |
|-----|------|-------|-------|---------|-------------|
| `reverse` | boolean |  |  | `false` |  |

<a id="processing-envloginfo"></a>

### `envlog`

Envelope detection/log compression settings.

| Key | Type | Units | Range | Default | Description |
|-----|------|-------|-------|---------|-------------|
| `method` | integer |  | 0 – 1 | `0` |  |
| `dynrange` | number | dB | 0 – 255 |  |  |
| `noisefloor` | number | dB | 0 – 255 |  |  |
| `decim` | integer |  | 1 – 128 |  |  |
| `filter` | integer |  |  |  |  |
| `type` | [DataType (general)](#enum-cus-datatype) |  |  | `B pre-scan` |  |

<a id="processing-enhanceinfo"></a>

### `cfienhance`, `enhance`

The steps for an enhancement filter.

| Key | Type | Units | Range | Default | Description |
|-----|------|-------|-------|---------|-------------|
| `gamma` | number |  |  | `1` |  |
| `speckleSize` | number |  |  | `0.1` |  |
| `anisSmoothGain` | number |  |  | `2` |  |
| `edgeContinuity` | number |  |  | `0.5` |  |
| `edgeDiffusion` | number |  |  | `8` |  |
| `negEdgeFactor` | number |  |  | `1` |  |
| `posEdgeFactor` | number |  |  | `1` |  |
| `tmax` | number |  |  | `50` |  |
| `cfitype` | [CfiType](#enum-cus-cfitype) |  |  | `velocity` | The type of data to send as output, velocity, power, or variance |
| `contrast` | integer |  | -500 – 500 | `0` |  |
| `brightness` | integer |  | -500 – 500 | `0` |  |
| `maskContrast` | integer |  | -500 – 500 | `300` |  |
| `maskBrightness` | integer |  | -500 – 500 | `0` |  |
| `weight` | integer | % | 0 – 100 | `50` |  |
| `scale` | integer | % | 0 – 100 | `30` |  |
| `scalev` | integer (optional) | % | 0 – 100 |  |  |
| `filterin` | integer |  | 0 – 24 | `0` |  |
| `filterout` | integer |  | 0 – 24 | `0` |  |
| `kernel` | integer |  | 0 – 10 | `0` |  |
| `signScale` | integer | % | 0 – 100 | `50` |  |
| `signFilter` | integer |  | 0 – 24 | `0` |  |
| `velocity` | integer | % | 0 – 100 | `0` | Minimum velocity to apply after cfi enhancement |
| `enabled` | boolean |  |  | `true` | Flag to disable enhance, and just run scaler and blending |
| `mask` | boolean |  |  | `false` |  |

<a id="processing-edgeinfo"></a>

### `edge`

Edge enhancement settings.

| Key | Type | Units | Range | Default | Description |
|-----|------|-------|-------|---------|-------------|
| `kernel` | integer |  | 0 – 6 |  |  |
| `gain` | integer | % | 0 – 500 | `100` |  |

<a id="processing-gammainfo"></a>

### `gamma`

Gamma filter settings.

| Key | Type | Units | Range | Default | Description |
|-----|------|-------|-------|---------|-------------|
| `contrast` | integer |  | -500 – 500 | `0` |  |
| `brightness` | integer |  | -255 – 255 | `0` |  |
| `gamma` | number |  |  | `1` |  |
| `user` | boolean |  |  | `false` |  |

<a id="processing-scurveinfo"></a>

### `scurve`

S-curve filter settings.

| Key | Type | Units | Range | Default | Description |
|-----|------|-------|-------|---------|-------------|
| `a` | number |  |  | `0` |  |
| `b` | number |  |  | `1` |  |
| `e` | number |  |  | `1` |  |
| `max` | number |  |  | `255` |  |
| `reverse` | boolean |  |  | `false` |  |

<a id="processing-scaleinfo"></a>

### `scale`

Scale filter settings.

| Key | Type | Units | Range | Default | Description |
|-----|------|-------|-------|---------|-------------|
| `weight` | integer | % | 0 – 100 | `100` |  |
| `scale` | integer | % | 0 – 100 | `50` |  |
| `filterin` | integer |  | 0 – 24 | `0` |  |
| `filterout` | integer |  | 0 – 24 | `0` |  |

<a id="processing-persistinfo"></a>

### `persist`

Persistence settings.

| Key | Type | Units | Range | Default | Description |
|-----|------|-------|-------|---------|-------------|
| `strength` | integer | % | 0 – 100 |  |  |
| `cfitype` | [CfiType](#enum-cus-cfitype) (optional) |  |  |  | Cfi data type |

<a id="processing-flowdepthinfo"></a>

### `flowdepth`

Flow depth settings.

| Key | Type | Units | Range | Default | Description |
|-----|------|-------|-------|---------|-------------|
| `threshold` | integer |  |  | `30` |  |
| `cfitype` | [CfiType](#enum-cus-cfitype) |  |  |  | Cfi data type |

<a id="processing-jpeginfo"></a>

### `compress`

Compression (jpeg) settings.

| Key | Type | Units | Range | Default | Description |
|-----|------|-------|-------|---------|-------------|
| `quality` | integer | % | 0 – 100 |  | Standard JPEG quality in percent. |

<a id="processing-autogaininfo"></a>

### `autogain`

Autogain settings.

| Key | Type | Units | Range | Default | Description |
|-----|------|-------|-------|---------|-------------|
| `dynrange` | integer | dB | 0 – 100 |  |  |
| `noisefloor` | integer | dB | 0 – 100 |  |  |
| `depth` | number | cm | 0 – 50 |  |  |
| `targetGain` | number | dB | 0 – 100 |  |  |
| `adjustThreshold` | integer | dB | 0 – 100 | `1` |  |
| `deadThreshold` | integer | dB | 0 – 100 | `3` |  |
| `strength` | integer | % | 0 – 100 | `75` |  |
| `smooth` | number |  |  | `5` |  |
| `median` | integer |  | 0 – 2 | `0` |  |
| `gridx` | integer |  | 1 – 10 | `3` |  |
| `gridy` | integer |  | 1 – 15 | `3` |  |
| `vsound` | number | m/s |  | `1540` |  |
| `targetNf` | number (optional) | dB | 0 – 100 |  |  |

<a id="processing-flashsuppressinfo"></a>

### `flash`

Flash suppression settings.

| Key | Type | Units | Range | Default | Description |
|-----|------|-------|-------|---------|-------------|
| `strength` | integer | % | 0 – 100 | `100` |  |
| `median` | integer |  | 0 – 5 | `3` |  |
| `cfitype` | [CfiType](#enum-cus-cfitype) |  |  |  | Cfi data type |

<a id="processing-cfilfinfo"></a>

### `cfilf`

Color line formation settings.

| Key | Type | Units | Range | Default | Description |
|-----|------|-------|-------|---------|-------------|
| `ensemble` | integer |  | 1 – 24 |  |  |
| `type` | [DataType (general)](#enum-cus-datatype) |  |  | `IQ` |  |

<a id="processing-cfiwfacinfo"></a>

### `cfiwfac`

Color wallfilter and autocorrelation settings.

| Key | Type | Units | Range | Default | Description |
|-----|------|-------|-------|---------|-------------|
| `ensemble` | integer |  | 1 – 24 |  | The # of color pulses used for estimating speed |
| `order` | integer |  | 1 – 10 |  | The wall filter iir order |
| `wf` | number | Hz | 1 – 5000 |  | The wall filter cutoff frequency |
| `prf` | number | Hz | 1 – 25000 |  | The pulse repetition frequency of the acquisition |
| `shift` | integer |  | 0 – 32 | `14` | Shift value input for applying to the wf summation |
| `tissue` | boolean |  |  | `false` | Flag for running a low pass filter for tissue doppler |

<a id="processing-cfiprocinfo"></a>

### `cfiproc`

Color flow processing settings.

| Key | Type | Units | Range | Default | Description |
|-----|------|-------|-------|---------|-------------|
| `output` | [CfiType](#enum-cus-cfitype) |  |  |  | The type of data to send as output, velocity, power, or variance |
| `variance` | integer | % | 0 – 100 | `100` | The maximum variance threshold for cutting off the signal |
| `velocity` | integer | % | 0 – 100 | `0` | The minimum velocity threshold for cutting off the signal |
| `clutter` | number | dB | 0 – 255 | `255` | The maximum r0 clutter (pre-wall filtered) for cutting off the signal |
| `dynrange` | number | dB | 0 – 255 | `50` | Dynamic range of the power signal |
| `noiseFloor` | number | dB | 0 – 255 | `0` | Noise floor of the power signal |
| `invertClutter` | boolean |  |  | `false` | Flag to inverse the variance and clutter thresholding for marker isolation |
| `scaleFactor` | number |  | 1 – 10 | `1` | Scalar for the output values |

<a id="processing-pwwfinfo"></a>

### `pwwf`

Pulsed Wave Doppler wallfilter settings.

| Key | Type | Units | Range | Default | Description |
|-----|------|-------|-------|---------|-------------|
| `order` | integer |  | 1 – 10 |  | The wall filter iir order |
| `wf` | number | Hz | 1 – 5000 |  | The wall filter cutoff frequency |
| `prf` | number | Hz | 1 – 25000 |  | The pulse repetition frequency of the acquisition |
| `linesOut` | integer |  | 1 – 128 |  | Number of output lines |
| `window` | [WindowType](#enum-cus-windowtype) |  |  | `hanning` | Window type to apply to iq doppler data |
| `tissue` | boolean |  |  | `false` | Flag for running a low pass filter for tissue doppler |
| `audioGain` | number |  | 0.1 – 1000 | `1` | Gain amplifier to apply to audio samples |
| `audioFilter` | integer |  |  | `1` | Directional audio filter selection, 0 is off |
| `angleCorrect` | number | degrees |  | `0` | Angle correction |

<a id="processing-pwfftinfo"></a>

### `pwfft`

Pulsed Wave Doppler FFT settings.

| Key | Type | Units | Range | Default | Description |
|-----|------|-------|-------|---------|-------------|
| `size` | integer |  | 8 – 1024 | `128` | Fft size |
| `dynRange` | integer | dB | 0 – 255 | `60` | Dynamic range for the spectrum |
| `noiseFloor` | integer | dB | 0 – 255 | `10` | Noise floor for the spectrum |
| `window` | [WindowType](#enum-cus-windowtype) |  |  | `hanning` | Window type to apply to fft input data |

<a id="processing-strainprocinfo"></a>

### `strain`

Strain imaging processing settings.

| Key | Type | Units | Range | Default | Description |
|-----|------|-------|-------|---------|-------------|
| `searchThreshold` | number |  | 0 – 1 | `0.5` | Recovery search threshold |
| `correlationThreshold` | number |  | 0 – 1 | `0.6` | Correlation threshold |
| `strainAmplitude` | number |  | 0.1 – 2 | `1` | Strain Amplitude in Percentage |
| `dynamicScaling` | number |  | 0 – 5 | `1` | Dynamic scaling of mean strain value find the range |
| `decimation` | integer |  | 2 – 24 | `16` | Decimation from RF signal |
| `windowSize` | integer |  | 8 – 256 | `52` | Window size for cross correlation |
| `searchRadius` | integer |  | 10 – 50 | `30` | Search radius for cross correlation |
| `fullSearch` | integer |  | 5 – 50 | `10` | Number of full search allowed per scan line |
| `median` | integer |  | 1 – 7 | `3` | 2D median filter size |
| `lseSize` | integer |  | 2 – 16 | `4` | Least Squares Window size for strain estimation |
| `fullSearchSpacing` | integer |  | 1 – 10 | `4` | Spacing between full search |
| `noiseFloor` | integer | dB | 0 – 100 | `0` | Reject for RF signal |

<a id="processing-spatialprocinfo"></a>

### `spatialfilter`

Spatial filter processing settings.

| Key | Type | Units | Range | Default | Description |
|-----|------|-------|-------|---------|-------------|
| `filtertype` | [SpatialFilterType](#enum-cus-sequence-spatialfiltertype) |  |  |  | 2D filter type |
| `datatype` | [SpatialDataType](#enum-cus-sequence-spatialdatatype) |  |  |  | Input data type (gray, velocity) |
| `size` | integer |  | 0 – 63 | `3` | 2D filter size |
| `minVelocity` | integer | % | 0 – 100 | `10` | Min value for accepting cfi data |

<a id="processing-rawdatainfo"></a>

### `rawdata`

Raw data buffering settings.

| Key | Type | Units | Range | Default | Description |
|-----|------|-------|-------|---------|-------------|
| `dataType` | [DataType (raw)](#enum-cus-raw-datatype) |  |  |  |  |
| `size` | integer | MB | 0 – 512 |  |  |
| `storeImu` | boolean |  |  | `false` |  |
| `freq` | number | MHz |  | `0` |  |
| `focus` | number | mm |  | `0` |  |
| `depth` | number | mm |  | `0` |  |
| `pulse` | string (optional) |  |  |  |  |
| `mla` | integer (optional) |  |  |  |  |
| `prf` | number (optional) | kHz |  |  |  |
| `ensemble` | integer (optional) |  |  |  |  |

<a id="processing-imagebufferinfo"></a>

### `imagebuffer`

Image buffering settings.

| Key | Type | Units | Range | Default | Description |
|-----|------|-------|-------|---------|-------------|
| `size` | number | MB | 0 – 512 | `16` |  |

<a id="processing-sendstreaminfo"></a>

### `stream`

Stream settings.

| Key | Type | Units | Range | Default | Description |
|-----|------|-------|-------|---------|-------------|
| `delay` | integer | ms |  | `30` | Delay time to ignore sending frames while power supply adjusts |
| `frameRate` | integer | Hz |  | `0` | Max frame rate to stream the data |

<a id="processing-processinfo"></a>

### `imageprocessing`

Image processing chains.

| Key | Type | Units | Range | Default | Description |
|-----|------|-------|-------|---------|-------------|
| `type` | [ProcessType](#enum-cus-sequence-processtype) |  |  |  |  |
| `id` | string |  |  |  |  |
| `enabled` | boolean |  |  | `true` |  |
| `forward` | boolean |  |  | `false` | Flag to forward output to next stream as well |

<a id="processing-imageconfig"></a>

### `imaging`

Image streams (sequence + processing chain).

| Key | Type | Units | Range | Default | Description |
|-----|------|-------|-------|---------|-------------|
| `seq` | string (optional) |  |  |  | ID of the sequence to use. |
| `imgpro` | string |  |  |  | ID of the image processing chain to use. |
| `enabled` | boolean |  |  | `true` | Whether to enable the stream. |

<a id="processing-inertialinfo"></a>

### `inertial`

Inertial module settings.

| Key | Type | Units | Range | Default | Description |
|-----|------|-------|-------|---------|-------------|
| `enabled` | boolean |  |  |  |  |
| `applyBias` | boolean |  |  | `true` |  |
| `rate` | integer | Hz |  | `100` |  |
| `aodr` | [AOdr](#enum-cus-inertial-aodr) |  |  | `119` |  |
| `ascale` | [AScale](#enum-cus-inertial-ascale) |  |  | `2` |  |
| `alpf` | [ALpf](#enum-cus-inertial-alpf) |  |  | `none` |  |
| `adcf` | [ADcf](#enum-cus-inertial-adcf) |  |  | `none` |  |
| `aenx` | boolean |  |  | `true` |  |
| `aeny` | boolean |  |  | `true` |  |
| `aenz` | boolean |  |  | `true` |  |
| `godr` | [GOdr](#enum-cus-inertial-godr) |  |  | `119` |  |
| `gscale` | [GScale](#enum-cus-inertial-gscale) |  |  | `245` |  |
| `glpf` | [GLpf](#enum-cus-inertial-glpf) |  |  | `low` |  |
| `ghpf` | [GHpf](#enum-cus-inertial-ghpf) |  |  | `none` |  |
| `genx` | boolean |  |  | `true` |  |
| `geny` | boolean |  |  | `true` |  |
| `genz` | boolean |  |  | `true` |  |
| `gflipx` | boolean |  |  | `false` |  |
| `gflipy` | boolean |  |  | `false` |  |
| `gflipz` | boolean |  |  | `false` |  |
| `glowpower` | boolean |  |  | `false` |  |
| `glatch` | boolean |  |  | `false` |  |
| `modr` | [MOdr](#enum-cus-inertial-modr) |  |  | `80` |  |
| `mscale` | [MScale](#enum-cus-inertial-mscale) |  |  | `4` |  |
| `moperation` | [MOperation](#enum-cus-inertial-moperation) |  |  | `continuous` |  |
| `mxyperf` | [MPerf](#enum-cus-inertial-mperf) |  |  | `ultra` |  |
| `mzperf` | [MPerf](#enum-cus-inertial-mperf) |  |  | `ultra` |  |
| `mlowpower` | boolean |  |  | `false` |  |
| `mtempcomp` | boolean |  |  | `true` |  |
| `hd3alpf` | [HD3ALpf](#enum-cus-inertial-hd3alpf) |  |  | `2` |  |
| `hd3glpf` | [HD3GLpf](#enum-cus-inertial-hd3glpf) |  |  | `highest` |  |
| `hd3ghpf` | [HD3GHpf](#enum-cus-inertial-hd3ghpf) |  |  | `none` |  |
| `hd3modr` | [HD3MOdr](#enum-cus-inertial-hd3modr) |  |  | `100` |  |
| `hd3godr` | [HD3GOdr](#enum-cus-inertial-hd3godr) |  |  | `104` |  |
| `hd3gscale` | [HD3GScale](#enum-cus-inertial-hd3gscale) |  |  | `250` |  |
| `hd3mlpf` | boolean |  |  | `false` |  |
| `hd3moc` | boolean |  |  | `false` |  |
| `hd3msoc` | boolean |  |  | `false` |  |

## Sequences

### High-level sequences (`frames` + `blocks`)

<a id="sequences-blocks"></a>

#### Top-level keys

The script describing sequence blocks.

| Key | Type | Units | Range | Default | Description |
|-----|------|-------|-------|---------|-------------|
| `frames` | map of id → [FrameInfo](#sequences-frameinfo) |  |  |  | Frames prototypes which will be used when creating sequences. |
| `tx` | map of id → [TransmitBasic](#sequences-transmitbasic) |  |  |  | Transmit prototypes which will be used when creating sequences. |
| `rx` | map of id → [ReceiveBasic](#sequences-receivebasic) |  |  |  | Receive prototypes which will be used when creating sequences. |
| `blocks` | list of [Block](#sequences-block) |  |  |  | Blocks which will be transformed into sequences. |

<a id="sequences-frameinfo"></a>

#### `frames`

Frames prototypes which will be used when creating sequences.

| Key | Type | Units | Range | Default | Description |
|-----|------|-------|-------|---------|-------------|
| `start` | number | cm | 0 – 50 |  | Start depth for data capture |
| `end` | number | cm | 0 – 50 |  | End depth for data capture |
| `lines` | integer |  | 1 – 2048 |  | Number of lines across the frame |
| `decim` | integer |  | 1 – 128 |  | Decimation factor for the output |
| `lpf` | string |  |  |  | Low-pass filter id for decimation |
| `output` | [DataType (general)](#enum-cus-datatype) |  |  |  | Output type for the frame |
| `tgc` | string |  |  |  | Analog tgc to use |
| `start element` | number |  | ≤ 2048 |  | First element to use |
| `end element` | number |  | ≤ 2048 |  | Last element to use |
| `start angle` | number | degrees | -90 – 90 |  | First angle to use |
| `end angle` | number | degrees | -90 – 90 |  | Last angle to use |
| `vsound` | number | m/s |  | `1540` | Speed of sound |
| `sync` | [Sync](#enum-cus-sequence-sync) |  |  | `none` | Synchronization flag for various purposes |
| `syncSelect` | integer (optional) |  | 0 – 50000 |  | Selected line for sync output |
| `blankLines` | boolean |  |  | `false` | Blank line flag for cfi |
| `overlap` | integer |  |  | `0` | Number of overlapping lines between events |
| `spectralLine` | boolean |  |  | `false` | Spectral line flag to bypass lineformation and use regular dma |
| `acoustic mode` | [Mode (acoustic)](#enum-cus-acoustic-mode) |  |  |  | Acoustic mode |
| `focus` | list of [FocusInfo](#sequences-focusinfo) |  |  |  | Focus info for each line |
| `minLineDuration` | integer (optional) | µs | 0 – 1000 |  | Minimum line duration for each event |
| `afe` | string (optional) |  |  |  | Analog front-end settings. |
| `lgc` | string (optional) |  |  |  | Digital lgc to use |
| `egc` | string (optional) |  |  |  | Element lgc to use |
| `color` | [ColorInfo](#sequences-colorinfo) (optional) |  |  |  | Color doppler info |
| `duplex` | [DuplexInfo](#sequences-duplexinfo) (optional) |  |  |  | Duplex info for m-mode or pwd |
| `interleave` | integer (optional) |  |  |  | Interleave streams count |
| `psSync` | boolean |  |  | `false` | Flag to enable power supply synchronization |

<a id="sequences-transmitbasic"></a>

#### `tx`

Transmit prototypes which will be used when creating sequences.

| Key | Type | Units | Range | Default | Description |
|-----|------|-------|-------|---------|-------------|
| `shape` | string |  |  |  |  |
| `freq` | string |  |  |  |  |
| `fnumber` | string |  |  |  |  |
| `maxApt` | string |  |  |  |  |

<a id="sequences-receivebasic"></a>

#### `rx`

Receive prototypes which will be used when creating sequences.

| Key | Type | Units | Range | Default | Description |
|-----|------|-------|-------|---------|-------------|
| `shallow` | string |  |  |  |  |
| `deep` | string |  |  |  |  |
| `depth` | string |  |  |  |  |
| `fnumber` | string |  |  |  |  |
| `apod` | string |  |  |  |  |
| `type` | [FocusType](#enum-cus-sequence-focustype) |  |  |  |  |

<a id="sequences-block"></a>

#### `blocks`

Blocks which will be transformed into sequences.

| Key | Type | Units | Range | Default | Description |
|-----|------|-------|-------|---------|-------------|
| `id` | string |  |  |  | The ID of the block. |
| `angle` | number | degrees |  |  | The angle at which to sequence the frame. |
| `frame` | string |  |  |  | The ID of the frame to sequence. |
| `enabled` | boolean |  |  | `true` |  |

<a id="sequences-focusinfo"></a>

#### `frames.focus`

Focus info for each line.

| Key | Type | Units | Range | Default | Description |
|-----|------|-------|-------|---------|-------------|
| `dtgcs` | list of string |  |  |  | Digital tgcs to use for each beamformer |
| `focus` | string |  |  |  | Transmit focus depth |
| `tx` | string |  |  |  | Transmit id |
| `rx` | string |  |  |  | Receive id |
| `channels` | string |  |  |  | Channel selection |
| `txLineOffset` | integer |  |  | `0` | Transmit line offset to apply to each event |
| `rxLineOffset` | integer |  |  | `0` | Receive line offset to apply to each event |
| `rxAptOffset` | integer |  | -64 – 64 | `0` | Offset to apply to the receive aperture (for synthetic aperture) |
| `enabled` | boolean |  |  | `true` |  |

<a id="sequences-colorinfo"></a>

#### `frames.color`

Color doppler info.

| Key | Type | Units | Range | Default | Description |
|-----|------|-------|-------|---------|-------------|
| `ensemble` | integer |  | 1 – 24 |  | Number of times to repeat each line for cfi |
| `prf` | number | kHz | 0.1 – 10 |  | Prf in khz |
| `wf` | number | Hz | 1 – 2000 |  | Wall filter in hz |
| `blankDuration` | number (optional) | ms |  |  | Duration to sequence blank lines to mitigate supply droop artefacts |

<a id="sequences-duplexinfo"></a>

#### `frames.duplex`

Duplex info for m-mode or pwd.

| Key | Type | Units | Range | Default | Description |
|-----|------|-------|-------|---------|-------------|
| `mode` | [DuplexMode](#enum-cus-sequence-duplexmode) |  |  | `duplex` |  |
| `prf` | number | kHz | 0.05 – 20 |  | Duplex PRF in kHz for M-mode or PW Doppler |
| `linesPerDma` | integer |  |  |  | # of lines in a single dma block for duplex modes (m/pw), if jpeg used, then this should be a multiple of 8 |
| `blankBTime` | integer | µs |  | `0` | Time to sequence blank lines for |
| `wf` | number (optional) | Hz | 1 – 1500 |  | Duplex WF in Hz for PW Doppler |
| `hprf` | boolean |  |  | `false` | Whether high-PRF wrapping is permitted; range-wraps the spectral line when the gate will not fit one PRP, in any display mode |

### Event-by-event sequences (`seq` + `events`)

<a id="sequences-sequences"></a>

#### Top-level keys

The script describing sequences.

| Key | Type | Units | Range | Default | Description |
|-----|------|-------|-------|---------|-------------|
| `tx` | map of id → [TransmitInfo](#sequences-transmitinfo) |  |  |  |  |
| `rx` | map of id → [ReceiveInfo](#sequences-receiveinfo) |  |  |  |  |
| `seq` | map of id → [SequenceInfo](#sequences-sequenceinfo) |  |  |  |  |

<a id="sequences-transmitinfo"></a>

#### `tx`

The information for a single transmit pattern.

| Key | Type | Units | Range | Default | Description |
|-----|------|-------|-------|---------|-------------|
| `shape` | string |  |  |  |  |
| `focus` | number | mm | 0 – 1000 |  |  |
| `freq` | number | MHz | 1 – 40 |  |  |
| `fnumber` | number |  | 0.01 – 20 |  |  |
| `channels` | string |  |  |  |  |
| `maxApt` | integer |  | 0 – 512 |  |  |
| `cwMode` | boolean |  |  | `false` | CW mode flag |

<a id="sequences-receiveinfo"></a>

#### `rx`

The information for a single receive pattern.

| Key | Type | Units | Range | Default | Description |
|-----|------|-------|-------|---------|-------------|
| `shallow` | number | MHz | 1 – 200 |  |  |
| `deep` | number | MHz | 1 – 200 |  |  |
| `depth` | number | mm | 0 – 500 |  |  |
| `fnumber` | number |  | 0.01 – 20 |  |  |
| `channels` | string |  |  |  |  |
| `apod` | string |  |  |  |  |
| `dtgc` | string |  |  |  |  |
| `type` | [FocusType](#enum-cus-sequence-focustype) |  |  |  |  |

<a id="sequences-sequenceinfo"></a>

#### `seq`

The description of a single sequence.

| Key | Type | Units | Range | Default | Description |
|-----|------|-------|-------|---------|-------------|
| `start` | number | cm | 0 – 50 |  | Start depth for data capture. |
| `end` | number | cm | 0 – 50 |  | End depth for data capture. |
| `vsound` | number | m/s |  | `1540` | Speed of sound |
| `targetLineDuration` | integer | µs | ≥ 0 |  | Time duration for each event in the sequence. |
| `events` | list of [EventInfo](#sequences-eventinfo) |  |  |  | Events which make up the sequence. |
| `decim` | integer |  | 1 – 128 |  | Decimation factor for the output. |
| `output` | [DataType (general)](#enum-cus-datatype) |  |  |  | Output type for the sequence. |
| `repeat` | list of [EventRepeat](#sequences-eventrepeat) |  |  |  | Instructions for repeating events. |
| `color` | [ColorInfo](#sequences-colorinfo) (optional) |  |  |  | Color information for the sequence. |
| `duplex` | [DuplexOutput](#sequences-duplexoutput) (optional) |  |  |  | Duplex information for the sequence. |
| `afe` | string (optional) |  |  |  | Analog front-end settings. |
| `lgc` | string (optional) |  |  |  | Angle lgc |
| `egc` | string (optional) |  |  |  | Element lgc |
| `interleave` | integer (optional) |  |  |  | Interleave streams count |

<a id="sequences-eventinfo"></a>

#### `seq.events`

Events which make up the sequence.

| Key | Type | Units | Range | Default | Description |
|-----|------|-------|-------|---------|-------------|
| `el` | number |  | -1 – 513 |  | Element on which the transmit is centered |
| `rxAngle` | number | degrees | -90 – 90 |  |  |
| `txAngle` | number | degrees | -90 – 90 |  |  |
| `rxAptOffset` | integer |  | -256 – 256 | `0` | Offset to apply to the receive aperture (for synthetic aperture) |
| `txAptOffset` | integer |  | -256 – 256 | `0` | Offset to apply to the transmit aperture (for synthetic aperture) |
| `tx` | string |  |  |  | Transmit ID to use for this event |
| `rx` | list of [RxMapping](#sequences-rxmapping) |  |  |  | List of receive mappings to use for the different beamformers |
| `tgc` | string |  |  |  | Analog tgc to use for this event |
| `lpf` | integer |  |  |  | Low-pass filter id for decimation |
| `lineDuration` | integer (optional) | µs | ≥ 0 |  | Time duration the event |
| `sync` | boolean |  |  | `false` | Synchronization flag to trigger the ttl output |
| `spectralLine` | boolean |  |  | `false` | Spectral line flag to bypass line formation and use regular dma |
| `blank` | boolean |  |  | `false` | Creates blank line |
| `cw` | boolean |  |  | `false` | Enables cw transmission |
| `psSync` | boolean |  |  | `false` | Flag to enable power supply synchronization |

<a id="sequences-eventrepeat"></a>

#### `seq.repeat`

Instructions for repeating events.

| Key | Type | Units | Range | Default | Description |
|-----|------|-------|-------|---------|-------------|
| `count` | integer |  |  |  | Number of events in the sequence to repeat. |
| `times` | integer |  |  |  | Number of times to repeat the events in the sequence. |
| `element offset` | number |  | -513 – 513 |  | How much to offset the elements each repetition. |
| `rx angle offset` | number | degrees | -90 – 90 |  | How much to offset the receive angle each repetition. |
| `tx angle offset` | number | degrees | -90 – 90 |  | How much to offset the transmit angle each repetition. |

<a id="sequences-duplexoutput"></a>

#### `seq.duplex`

Duplex information for the sequence.

| Key | Type | Units | Range | Default | Description |
|-----|------|-------|-------|---------|-------------|
| `enabled` | boolean |  |  | `false` |  |
| `mode` | [DuplexMode](#enum-cus-sequence-duplexmode) |  |  | `duplex` |  |
| `interleave` | integer |  | 0 – 255 |  |  |
| `linesPerDma` | integer |  |  |  | # of lines in a single dma block for duplex modes (m/pw), if jpeg used, then this should be a multiple of 8 |
| `blankLines` | integer |  |  |  |  |
| `blankLineDurationMicrosec` | integer |  |  |  |  |
| `prpMicrosec` | integer |  |  |  |  |
| `linePeriodMicrosec` | integer |  |  |  |  |
| `linePeriodLastMicrosec` | integer |  |  |  |  |
| `linePeriodLastMicrosecCompound` | integer |  |  |  |  |
| `wf` | number (optional) | Hz |  |  | Duplex WF in Hz for PW Doppler |
| `phantomGateCM` | list of number |  |  |  | Phantom (range-ambiguous) gate depths for HPRF, for display markers |

<a id="sequences-rxmapping"></a>

#### `seq.events.rx`

List of receive mappings to use for the different beamformers.

| Key | Type | Units | Range | Default | Description |
|-----|------|-------|-------|---------|-------------|
| `el-offset` | number |  | -256 – 256 | `0` |  |
| `angle-offset` | number | degrees | -90 – 90 | `0` |  |
| `rx` | string |  |  |  |  |

## Probe

<a id="probe-probe"></a>

### Top-level keys

Probe definition.

| Key | Type | Units | Range | Default | Description |
|-----|------|-------|-------|---------|-------------|
| `geometry` | [Geometry](#probe-geometry) |  |  |  |  |
| `capabilities` | [Capabilities](#probe-capabilities) |  |  |  |  |
| `stackinfo` | [StackInfo](#probe-stackinfo) |  |  |  |  |
| `vet` | boolean |  |  | `false` |  |
| `adapter` | [Adapter](#probe-adapter) (optional) |  |  |  |  |
| `defaults` | [Defaults](#probe-defaults) (optional) |  |  |  |  |
| `biopsy` | [Biopsy](#probe-biopsy) (optional) |  |  |  |  |
| `freq` | [FrequencyRange](#probe-frequencyrange) (optional) |  |  |  |  |

<a id="probe-geometry"></a>

### `geometry`

The probe geometry.

| Key | Type | Units | Range | Default | Description |
|-----|------|-------|-------|---------|-------------|
| `type` | [Type (probe)](#enum-cus-probe-type) |  |  |  | The type of element configuration. |
| `elements` | integer |  | 1 – 512 |  | The number of elements. |
| `pitch` | number | µm | 1 – 10000 |  | The distance from one element center to the next. |
| `radius` | number | mm | -1000 – 1000 |  | The probe radius (for curved probes). |
| `lensThickness` | number | mm | 0 – 10 |  | The probe lens thickness (distance from element to probe surface). |
| `startelement` | integer |  | 0 – 511 | `0` | The start element for the geometry. |

<a id="probe-capabilities"></a>

### `capabilities`

The probe capabilities.

| Key | Type | Units | Range | Default | Description |
|-----|------|-------|-------|---------|-------------|
| `scanlines` | integer |  | 1 – 512 |  | The number of elements. |
| `tx` | integer |  | 1 – 256 |  | The number of transmit channels. |
| `rx` | integer |  | 1 – 256 |  | The number of receive channels. |
| `bf` | integer |  | 1 – 8 |  | The maximum number of beamformers. |
| `mla` | integer |  | 1 – 8 | `4` | The default number of MLA lines |
| `txClock` | number | MHz | 1 – 200 |  | The base transmit clock frequency. |
| `rxClock` | number | MHz | 1 – 200 |  | The base receive clock frequency. |
| `platform` | [Platform](#enum-cus-version-platform) |  |  |  |  |
| `revision` | integer |  |  | `1` |  |

<a id="probe-stackinfo"></a>

### `stackinfo`

The stack information.

| Key | Type | Units | Range | Default | Description |
|-----|------|-------|-------|---------|-------------|
| `elevationHeight` | number | mm | -1000 – 1000 |  | Elevation height of an element |
| `elevationFocus` | number | mm | -1000 – 1000 |  | Elevation focus location |
| `centerFreq` | number | MHz | 1 – 25 |  | Center frequency |
| `lowFreq` | number | MHz | 1 – 40 |  | Lower range of the bandwidth |
| `upperFreq` | number | MHz | 1 – 40 |  | Upper range of the bandwidth |
| `phased array` | boolean |  |  | `false` | Phased array flag |

<a id="probe-adapter"></a>

### `adapter`

The probe adapter information.

| Key | Type | Units | Range | Default | Description |
|-----|------|-------|-------|---------|-------------|
| `type` | [AdapterType](#enum-cus-probe-adaptertype) |  |  |  | The type of adapter. |
| `thickness` | number | mm | 0 – 100 |  | The thickness of the adapter at the center of the probe face. |
| `width` | number | mm | 0 – 300 |  | The width of the adapter. |

<a id="probe-defaults"></a>

### `defaults`

The probe default parameters.

| Key | Type | Units | Range | Default | Description |
|-----|------|-------|-------|---------|-------------|
| `depth` | number | cm | 1 – 30 | `5` | Default depth |
| `dopplerFreq` | number | MHz | 1 – 20 | `5` | Default doppler frequency |
| `compound angle` | number | degrees | 0 – 45 | `0` | Default compounding angle |
| `extension angle` | number | degrees | 0 – 45 | `0` | Default extension angle |
| `cardiac angle` | number | degrees | 0 – 60 | `45` | Default cardiac angle |
| `max steering angle` | number | degrees | 0 – 45 | `0` | Maximum steering angle |
| `needle start` | number | degrees | 0 – 45 | `0` | Needle start angle |
| `needle step` | number | degrees | 0 – 25 | `0` | Needle step angle |
| `max zoom` | number | % | 100 – 2000 | `500` | Maximum zoom |
| `compound gain compensation` | number | dB | -50 – 50 | `20` | Edge gain compensation |

<a id="probe-biopsy"></a>

### `biopsy`

Probe biopsy information.

| Key | Type | Units | Range | Default | Description |
|-----|------|-------|-------|---------|-------------|
| `x origin` | number | mm |  |  | X coordinate of the opening, relative to the center of the probe surface, in mm |
| `y origin` | number | mm |  |  | Y coordinate of the opening, relative to the center of the probe surface, in mm |
| `width` | number | mm |  |  | Width of the guide on screen in mm |
| `angle` | number | degrees |  |  | Angle of the guide on screen in degrees |

<a id="probe-frequencyrange"></a>

### `freq`

Sliding frequency range for imaging.

| Key | Type | Units | Range | Default | Description |
|-----|------|-------|-------|---------|-------------|
| `start depth` | number | mm | -1000 – 1000 |  | Start depth to start sliding frequency |
| `end depth` | number | mm | -1000 – 1000 |  | End depth to start sliding frequency |
| `lowFreq` | number | MHz | 1 – 40 |  | Lowest frequency to slide to |
| `upperFreq` | number | MHz | 1 – 40 |  | High frequency to start with |

## Parameters

<a id="parameters-definitions"></a>

### Top-level keys

Parameter definitions and values (from the script).

| Key | Type | Units | Range | Default | Description |
|-----|------|-------|-------|---------|-------------|
| `params` | map of id → string |  |  |  | Parameter values/equations. |
| `definitions` | list of [Info](#parameters-info) |  |  |  | Parameter definitions. |

<a id="parameters-info"></a>

### `definitions`

Parameter definitions.

| Key | Type | Units | Range | Default | Description |
|-----|------|-------|-------|---------|-------------|
| `id` | string |  |  |  | Parameter identifier |
| `description` | string |  |  |  | Parameter description |
| `units` | [UnitType](#enum-cus-unittype) (optional) |  |  |  | Physical units |
| `min` | number (optional) |  |  |  | Minimum value |
| `max` | number (optional) |  |  |  | Maximum value |
| `value` | number (optional) |  |  |  |  |
| `step` | number (optional) |  |  |  |  |
| `slow` | number (optional) |  |  |  | Slow value |
| `fast` | number (optional) |  |  |  | Fast value |
| `min equation` | string (optional) |  |  |  | Equation for the minimum value, evaluated against the collection at load (e.g. a probe-derived limit); overrides 'min' when present |
| `max equation` | string (optional) |  |  |  | Equation for the maximum value, evaluated against the collection at load (e.g. a probe-derived limit); overrides 'max' when present |
| `step equation` | string (optional) |  |  |  | Equation for the step value, evaluated against the collection at load; overrides 'step' when present |

## Enumerations

Enumerated keys accept one of the values below, written exactly as shown.

<a id="enum-cus-afe-acterm"></a>

### AcTerm

The active termination value. Used by: `afe.activeterm`.

`off`, `low`, `med`, `high`, `ultra`

<a id="enum-cus-probe-adaptertype"></a>

### AdapterType

The types of probe adapter. Used by: `adapter.type`.

| Value | Description |
|-------|-------------|
| `linear` | Adapting to a linear surface. |
| `phased` | Adapting to a phased surface. |

<a id="enum-cus-inertial-adcf"></a>

### ADcf

Accelerometer digital filter bandwidth. Used by: `inertial.adcf`.

`none`, `odr9`, `odr50`, `odr100`, `odr400`

<a id="enum-cus-inertial-alpf"></a>

### ALpf

Accelerometer low pass filter. Used by: `inertial.alpf`.

`none`, `50`, `105`, `211`, `408`

<a id="enum-cus-inertial-aodr"></a>

### AOdr

Accelerometer output data rate. Used by: `inertial.aodr`.

`off`, `10`, `50`, `119`, `238`, `476`, `952`

<a id="enum-cus-sequence-apodizationtype"></a>

### ApodizationType

The type of apodization to apply in beamforming. Used by: `apod.shape`.

| Value | Description |
|-------|-------------|
| `hamming` | Standard Hamming window with the specified width. |
| `hanning` | Standard Hanning window with the specified width. |
| `rectangular` | Rectangle window with the specified width. |
| `zero` | All zero values. |
| `ones` | All one values (including the first sample). |
| `triangular` | Ramp from zero to one at the specified width. |

<a id="enum-cus-inertial-ascale"></a>

### AScale

Accelerometer scale. Used by: `inertial.ascale`.

`2`, `4`, `8`, `16`

<a id="enum-cus-cfitype"></a>

### CfiType

The type of output from color Doppler autocorrelation. Used by: `cfiproc.output`, `enhance.cfitype`, `flash.cfitype`, `flowdepth.cfitype`, `persist.cfitype`.

| Value | Description |
|-------|-------------|
| `velocity` | Velocity data, signed 8 bit |
| `power` | Power data, unsigned 8 bit |
| `variance` | Sigma data, unsigned 8 bit |
| `clutter` | Clutter data, unsigned 8 bit |

<a id="enum-cus-datatype"></a>

### DataType (general)

The types of image data which are handled in the software. Used by: `cfilf.type`, `envlog.type`, `frames.output`, `seq.output`.

| Value | Description |
|-------|-------------|
| `B pre-scan` | Pre-scan-converted B-mode data. |
| `B post-scan` | Post-scan-converted B-mode data. |
| `B post-scan grayscale` | Post-scan-converted B-mode data (grayscale). |
| `color pre-scan` | Pre-scan-converted color-mode data (velocity or power). |
| `M pre-scan` | Pre-scan-converted M-mode data. |
| `PW spectrum` | FFT computed Pulsed Wave Doppler spectrum. |
| `strain pre-scan` | Pre-scan-converted strain imaging data. |
| `contrast pre-scan` | Pre-scan-converted contrast imaging data. |
| `A` | A 16-bit signed data. |
| `RF` | RF 16-bit signed data. |
| `Channel` | RF 14-bit signed data. |
| `IQ` | I and Q 16-bit signed data packed into a 32-bit integer. |
| `Transmit Only` | Empty data for arfi pushes, etc. |

<a id="enum-cus-raw-datatype"></a>

### DataType (raw)

The types of raw data. Used by: `rawdata.dataType`.

`iq`, `env`, `sc`, `m`, `rf`, `channel`, `cfi`, `pw`, `strain`, `ce`, `imu`, `volume`

<a id="enum-cus-afe-digihpf"></a>

### DigiHpf

The digital high pass filter setting. Used by: `afe.digihpf`.

`off`, `low`, `med`, `high`

<a id="enum-cus-sequence-duplexmode"></a>

### DuplexMode

The type of duplex modes. Used by: `frames.duplex.mode`, `seq.duplex.mode`.

`duplex`, `mono`, `bimage`

<a id="enum-cus-sequence-focustype"></a>

### FocusType

The type of focusing to apply in beamforming. Used by: `rx.type`.

| Value | Description |
|-------|-------------|
| `none` | Receive with a constant delay curve. |
| `dynamic` | Receive with a dynamic delay curve. |

<a id="enum-cus-inertial-ghpf"></a>

### GHpf

Gyroscope high pass filter. Used by: `inertial.ghpf`.

`none`, `lowest`, `lower`, `low`, `medium1`, `medium2`, `medium3`, `high`, `higher`, `highest`, `maximum`

<a id="enum-cus-inertial-glpf"></a>

### GLpf

Gyroscope low pass filter. Used by: `inertial.glpf`.

`low`, `medium`, `high`, `highest`

<a id="enum-cus-inertial-godr"></a>

### GOdr

Gyroscope output data rate. Used by: `inertial.godr`.

`off`, `15`, `60`, `119`, `238`, `476`, `952`

<a id="enum-cus-inertial-gscale"></a>

### GScale

Gyroscope scale. Used by: `inertial.gscale`.

`245`, `500`, `2000`

<a id="enum-cus-inertial-hd3alpf"></a>

### HD3ALpf

Accelerometer low pass filter for HD3. Used by: `inertial.hd3alpf`.

`2`, `4`, `10`, `20`, `45`, `100`, `200`, `400`, `800`

<a id="enum-cus-inertial-hd3ghpf"></a>

### HD3GHpf

Gyro high pass filter cutoff in mHz. Used by: `inertial.hd3ghpf`.

`none`, `16`, `65`, `260`, `1040`

<a id="enum-cus-inertial-hd3glpf"></a>

### HD3GLpf

Gyroscope low pass filter bandwidth for HD3. Used by: `inertial.hd3glpf`.

`highest`, `higher`, `high`, `medium1`, `medium2`, `low`, `lower`, `lowest`

<a id="enum-cus-inertial-hd3godr"></a>

### HD3GOdr

Gyroscope output data rate for HD3. Used by: `inertial.hd3godr`.

`off`, `12`, `26`, `52`, `104`, `208`, `416`, `833`, `1660`, `3330`, `6660`

<a id="enum-cus-inertial-hd3gscale"></a>

### HD3GScale

Gyroscope scale. Used by: `inertial.hd3gscale`.

`250`, `500`, `1000`, `2000`

<a id="enum-cus-inertial-hd3modr"></a>

### HD3MOdr

Magnetometer output data rate for hd3. Used by: `inertial.hd3modr`.

`10`, `20`, `50`, `100`

<a id="enum-cus-afe-lnaclamp"></a>

### LnaClamp

The lna clamp setting. Used by: `afe.lnaclamp`.

`auto`, `low`, `med`, `high`

<a id="enum-cus-afe-lnagain"></a>

### LnaGain

The lna gain setting. Used by: `afe.lnagain`.

`low`, `med`, `high`

<a id="enum-cus-afe-lnahpf"></a>

### LnaHpf

The lna high pass filter setting. Used by: `afe.lnahpf`.

`off`, `low`, `med`, `high`, `ultra`

<a id="enum-cus-afe-lpf"></a>

### Lpf

The low pass filter setting. Used by: `afe.lpf`.

`low`, `med`, `high`, `ultra`

<a id="enum-cus-acoustic-mode"></a>

### Mode (acoustic)

Acoustic modes. Used by: `frames.acoustic mode`.

`b`, `color`, `m`, `pw`, `rf`, `a`

<a id="enum-cus-inertial-modr"></a>

### MOdr

Magnetometer output data rate. Used by: `inertial.modr`.

`0.625`, `1.25`, `2.5`, `5`, `10`, `20`, `40`, `80`

<a id="enum-cus-inertial-moperation"></a>

### MOperation

Magnetometer operation. Used by: `inertial.moperation`.

`off`, `single`, `continuous`

<a id="enum-cus-inertial-mperf"></a>

### MPerf

Magnetometer performance. Used by: `inertial.mxyperf`, `inertial.mzperf`.

`low`, `medium`, `high`, `ultra`

<a id="enum-cus-inertial-mscale"></a>

### MScale

Magnetometer scale. Used by: `inertial.mscale`.

`4`, `8`, `12`, `16`

<a id="enum-cus-afe-pgaclamp"></a>

### PgaClamp

The pga clamp setting. Used by: `afe.pgaclamp`.

`disabled`, `m2`, `0`

<a id="enum-cus-afe-pgagain"></a>

### PgaGain

The pga gain setting. Used by: `afe.pgagain`.

`low`, `med`, `high`, `ultra`

<a id="enum-cus-version-platform"></a>

### Platform

Major Clarius platforms. Used by: `capabilities.platform`.

| Value | Description |
|-------|-------------|
| `v3` | Third generation (HD3) |

<a id="enum-cus-afe-powerdownmode"></a>

### PowerDownMode

The AFE power down mode settings. Used by: `lineformation.powerdown`.

`off`, `partial`, `full`

<a id="enum-cus-sequence-processtype"></a>

### ProcessType

The type of image processing which will occur in a step. Used by: `imageprocessing.type`.

`lineformation`, `envlog`, `enhance`, `edge`, `gamma`, `scurve`, `scale`, `persist`, `flowdepth`, `compress`, `stream`, `autogain`, `flashsuppress`, `cfilf`, `cfiwfac`, `cfiproc`, `cfienhance`, `pwwf`, `pwfft`, `strain`, `spatialfilter`, `rawdata`, `imagebuffer`, `celf`

<a id="enum-cus-sequence-spatialdatatype"></a>

### SpatialDataType

The spatial filter data types. Used by: `spatialfilter.datatype`.

`gray`, `velocity`

<a id="enum-cus-sequence-spatialfiltertype"></a>

### SpatialFilterType

The spatial filter types. Used by: `spatialfilter.filtertype`.

| Value | Description |
|-------|-------------|
| `median` | Median in a 2D window |
| `lineToLine` | Averaging gain from line to line |

<a id="enum-cus-sequence-sync"></a>

### Sync

The sync pulse type. Used by: `frames.sync`.

| Value | Description |
|-------|-------------|
| `none` | No sync |
| `frame` | Sync on center line |
| `line` | Sync on all lines |
| `select` | Sync on selected line |

<a id="enum-cus-probe-type"></a>

### Type (probe)

The types of probes. Used by: `geometry.type`.

| Value | Description |
|-------|-------------|
| `curved` | Curved array of elements (radius must be specified). |
| `linear` | Linear array of elements. |

<a id="enum-cus-unittype"></a>

### UnitType

The physical unit types which the software recognizes. Used by: `definitions.units`.

`µm`, `mm`, `cm`, `m`, `mm²`, `cm²`, `m²`, `cm³`, `mm³`, `cc`, `mL`, `L`, `ng/mL`, `ng/mL²`, `L/min`, `mL/min`, `ns`, `µs`, `ms`, `s`, `minutes`, `hours`, `days`, `weeks`, `years`, `cm/s`, `m/s`, `cm/s²`, `m/s²`, `g/m²`, `Hz`, `kHz`, `MHz`, `bpm`, `dB`, `dBm`, `°`, `rad`, `%`, `mg`, `g`, `kg`, `Pa`, `kPa`, `bits`, `bps`, `kbps`, `Mbps`, `Gbps`, `bytes`, `kB`, `MB`, `GB`, `mA`, `A`, `kA`, `mV`, `V`, `kV`, `mW`, `W`, `kW`, `mmHg`, `mAh`, `inches`, `feet`, `lbs`, `sqft`

<a id="enum-cus-afe-vcapower"></a>

### VcaPower

The vca power level. Used by: `afe.vcapower`.

`high`, `normal`, `low`

<a id="enum-cus-windowtype"></a>

### WindowType

The type of window types to apply to signals. Used by: `pwfft.window`, `pwwf.window`.

| Value | Description |
|-------|-------------|
| `hanning` | Hanning window |
| `hamming` | Hamming window |
| `blackman` | Blackman window |
| `flatTop` | Flat top window |
| `blackmanHarris` | Blackman harris window |
| `blackmanNuttal` | Blackman nuttal window |
| `nuttal` | Nuttal window |
| `sine` | Sine window |
| `rectangle` | Rectangle window |
