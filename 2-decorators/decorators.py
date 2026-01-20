from functools import wraps

def limit_args(max_value: int, mode:str):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            clip_args = []
            for key in args:
                if key > max_value:
                    match mode:
                        case "error":
                            raise ValueError(f"Значение {key} превышает максимальное")
                        case "clip": 
                            clip_args.append(max_value)
                else:
                    clip_args.append(key)
            result = func(*clip_args, **kwargs)
            return result
        return wrapper
    return decorator

@limit_args(max_value=10, mode="clip")
def multiply(a, b):
    return a * b

@limit_args(max_value=10, mode="error")
def multiply2(a, b):
    return a * b

print(multiply(2, 3))
print(multiply(100, 3))

print(multiply2(2, 3))
print(multiply2(100, 3))