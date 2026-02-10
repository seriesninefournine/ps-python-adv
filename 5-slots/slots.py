import sys

class User:
    def __init__(self, name: str) -> None:
        self.name = name
        self.email = "user_email"
        self.password = "user_password"

class SlotUser:
    __slots__ = ("name", "email", "password")

    def __init__(self, name: str) -> None:
        self.name = name
        self.email = "user_email"
        self.password = "user_password"

user_list = []
slot_user_list = []

for iter in range(100000):
    user_list.append(User(str(iter)))
    slot_user_list.append(SlotUser(str(iter)))

total_user = sum(sys.getsizeof(u) for u in user_list)
total_slot = sum(sys.getsizeof(s) for s in slot_user_list)

print(total_user)
print(total_slot)