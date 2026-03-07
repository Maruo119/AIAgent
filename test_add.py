from operator import add
from target_code import multiply, subtract

def test_subtract_decimal():
    assert subtract(2.5, 1.5) == 1.0
