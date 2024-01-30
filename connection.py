from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable
from nodes_models import *
from relation_models import *
from datetime import date

uri = "bolt://localhost:7687"
username = "neo4j"
password = "Billa@12"

today_date = date.today()


def run_query(query):
    with GraphDatabase.driver(uri, auth=(username, password)) as driver:
        # Start a session
        with driver.session() as session:
            a = session.run(query)
            print("Query executed")


def fetch_query1(query):
    with GraphDatabase.driver(uri, auth=(username, password)) as driver:
        # Start a session
        with driver.session() as session:
            result = session.run(query)
            account_properties = dict(result.single()["account"].items())

            # Print the dictionary
            print("Query executed")

            return account_properties


def run_main_query1(query):
    with GraphDatabase.driver(uri, auth=(username, password)) as driver:
        # Start a session
        with driver.session() as session:
            result = session.run(query)

            # Convert result to a list of dictionaries
            data = [record.data() for record in result]
            print("Query executed")
            # df = pd.DataFrame(data)
            # print(df)