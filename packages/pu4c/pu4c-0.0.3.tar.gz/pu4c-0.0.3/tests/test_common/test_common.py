import unittest
import numpy as np

class TestCommon(unittest.TestCase):

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)

    # @unittest.skip("")
    def test_printvar(self):
        pass

    @unittest.skip("")
    def test_simple_colormap(self):
        pass

if __name__ == '__main__':
    unittest.main()