import json
from controller.account_parser import parse_account_file
from controller.transaction_parser import parse_transaction_file
from controller.custom_encoder import CustomEncoder
from model.account import Account
from view.banking_view import BankingView
import tkinter as tk
from pathlib import Path
from graphs.plots import plot_pie_chart
from model.transaction import Transaction

class AppController:        # below will be  methods in AppController

    data_path = Path(__file__).parent.parent.joinpath('data')

    def __init__(self):
        window = tk.Tk()                                # initialize TK

        screen_height = window.winfo_screenheight()     # fix screen size
        screen_width = window.winfo_screenwidth()

        #window.geometry("600x400+100+100")             # size 600x400, offset 100+100
        window.geometry(f"{screen_width-200}x{screen_height-200}+100+100")

        self.view = BankingView(window)         # controller controls the view by creating a bankingView as an instance
        self.init_button_handlers()
        self.accounts_file = None
        self.transaction_file = None

        window.mainloop()                       # listen to the events by looping untill closed

    def init_button_handlers(self):
        self.view.accounts_btn.config(command=lambda: self.load_accounts())
        self.view.transactions_btn.config(command=lambda: self.load_transactions())
        self.view.process_btn.config(command=lambda: self.process_transactions())
        self.view.analyse_btn.config(command=lambda: self.analyse_transactions())


    # Read data file
    def get_file_content(self, filename):
        with open(filename, 'r') as f:
            content = f.read()

        return content

    def get_filename(self, title, description, definition):
        file_types = (description, definition),
        filename = self.view.get_file(AppController.data_path, title, file_types)   # opens up the prompt to read fromthe file
        return filename

    def load_accounts(self):
        self.accounts_file = self.get_filename('Load Accounts', 'account files', '*.json')

        if self.accounts_file:
            content = self.get_file_content(self.accounts_file)
            self.view.write_account_details(content)
            self.view.select_accounts_tab()
            #self.view.write_account_details('account details')

    def load_transactions(self):
        self.transaction_file = self.get_filename('Load Transactions', 'transaction files', '*.txt')

        if self.transaction_file:
            content = self.get_file_content(self.transaction_file)
            self.view.write_transaction_details(content)
            self.view.select_transaction_tab()
            #self.view.write_transaction_details('transaction details')

    def process_transactions(self):
        if not self.accounts_file:
            self.view.show_popup_error("File Not Selected", "You have not selected an accounts file to process")
            return

        if not self.transaction_file:
            self.view.show_popup_error("File Not Selected", "You have not selected a transaction file to process")
            return

        json_output = self.parse_data(self.accounts_file, self.transaction_file)
        self.view.write_output_details(json_output)
        self.view.select_output_tab()
        #self.view.write_output_details('output details')

    def analyse_transactions(self):
        credits, debits = self.get_credits_and_debits()
        fig = plot_pie_chart(credits, debits)
        self.view.draw_graph("Pie Chart", fig)

    def parse_data(self, accounts_path, transaction_path):
        parse_account_file(accounts_path)
        parse_transaction_file(transaction_path)

        json_output = json.dumps(list(Account.get_accounts().values()), indent=4, cls=CustomEncoder)

        return json_output

    def get_credits_and_debits(self):

        if not Account.get_accounts():
            self.view.show_popup_error("Error : ", "Transactions have not been processed")
            return

        credits = 0
        debits = 0

        for account in Account.get_accounts().values():
            for transaction in account.get_transactions():
                transaction_amount = transaction.transaction_amount
                transaction_type = transaction.transaction_type

                if transaction_type == "C":
                    credits += transaction_amount
                else:
                    debits -= transaction_amount

        return (credits, debits)


