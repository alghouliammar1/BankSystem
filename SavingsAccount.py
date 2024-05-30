from BankAccount import BankAccount


class SavingsAccount(BankAccount):
    def __init__(self, account_number, name, balance, pin, interest_rate=0.01):
        super().__init__(account_number, name, balance, pin, "Savings")
        self.interest_rate = interest_rate

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            self.log_transaction(f"Deposit: ${amount:.2f}")
            print(f"Deposit successful. New balance: ${self.balance:.2f}")
        else:
            print("Invalid deposit amount.")
