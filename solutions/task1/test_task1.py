import pytest

from solutions.task1.solution import strict


@strict
def add(a: int, b: int) -> int:
    return a + b

def test_add_correct_types():
    assert add(1, 2) == 3

def test_add_incorrect_type_a():
    with pytest.raises(TypeError):
        add("1", 2)

def test_add_incorrect_type_b():
    with pytest.raises(TypeError):
        add(1, "2")