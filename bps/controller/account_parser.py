import json
from model.account import Account

#
# - globals
#




#
# - methods
#

def parse_account_file_content(content):
    global accounts
    parsed_content = json.loads(content)

    for parsed_account in parsed_content.get('accounts'):
        account_code = int(parsed_account.get('id'))
        opening_balance = float(parsed_account.get('balance'))

        account = Account(account_code, opening_balance=opening_balance)
        Account.add_account(account)



def parse_account_file(file_path):
    with open(file_path, "r") as f:
        content = f.read()
        parse_account_file_content(content)


#
# -- Test
#

if __name__ == "__main__":
    file_path = "../../data/accounts.json"
    parse_account_file(file_path)

    for account_code, account in Account.get_accounts().items():
        print(account)
