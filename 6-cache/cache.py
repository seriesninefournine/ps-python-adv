from typing import Optional, TypeVar, Generic, TypeGuard

T = TypeVar("T")
R = TypeVar("R")

class Cache(Generic[T, R]):
    def __init__(self) -> None:
        self.val_dict: dict[T, R] = {}

    def set(self, key: T, val: R) -> None:
        if isinstance(val, int):
            self.val_dict[key] = val
        else:
            print(f"Ошибка типа. Переменная {val} имеет тип {type(val)}, а не int")

    def get(self, key: T) -> Optional[R]:
        if isinstance(key, str):
            return self.val_dict.get(key)
        else:
            print(f"Ошибка типа. Переменная {key} имеет тип {type(key)}, а не str")

    def keys(self) -> list[T]:
        return list(self.val_dict.keys())

    def values(self) -> list[R]:
        return list(self.val_dict.values())
    

hits = Cache[str, int]()
hits.set("home", 10)
hits.set("about", 3)
x = hits.get("home")        # x: int | None
paths = hits.keys()         # list[str]
counts = hits.values()      # list[int]

hits.set("contacts", "5")   # ❌ ошибка типов
hits.get(123)               # ❌ ошибка типов
print(x)
print(paths)
print(counts)