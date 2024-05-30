from BankAccount import BankAccount
class CheckingAccount(BankAccount):
    def __init__(self, account_number, name, balance, pin, overdraft_limit=0):
        super().__init__(account_number, name, balance, pin, "Checking")
        self.overdraft_limit = overdraft_limit

    def withdraw(self, amount):
        if 0 < amount <= self.balance + self.overdraft_limit:
            self.balance -= amount
            self.log_transaction(f"Withdrawal: ${amount:.2f}")
            print(f"Withdrawal successful. New balance: ${self.balance:.2f}")
        else:
            print("Insufficient funds.")

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            self.log_transaction(f"Deposit: ${amount:.2f}")
            print(f"Deposit successful. New balance: ${self.balance:.2f}")
        else:
            print("Invalid deposit amount.")

    