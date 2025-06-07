from gamealloc import sequential_priority, Preference
import pytest, itertools

def test_base_case():
    # Given Agents' and Objects' name
    pref = Preference(prefs=[[1,0,2], [0,1,2], [1,2,0]], agents=["A", "B", "C"], objects=["a", "b", "c"])
    test1 = [2,1,0]
    assert sequential_priority(test1, pref).to_list() == [2,0,1]
    assert sequential_priority(test1, pref).to_dict() == {"A": "c", "B": "a", "C": "b"}
    test2 = [0,1,2]
    assert sequential_priority(test2, pref).to_list() == [1,0,2]
    assert sequential_priority(test2, pref).to_dict() == {"A": "b", "B": "a", "C": "c"}
    # Not given Agents' and Objects' name
    pref = Preference(prefs=[[1,0,2], [0,1,2], [1,2,0]])
    res1, res2 = [2,0,1], [1,0,2]
    assert sequential_priority(test1, pref).to_dict() == {f"agent_{i}": f"object_{res1[i]}" for i in range(len(res1))}
    assert sequential_priority(test2, pref).to_dict() == {f"agent_{i}": f"object_{res2[i]}" for i in range(len(res2))}

def test_empty():
    pref = Preference([])
    assert sequential_priority([], pref).to_list() == []
    assert sequential_priority([], pref).to_dict() == {}

def test_single_agent():
    pref = Preference(prefs=[[0]])
    assert sequential_priority([0], pref).to_list() == [0]
    assert sequential_priority([0], pref).to_dict() == {"agent_0": "object_0"}

def test_same_preference():
    size = 5
    pref = Preference(prefs=[list(range(size)) for _ in range(size)])
    orders = list(itertools.permutations(range(size)))
    for order in orders:
        res = [None for _ in range(size)]
        for i, v in enumerate(order):
            res[v] = i
        assert sequential_priority(order, pref).to_list() == res

def test_incorrect_order_type_error():
    pref = Preference(prefs=[[0,1], [1,0]])
    with pytest.raises(TypeError):
        # each element in order should be int
        sequential_priority([1.5, 0], pref)
    with pytest.raises(TypeError):
        # each element in order should be int
        sequential_priority([1, "0"], pref)

def test_incorrect_order_value_error():
    pref = Preference(prefs=[[0,1], [1,0]])
    with pytest.raises(ValueError):
        # len(order) should be 2
        sequential_priority([0], pref)
    with pytest.raises(ValueError):
        # order should contains only 0 and 1
        sequential_priority([1,2], pref)
    with pytest.raises(ValueError):
        # len(order) should be 2 and contains only 0 and 1
        sequential_priority([1,0,0], pref)

def test_base_case():
    # Given Agents' and Objects' name
    pref = Preference(prefs=[[1,0,2], [0,1,2], [1,2,0]], agents=["A", "B", "C"], objects=["a", "b", "c"])
    test1 = [2,1,0]
    assert sequential_priority(test1, pref).to_list() == [2,0,1]
    assert sequential_priority(test1, pref).to_dict() == {"A": "c", "B": "a", "C": "b"}
    test2 = [0,1,2]
    assert sequential_priority(test2, pref).to_list() == [1,0,2]
    assert sequential_priority(test2, pref).to_dict() == {"A": "b", "B": "a", "C": "c"}
    # Not given Agents' and Objects' name
    pref = Preference(prefs=[[1,0,2], [0,1,2], [1,2,0]])
    res1, res2 = [2,0,1], [1,0,2]
    assert sequential_priority(test1, pref).to_dict() == {f"agent_{i}": f"object_{res1[i]}" for i in range(len(res1))}
    assert sequential_priority(test2, pref).to_dict() == {f"agent_{i}": f"object_{res2[i]}" for i in range(len(res2))}

def test_empty():
    pref = Preference([])
    assert sequential_priority([], pref).to_list() == []
    assert sequential_priority([], pref).to_dict() == {}

def test_single_agent():
    pref = Preference(prefs=[[0]])
    assert sequential_priority([0], pref).to_list() == [0]
    assert sequential_priority([0], pref).to_dict() == {"agent_0": "object_0"}

def test_same_preference():
    size = 5
    pref = Preference(prefs=[list(range(size)) for _ in range(size)])
    orders = list(itertools.permutations(range(size)))
    for order in orders:
        res = [None for _ in range(size)]
        for i, v in enumerate(order):
            res[v] = i
        assert sequential_priority(order, pref).to_list() == res

def test_incorrect_order_type_error():
    pref = Preference(prefs=[[0,1], [1,0]])
    with pytest.raises(TypeError):
        # each element in order should be int
        sequential_priority([1.5, 0], pref)
    with pytest.raises(TypeError):
        # each element in order should be int
        sequential_priority([1, "0"], pref)

def test_incorrect_order_value_error():
    pref = Preference(prefs=[[0,1], [1,0]])
    with pytest.raises(ValueError):
        # len(order) should be 2
        sequential_priority([0], pref)
    with pytest.raises(ValueError):
        # order should contains only 0 and 1
        sequential_priority([1,2], pref)
    with pytest.raises(ValueError):
        # len(order) should be 2 and contains only 0 and 1
        sequential_priority([1,0,0], pref)
