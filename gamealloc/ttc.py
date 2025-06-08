from typing import *
from .preference import Preference
from .allocation import Allocation

def top_trading_cycles(endowment: Union[List[int], tuple[int]], preferences: Preference) -> Allocation:
    """
    This function implements top-trading-cycle (TTC) algorithm.
    Given each agent's preference and initial endowment, it suggests an object allocation satisfy Pareto Efficiency.

    Parameters
    --------
    endowment: List[int] | tuple[int]
        endowment[i] is the object held by agent i
    preferences: Preference
        preferences.prefs[i] is agent i's preference profile
    
    Returns
    --------
    allocation: Allocation
        allocation.allocation[i] is the assigned object for agent i
    
    Examples
    --------
    >>> endowment = [0, 1, 2, 3]
    >>> preferences = Preference(
            prefs = [[1, 2, 0, 3], [2, 0, 1, 3], [0, 3, 2, 1], [0, 1, 3, 2]],
            agents = ["Alice", "Bob", "Carol", "David"],
            objects = ["A", "B", "C", "D"]
        )
    >>> top_trading_cycle(preferences, endowment).to_pairs()
    [("Alice", "B"), ("Bob", "C"), ("Carol", "A"), ("David", "D")]

    Warnings
    --------
    endowment is 0-based, and it contains integer only from 0 to n-1 for n agents.
    
    See Also
    --------
    Preference: 
        Data class for agent preferences. Please refer to *preference.py*.
    Allocation: 
        Data class for allocation result, having method such as .to_list(), .to_dict(), .to_pairs(), and so on. Please refer to *allocation.py*.
    
    Todos
    --------
    - Currently, one-to-one matching is assumed.
    - Opposite endowment representation (endowment[i] is the agent who owns object i).
    """

    if not all(isinstance(x, int) for x in endowment):
        raise TypeError("Each element in endowment should be int.")
    if not isinstance(preferences, Preference):
        raise TypeError("preferences should be Preference type.")
    if len(endowment) != len(preferences.prefs):
        raise ValueError("The length of endowment should be same as the length of preference profile.")
    set_endo = set(endowment)
    if len(endowment) != len(set_endo):
        raise ValueError("One object cannot held by multi-agent.")
    if set_endo != set(range(len(set_endo))):
        raise ValueError("endowment only contains integers from 0 to n-1, where n is the number of agents.")
    
    # find top choices for agents
    n = len(endowment)
    top_choices = [None for _ in range(n)]
    allocation = [None for _ in range(n)]
    remaining_obj = list(range(n))
    remaining_agent = list(range(n))
    
    # find cycles
    while remaining_obj:
        # find top choices for agents
        for i, v in enumerate(preferences.prefs):
            if allocation[i] is None: # agent has not been assigned
                for obj in v:
                    if obj in remaining_obj: # object still available
                        top_choices[i] = obj
                        break
        cycle = []
        visited = set()
        next = remaining_agent[0]
        while next not in visited:
            cycle.append(next)
            visited.add(next)
            next = endowment.index(top_choices[next])
        start_point = cycle.index(next)

        # one cycle found
        for agent in cycle[start_point:]:
            allocation[agent] = top_choices[agent]
            remaining_obj.remove(top_choices[agent])
            remaining_agent.remove(agent)

    return Allocation(allocation, preferences.agents, preferences.objects)
