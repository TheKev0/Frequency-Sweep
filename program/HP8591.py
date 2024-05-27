import pyvisa
import pyvisa.constants
import pyvisa_py
import time

class HP8591:

  def __init__(self):
    # Open the connection.
    self._rm = pyvisa.ResourceManager()
    self._inst = self._rm.open_resource('GPIB0::8::INSTR',access_mode=pyvisa.constants.AccessModes.exclusive_lock)
    # self._inst.write_termination = "\r"
    # self._inst.send_end = True

    # Set defaults.
    self.reset()

    # Always use single sweep mode.
    self._inst.write("SNGLS;")
  
  def __del__(self):
    # For GPIB devices, return control back to the instrument's front panel (aka. local mode).
    if isinstance(self._inst, pyvisa.resources.GPIBInstrument):
      try:
        self._inst.control_ren(pyvisa.constants.RENLineOperation.deassert_gtl)
      except pyvisa.errors.VisaIOError:
        # Ignore pyvisa.errors.VisaIOError: VI_ERROR_RSRC_LOCKED
        pass
    
    self._inst.close()

  ## Return the instrument to it's default state with output off.
  def reset(self):
    self._inst.write("IP;")

  def get_peak_amplitude(self, center_frequency, span):
    # Set center frequency.
    self._inst.write("CF {};".format(center_frequency))

    # Set span
    self._inst.write("SP {};".format(span))
    # self._inst.write("PKZOOM;")

    # Set sweep time.
    sweep_time_ms = 1000
    self._inst.write("ST {}MS;".format(sweep_time_ms))

   
    # NOTE: Normally, the "TS;" command (take sweep) is used to do a sweep and block
    # this thread as long as the sweep takes. However, it results in a VISA IO error
    # without waiting at all. So instead we will set a known sweep time and wait slightly
    # longer.

    # # Set single sweep mode
    # self._inst.write("SNGLS;")
    # # Take a sweep.
    # self._inst.write("TS;",)

    # Do a single sweep. Wait an extra 500ms for sweep to complete.
    self._inst.write("SNGLS;")
    time.sleep((sweep_time_ms + 500) / 1000);

    # Configure and read peak marker
    self._inst.write("MKPK HI;")

    # Read peak marker.
    # Response format:
    #   amplitude [dBm]: "-12.34\r\n"
    #   frequency [Hz]: "123.4E3\r\n"
    # Just use float() to parse responses.
    peak_amp = float(self._inst.query("MKA?;"))
    peak_freq = float(self._inst.query("MKF?;"))

    return peak_freq, peak_amp