import unittest
import instrument_controller
import numpy as np
from tempfile import gettempdir

class Test_InstrumentController(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Generate test data.
        cls._freq = np.linspace(1, 10).tolist()
        cls._amp = np.random.random_integers(-3, 3).tolist()

    def test_write_to_csv_valid_chars(self):
        try:
            instrument_controller.write_to_csv("My File", self._freq, self._amp)
        except Exception:
            self.fail("write_to_csv() raised exception unexpectedly!")

    def test_write_to_csv_invalid_chars(self):
        try:
            instrument_controller.write_to_csv("50 mg/dl", self._freq, self._amp)
        except Exception:
            self.fail("write_to_csv() raised exception unexpectedly!")

if __name__ == '__main__':
    unittest.main()