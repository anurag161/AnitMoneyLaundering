from nodes_models import *
from relation_models import *
from connection import *
from neo4j.exceptions import ConstraintError
from datetime import date, datetime

today_date = str(date.today())


def customer():
    customer_id = input("Enter the customer ID (4-digit number): ")
    name = input("Enter the name of the customer: ")
    ques2 = input("Do you want to add internal account or external? (i/e)")
    query = ""
    balance = 1000
    if (ques2 == "i"):
        accountID = int("100" + str(customer_id))
        accountNumber = int("10000" + str(customer_id))
        print("your account number is: ", accountNumber)
        print("your account ID is: ", accountID)
        query = create_customer(name, accountNumber, accountID,
                                balance)  # create_customer(name, accountNumber, accountID)
        print(f"current balance: {balance}")
    else:
        accountID = int("111" + str(customer_id))
        accountNumber = int("11100" + str(customer_id))
        print("your account number is: ", accountNumber)
        print("your account ID is: ", accountID)
        country_name = input("Enter the country name: ")
        risk_score = input("Enter the risk score: ")
        iban_code = input("Enter the IBAN code: ")
        financial_inst_id = input("Enter the financial institution ID(int only): ")
        query = create_extrernal(accountNumber, iban_code, financial_inst_id, country_name, risk_score, name, accountID)
        print(f"current balance: {balance}")
        # create_extrernal(accountNumber, iban_code, financial_inst_id, country_name, risk_score, name, accountID):
    try:
        run_query(query)
        print(f"customer {customer_id} created")

    except ConstraintError:
        print("Account number already exists")


def transaction():
    ques1 = ""
    sender_account_number = input("Enter the sender's account Number: ")
    receiver_account_number = input("Enter the receiver's account Number: ")
    amount = input("Enter the amount of the transaction: ")
    current_time = datetime.now()
    a = str(current_time)
    transaction_id = int(a.replace(" ", "").replace(":", "").replace("-", "")[0:14])
    query = ""
    # print(str(sender_account_number)[0:5], str(receiver_account_number)[0:5])
    # print("h1")
    if (str(sender_account_number)[0:5] == "10000" and str(receiver_account_number)[0:5] == "10000"):
        query = sends_internal(amount, today_date, transaction_id, sender_account_number, receiver_account_number)
        print("internal --> internal")
    elif (str(sender_account_number)[0:5] == "11100" and str(receiver_account_number)[0:5] == "10000"):
        query = recieves_external(amount, today_date, transaction_id, sender_account_number, receiver_account_number)
        print("external --> internal")
    elif (str(sender_account_number)[0:5] == "10000" and str(receiver_account_number)[0:5] == "11100"):
        query = sends_external(amount, today_date, transaction_id, sender_account_number, receiver_account_number)
        print("internal --> external")
    else:
        print("Issue in account numbers")

    # sends_external(amount, date, transaction_ID, accountNumber_sender, accountNumber_receiver)
    # sends_internal(amount, date, transaction_ID, accountNumber_sender, accountNumber_receiver)
    # recieves_external(amount, date, transaction_ID, accountNumber_sender, accountNumber_receiver)

    try:
        run_query(query)
        print(f"transaction {transaction_id} created")

    except ConstraintError:
        print("Account number already exists")

    print(query)


def cash_deposit():
    cash = input("Enter the amount of cash deposited: ")
    accountNumber = input("Enter the account number: ")
    print("current balance: ", check_bank_balance(accountNumber))
    current_time = datetime.now()
    a = str(current_time)
    transaction_id = int(a.replace(" ", "").replace(":", "").replace("-", "")[0:14])
    query = cash_deposit_query(cash, today_date, transaction_id, accountNumber)
    run_query(query)
    print(f"cash_deposit successful")
    print("current balance: ", check_bank_balance(accountNumber))


def cash_withdraw():
    cash = input("Enter the amount of cash withdraw: ")
    accountNumber = input("Enter the account number: ")
    print("current balance: ", check_bank_balance(accountNumber))
    current_time = datetime.now()
    a = str(current_time)
    transaction_id = int(a.replace(" ", "").replace(":", "").replace("-", "")[0:14])
    query = cash_withdraw_query(cash, today_date, transaction_id, accountNumber)
    run_query(query)
    print(f"cash_withdraw successful")
    print("current balance: ", check_bank_balance(accountNumber))
    current_time = datetime.now()


def check_bank_balance(accountNumber):
    query = check_balance_query(accountNumber)
    result = fetch_query1(query)
    return result['balance']
    # print(f"balance: {result['balance']}")