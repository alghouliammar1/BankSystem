from  BankAccount import BankAccount
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

    # def transfer(self, to_account_number, amount):
    #     bank_system =BankSystem()
    #     if amount <= 0:
    #         print("Transfer amount must be positive.")
    #         return False

    #     if to_account_number == self.account_number:
    #         print("Cannot transfer money to the same account.")
    #         return False

    #     if not bank_system.is_account_valid(to_account_number):
    #         print(f"Invalid recipient account number: {to_account_number}")
    #         return False

    #     # Check if sufficient funds are available (including overdraft limit for CheckingAccount)
    #     if self.balance + self.overdraft_limit < amount:
    #         print("Insufficient funds.")
    #         return False

    #     # Get recipient account object
    #     recipient_account = bank_system.get_Account(to_account_number)

    #     # Perform the transfer (deduct from this account, add to recipient account)
    #     self.withdraw(amount)
    #     recipient_account.deposit(amount)

    #     # Log the transaction in both accounts
    #     self.log_transaction(f"Transfer: -${amount:.2f} to account {to_account_number}")
    #     recipient_account.log_transaction(f"Transfer: +${amount:.2f} from account {self.account_number}")

    #     print(f"Transfer successful! Transferred ${amount:.2f} to account {to_account_number}.")
    #     return True

