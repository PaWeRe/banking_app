from enum import Enum
from datetime import datetime
    
class Account:
    ''' defines a bank account with deposit and transfer functions,
        and getter functions for private attributes
    '''
    #TODO: potential improvement - maybe create dedicated class for Transactions or use dict?
    def __init__(self, account_number, balance):
        # per default set members protected to prevent public 
        # mod but enable access for children
        self._anumber = account_number
        self._balance = balance
        self._transactions = []

    def get_balance(self):
        return self._balance
    
    def get_anumber(self):
        return self._anumber
    
    def get_transactions(self):
        return self._transactions

    def deposit(self, amount, sender_id):
        #TODO: should amount be subtracted from sender_id?
        self._balance += amount
        self._transactions.append(('deposit', amount, sender_id))

    def transfer(self, amount, recipient):
        if type(recipient) is not Account:
            raise TypeError('Only full accounts can receive money.')
        elif amount > self._balance:
            raise ValueError('Amount to be transferred exeeds account balance.')
        else:
            self._balance -= amount
            recipient.deposit(amount, self._anumber)
            self._transactions.append(('transfer', amount, recipient.get_anumber()))

def top_k_outgoing(accounts, k=2):
    ''' return top k accounts in terms of outgoing money
        outgoing money := sum of amounts of transfers per account
    '''
    #TODO: potential improvement - maybe double for loop not necessary?
    outgoing_dict = {}
    for account in accounts:
        outgoing_money = 0
        for transaction in account.get_transactions():
            if transaction[0] == 'transfer':
                outgoing_money += transaction[1]
        outgoing_dict.update({account: outgoing_money})
    top_k = sorted(outgoing_dict.items(), key=lambda x:x[1], reverse=True)[:k]
    return top_k


def main():
    account1 = Account(1,100)
    account2 = Account(2,100)
    account3 = Account(2,100)
    account3.transfer(4, account2)
    account1.transfer(4, account2)
    account1.transfer(4, account2)
    account1.transfer(4, account2)
    account1.transfer(4, account2)
    account2.transfer(4, account1)
    account2.transfer(4, account1)
    account2.transfer(4, account1)
    list_top_k = top_k_outgoing([account1,account2])
    print(list_top_k)

if __name__=="__main__":
    main()


