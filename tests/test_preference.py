from gamealloc import Preference
import pytest

def test_preferences_value_error():
    with pytest.raises(ValueError):
        Preference(prefs=[[0,0], [1,1]])
    with pytest.raises(ValueError) as e:
        Preference([[0, 0]], ["A", "B"], ["A", "B"])
    assert "different" in str(e.value)
    with pytest.raises(ValueError) as e:
        Preference([[0, 1]], ["A", "B"], ["A", "B"])
    assert "Too many" in str(e.value)

def test_preferences_warning():
    with pytest.warns(UserWarning, match="agent_0"):
        Preference(prefs=[[0], [1,0]])
    with pytest.warns(UserWarning, match="agent_1"):
        Preference(prefs=[[0,1], []])

def test_preferences_type_error():
    with pytest.raises(TypeError):
        Preference(prefs=["not a list"])
    with pytest.raises(TypeError):
        Preference(prefs=[0])
    with pytest.raises(TypeError):
        Preference(prefs=[1,2,3])

def test_preferences_empty():
    assert Preference([]).prefs == []
    
def test_agents_value_error():
    prefs =[[0,1], [1,0]]
    obj=["a", "b"]
    with pytest.raises(ValueError):
        Preference(prefs, agents=["A", "B", "C"], objects=obj)
    with pytest.raises(ValueError):
        Preference(prefs, agents=["A", "A"], objects=obj)

def test_agents_warning():
    prefs =[[0,1], [1,0]]
    obj=["a", "b"]
    with pytest.warns(UserWarning, match="agent_i"):
        Preference(prefs, agents=["A"], objects=obj)

def test_agents_type_error():
    prefs =[[0,1], [1,0]]
    obj=["a", "b"]
    with pytest.raises(TypeError):
        Preference(prefs, agents=["A", []], objects=obj)
    with pytest.raises(TypeError):
        Preference(prefs, agents=["A", None], objects=obj)
    with pytest.raises(TypeError):
        Preference(prefs, agents=["A", 1], objects=obj)
        
def test_objects_value_error():
    prefs =[[0,1], [1,0]]
    agents=["A", "B"]
    with pytest.raises(ValueError):
        Preference(prefs, agents, objects=["a", "b", "c"])
    with pytest.raises(ValueError):
        Preference(prefs, agents, objects=["a", "a"])

def test_objects_warning():
    prefs =[[0,1], [1,0]]
    agents=["A", "B"]
    with pytest.warns(UserWarning, match="object_i"):
        Preference(prefs, agents, objects=["a"])
    
def test_objects_type_error():
    prefs =[[0,1], [1,0]]
    agents=["A", "B"]
    with pytest.raises(TypeError):
        Preference(prefs, agents, objects=["a", []])
    with pytest.raises(TypeError):
        Preference(prefs, agents, object=["a", None])
    with pytest.raises(TypeError):
        Preference(prefs, agents, object=["a", 1])
