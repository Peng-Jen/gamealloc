import pytest
from gamealloc import manipulation, sequential_priority, top_trading_cycles, Preference, Allocation

def test_manipulation_base():
    pref = Preference([[0, 1, 2], [2, 0, 1], [2, 1, 0]], ["Alice", "Bob", "Carol"], ["A", "B", "C"])
    assert manipulation(0, pref, order=[2, 1, 0], endowment=[0, 2, 1]) == {"Sequential Priority": {}, "TTC":{}}
    assert manipulation("Alice", pref, order=[2, 1, 0], endowment=[0, 2, 1]) == {"Sequential Priority": {}, "TTC":{}}

def test_manipulation_not_given_arg():
    with pytest.raises(ValueError) as e:
        manipulation(0, Preference([[0]]))
    assert "is given" in str(e.value)
