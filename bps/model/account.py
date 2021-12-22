import datetime
from model.transaction import Transaction


class Account:

    _accounts = {}

    @staticmethod
    def add_account(account):
        Account._accounts[account.account_code] = account

    @staticmethod
    def get_account(account_code:int):
        _account = Account._accounts.get(account_code)

        if not _account:
            _account = Account(account_code)
            Account.add_account(_account)

        return _account

    @staticmethod
    def get_accounts():
        return Account._accounts

    def __init__(self, account_code:int, transaction_count:int=0, opening_balance:float=0.0):
        self.account_code = account_code
        self.transaction_count = transaction_count
        self.opening_balance = opening_balance
        self.closing_balance = opening_balance
        self.transactions = []

    def __str__(self):
        return str({
            "account_code": self.account_code,
            "transaction_count": self.transaction_count,
            "opening_balance": self.opening_balance,
            "closing_balance": self.closing_balance,
            "transactions": [eval(str(_transaction)) for _transaction in self.transactions]
        })

    def to_json(self):
        return {
            "account_code": self.account_code,
            "transaction_count": self.transaction_count,
            "opening_balance": self.opening_balance,
            "closing_balance": self.closing_balance,
            "transactions": self.transactions
        }

    def add_transaction(self, transaction:Transaction):
        self.transactions.append(transaction)
        self.transaction_count += 1

        if transaction.transaction_type == 'C':
            self.closing_balance += transaction.transaction_amount
        else:
            self.closing_balance -= transaction.transaction_amount


    def get_transactions(self):
        return self.transactions