
from CheckingAccount  import CheckingAccount
from SavingsAccount  import SavingsAccount
import uuid

class BankSystem:
    def __init__(self):
        self.accounts = {}  # Dictionary to store accounts (key: account number, value: BankAccount object)
        self.load_accounts_from_file()  

    def generate_account_number(self):
      
        
        # import random
        # account_number = random.randint(100000, 999999)
        # while account_number in self.accounts:
        #     account_number = random.randint(100000, 999999)
        # return account_number
        account_number = uuid.uuid4()
        return account_number
    def create_account(self, name, pin, account_type="savings", starting_balance=0, interest_rate=0.01, overdraft_limit=0):
        account_number = self.generate_account_number()
        if account_type == "savings":
            new_account = SavingsAccount(account_number, name, starting_balance, pin, interest_rate)
        elif account_type == 'checking':
            new_account = CheckingAccount(account_number, name, starting_balance, pin, overdraft_limit)
        else:
            raise ValueError("Invalid account type. Choose from 'Savings' or 'Checking'.")
        self.accounts[account_number] = new_account
        self.write_accounts_to_file()  # Call method to write accounts to file

        return new_account

    def load_accounts_from_file(self):
        try:
            with open("accounts.txt", "r") as f:
                for line in f:
                    data = line.strip().split(",")
                    account_number, name, balance, pin, account_type = data[0:5]
                    if account_type == "Savings":
                        interest_rate = float(data[5])
                        account = SavingsAccount(
                            int(account_number), name, float(balance), int(pin), interest_rate
                        )
                    elif account_type == "Checking":
                        overdraft_limit = float(data[5])
                        account = CheckingAccount(int(account_number), name, float(balance), int(pin), overdraft_limit)
                    else:
                        raise ValueError("Invalid account data found in file.")
                    self.accounts[int(account_number)] = account
            print("Accounts loaded successfully.")
        except FileNotFoundError:
            print("No accounts file found. Creating a new one.")

    def write_accounts_to_file(self):
        with open("accounts.txt", "w") as f:
            for account in self.accounts.values():
                if isinstance(account, SavingsAccount):
                    account_data = (
                        account.account_number,
                        account.name,
                        account.balance,
                        account.pin,
                        account.account_type,
                        account.interest_rate,
                    )
                elif isinstance(account, CheckingAccount):
                    account_data = (
                        account.account_number,
                        account.name,
                        account.balance,
                        account.pin,
                        account.account_type,
                        account.overdraft_limit,
                    )
                else:
                    raise ValueError("Unexpected account type found.")
                f.write(",".join(map(str, account_data)) + "\n")
        print("Accounts saved successfully.")
    def get_Account(self,account_number):
        if account_number in self.accounts:
            account = self.accounts[account_number]
            return account
        else:
            print("Account not found.")
        return None
    def authenticate_user(self, account_number, entered_pin):
        if account_number in self.accounts:
            account = self.accounts[account_number]
            if account.authenticate(entered_pin):
                return account
            else:
                print("Invalid PIN.")
        else:
            print("Account not found.")
        return None

    def manage_account(self, account):
        while True:
            print("\nAccount Management Menu")
            print("1. View Balance")
            print("2. Deposit")
            # Check account type for appropriate options (e.g., withdraw for checking accounts)
            if isinstance(account, CheckingAccount):
                print("3. Withdraw")
            if isinstance(account, CheckingAccount):
                print("4. Transfer")
            print("5. Transaction Log")
            print("6. Exit")

            choice = input("Enter your choice: ")

            if choice == "1":
                print(f"Your current balance: ${account.get_balance():.2f}")
            elif choice == "2":
                amount = float(input("Enter deposit amount: "))
                account.deposit(amount)
            elif choice == "3" and isinstance(account, CheckingAccount):
                amount = float(input("Enter withdrawal amount: "))
                account.withdraw(amount)
            elif choice == "4" and isinstance(account, CheckingAccount):
                to_account_number = float(input("Enter recipient account number: "))
                amount = float(input("Enter withdrawal amount: "))
                transfer(account,to_account_number,amount)
            elif choice == "5":
                transactions=account.read_transaction_log()
                if transactions:
                    for transaction in transactions:
                        print(transaction)
                else:
                    print("No transactions found in your log.")
            elif choice == "6":
                return
            else:
                print("Invalid choice.")

    def is_account_valid(self, account_number):
        return account_number in self.accounts

    def transfer(self,account, to_account_number, amount):      
        if amount <= 0:
            print("Transfer amount must be positive.")
            return False

        if to_account_number == self.account_number:
            print("Cannot transfer money to the same account.")
            return False

        if not self.is_account_valid(to_account_number):
            print(f"Invalid recipient account number: {to_account_number}")
            return False

        # Check if sufficient funds are available (including overdraft limit for CheckingAccount)
        if account.balance + account.overdraft_limit < amount:
            print("Insufficient funds.")
            return False

        # Get recipient account object
        recipient_account = self.get_Account(to_account_number)

        # Perform the transfer (deduct from this account, add to recipient account)
        account.withdraw(amount)
        recipient_account.deposit(amount)

        # Log the transaction in both accounts
        account.log_transaction(f"Transfer: -${amount:.2f} to account {to_account_number}")
        recipient_account.log_transaction(f"Transfer: +${amount:.2f} from account {self.account_number}")

        print(f"Transfer successful! Transferred ${amount:.2f} to account {to_account_number}.")
        return True

