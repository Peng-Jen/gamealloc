from typing import *
from .preference import Preference
from .allocation import Allocation

def sequential_priority(order: List[int], preferences: Preference) -> Allocation:
    """
    This function implements sequential priority algorithm.
    Given the order of agents and each agent's preference, it suggests an object allocation satisfy Pareto Efficiency.

    Parameters
    --------
    order: List[int] | tuple[int] 
        determine the assigning order for agents. order[0] will be assigned first, then order[1], and so on.
    preferences: Preference
        preferences.prefs[i] is agent i's preference profile
    
    Returns
    --------
    allocation: Allocation
        allocation.allocation[i] is the assigned object for agent i
    
    Examples
    --------
    >>> order = [0, 1, 2]
    >>> preferences = Preference(
            prefs = [[0, 1, 2], [2, 0, 1], [2, 1, 0]],
            agents = ["Alice", "Bob", "Carol"],
            objects = ["A", "B", "C"]
        )
    >>> sequential_priority(order, preferences).to_pairs()
    [("Alice", "A"), ("Bob", "C"), ("Carol", "B")]

    Warnings
    --------
    order is 0-based, and it should only contain integers from 0 to n-1 for n agents.
    
    See Also
    --------
    Preference: 
        Data class for agent preferences. Please refer to *preference.py*.
    Allocation: 
        Data class for allocation result, having method such as .to_list(), .to_dict(), .to_pairs(), and so on. Please refer to *allocation.py*.
    
    Todos
    --------
    Currently, one-to-one matching is assumed.
    """

    if not all(isinstance(x, int) for x in order):
        raise TypeError(f"Each element in order should be int.")
    if set(order) != set(range(len(order))):
        raise ValueError(f"order only contains integers from 0 to n-1, where n is the number of agents.")
   
    n = len(order) # number of agents 
    picked = set() # record picked objects
    allocation = [None for _ in range(n)]
    for agent in order:
        for obj in preferences.prefs[agent]:
            if obj not in picked:
                allocation[agent] = obj
                picked.add(obj)
                break
    return Allocation(allocation, preferences.agents, preferences.objects)
