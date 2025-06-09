from dataclasses import dataclass
from typing import *
import warnings

@dataclass
class Preference:
    """
    Store agent names, object names, and each agent's preference.

    Parameters
    --------
    prefs: List[List[int]]
        Agent preference profile. If agent k has preference: 0 > 1 > 2 > ..., then prefs[k] = [0, 1, 2, ...]
    agents: List[str], optional
        Names or identifiers of the agents.
    objects: List[str], optional
        Names or identifiers of the objects.

    Attributes
    --------
    prefs: List[List[int]]
        Agent preference profile. If agent k has preference: 0 > 1 > 2 > ..., then prefs[k] = [0, 1, 2, ...]
    agents : Optional[List[str]]
        Names or identifiers of the agents. If not provided, default names "agent_0", "agent_1", ... are used.
    objects : Optional[List[str]]
        Names or identifiers of the objects. If not provided, default names "object_0", "object_1", ... are used.
    
    Methods
    --------
    validate() -> Preference
        Checks and enforces the consistency and validity of the object.  
        Returns a validated Preference if all checks pass.

    Examples
    --------
    >>> pref = Preference(
        prefs=[[0, 1, 2], [2, 1, 0], [1, 0]], 
        agents=["Alice", "Bob", "Carol"], 
        objects=["A", "B", "C"]
        )
    UserWarning: Preference for agent Carol is partial. Missing [2] have been appended to the end.

    >>> pref.prefs
    [[0, 1, 2], [2, 1, 0], [1, 0, 2]]

    >>> pref.agents
    ["Alice", "Bob", "Carol"]

    >>> pref.objects
    ["A", "B", "C"]

    Warnings
    --------
    It is strongly recommended not to modify the content of a Preference object after initialization.
    If you must make changes, please call the `.validate()` method after any modification to ensure the object remains consistent and valid.
    """
    
    prefs: List[List[int]]      
    agents: Optional[List[str]] = None
    objects: Optional[List[str]] = None

    def _valid_prefs(self):
        """Check data type in prefs"""
        if not all(isinstance(pref, list) for pref in self.prefs):
            raise TypeError("Each element in prefs should be a list.")
        for pref in self.prefs:
            if not all(isinstance(x, int) for x in pref):
                raise TypeError("Each agent's preference profile should only contain int.")
            if set(pref) != set(range(len(pref))):
                raise ValueError("Elements in each agent's preference should be different and contains only 0 to n-1, where n is the number of objects.")
            # one-to-one matching assumption
            if len(pref) > 0 and max(pref) >= len(self.prefs):
                raise ValueError("Too many objects in preference profile.")
        return self
    
    def _valid_agents(self):
        """Check data type in agents"""
        if self.agents is not None:
            if not all(isinstance(agent, str) for agent in self.agents):
                raise TypeError("Each agent's name should be string")
            if len(set(self.agents)) != len(self.agents):
                raise ValueError("Each agent's name should be different")
        return self
    
    def _valid_objects(self):
        """Check data type in agents"""
        if self.objects is not None:
            if not all(isinstance(obj, str) for obj in self.objects):
                raise TypeError("Each object's name should be string")
            if len(set(self.objects)) != len(self.objects):
                raise ValueError("Each object's name should be different")
        return self
    
    def validate(self):
        """
        Checks and enforces the consistency and validity of the object.  
        Returns a validated Preference if all checks pass (in-place).
        """
        return self._valid_prefs()._valid_agents()._valid_objects()

    def __post_init__(self):
        # TODO: Support #(agents) != #(objects)
        self._valid_prefs()._valid_agents()._valid_objects()
        n = len(self.prefs)
        m = n # m = len(self.prefs[0]) (It will occurs IndexError when n = 0)
        agents = [f"agent_{i}" for i in range(n)]
        objects = [f"object_{i}" for i in range(m)]
        if self.agents is None:
            self.agents = agents
        elif len(self.agents) > n:
            raise ValueError("Number of agents should be same as the length of preference profile.")
        else:
            if len(self.agents) < n:
                warnings.warn(f"List of agents is partial. \
                                Missing names have been appended as \"agent_i\" for the i-th agent.", UserWarning)
            self.agents += agents[len(self.agents):]
        if self.objects is None:
            self.objects = objects
        elif len(self.objects) > m:
            raise ValueError("Number of objects should be same as the length of preference profile.")
        else:
            if len(self.objects) < m:
                warnings.warn(f"List of objects is partial. \
                                Missing names have been appended as \"object_i\" for the i-th object.", UserWarning)
            self.objects += objects[len(self.objects):]
        for i, v in enumerate(self.prefs):
            set_v = set(v)
            if len(set_v) == 0 or set_v != set(range(m)):
                missing = [x for x in range(m) if x not in v]
                self.prefs[i] += missing
                if missing:
                    warnings.warn(f"Preference for agent {self.agents[i]} is partial. \
                                  Missing {missing} have been appended to the end.", UserWarning)
