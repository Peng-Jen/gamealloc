# gamealloc

_Version 0.1.2_

A Python package for classical resource allocation in game theory.

## Features

- Fast implementation of Sequential Priority (SP), Top Trading Cycles (TTC), and Pareto efficiency detection
- Flexible Preference and Allocation classes
- Random instance generator for benchmarking and teaching
- Support for agent manipulation analysis and strategy-proofness evaluation

## Installation

```bash
git clone https://github.com/yourname/gamealloc.git
cd gamealloc
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

## Quick Start
```python
from gamealloc import Preference, Assignment, top_trading_cycles

# Build preferences: 3 agents, 3 objects
endowment = [1, 2, 0]
order = [2, 0, 1]
prefs = Preference([[0, 1, 2], [2, 0, 1], [2, 1, 0]], ["Alice", "Bob", "Carol"], ["A", "B", "C"])

ttc = top_trading_cycles(endowment, prefs)
print(ttc)              # Pretty print result
print(ttc.to_pairs())   # List of (agent, object) pairs

sp = sequential_priority(order, prefs)
print(sp)
print(sp.to_dict())     # Dict of agent: object

```

```output
=============== Allocation ===============
Alice → A
Bob → C
Carol → B
==========================================
[('Alice', 'A'), ('Bob', 'C'), ('Carol', 'B')]
=============== Allocation ===============
Alice → A
Bob → B
Carol → C
==========================================
{'Alice': 'A', 'Bob': 'B', 'Carol': 'C'}
```

Or, you can just simply run
```bash
python examples.py
```
to quickly try out the package.
The provided `examples.py` demonstrates how to create preferences, run allocation algorithms, and view the results — making it easy to explore the basic functionality without additional setup.

## Main APIs

- `Preference(prefs: List[List[int]], agents: Optional[List[str]], objects: Optional[List[str]])`
- `Assignment(allocation: List[int], agents: Optional[List[str]], objects: Optional[List[str]])`
- `sequential_priority(order: List[int], preferences: Preference)`
- `top_trading_cycles(endowment: List[int], preferences: Preference)`
- `is_pareto_efficient(allocation: Allocation, preference: Preference)`
- `find_all_pareto_efficient_allocations(preference: Preference)`
- `random_objects_preference_instance(size, seed=42)`
- `random_objects_allocation_instance(size, seed=42)`
- `manipulation(agent: Union[int, str], preferences: Preference, order: Optional[List[int]], endowment: Optional[List[int]])`

## Tests
To run the unit tests and see the coverage, make sure you have installed pytest and pytest-cov. 

Run the following commands in your terminal:
```bash
pip install pytest pytest-cov
cd gamealloc
pytest --cov=src/gamealloc 
coverage report -m
```
- All test scripts are located in the `tests/` directory.
- By default, pytest will automatically find and run all files that start with `test_`.

To view a detailed coverage report in your browser, you can run:
```bash
pytest --cov=gamealloc --cov-report=html
open htmlcov/index.html
```
- The HTML report provides line-by-line details of which code is covered by your tests.
- Coverage is currently 99%. Because both SP and TTC are strategy-proof, it is impossible to construct test cases where an agent can obtain a strictly better allocation by misrepresenting their preferences.

## Advanced usage

- Generate random allocation problems with specified seed for reproducible experiments
- Analyze all Pareto efficient allocations for a given preference profile
- Simulate agent manipulation and evaluate strategy-proofness for different algorithms

## Planned Features

- Support for matching problems (e.g., Gale-Shapley stable matching)
- More flexible preference types (e.g., partial orders, ties / indifferences)
- Advanced manipulation analysis tools (e.g. conditional sequential priority)
- Batch evaluation and benchmarking framework
- Documentation website / API doc auto-generation

## Contributing

_Features marked as “planned” are under active development.  
Suggestions, PRs, and collaboration are very welcome!_

Contact: tim.pjchen@email.com

## License

Licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Reference

If you use this package for research or teaching, please cite:
Peng-Jen Chen, https://github.com/Peng-Jen/gamealloc, 2025
