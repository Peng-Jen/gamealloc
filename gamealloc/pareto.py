from typing import *
import itertools
import warnings
from .preference import Preference
from .allocation import Allocation

def _build_graph(allocation: Allocation, preference: Preference):
    """
    Build a directed graph where each node is an object based on allocation and preference.
    There is an edge from object i to object j if the agent holding object i strictly prefers object j over i.

    Parameters
    ----------
    Allocation : allocation
        The allocation result for each agent.
    preference : Preference
        The preference profile for each agent.

    Returns
    -------
    graph : List[List[int]]
        Adjacency list representing the directed graph.
    
    Example
    -------
    >>> allocation = Allocation([0, 1, 2])
    >>> preference = Preference([[1, 2, 0], [2, 0, 1], [0, 1, 2]])
    >>> _build_graph(allocation, preference)
    [[1, 2], [2, 0], [0, 1]]

    Todos
    --------
    Currently, the graph is object-based. Agent-based graph would be more intuitive to point out the cycles and easier to give suggestion to agents.
    """

    graph = [[] for _ in range(len(allocation.allocation))] # adjacency list
    for i, v in enumerate(preference.prefs):
        curr_rank = v.index(allocation.allocation[i])
        graph[allocation.allocation[i]] += v[:curr_rank] # append all objects that the agent strictly prefers over the assigned one
    return graph

def _has_cycle(graph: List[List[int]]):
    """
    Check whether there is a directed cycle in the graph.

    Parameters
    ----------
    graph : List[List[int]]
        The adjacency list of the directed graph.

    Returns
    -------
    bool
        True if there exists a cycle; otherwise, False.

    Example
    -------
    >>> graph = [[1, 2], [2, 0], [0, 1]]
    >>> _has_cycle(graph)
    True
    """
    visited = set() # nodes have been completly searched
    path = set()
    def dfs(node):
        if node in path:
            return True
        if node in visited:
            return False
        path.add(node)
        for neighbor in graph[node]:
            if dfs(neighbor):
                return True
        path.remove(node)
        visited.add(node)
        return False
    for node in range(len(graph)):
        if dfs(node):
            return True
    return False


def is_pareto_efficient(allocation: Allocation, preference: Preference) -> bool:
    """
    Return True if allocation is Pareto efficient.

    Parameters
    --------
    allocation: Allocation
        The allocation result for each agent.
    preference: Preference
        The preference profile for each agent.

    Returns
    --------
    bool
        True if the current allocation is Pareto efficient.
    
    Examples
    --------
    >>> allocation = Allocation([0, 1, 2], ["Alice", "Bob", "Carol"], ["A", "B", "C"])
    >>> preference = Preference([[0, 1, 2], [1, 0, 2], [2, 0, 1]], ["Alice", "Bob", "Carol"], ["A", "B", "C"])
    >>> is_pareto_efficient(allocation, preference)
    True

    >>> allocation = Allocation([0, 2, 1])
    >>> preference = Preference([[0, 1, 2], [1, 0, 2], [2, 0, 1]], ["Alice", "Bob", "Carol"], ["A", "B", "C"])
    >>> is_pareto_efficient(allocation, preference)
    False

    >>> allocation = Allocation([0, 1, 2], ["Alice", "Bob", "David"], ["A", "B", "C"])
    >>> preference = Preference([[0, 1, 2], [1, 0, 2], [2, 0, 1]], ["Alice", "Bob", "Carol"], ["A", "B", "C"])
    >>> is_pareto_efficient(allocation, preference)
    ValueError: "Agents in allocation should be same as agents in preference"
    """
    n = len(allocation.allocation)
    if n == 0:
        warnings.warn("No agents exist. The allocation will always be Pareto Efficiency.", UserWarning)
    default_agents = [f"agent_{i}" for i in range(n)]
    default_objects = [f"object_{i}" for i in range(n)]
    if allocation.agents != default_agents and allocation.agents != preference.agents:
        raise ValueError("Agents in allocation should be same as agents in preference")
    if allocation.objects != default_objects and allocation.objects != preference.objects:
        raise ValueError("Objects in allocation should be same as objects in preference")
    if len(preference.prefs) != n:
        raise ValueError(f"Lists in preference should be same as number of elements in allocation.")
    
    graph = _build_graph(allocation, preference)
    return not _has_cycle(graph)

def find_all_pareto_efficient_allocations(preference: Preference) -> List[Allocation]:
    """
    Returns all pareto efficient allocations.

    Parameters
    --------
    preference: Preference
        Agent preference profile.

    Returns
    --------
    allocations: List[Allocation]
        The allocation list for pareto efficient allocations.
    
    Examples
    --------
    >>> preference = Preference([[0, 1, 2], [1, 2, 0], [0, 1, 2]], ["Alice", "Bob", "Carol"], ["A", "B", "C"])
    >>> find_all_pareto_efficient_allocation(preference)
    [Allocation([0, 1, 2], agents=['Alice', 'Bob', 'Carol'], objects=['A', 'B', 'C']), Allocation([0, 2, 1], agents=['Alice', 'Bob', 'Carol'], objects=['A', 'B', 'C']), Allocation([1, 2, 0], agents=['Alice', 'Bob', 'Carol'], objects=['A', 'B', 'C']), Allocation([2, 1, 0], agents=['Alice', 'Bob', 'Carol'], objects=['A', 'B', 'C'])]
    
    Warnings
    --------
    The time complexity for this funcion is O(n!). Use it carefully with large number of agents (n >= 7).
    """

    n = len(preference.prefs)
    if n >= 7:
        warnings.warn("The time complexity for this funcion is O(n!). Use it carefully with large number of agents (n >= 7).", UserWarning)
    permutation = itertools.permutations(range(n))
    res = []
    if n > 0: # Check there is at least an agent
        for p in permutation:
            allocation = Allocation(list(p), preference.agents, preference.objects)
            if is_pareto_efficient(allocation, preference):
                res.append(allocation)
    return res
