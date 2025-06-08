from dataclasses import dataclass
from typing import *
import warnings

@dataclass
class Allocation:
    """
    Stores the allocation of objects to agents.

    This class represents the result of an allocation (matching) between agents and objects.
    It provides methods to convert the allocation into different formats and to check the validity of the allocation data.
    
    Parameters
    ----------
    allocation : List[int]
        allocation[i] is the index of the object assigned to agent i.
    agents : Optional[List[str]], optional
        Names or identifiers of the agents.
    objects : Optional[List[str]], optional
        Names or identifiers of the objects.

    Attributes
    ----------
    allocation : List[int]
        allocation[i] is the index of the object assigned to agent i.
    agents : Optional[List[str]]
        Names or identifiers of the agents. If not provided, default names "agent_0", "agent_1", ... are used.
    objects : Optional[List[str]]
        Names or identifiers of the objects. If not provided, default names "object_0", "object_1", ... are used.

    Methods
    -------
    to_list() -> List
        Return the allocation as a list of assigned object indices.
    to_dict() -> Dict[str, str]
        Convert the allocation to a dictionary mapping agent names to object names.
    to_pairs() -> List[tuple]
        Return the allocation as a list of (agent, object) pairs.
    validate() -> Allocation
        Checks and enforces the consistency and validity of the object.  
        Returns a validated Allocation if all checks pass.
    __str__()
        Return a pretty string representation of the allocation.
    __repr__()
        Return the string representation of the allocation (same as __str__).
    
    Examples
    --------
    >>> allocation = Allocation([2, 1, 0], ["Alice", "Bob", "Carol"], ["A", "B", "C"])
    >>> print(a)
    =============== Allocation ===============
    Alice → C
    Bob → B
    Carol → A
    ==========================================
    >>> allocation.to_dict()
    {"Alice": "C", "Bob": "B", "Carol": "A"}
    >>> allocation.to_pairs()
    [("Alice", "C"), ("Bob", "B"), ("Carol", "A")]

    Warnings
    --------
    It is strongly recommended not to modify the content of a Allocation object after initialization.
    If you must make changes, please call the `.validate()` method after any modification to ensure the object remains consistent and valid.
    """
    allocation: List[int]
    agents: Optional[List[str]] = None
    objects: Optional[List[str]] = None

    def to_list(self) -> List[int]:
        """Return the allocation as a list of assigned object indices."""
        return list(self.allocation)
    
    def to_dict(self) -> Dict[Any, Any]:
        """Convert the allocation to a dictionary mapping agent names to object names."""
        return {self.agents[i]: self.objects[v] for i, v in enumerate(self.allocation)}

    def to_pairs(self) -> List[tuple]:
        """Return the allocation as a list of (agent, object) pairs."""
        return [(self.agents[i], self.objects[v]) for i, v in enumerate(self.allocation)]
    
    def __str__(self):
        res = self.to_pairs()
        os = [f"\n{'=' * 15} Allocation {'=' * 15}"]
        for agent, object in res:
            os.append(f"{agent} \u2192 {object}")
        os.append("=" * 42)
        return "\n".join(os)
    
    def __repr__(self):
        return f"Allocation({self.allocation}, agents={self.agents!r}, objects={self.objects!r})"
    
    def _valid_allocation(self):
        """Check data type in allocation"""
        if not all(isinstance(x, int) and x >= 0 for x in self.allocation):
            raise TypeError("Each element in allocation should be non-negative int.")
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
        Returns a validated Allocation if all checks pass (in-place).
        """
        return self._valid_allocation()._valid_agents()._valid_objects()
    
    def __post_init__(self):
        # TODO: #(agent) > #(object), use -1 to indicate agent who is not be assigned
        self._valid_allocation()._valid_agents()._valid_objects()
        n = len(self.allocation)
        set_allocation = set(self.allocation)
        agents = [f"agent_{i}" for i in range(n)]
        objects = [f"object_{i}" for i in range(n)]
        if len(set_allocation) != n:
            raise ValueError("One object cannot be assigned to multi-agents")
        if self.agents is None:
            self.agents = agents
        elif len(self.agents) > n:
            raise ValueError("Number of agents should be same as the length of allocation.")
        else:
            if len(self.agents) < n:
                warnings.warn(f"List of agents is partial. \
                                Missing names have been appended as \"agent_i\" for the i-th agent.", UserWarning)
            self.agents += agents[len(self.agents):]
        if self.objects is None:
            self.objects = objects
        elif len(self.objects) < n:
            raise ValueError("Number of objects should not less than number of agents.")
        elif n > 0 and max(self.allocation) >= len(self.objects):
            raise ValueError("Object index is out of range.")
