from gamealloc import find_all_pareto_efficient_allocations, is_pareto_efficient, Preference, Allocation
import pytest, itertools

def test_is_pareto_efficient_base():
    prefs = Preference([[1, 0, 2], [1, 2, 0], [2, 0, 1]])
    alloc = Allocation([0, 1, 2])
    assert is_pareto_efficient(alloc, prefs) == True
    alloc.allocation = [2, 0, 1]
    assert is_pareto_efficient(alloc, prefs) == False

def test_is_pareto_efficient_agents_value_error():
    alloc = Allocation([0, 1, 2], ["Alice", "Bob", "David"], ["A", "B", "C"])
    prefs = Preference([[0, 1, 2], [1, 0, 2], [2, 0, 1]], ["Alice", "Bob", "Carol"], ["A", "B", "C"])
    with pytest.raises(ValueError) as e:
        is_pareto_efficient(alloc, prefs)
    assert "agents in preference" in str(e.value)

def test_is_pareto_efficient_objects_value_error():
    alloc = Allocation([0, 1, 2], ["Alice", "Bob", "Carol"], ["A", "B", "D"])
    prefs = Preference([[0, 1, 2], [1, 0, 2], [2, 0, 1]], ["Alice", "Bob", "Carol"], ["A", "B", "C"])
    with pytest.raises(ValueError) as e:
        is_pareto_efficient(alloc, prefs)
    assert "objects in preference" in str(e.value)

def test_is_pareto_efficient_partial_warning():
    with pytest.raises(ValueError) as e:
        with pytest.warns(UserWarning, match="partial"):
            is_pareto_efficient(Allocation([0, 1, 2]), Preference([[0, 1], []]))
    assert "Lists in preference" in str(e.value)

def test_is_pareto_efficient_empty_warning():
    with pytest.warns(UserWarning, match="No agents"):
        assert is_pareto_efficient(Allocation([]), Preference([])) == True

def test_find_all_pareto_efficient_allocations_base():
    pref = Preference([[0, 1, 2], [1, 2, 0], [0, 1, 2]])
    assert list(map(lambda x: x.to_list(), find_all_pareto_efficient_allocations(pref))) == [[0, 1, 2], [0, 2, 1], [1, 2, 0], [2, 1, 0]]
    
def test_find_all_pareto_efficient_allocations_same_preference():
    pref = Preference([[1, 2, 0], [1, 2, 0], [1, 2, 0]])
    assert list(map(lambda x: x.to_list(), find_all_pareto_efficient_allocations(pref))) == list(map(list, itertools.permutations(range(len(pref.prefs)))))

def test_find_all_pareto_efficient_allocations_empty():
    assert find_all_pareto_efficient_allocations(Preference([])) == []

def test_find_all_pareto_efficient_allocations_big_n():
    with pytest.warns(UserWarning, match=r"O\(n\!\)"):
        find_all_pareto_efficient_allocations(Preference([list(range(7)) for _ in range(7)]))