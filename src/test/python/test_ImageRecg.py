import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'main', 'python'))

from ImageRecg import ImageRecg

import pytest

class TestImageRecg(object):
    
    def test_salute(self):
        assert salute() == "Hello world!"
