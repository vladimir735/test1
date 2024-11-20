def strict(func):
    def wrapper(*args, **kwargs):
        annotations = func.__annotations__
        print(annotations)
        for arg_name, arg_value in zip(annotations.keys(), args):
            expected_type = annotations[arg_name]
            if not isinstance(arg_value, expected_type):
                raise TypeError(f"Аргумент '{arg_name}' должен быть {expected_type.__name__},"
                                f"Ваш аргумент {type(arg_value).__name__}.")
        return func(*args, **kwargs)
    return wrapper

@strict
def sum_two(a: int, b: int) -> int:
    return a + b

print(sum_two(1, 2))  # >>> 3
print(sum_two(1, 2.4))  # >>> TypeError
