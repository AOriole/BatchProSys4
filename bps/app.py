# -*- coding: utf-8 -*-

from flask import Flask, render_template, url_for, request
from controller.app_controller import AppController

#create flask obj
app = Flask(__name__)

@app.route('/')  # route to our index page
def home():
    return render_template('index.html')


accounts_path = "../data/accounts.json"
transaction_path = "../data/transactions.txt"

@app.route('/controller', methods=['POST'])
def controller():
    #run flask app
    if request.method == 'POST':
        output = AppController()
        return render_template('index.html', prediction=output)


if __name__ == '__main__':
    app.run(debug=True)



