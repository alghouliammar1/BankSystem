
from BankSystem import BankSystem
import logging

# Configure a logger with INFO level
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create a handler to print to the console
handler = logging.StreamHandler()
#handler.setLevel(logging.ERROR)  # Set handler level to match logger level

# Add the handler to the logger
logger.addHandler(handler)
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
                    logger.error("Unexpected value type found.")
                    raise ValueError("Unexpected value type found.")
                   
            elif account_type == "checking":
                overdraft_limit = float(input("Enter overdraft limit (optional, default 0): ") or 0)
                new_account = bank_system.create_account(
                    name, pin, account_type, starting_balance, overdraft_limit
                )
            else:
                logger.error("Invalid account type. Choose from 'Savings' or 'Checking'.")
                continue
            logger.info(f"Account created successfully! Your account number is: {new_account.account_number}")
        elif choice == "2":
           try:
            account_number = (input("Enter your account number: "))
            entered_pin = int(input("Enter your PIN: "))
            authenticated_account = bank_system.authenticate_user(account_number, entered_pin)
            if authenticated_account:
                bank_system.manage_account(authenticated_account)
            else:
                logger.error("Authentication failed.")
            logger.info("Accounts loaded successfully.")
           except FileNotFoundError:
            logger.error("No accounts file found. Creating a new one.")
        elif choice == "3": 
            return False


if __name__ == "__main__":
    main()