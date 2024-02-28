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
        self._transactions = {}

    def get_balance(self):
        return self._balance
    
    def get_anumber(self):
        return self._anumber
    
    def get_transactions(self):
        return self._transactions

    def instant_deposit(self, amount, sender):
        #TODO: should be indpendent of transfer and also include error msg for balance
        if type(sender) is not Account:
            raise ValueError('Only full accounts can deposit money.')
        self._balance += amount
        self._transactions.append(('insant_deposit', amount, sender, datetime.now()))

    def instant_transfer(self, amount, recipient):
        #TODO: shoudld be independent of deposit?
        if type(recipient) is not Account:
            raise TypeError('Only full accounts can receive money.')
        elif amount > self._balance:
            raise ValueError('Amount to be transferred exeeds account balance.')
        else:
            recipient.instant_deposit(amount, self._anumber)
            self._transactions.append(('instant_transfer', amount, recipient.get_anumber(), datetime.now()))

    def schedule_transfer(self, amount, recipient, time):
        if type(recipient) is not Account:
            raise TypeError('Only full accounts can receive money.')
        elif amount > self._balance:
            raise ValueError('Amount to be transferred exeeds account balance.')
        elif time <= datetime.now():
            raise ValueError('Scheduled time: {} is in the present/past - has to be in the future!'.format(time))
        else:
            # extra function will be written to go through all scheduled transfers and execute them if its time
            self._transactions.append(('scheduled_transfer', amount, recipient.get_anumber(), time))

    def execute_scheduled_transfer(self, account):
        if 'scheduled_transfer' not in account.get_transactions()[:][0]:
            raise ValueError('Account has no scheduled transfers!')
        else:
            #TODO: dont forget to transform scheduled_transfer into instant to mark as done!

    def cancel_scheduled_transfer(self, account, transaction_id):
        #TODO: include transaction_id in list tuples to better access transactions

def top_k_outgoing(accounts, k=2):
    ''' return top k accounts in terms of outgoing money
        outgoing money := sum of amounts of transfers per account
    '''
     #TODO: potential improvement - maybe double for loop not necessary?
    outgoing_dict = {}
    for account in accounts:
        outgoing_money = 0
        for transaction in account.get_transactions():
            if transaction[0] == 'instant_transfer':
                outgoing_money += transaction[1]
        outgoing_dict.update({account: outgoing_money})
    top_k = sorted(outgoing_dict.items(), key=lambda x:x[1], reverse=True)[:k]
    return top_k


def main():
    account1 = Account(1,100)
    account2 = Account(2,100)
    account3 = Account(2,100)
    account3.instant_transfer(4, account2)
    account1.instant_transfer(4, account2)
    account1.instant_deposit(4, account2)
    account1.instant_transfer(4, account2)
    account1.instant_transfer(4, account2)
    account1.instant_transfer(4, account2)
    account2.instant_transfer(4, account1)
    account2.instant_transfer(4, account1)
    account2.instant_transfer(4, account1)
    list_top_k = top_k_outgoing([account1,account2])
    print(list_top_k)

if __name__=="__main__":
    main()


