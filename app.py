from flask import Flask, render_template, request, jsonify
from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable

import queries
from nodes_models import *
from relation_models import *
from datetime import date, datetime
from queries import *

app = Flask(__name__)

# Neo4j configuration
neo4j_uri = "bolt://localhost:7687"
neo4j_user = "neo4j"
neo4j_password = "Billa@12"

today_date = date.today()

def check_bank_balance(accountNumber):
    query = check_balance_query(accountNumber)
    result = fetch_query1(query)
    return result['balance']
    # print(f"balance: {result['balance']}")

def get_transactions_from_neo4j():
    # Implement the logic to retrieve data from Neo4j
    # Example code using the neo4j Python driver
    with GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password)) as driver:
        with driver.session() as session:
            result = session.run("MATCH (t:Transaction) RETURN t.type AS account, t.name as name, t.toWhom AS toWhom, t.key AS key")
            print(result)
            transactions = [record for record in result]

    return transactions

def save_customer_data_to_neo4j(account_no, name, accID, custID):
    try:
        with GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password)) as driver:
            with driver.session() as session:
                result = session.run(create_customer(name,account_no,accID))
                print(result)

        print("customer data saved succesfully")
    except Exception as e:
        print(f"Error connecting to Neo4j Database: {e}")


def save_customerE_data_to_neo4j(account_no, name, accID, custID, country, risk, iban, fid):
    try:
        with GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password)) as driver:
            with driver.session() as session:
                result = session.run(create_extrernal(account_no, iban, fid, country, risk, name,accID))
                print(result)

        print("customerE data saved succesfully")
    except Exception as e:
        print(f"Error connecting to Neo4j Database: {e}")

def run_external_transaction(sender, receiver, amount, transaction_key):
    try:
        with GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password)) as driver:
            with driver.session() as session:
                result = session.run(sends_external(amount, today_date, transaction_key, sender, receiver))
                print(result)

        print("customerE data saved succesfully")
    except Exception as e:
        print(f"Error connecting to Neo4j Database: {e}")

def run_internal_transaction(sender, receiver, amount, transaction_key):
    try:
        with GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password)) as driver:
            with driver.session() as session:
                result = session.run(sends_internal(amount, today_date, transaction_key, sender, receiver))
                print(result)

        print("customerI data saved succesfully")
    except Exception as e:
        print(f"Error connecting to Neo4j Database: {e}")

def get_res1_from_neo4j():
    with GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password)) as driver:
        # Start a session
        with driver.session() as session:
            result = session.run(queries.query1())
            # Convert result to a list of dictionaries
            data = [record.data() for record in result]
            print("Query executed")
            # print(data)
    return data

def get_res2_from_neo4j():
    with GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password)) as driver:
        # Start a session
        with driver.session() as session:
            result = session.run(queries.query2())
            # Convert result to a list of dictionaries
            data = [record.data() for record in result]
            print("Query executed")
            # print(data)
    return data

def deposit_execution(cash,AccountNo):
    try:
        with GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password)) as driver:
            with driver.session() as session:
                current_time = datetime.now()
                a = str(current_time)
                transaction_id = int(a.replace(" ", "").replace(":", "").replace("-", "")[0:14])
                query = cash_deposit_query(cash, today_date, transaction_id, AccountNo)
                print(query)
                session.run(query)
                print(f"cash_deposit successful")
                print("current balance: ", check_bank_balance(AccountNo))

        print("deposit saved succesfully")
    except Exception as e:
        print(f"Error connecting to Neo4j Database: {e}")
def withdraw_execution(cash, AccountNo):
    print(cash+"cash")
    try:
        with GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password)) as driver:
            with driver.session() as session:
                current_time = datetime.now()
                a = str(current_time)
                transaction_id = int(a.replace(" ", "").replace(":", "").replace("-", "")[0:14])
                query = cash_withdraw_query(cash, today_date, transaction_id, AccountNo)
                print(query)
                session.run(query)
                print(f"cash_withdraw successful")
                print("current balance: ", check_bank_balance(AccountNo))

        print("withdraw saved succesfully")
    except Exception as e:
        print(f"Error connecting to Neo4j Database: {e}")

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/api/save_transactionI', methods=['POST'])
def save_transactionI():
    data = request.get_json()
    sender = data.get('sender')
    receiver = data.get('receiver')
    amount = data.get('amount')
    transaction_key = data.get('transactionKey')
    current_time = datetime.now()
    a = str(current_time)
    transaction_id = int(a.replace(" ", "").replace(":", "").replace("-", "")[0:14])

    run_internal_transaction(sender, receiver, amount, transaction_id)

    return jsonify({'message': 'Transaction saved successfully from save_transactionI'})

@app.route('/api/save_transactionE', methods=['POST'])
def save_transactionE():
    data = request.get_json()
    sender = data.get('sender')
    receiver = data.get('receiver')
    amount = data.get('amount')
    transaction_key = data.get('transactionKey')
    current_time = datetime.now()
    a = str(current_time)
    transaction_id = int(a.replace(" ", "").replace(":", "").replace("-", "")[0:14])

    run_external_transaction(sender, receiver, amount, transaction_id)

    return jsonify({'message': 'Transaction saved successfully from save_transactionE'})

@app.route('/api/save_customerData', methods=['POST'])
def customer_data():
    data = request.get_json()
    account_no = data.get('account_No')
    name = data.get('name')
    accID = data.get('accID')
    custID = data.get('custID')

    save_customer_data_to_neo4j(account_no, name, accID, custID)

    return jsonify({'message': 'Customer saved successfully internal'})

@app.route('/api/save_customerEData', methods=['POST'])
def customerE_data():
    data = request.get_json()
    account_no = data.get('account_No')
    name = data.get('name')
    accID = data.get('accID')
    custID = data.get('custID')
    country = data.get('country')
    risk = data.get('risk_score')
    iban = data.get('iban_code')
    fid = data.get('fid')

    save_customerE_data_to_neo4j(account_no, name, accID, custID, country, risk, iban, str(fid))

    return jsonify({'message': 'Customer saved successfully external'})



@app.route('/api/get_transactions', methods=['GET'])
def get_transactions():
    transactions = get_transactions_from_neo4j()
    print(transactions)
    return jsonify(transactions)

@app.route('/api/get_query1_results', methods=['GET'])
def get_q1_results():
    res1 = get_res1_from_neo4j()
    # print(res1)
    res2 = [res1[0].get('cu.accountName'), res1[1].get('cu.accountName')]
    print(res2)
    return jsonify(res2)

@app.route('/api/get_query2_results', methods=['GET'])
def get_q2_results():
    res1 = get_res2_from_neo4j()
    res2 = [res1[0].get('cu.accountName')]
    print(res2)
    return jsonify(res2)

@app.route('/api/save_cash_deposit', methods=['POST'])
def do_deposit():

     data = request.get_json()
     cash = data.get('cash')
     accNo = data.get('deposit')
     deposit_execution(cash,accNo)
     return jsonify({'message': 'deposit done successfully external'})

@app.route('/api/save_cash_withdraw', methods=['POST'])
def do_withdraw():
    data = request.get_json()
    print(data)
    cash = data.get('cash')
    accNo = data.get('withdraw')
    withdraw_execution(cash, accNo)
    return jsonify({'message': 'withdraw done successfully external'})

if __name__ == '__main__':
    app.run(debug=True)
