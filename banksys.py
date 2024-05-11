import datetime


class User:
    def __init__(self, name, pin):
        self.name = name
        self.pin = pin

    def authenticate(self, entered_pin):
        return self.pin == entered_pin


class BankAccount(User):
    def __init__(self, account_number, name, balance, pin, account_type="Standard"):
        super().__init__(name, pin)
        self.account_number = account_number
        self.balance = balance
        self.account_type = account_type
        self.transaction_log = []  # List to store transaction history

    def get_balance(self):
        return self.balance


    def log_transaction(self, message):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.transaction_log.append(f"{timestamp} - {message}")
        self.write_transaction_log_to_file()

    def write_transaction_log_to_file(self):
        with open(f"{self.account_number}_transactions.txt", "a") as f:
            for transaction in self.transaction_log:
                f.write(transaction + "\n")
        self.transaction_log = []  # Clear transaction log after writing to file
    def read_transaction_log(self):
        """Reads the transaction log from the file and returns a list of transactions."""
        try:
            # Construct the filename based on account number
            filename = f"{self.account_number}_transactions.txt"
            with open(filename, "r") as f:
                transactions = [line.strip() for line in f.readlines()]
            return transactions
        except FileNotFoundError:
            # Handle the case where the transaction log file doesn't exist
            print(f"Transaction log file not found for account {self.account_number}.")
            return []
        except Exception as e:
            # Handle other potential errors
            print(f"An error occurred while reading the transaction log: {e}")
            return []

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

    def transfer(self, to_account_number, amount):
        bank_system =BankSystem()
        if amount <= 0:
            print("Transfer amount must be positive.")
            return False

        if to_account_number == self.account_number:
            print("Cannot transfer money to the same account.")
            return False

        if not bank_system.is_account_valid(to_account_number):
            print(f"Invalid recipient account number: {to_account_number}")
            return False

        # Check if sufficient funds are available (including overdraft limit for CheckingAccount)
        if self.balance + self.overdraft_limit < amount:
            print("Insufficient funds.")
            return False

        # Get recipient account object
        recipient_account = bank_system.get_Account(to_account_number)

        # Perform the transfer (deduct from this account, add to recipient account)
        self.withdraw(amount)
        recipient_account.deposit(amount)

        # Log the transaction in both accounts
        self.log_transaction(f"Transfer: -${amount:.2f} to account {to_account_number}")
        recipient_account.log_transaction(f"Transfer: +${amount:.2f} from account {self.account_number}")

        print(f"Transfer successful! Transferred ${amount:.2f} to account {to_account_number}.")
        return True




class BankSystem:
    def __init__(self):
        self.accounts = {}  # Dictionary to store accounts (key: account number, value: BankAccount object)
        self.load_accounts_from_file()  # Call method to load accounts from file (if it exists)

    def generate_account_number(self):
        # Implement logic to generate a unique account number
        # Here's a simple example (replace with a more robust approach)
        import random
        account_number = random.randint(100000, 999999)
        while account_number in self.accounts:
            account_number = random.randint(100000, 999999)
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
                account.transfer(to_account_number,amount)
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




def main():
    bank_system = BankSystem()

    while True:
        print("\nBank System Menu")
        print("1. Create Account")
        print("2. Login")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            name = input("Enter your name: ")
            pin = int(input("Enter your PIN (4 digits): "))
            account_type = input("Choose account type (Savings or Checking): ").lower()
            starting_balance = float(input("Enter starting balance (optional, default 0): ") or 0)
            if account_type == "savings":
                try:
                    interest_rate = float(input("Enter interest rate (optional, default 0.01): ") or 0.01)
                    new_account = bank_system.create_account(
                        name, pin, account_type, starting_balance, interest_rate
                    )
                except:
                    raise ValueError("Unexpected value type found.")
            elif account_type == "checking":
                overdraft_limit = float(input("Enter overdraft limit (optional, default 0): ") or 0)
                new_account = bank_system.create_account(
                    name, pin, account_type, starting_balance, overdraft_limit
                )
            else:
                print("Invalid account type. Choose from 'Savings' or 'Checking'.")
                continue
            print(f"Account created successfully! Your account number is: {new_account.account_number}")
        elif choice == "2":
           try:
            account_number = int(input("Enter your account number: "))
            entered_pin = int(input("Enter your PIN: "))
            authenticated_account = bank_system.authenticate_user(account_number, entered_pin)
            if authenticated_account:
                bank_system.manage_account(authenticated_account)
            else:
                print("Authentication failed.")
            print("Accounts loaded successfully.")
           except FileNotFoundError:
            print("No accounts file found. Creating a new one.")



if __name__ == "__main__":
    main()