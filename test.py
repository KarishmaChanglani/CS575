import unittest
import backend
from tests import testdatabse

if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(unittest.defaultTestLoader.loadTestsFromModule(testdatabse))
    unittest.TextTestRunner().run(suite)
