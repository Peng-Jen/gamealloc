from gamealloc import Allocation
import pytest

def allocation_pattern(res, size=15):
    os = [f"\n{'=' * size} Allocation {'=' * size}"]
    for agent, object in res:
        os.append(f"{agent} \u2192 {object}")
    os.append("=" * (size * 2 + 12))
    return "\n".join(os)

def test_to_list():
    allocation = Allocation([0,1,2], ["A","B","C"], ["a","b","c"])
    assert allocation.to_list() == [0,1,2]

def test_to_dict():
    allocation = Allocation([0,1,2], ["A","B","C"], ["a","b","c"])
    assert allocation.to_dict() == {"A":"a", "B":"b", "C":"c"}

def test_to_pairs():
    allocation = Allocation([0,1,2], ["A","B","C"], ["a","b","c"])
    assert allocation.to_pairs() == [("A","a"), ("B","b"), ("C","c")]

def test_str():
    allocation = Allocation([0,1,2], ["A","B","C"], ["a","b","c"])
    res = allocation.to_pairs()
    assert str(allocation) == allocation_pattern(res)

def test_repr():
    allocation = Allocation([0,1,2], ["A","B","C"], ["a","b","c"])
    assert repr(allocation) == f"Allocation([0, 1, 2], agents=['A', 'B', 'C'], objects=['a', 'b', 'c'])"

def test_allocation_type_error():
    with pytest.raises(TypeError):
        Allocation(["0"])
    with pytest.raises(TypeError):
        Allocation([1.5])
    with pytest.raises(TypeError):
        Allocation([[]])
    with pytest.raises(TypeError) as e:
        Allocation([-1])
    assert "non-negative" in str(e.value)

def test_allocation_value_error():
    with pytest.raises(ValueError) as e:
        Allocation([1,1])
    assert "multi-agents" in str(e.value)
    with pytest.raises(ValueError) as e:
        Allocation([1,3,0],None,["a","b","c"])
    assert "index is out of range" in str(e.value)

def test_empty():
    assert Allocation([]).to_pairs() == []
    assert Allocation([]).to_list() == []


def test_agents_type_error():
    with pytest.raises(TypeError):
        Allocation([0], [0])
    with pytest.raises(TypeError):
        Allocation([0,1], [[1], 0.5])

def test_agents_value_error():
    with pytest.raises(ValueError) as e:
        Allocation([0,1], ["A", "B", "C"])
    assert "length of allocation" in str(e.value)

def test_agents_warning():
    with pytest.warns(UserWarning, match="agent_i"):
        Allocation([0,1],["A"])

def test_objects_type_error():
    with pytest.raises(TypeError):
        Allocation([0], None, [0])
    with pytest.raises(TypeError):
        Allocation([0,1], None, [[1], 0.5])

def test_objects_value_error():
    with pytest.raises(ValueError) as e:
        Allocation([0,1], None, ["a"])
    assert "number of agents" in str(e.value)
