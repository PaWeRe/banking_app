from enum import Enum
from datetime import datetime

# class TransactionType(Enum):
#     ACCOUNT_CREATION = 0
#     DEPOSIT = 1
#     TRANSFER = 2

# class Transaction:
#     def __init__(self, type, time, recipient, sender):
#         # public members for Account class to access and set
#         self.type = type
#         self.time = time
#         self.recipient = recipient
#         self.sender = sender
    
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


def main():
    account1 = Account(1,10)
    account2 = Account(2,5)
    account1.transfer(4, account2)
    account2.transfer(4, 'human')
    print(account1.get_balance())

if __name__=="__main__":
    main()


