from typing import *
import random
from .allocation import Allocation
from .preference import Preference

def random_objects_preference_instance(size: int, seed: int = 42):
    """
    Return a list of list of integer, which is one of acceptable preference profile.

    Parameters
    --------
    size: int
        Number of agents.
    seed: int
        Random seed, optional (default = 42).
    
    Returns
    --------
    List
        List of list of integer, which is one of acceptable preference profile.
    
    Examples
    --------
    >>> random_objects_preference_instance(4)
    [[0, 3, 1, 2], [1, 0, 2, 3], [3, 0, 2, 1], [1, 0, 2, 3]]
    """
    random.seed(seed)
    if size <= 0:
        raise ValueError("Number of agents should be a positive integer.")
    return [random.sample(range(size), size) for _ in range(size)]

def random_objects_allocation_instance(size: int, seed: int = 42) -> List:
    """
    Return a list of integer, which is one of acceptable allocations.

    Parameters
    --------
    size: int
        Number of agents.
    seed: int
        Random seed, optional (default = 42).
    
    Returns
    --------
    List
        list of integer, which is one of acceptable allocations.
    
    Examples
    --------
    >>> random_objects_allocation_instance(4)
    [0, 3, 1, 2]
    """
    random.seed(seed)
    if size <= 0:
        raise ValueError("Number of agents should be a positive integer.")
    return random.sample(range(size), size)
