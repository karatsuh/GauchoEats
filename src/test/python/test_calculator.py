import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'main', 'python'))

from Calculator import Calculator

import pytest

#def test_blah():
#    assert 5 == 5

class TestCalculator(object):
    
    def setup_method(self):
        self.cal = Calculator()

    def teardown_method(self):
        self.cal = None

    def test_add(self):
        res = self.cal.add(2, 3)
        assert res == 5

    def test_sub(self):
        res = self.cal.sub(2, 3)
        assert res == -1

    def test_mul(self):
        res = self.cal.mul(2, 3)
        assert res == 6

    def test_div(self):
        res = self.cal.div(2, 3)
        assert res == 2/3

    def test_div_with_exception(self):
        with pytest.raises(ZeroDivisionError):
            self.cal.div(2, 0)
