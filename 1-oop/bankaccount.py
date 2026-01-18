from decimal import Decimal
class BankAccount:
    accounts = []
    def __init__(self, owner: str, acc_number: str, balance:float | Decimal | int) -> None:
        self.owner = owner
        self.acc_number = acc_number
        self.balance = round(Decimal(balance),2)
        BankAccount.accounts.append(self)
    
    def deposit(self, amount:float | Decimal):
        """Пополнение счёта на сумму amount"""
        summ = round(Decimal(amount),2)
        self.balance += summ
        print(f"Счет {self.acc_number} пополнен на сумму {summ}. Текущий баланс: {self.balance}")

    def withdraw(self, amount:float | Decimal) -> bool:
        """Снятие денег со счёта. Нельзя уйти в минус."""
        summ = round(Decimal(amount),2)
        if self.balance < summ:
            print(f"Недостаточно средств на счете {self.acc_number}, операция отменена. Текущий баланс: {self.balance}")
            return False
        self.balance -= summ
        print(f"Со счета {self.acc_number} снята сумма {summ}. Текущий баланс: {self.balance}")
        return True
    

    def transferto(self, otheraccount: "BankAccount", amount:float | Decimal):
        """Перевод денег на другой счёт BankAccount."""
        amount = round(Decimal(amount),2)
        if self.withdraw(amount):
            otheraccount.deposit(amount)
            print(f"Перевод со счета {self.acc_number} на счет {otheraccount.acc_number} суммы {amount} выполнен. Текущий баланс: {self.balance}")
            return True
        print(f"Перевод со счета {self.acc_number} на счет {otheraccount.acc_number} суммы {amount} не выполнен. Текущий баланс: {self.balance}")
        return False

    def info(self):
        """возвращать строку с краткой информацией о счёте"""
        return f"Владелец: {self.owner}, номер счета: {self.acc_number}, текущий баланс {self.balance}"

    @classmethod
    def get_accounts_created(cls):
        """возвращает количество созданных счетов."""
        return len(cls.accounts)


acc01 = BankAccount("Петрович", "ACC202601-001", 300)
acc02 = BankAccount("Иваныч", "ACC202601-001", 123.43)
print(acc01.info())
print(acc02.info())
print("--------------------------")
acc01.transferto(acc02,200)
print(acc01.info())
print(acc02.info())
print("--------------------------")
acc01.transferto(acc02,200)
print(acc01.info())
print(acc02.info())
print(acc02.get_accounts_created())