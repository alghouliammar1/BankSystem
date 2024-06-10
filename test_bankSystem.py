import unittest
from CheckingAccount import CheckingAccount
from SavingsAccount import SavingsAccount
from BankSystem import BankSystem

# Sample data for testing
test_data = [
    {
        "account_number": "12345678-1234-1234-1234-123456789012",
        "name": "John Doe",
        "balance": 100.00,
        "pin": 1234,
        "account_type": "Savings",
        "interest_rate": 0.01
    },
    {
        "account_number": "87654321-1234-1234-1234-123456789012",
        "name": "Jane Doe",
        "balance": 500.00,
        "pin": 5678,
        "account_type": "Checking",
        "overdraft_limit": 200.00
    }
]


class TestBank(unittest.TestCase):

    def setUp(self):
        self.bank = BankSystem()
        # Load test data into the bank
        for account_data in test_data:
            account_type = account_data["account_type"]
            if account_type == "Savings":
                account_number=account_data["account_number"],
                name=account_data["name"],
                balance=account_data["balance"],
                pin=account_data["pin"],
                interest_rate=account_data["interest_rate"]
                account = SavingsAccount(
                    account_number,
                    name,
                    balance,
                    pin,
                    interest_rate
                )
            else:
                account = CheckingAccount(
                    account_data["account_number"],
                    account_data["name"],
                    account_data["balance"],
                    account_data["pin"],
                    account_data["overdraft_limit"]
                )
            self.bank.accounts[account_data["account_number"]] = account

    # Test creating a new savings account
    def test_create_savings_account(self):
        account = self.bank.create_account(
            "John Smith", 1111, "Savings", 200.00, 0.02)
        self.assertIsInstance(account, SavingsAccount)
        self.assertEqual(account.balance, 200.00)
        self.assertEqual(account.interest_rate, 0.02)

    # Test creating a new checking account
    def test_create_checking_account(self):
        account = self.bank.create_account(
            "Jane Smith", 2222, "Checking", 1000.00, 100.00)
        self.assertIsInstance(account, CheckingAccount)
        self.assertEqual(account.balance, 1000.00)
        self.assertEqual(account.overdraft_limit, 100.00)

    # Test creating an account with invalid type
    def test_create_invalid_account_type(self):
        with self.assertRaises(ValueError):
            self.bank.create_account("Alice", 3333, "Invalid", 500.00)

    # Test loading accounts from a file (replace with your implementation for testing)
    def test_load_accounts_from_file(self):
        # Replace this with your logic to test loading from a file
        # You can mock the file access or create a temporary test file
        # with the test data and test the loading process
        pass

    # Test getting an account by number
    def test_get_account(self):
        account_number = "12345678-1234-1234-1234-123456789012"
        account = self.bank.get_account(account_number)
        self.assertIsInstance(account, SavingsAccount)
        self.assertEqual(account.name, "John Doe")

    # Test getting a non-existent account
    def test_get_nonexistent_account(self):
        account_number = "99999999-1234-1234-1234-123456789012"
        account = self.bank.get_account(account_number)
        self.assertIsNone(account)  # Expect None for non-existent account


        
test=TestBank()
test.setUp()
test.test_create_invalid_account_type()
test.test_create_checking_account()
test.test_create_savings_account()
test.test_get_account()
test.test_load_accounts_from_file()
