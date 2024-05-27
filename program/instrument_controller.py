import time
import SDG2042
import HP8591

# Return a dictionary with frequency as keys and amplitude as values.


def frequency_response(input_amplitude_vpp, start_frequency_hz, end_frequency_hz, step_size_hz):
  sig_gen = SDG2042.SDG2042()
  spec_analyzer = HP8591.HP8591()

  # Measure frequency response.
  amplitudes = {}
  for freq in range(start_frequency_hz, end_frequency_hz, step_size_hz):
    # Set input waveform.
    sig_gen.output_off()
    sig_gen.set_waveform(frequency_hz=freq, amplitude_vpp=input_amplitude_vpp)
    sig_gen.output_on()

    # Wait 100ms
    time.sleep(0.1)

    # Measure peak frequency and amplitude
    # Set center frequency, span and bandwidth
    peak_freq, peak_amp = spec_analyzer.get_peak_amplitude(
        center_frequency=freq, span=10000)

    amplitudes.update({peak_freq: peak_amp})

  return amplitudes


amplitudes = frequency_response(
    input_amplitude_vpp=0.1, start_frequency_hz=10000, end_frequency_hz=100000, step_size_hz=50000)
print(amplitudes.values())
