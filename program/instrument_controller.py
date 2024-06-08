import time
import sys
import plotly.graph_objects as go
from PySide6 import QtCore, QtWidgets, QtGui

import SDG2042
import HP8591

# A helper class for running long tasks in a separate thread.
# See https://stackoverflow.com/questions/20324804/how-to-use-qthread-correctly-in-pyqt-with-movetothread
class Worker(QtCore.QObject):
  start = QtCore.Signal(str, float, int, int, int)
  finished = QtCore.Signal()

  def __init__(self, function, *args, **kwargs):
        super(Worker, self).__init__()

        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.start.connect(self.run)

  @QtCore.Slot()
  def run(self, title, input_amp, start, end, step):
    # self.function(*self.args, **self.kwargs)
    self.function(title, input_amp, start, end, step)
    self.finished.emit()

# The GUI
class MyWidget(QtWidgets.QWidget):
  def __init__(self):
    super().__init__()

    # self.layout = QtWidgets.QGridLayout(self)
    self.layout = QtWidgets.QFormLayout(self)

    # Create input fields.
    self._line_edit_title = QtWidgets.QLineEdit(MaxLength=64)
    self._line_edit_freq_start = QtWidgets.QLineEdit(PlaceholderText="100000", MaxLength=7)
    self._line_edit_freq_end = QtWidgets.QLineEdit(PlaceholderText="1000000", MaxLength=7)
    self._line_edit_freq_step = QtWidgets.QLineEdit(PlaceholderText="5000", MaxLength=7)
    self._line_edit_input_amp = QtWidgets.QLineEdit(PlaceholderText="0.1", MaxLength=5)
    self.layout.addRow("Sample Name", self._line_edit_title)
    self.layout.addRow("Start Frequency [Hz]", self._line_edit_freq_start)
    self.layout.addRow("End Frequency [Hz]", self._line_edit_freq_end)
    self.layout.addRow("Step Frequency [Hz]", self._line_edit_freq_step)
    self.layout.addRow("Input Amplitude [Vpp]", self._line_edit_input_amp)

    # Create button.
    self._button = QtWidgets.QPushButton("Run Frequency Sweep")
    self.layout.addRow(self._button)
    self._button.clicked.connect(self.button_pressed)

    # Create a QThread and Worker object to do work asynchronously.
    # Reference: https://stackoverflow.com/questions/20324804/how-to-use-qthread-correctly-in-pyqt-with-movetothread
    # Reference: https://realpython.com/python-pyqt-qthread/
    self.worker_thread = QtCore.QThread()
    self.worker_thread.start()
    self.worker = Worker(self.run_freq_sweep)
    self.worker.finished.connect(self.on_completion)
    self.worker.moveToThread(self.worker_thread)

  @QtCore.Slot()
  def button_pressed(self):
    # Read inputs
    # TODO Validate inputs.
    title = self._line_edit_title.text()
    start = int(self._line_edit_freq_start.text())
    end = int(self._line_edit_freq_end.text())
    step = int(self._line_edit_freq_step.text())
    input_amp = float(self._line_edit_input_amp.text())
    print("")
    print("Starting Test")
    print("Frequency Sweep: {}Hz to {}Hz, Stepping {}Hz. Input Amplitude {}Vpp".format(
        start, end, step, input_amp))
    
    # Disable the window to prevent user input.
    self.setEnabled(False)

    # Start the measurement in another thread to not block the GUI.
    self.worker.start.emit(title, input_amp, start, end, step)

  def run_freq_sweep(self, title, input_amp, start, end, step):
    # Run the frequency sweep.
    amplitudes = frequency_response_measure(input_amp, start, end, step)
    print("Raw Values: ", end="")
    print(amplitudes)

    # Graph it.
    frequency_response_graph(title=title, frequencies=tuple(amplitudes.keys()), amplitudes=tuple(amplitudes.values()))
  
  def on_completion(self):
    # Re-enable button.
    self.setEnabled(True)
    print("Done!")

# Return a dictionary with frequency as keys and amplitude as values.
def frequency_response_measure(input_amplitude_vpp, start_frequency_hz, end_frequency_hz, step_size_hz):
  sig_gen = SDG2042.SDG2042()
  spec_analyzer = HP8591.HP8591()

  # Measure frequency response.
  amplitudes = {}
  for freq in range(start_frequency_hz, end_frequency_hz, step_size_hz):
    # Set input waveform.
    sig_gen.output_off()
    sig_gen.set_waveform(frequency_hz=freq, amplitude_vpp=input_amplitude_vpp)
    sig_gen.output_on()

    # Wait for the signal generator to enable it's output.
    time.sleep(0.2)

    # Measure peak frequency and amplitude
    # Set center frequency, span and bandwidth
    peak_freq, peak_amp = spec_analyzer.get_peak_amplitude(
        center_frequency=freq, span=10000)
    print("Nominal Freq={}Hz Peak Freq={}Hz Peak Amp={}dBm".format(freq, peak_freq, peak_amp))

    amplitudes.update({peak_freq: peak_amp})

  return amplitudes

def frequency_response_graph(title="Frequency Response", frequencies=(), amplitudes=()):
  fig = go.Figure()
  fig.add_trace(go.Scatter(x=frequencies, y=amplitudes))
  fig.update_layout(
    title=title,
    xaxis_title="Frequency [Hz]",
    yaxis_title="Amplitude [dBm]",
  )
  fig.show()

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.setWindowTitle("Frequency Response")
    widget.show()

    sys.exit(app.exec())
