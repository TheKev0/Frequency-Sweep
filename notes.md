# Developemnt Notes

## User Needs

- Measure frequency response by inputting the start/stop frequency, and step size.
- Plot and save the frequency response.
  - Plot in GUI and save via screenshot?
  - Output HTML file and view in browser?
- Output the measured data (frequencies and amplitudes) in raw form.
  - Print to console?
  - Write csv file?
- Easy setup
  - Windows Python installer?
- Readme for Devs

## General Setup

- First I installed [National Instruments NI-VISA Software](https://www.ni.com/en/support/downloads/drivers/download.ni-visa.html#521671)
- **Signal Generator**: Open NI Max application. Expand "Devices and Interfaces", select the SDG2042 function generator, click "Open VISA Test Panel". In the test panel you can send and receive commands with the signal generator according to the instrument's programming manual.
- **Spectrum Analyzer**: Plugged the NI USB-GPIB adapter (aka. GPIB-USB-HS) to the computer and spectrum analyzer, and turned on the spectrum analyzer, but NI Max and Windows Device Manager report that no driver is found. Solution: Open "NI Package Manager" on Windows (it came with the NI-VISA Software installed earlier), select "Drivers" on the left, search for "NI-488.2", and install it. This is the GPIB-USB-HS driver. In Windows, open "Visa Interactive Control" select device "GPIB0::8::INSTR" which opens the interactive control panel. Now you can go to the Input/Output tab and send the commands described in the spectrum analyzer's programming manual.

## Python setup

- Create and activate venv: https://python.land/virtual-environments/virtualenv
- Install requirements from requirements.txt.

## Controlling the Signal Generator

### Pseudocode

```C
// Get Instrument info.
"IDN?"

// Reset the instrument state.
"*RST"

// Turn output off.
"C1:OUTP OFF"

// Configure a Waveform type, frequency, amplitude, DC offset, and phase.
"C1:BSWV WVTP,SINE,FRQ,500000,AMP,0.100Vpp,OFST,0,PHSE,0"

// Output On
"C1:OUTP ON"
```

### Python Example

```python
import pyvisa

rm = pyvisa.ResourceManager()
rm.list_resources()
inst = rm.open_resource('USB0::0xF4EC::0x1102::SDG2XFBQ7R2430::INSTR')

print(inst.query("*IDN?"))
```

## Controlling the Spectrum Analyzer

### Pseudocode

### Python Example

```python
import pyvisa

rm = pyvisa.ResourceManager()
rm.list_resources()
inst = rm.open_resource('USB0::0xF4EC::0x1102::SDG2XFBQ7R2430::INSTR')

# "Instrument Preset" - set settings to default values.
print(inst.query("IP;"))
```
