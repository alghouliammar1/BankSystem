import datetime
from User import User
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
        with open(f"Transactions/{self.account_number}_transactions.txt", "a") as f:
            for transaction in self.transaction_log:
                f.write(transaction + "\n")
        self.transaction_log = []  # Clear transaction log after writing to file
    def read_transaction_log(self):
        """Reads the transaction log from the file and returns a list of transactions."""
        try:
            # Construct the filename based on account number
            filename = f"Transactions/{self.account_number}_transactions.txt"
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
