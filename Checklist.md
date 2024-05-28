# Checklist

- [ ] Vetting
  - [x] Get commands for spectrum analyzer.
  - [x] Get commands for function generator.
- [x] Install NI GPIB adapter drivers for spectrum analyzer.
- [x] Verify that I can control the spectrum analyzer.
- [x] Verify that I can control the signal generator.
- [x] Control function generator to output desired signal (constant sine wave of given freq.)
- [x] Control spectrum analyzer to set current BW, enable peak detect, and read out the peak.
- [x] Write function to do a frequency sweep with the function gen and spectrum analyzer and save output results.
- [x] Graph bode plot (amplitude vs. freq).
- [x] Create GUI
  - [x] Input test name, start freq, end freq, and step size.
  - [x] Run sweep button
  - [x] Save output to file
- [ ] Generate Python installer.
- [ ] Misc.
  - [ ] Use regex to find VISA address of device instead of hard-coding it.
  - [ ] Input validation