from gamealloc import *

print("-" * 100)
print("Welcome to gamealloc — a Python package for classical resource allocation in game theory.\n")

print("In this example, you will learn how to use this package step by step.\n")

# Build preferences: 3 agents, 3 objects
print("First, we build a preference profile for 3 agents and 3 objects:\n")
print(">>> prefs = Preference([[0, 1, 2], [2, 0, 1], [2, 1, 0]], ['Alice', 'Bob', 'Carol'], ['A', 'B', 'C'])\n")

prefs = Preference([[0, 1, 2], [2, 0, 1], [2, 1, 0]], ["Alice", "Bob", "Carol"], ["A", "B", "C"])

print("This means:\n")
print("  - Alice prefers A > B > C")
print("  - Bob prefers C > A > B")
print("  - Carol prefers C > B > A\n")

print("Now, we demonstrate two allocation mechanisms: Sequential Priority (SP) and Top Trading Cycles (TTC).\n")

# Sequential Priority example
print("First, we run Sequential Priority (SP) allocation.\n")

print("Given the following selection order:\n")
print(">>> order = [2, 0, 1]\n")
order = [2, 0, 1]

print("This means the selection order is: Carol → Alice → Bob.\n")

print("Calling SP and displaying the result:\n")
print(">>> sp_result = sequential_priority(order, prefs)")
print(">>> print(sp_result)")
sp_result = sequential_priority(order, prefs)
print(sp_result)

print("\nWe can also convert the result to a dictionary for further analysis:\n")
print(">>> print(sp_result.to_dict())\n")
print(sp_result.to_dict())

# Top Trading Cycles example
print("\nNow, we demonstrate Top Trading Cycles (TTC) allocation.\n")

print("Given an initial endowment:\n")
print(">>> endowment = [1, 2, 0]\n")
endowment = [1, 2, 0]

print("This means:\n")
print("  - Alice initially holds B\n")
print("  - Bob initially holds C\n")
print("  - Carol initially holds A\n")

print("Calling TTC and displaying the result:\n")
print(">>> ttc_result = top_trading_cycles(endowment, prefs)")
ttc_result = top_trading_cycles(endowment, prefs)
print(">>> print(ttc_result)")
print(ttc_result)

print("\nWe can also convert the TTC result to a list of (agent, object) pairs:\n")
print(">>> print(ttc_result.to_pairs())\n")
print(ttc_result.to_pairs())

print("\nThis is just the beginning of using gamealloc.\n")
print("Feel free to explore and enjoy it!")
print("-" * 100)