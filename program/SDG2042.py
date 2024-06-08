import pyvisa
import re

class SDG2042:
  def __init__(self):
    # Open the connection.
    self._rm = pyvisa.ResourceManager()
    
    # Find the instrument address by regular expression
    # Expected hard coded value: "USB0::0xF4EC::0x1102::SDG2XFBQ7R2430::INSTR"
    # self._inst = self._rm.open_resource('USB0::0xF4EC::0x1102::SDG2XFBQ7R2430::INSTR')
    resources = self._rm.list_resources()
    address = ""
    for resource in resources:
      match = re.search("USB0::.*SDG2.*::INSTR", resource)
      if match is not None:
        address = match.group()
        self._inst = self._rm.open_resource(address)
        break
    if self._inst is not None:
      print("Connected to signal generator: {}".format(address))
    else:
      print("Could NOT connect to signal generator!")


    # Set defaults.
    self.reset()

  def __del__(self):  
    self._inst.close()

  ## Return the instrument to it's default state with output off.
  def reset(self):
    self._inst.write("*RST")

  def output_off(self):
    self._inst.write("C1:OUTP OFF")
  
  def output_on(self):
    self._inst.write("C1:OUTP ON")

  def set_waveform(self, frequency_hz, amplitude_vpp):
    # Always use a sine wave and set DC offset and phase to 0.
    cmd_string = "C1:BSWV WVTP,SINE,FRQ,{},AMP,{}Vpp,OFST,0,PHSE,0".format(frequency_hz, amplitude_vpp)
    self._inst.write(cmd_string)