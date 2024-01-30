from connection import *
def query1():
    a = '''

            // Main Query 1

            WITH date('2023-12-14') as endDate
            WITH endDate, endDate-duration({days:90}) as startDate
            MATCH p=(ctr:DepositAccount)-[:WITHDRAWALS]->(wt:Wire:Transaction)-[:RECEIVES_WIRE]
            ->(ext:ExternalAccount)-[:IBAN_ROUTING]->(iban:IBAN_Code)<-[:HAS_IBAN_CODE]-(fi:FinancialInstitution)-[:OPERATES_IN]->(cty:Country)
            WHERE wt.date >= startDate
                AND wt.date <= endDate
                AND cty.risk_Score > 0.6


            // Step 2 - find the accounts that had cash deposits that transferred to the account that did the wire transfer
            WITH ctr, wt, ext, iban, fi, cty

            MATCH g=(cu:AccountHolder)-[:HAS_ACCOUNT]->(src:DepositAccount)-[:WITHDRAWALS]->(srcTxn:ACH:Transaction)-[:INTERNAL_XFER]->(ctrTxn:ACH:Transaction)-[:DEPOSITS]->(ctr)<-[:HAS_ACCOUNT]-(cu2),
                (ctr)-[:WITHDRAWALS]-(wt)-[:RECEIVES_WIRE]-(ext)-[:IBAN_ROUTING]->(iban)<-[:HAS_IBAN_CODE]-(fi)-[:OPERATES_IN]->(cty), 
                (extName:External:AccountHolder)-[:HAS_ACCOUNT]->(ext)

            WHERE srcTxn.date <= wt.date
                AND duration.inDays(srcTxn.date, wt.date).days < 30

            RETURN cu.accountName, src.accountNumber, srcTxn.amount, srcTxn.transactionDate, ctr.accountNumber, cu2.accountName, wt.amount, wt.transactionDate,
            ext.accountNumber, extName.accountName, fi.bankName, cty.countryName 
            ORDER BY ctr.accountNumber, src.accountNumber;
'''
    return a


def query2():
    b='''
    //  main query 2
 WITH date('2023-12-10') as curDate
 WITH curDate, curDate-duration({days:35}) as curDate35
 MATCH (cu:AccountHolder)-[:HAS_ACCOUNT]->(da:DepositAccount)<-[:DEPOSITS]-(txn:Cash:Transaction)
 WHERE txn.date >= curDate35
 AND txn.date <= curDate 
WITH da.accountID as accountID, 
min(txn.date) as StartDate,
 max(txn.date) as EndDate, 
duration.inDays(min(txn.date),max(txn.date)).days as NumDays,
 count(txn.amount) as NumDeposits, 
sum(txn.amount) as TotalDeposits
 WHERE TotalDeposits > 8500
 WITH collect({accountID: accountID, startDate: StartDate, endDate: EndDate, numDays: NumDays,
 numDeposits: NumDeposits, totalDeposits: TotalDeposits}) as possAggregators


 // Step 2...now find all the rapid withdrawals of high percentage of deposits
 UNWIND possAggregators as curAgg
 MATCH (da:DepositAccount)-[:WITHDRAWALS]->(txn:Cash:Transaction)
 WHERE da.accountID=curAgg.accountID
 AND txn.date >= curAgg.startDate
 AND txn.date <= curAgg.endDate+duration({days:10})
 WITH da.accountID as AccountID,
 curAgg.startDate as StartDate,
 max(txn.date) as EndDate,
 duration.inDays(curAgg.startDate,max(txn.date)).days as NumDays,
 curAgg.numDeposits as NumDeposits,
 curAgg.totalDeposits as TotalDeposits, 
count(txn.amount) as NumWithdrawals,
 sum(txn.amount) as TotalWithdrawals,
 (100*abs(sum(txn.amount)))/curAgg.totalDeposits as pctWithdrawal
 WHERE pctWithdrawal > 75
 // Step 3 - Now add in the customer info
 MATCH (cu:AccountHolder)-[:HAS_ACCOUNT]->(da:DepositAccount)
 WHERE da.accountID=AccountID
 RETURN cu.accountName, da.accountNumber, StartDate, EndDate, 
NumDeposits, TotalDeposits, NumWithdrawals, TotalWithdrawals, pctWithdrawal
 ORDER BY pctWithdrawal DESC, TotalDeposits DESC LIMIT 100
// return  pctWithdrawal
    '''
    return b