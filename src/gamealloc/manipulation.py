# Discuss whether agent would get benefit from misrepresent his preference
from typing import *
import itertools
import warnings
from .preference import Preference
from .allocation import Allocation
from .ttc import top_trading_cycles
from .sp import sequential_priority

def manipulation(agent: Union[int, str], preference: Preference, order=None, endowment=None) -> Dict[str, Dict]:
    """
    Enumerate all possible manipulations for a given agent under specific allocation mechanisms.

    This function checks, for a specified agent and given allocation mechanism
    (Sequential Priority or Top Trading Cycles), whether there exists any preference misrepresentation
    (i.e., permutation of the agent's true preference) that can improve the assigned object.
    It returns all successful manipulations, i.e., permutations leading to strictly better outcomes.

    Parameters
    ----------
    agent : int or str
        The index or name of the agent whose manipulation potential is being checked.
    preference : Preference
        The preference profile of all agents.
    order : list, optional
        The assignment order for Sequential Priority (SP) mechanism. If provided, SP will be checked.
    endowment : list, optional
        The endowment (initial ownership) for Top Trading Cycles (TTC) mechanism. If provided, TTC will be checked.

    Returns
    -------
    result_report : Dict[str, Dict]
        Dictionary with keys as the mechanism name ("Sequential Priority" or "TTC") and values as another dict.
        The inner dict maps each object index that can be obtained via manipulation to a list of preference permutations (misreports)
        that allow the agent to obtain that object with a strictly better ranking.

        If the mechanism is strategy-proof, the result will be an empty dictionary.

    Examples
    --------
    >>> prefs = Preference([[0, 1, 2], [1, 2, 0], [2, 0, 1]])
    >>> manipulation(0, prefs, order=[0, 1, 2], endowment=[0, 1, 2])
    {'Sequential Priority': {}, 'TTC': {}}
    """

    def manipulation_helper(agent: Union[int, str], preference: Preference, alloc_func: Callable, alloc_func_arg: Any, alloc_func_arg_name: str):
        result_report = {}
        truth = preference.prefs[agent]
        curr = alloc_func(alloc_func_arg, preference).allocation[agent] # assigned objects with truth preference
        if curr != 0: # curr = 0 means current allocation is the best for the agent
            misrepresent = list(map(list, itertools.permutations(range(len(truth)))))
            for x in misrepresent:
                preference.prefs[agent] = x
                misresult = alloc_func(alloc_func_arg, preference).allocation[agent]
                if truth.index(misresult) < truth.index(curr): # successfully manipulate the outcome
                    result_report.setdefault(misresult, []).append(x)
            preference.prefs[agent] = truth
        return result_report
        
        

    if isinstance(agent, str):
        agent = preference.agents.index(agent) # transfrom name into index
    
    result_report = {}
    
    if order == None and endowment == None:
        raise ValueError("Neither order nor endowment is given.")
    
    if order is not None: # sp-based logic
        result_report["Sequential Priority"] = manipulation_helper(agent, preference, sequential_priority, order, "order")
    
    if endowment is not None: # TTC-based logic
        result_report["TTC"] = manipulation_helper(agent, preference, top_trading_cycles, endowment, "endowment")

    return result_report
