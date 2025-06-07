import pytest
from gamealloc import random_objects_preference_instance, random_objects_allocation_instance

def test_random_objects_preference_instance():
    res = [[[0]], [[1, 0], [0, 1]], [[1, 2, 0], [2, 1, 0], [2, 0, 1]], [[3, 1, 0, 2], [3, 2, 0, 1], [0, 3, 2, 1], [1, 2, 3, 0]]]
    for size in range(-5, 5):
        if size <= 0:
            with pytest.raises(ValueError):
                random_objects_preference_instance(size, 205)
        else:
            assert random_objects_preference_instance(size, 205) == res[size - 1]

def test_random_objects_allocation_instance():
    res = [[0], [0, 1], [2, 0, 1], [0, 3, 1, 2]]
    for size in range(-5, 5):
        if size <= 0:
            with pytest.raises(ValueError):
                random_objects_allocation_instance(size, 42)
        else:
            assert random_objects_allocation_instance(size, 42) == res[size - 1]
