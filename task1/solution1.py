import pytest


def strict(func):
    def wrapper(*args, **kwargs):
        annotations = func.__annotations__

        for arg_name, arg_value in zip(annotations.keys(), args):
            if arg_name in annotations:
                expected_type = annotations[arg_name]
                if not isinstance(arg_value, expected_type):
                    raise TypeError(
                        f"Argument '{arg_name}' must be of type {expected_type.__name__}, not {type(arg_value).__name__}")

        for arg_name, arg_value in kwargs.items():
            if arg_name in annotations:
                expected_type = annotations[arg_name]
                if not isinstance(arg_value, expected_type):
                    raise TypeError(
                        f"Argument '{arg_name}' must be of type {expected_type.__name__}, not {type(arg_value).__name__}")

        return func(*args, **kwargs)

    return wrapper


@strict
def sum_two(a: int, b: int) -> int:
    return a + b


### 1. Тесты для int
def test_int_correct():
    @strict
    def add(a: int, b: int) -> int:
        return a + b

    assert add(1, 2) == 3  # Корректные int


def test_int_incorrect():
    @strict
    def add(a: int, b: int) -> int:
        return a + b

    with pytest.raises(TypeError) as exc_info:
        add(1, "2")  # str вместо int
    assert "must be of type int, not str" in str(exc_info.value)


### 2. Тесты для float
def test_float_correct():
    @strict
    def divide(a: float, b: float) -> float:
        return a / b

    assert divide(5.0, 2.0) == 2.5  # Корректные float


def test_float_incorrect():
    @strict
    def divide(a: float, b: float) -> float:
        return a / b

    with pytest.raises(TypeError) as exc_info:
        divide(5.0, "2.0")  # str вместо float
    assert "must be of type float, not str" in str(exc_info.value)


### 3. Тесты для bool
def test_bool_correct():
    @strict
    def negate(flag: bool) -> bool:
        return not flag

    assert negate(True) is False  # Корректный bool


def test_bool_incorrect():
    @strict
    def negate(flag: bool) -> bool:
        return not flag

    with pytest.raises(TypeError) as exc_info:
        negate(1)  # int вместо bool
    assert "must be of type bool, not int" in str(exc_info.value)


### 4. Тесты для str
def test_str_correct():
    @strict
    def greet(name: str) -> str:
        return f"Hello, {name}!"

    assert greet("Alice") == "Hello, Alice!"  # Корректный str


def test_str_incorrect():
    @strict
    def greet(name: str) -> str:
        return f"Hello, {name}!"

    with pytest.raises(TypeError) as exc_info:
        greet(123)  # int вместо str
    assert "must be of type str, not int" in str(exc_info.value)


### 5. Смешанные типы
def test_mixed_types_correct():
    @strict
    def mixed(a: int, b: float, c: bool, d: str) -> str:
        return f"{a} {b} {c} {d}"

    assert mixed(1, 2.5, True, "test") == "1 2.5 True test"  # Все типы верны


def test_mixed_types_incorrect():
    @strict
    def mixed(a: int, b: float, c: bool, d: str) -> str:
        return f"{a} {b} {c} {d}"

    with pytest.raises(TypeError) as exc_info:
        mixed(1, 2.5, "True", "test")  # str вместо bool
    assert "must be of type bool, not str" in str(exc_info.value)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
