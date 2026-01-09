import threading

class BankAccount:
    def __init__(self, balance):
        self.balance = balance
        self.lock = threading.Lock()

    def deposit(self, amount):
        with self.lock:
            self.balance += amount
            print(f"Пополнено: {amount} | Баланс: {self.balance}")

    def withdraw(self, amount):
        with self.lock:
            if self.balance >= amount:
                self.balance -= amount
                print(f"Снято: {amount} | Баланс: {self.balance}")
            else:
                print(f"Недостаточно средств для снятия {amount}")


def worker(account):
    for _ in range(3):
        account.deposit(50)
        account.withdraw(30)


if __name__ == "__main__":
    account = BankAccount(100)

    threads = [threading.Thread(target=worker, args=(account,)) for _ in range(2)]

    for t in threads: t.start()
    for t in threads: t.join()

    print(f"Итоговый баланс: {account.balance}")