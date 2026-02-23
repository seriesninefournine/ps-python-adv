from typing import Optional, TypeVar, Generic, TypeGuard

T = TypeVar("T")
R = TypeVar("R")

def is_int(x: object) -> TypeGuard[int]:
    return isinstance(x, int)

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
        tmp_list: list[T] = []
        for k, _ in self.val_dict.items():
            tmp_list.append(k)
        return tmp_list

    def values(self) -> list[R]:
        tmp_list: list[R] = []
        for _, v in self.val_dict.items():
            tmp_list.append(v)
        return tmp_list
    

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