from CheckingAccount import CheckingAccount
from SavingsAccount import SavingsAccount
import uuid
import json


class BankSystem:
    def __init__(self):
        self.accounts = {}  # Dictionary to store accounts (key: account number, value: BankAccount object)
        self.load_accounts_from_file()

    def generate_account_number(self):
        account_number = uuid.uuid4()
        return account_number

    def create_account(
        self,
        name,
        pin,
        account_type="savings",
        starting_balance=0,
        interest_rate=0.01,
        overdraft_limit=0,
    ):
        account_number = self.generate_account_number()
        if account_type == "savings":
            new_account = SavingsAccount(
                account_number, name, starting_balance, pin, interest_rate
            )
            new_account.log_transaction(
                f"Create: +${account_number} with Initial Balance {starting_balance:.2f} and Interest Rate of {interest_rate:.2f}"
            )
        elif account_type == "checking":
            new_account = CheckingAccount(
                account_number, name, starting_balance, pin, overdraft_limit
            )
            new_account.log_transaction(
                f"Create: +${account_number} with Initial Balance {starting_balance:.2f} and Overdraft Limit of {overdraft_limit:.2f}"
            )

        else:
            raise ValueError(
                "Invalid account type. Choose from 'Savings' or 'Checking'."
            )
        self.accounts[account_number] = new_account
        self.write_accounts_to_file()  # Call method to write accounts to file
        self.load_accounts_from_file()
        return new_account

    # new load _accounts from json file
    def load_accounts_from_file(self):
        try:
            with open("Accounts/accounts.json", "r") as f:
                try:
                    data = json.load(f)
                except FileNotFoundError:
                    raise ValueError("empty file.")

            self.accounts = {}
            for account_data in data:
                account_number = account_data["account_number"]
                name = account_data["name"]
                balance = account_data["balance"]
                pin = account_data["pin"]
                account_type = account_data["account_type"]
                if account_type == "Savings":
                    interest_rate = account_data["interest_rate"]
                    account = SavingsAccount(
                        (account_number), name, float(balance), int(pin), interest_rate
                    )
                elif account_type == "Checking":
                    overdraft_limit = account_data["overdraft_limit"]
                    account = CheckingAccount(
                        (account_number),
                        name,
                        float(balance),
                        int(pin),
                        overdraft_limit,
                    )
                else:
                    raise ValueError("Invalid account data found in file.")
                self.accounts[(account_number)] = account
            print("Accounts loaded successfully.")
        except FileNotFoundError:
            print("No accounts file found. Creating a new one.")

    # here is the new function that write accounts into json file
    def write_accounts_to_file(self):
        account_data = []
        for account in self.accounts.values():
            if isinstance(account, SavingsAccount):
                account_data.append(
                    {
                        "account_number": account.account_number,
                        "name": account.name,
                        "balance": account.balance,
                        "pin": account.pin,
                        "account_type": account.account_type,
                        "interest_rate": account.interest_rate,
                    }
                )
            elif isinstance(account, CheckingAccount):
                account_data.append(
                    {
                        "account_number": account.account_number,
                        "name": account.name,
                        "balance": account.balance,
                        "pin": account.pin,
                        "account_type": account.account_type,
                        "overdraft_limit": account.overdraft_limit,
                    }
                )
            else:
                raise ValueError("Unexpected account type found.")

        with open("Accounts/accounts.json", "w") as f:
            json.dump(account_data, f, indent=4, cls=CustomJSONEncoder)
        print("Accounts saved successfully.")

    def get_account(self, account_number):
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

    # Transfer Function use to transfer  from one Account to Another account
    def transfer(self, account, to_account_number, amount):
        if amount <= 0:
            raise BusinessException("Transfer amount must be positive.")

        if to_account_number == self.account_number:
            raise BusinessException("Cannot transfer money to the same account.")

        if not self.is_account_valid(to_account_number):
            raise BusinessException(
                f"Invalid recipient account number: {to_account_number}"
            )

        # Check if sufficient funds are available (including overdraft limit for CheckingAccount)
        if account.balance + account.overdraft_limit < amount:
            raise BusinessException("Insufficient funds.")
        # Get recipient account object
        recipient_account = self.get_account(to_account_number)

        # Perform the transfer (deduct from this account, add to recipient account)
        account.withdraw(amount)
        recipient_account.deposit(amount)

        # Log the transaction in both accounts
        account.log_transaction(
            f"Transfer: -${amount:.2f} to account {to_account_number}"
        )
        recipient_account.log_transaction(
            f"Transfer: +${amount:.2f} from account {account.account_number}"
        )

        print(
            f"Transfer successful! Transferred ${amount:.2f} to account {to_account_number}."
        )
        return True

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
                to_account_number = input("Enter recipient account number: ")
                amount = float(input("Enter withdrawal amount: "))
                self.transfer(account, to_account_number, amount)
            elif choice == "5":
                transactions = account.read_transaction_log()
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


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, uuid.UUID):
            return str(obj)
        return json.JSONEncoder.default(self, obj)


class BusinessException(Exception):
    """Custom exception for business logic errors."""

    pass
