def create_customer(name, accountNumber, accountID):
    return f"CREATE (:AccountHolder {{accountName: '{name}'}})-[:HAS_ACCOUNT]->(:DepositAccount {{accountID: {accountID}, accountNumber:{accountNumber}}});"

def create_transaction(amount, date, transaction_id):
    return f"CREATE (:Transaction {{amount: {amount}, date: '{date}', transactionID : '{transaction_id}'}})" 
           
def create_extrernal(accountNumber, iban_code, financial_inst_id, country_name, risk_score, name, accountID):
    return f"CREATE (ext:ExternalAccount {{accountID: {accountID}, accountNumber:{accountNumber}}}), (iban:IBAN_Code {{iban: '{iban_code}'}}),(fi:FinancialInstitution {{id: {financial_inst_id}}}), (cty:Country {{countryName: '{country_name}', risk_Score:{risk_score}}}),(extName:External:AccountHolder {{accountName:'{name}'}}) CREATE(extName)-[:HAS_ACCOUNT]->(ext)-[:IBAN_ROUTING]->(iban)<-[:HAS_IBAN_CODE]-(fi)-[:OPERATES_IN]->(cty)"


