import datetime
from model.account import Account
from model.transaction import Transaction

#
# -- Globals
#

current_account:Account


#
# -- Methods
#

def parse_client_header(record):
    record_type = record[0:2]
    account_no_hex = record[2:6]
    account_no_dec = int(account_no_hex, 16)
    transaction_records = int(record[6:])

    account = Account.get_account(account_no_dec)

    return account


def parse_client_transaction(record):
    record_type = record[0:2]
    transaction_date_str = record[2:17]

    transaction_date = datetime.datetime(
        int(transaction_date_str[4:8]),     # year
        int(transaction_date_str[2:4]),     # month
        int(transaction_date_str[0:2]),     # day
        int(transaction_date_str[9:11]),    # hour
        int(transaction_date_str[11:13]),   # minute
        int(transaction_date_str[13:15])    # seconds
    )

    transaction_type = record[17]
    transaction_amount = float(record[18:37])
    third_party_account = int(record[37:])

    transaction = Transaction(transaction_date, transaction_type, transaction_amount, third_party_account)

    return transaction


def parse_record(record):
    global accounts
    global current_account

    record_type = record[0:2]

    if record_type == 'CH':
        current_account = parse_client_header(record)

    elif record_type == 'CT':
        transaction = parse_client_transaction(record)
        current_account.add_transaction(transaction)


def parse_transaction_file(file_path):
    with open(file_path, "r") as f:
        line = f.readline()

        while line:
            parse_record(line)
            line = f.readline()

#
# -- Test
#


if __name__ == "__main__":
    file_path = "../../data/transactions.txt"
    parse_transaction_file(file_path)

    for account_code, account in Account.get_accounts().items():
        print(account_code, account)


