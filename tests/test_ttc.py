from gamealloc import top_trading_cycles, Preference
import pytest, itertools

def test_base_case():
    # Given Agents' and Objects' name
    pref = Preference(prefs=[[1,0,2], [0,1,2], [1,2,0]], agents=["A", "B", "C"], objects=["a", "b", "c"])
    test1 = [2,1,0]
    assert top_trading_cycles(test1, pref).to_list() == [2,0,1]
    assert top_trading_cycles(test1, pref).to_dict() == {"A": "c", "B": "a", "C": "b"}
    test2 = [0,1,2]
    assert top_trading_cycles(test2, pref).to_list() == [1,0,2]
    assert top_trading_cycles(test2, pref).to_dict() == {"A": "b", "B": "a", "C": "c"}
    # Not given Agents' and Objects' name
    pref = Preference(prefs=[[1,0,2], [0,1,2], [1,2,0]])
    res1, res2 = [2,0,1], [1,0,2]
    assert top_trading_cycles(test1, pref).to_dict() == {f"agent_{i}": f"object_{res1[i]}" for i in range(len(res1))}
    assert top_trading_cycles(test2, pref).to_dict() == {f"agent_{i}": f"object_{res2[i]}" for i in range(len(res2))}

def test_empty():
    pref = Preference([])
    assert top_trading_cycles([], pref).to_list() == []
    assert top_trading_cycles([], pref).to_dict() == {}

def test_single_agent():
    pref = Preference(prefs=[[0]])
    assert top_trading_cycles([0], pref).to_list() == [0]
    assert top_trading_cycles([0], pref).to_dict() == {"agent_0": "object_0"}

def test_same_preference():
    size = 5
    pref = Preference(prefs=[list(range(size)) for _ in range(size)])
    endowments = list(itertools.permutations(range(size)))
    for endowment in endowments:
        assert top_trading_cycles(endowment, pref).to_list() == list(endowment)

def test_endowment_type_error():
    pref = Preference(prefs=[[0,1], [1,0]])
    with pytest.raises(TypeError):
        # each element in endowment should be int
        top_trading_cycles([1.5, 0], pref)
    with pytest.raises(TypeError):
        # each element in endowment should be int
        top_trading_cycles([1, "0"], pref)

def test_endowment_value_error():
    pref = Preference(prefs=[[0,1], [1,0]])
    with pytest.raises(ValueError):
        # len(endowment) should be 2
        top_trading_cycles([0], pref)
    with pytest.raises(ValueError):
        # endowment should contains only 0 and 1
        top_trading_cycles([1,2], pref)
    with pytest.raises(ValueError):
        # len(endowment) should be 2 and contains only 0 and 1
        top_trading_cycles([1,0,0], pref)
