import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'main', 'python'))

from imageRecognition import helloWorld

import pytest

class imageRecg(object):
    
def test_helloWorld():
    assert helloWorld() == "Hello world!"
