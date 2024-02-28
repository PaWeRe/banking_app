from enum import Enum
from datetime import datetime

class ScheduledTransactionStatus(Enum):
    PENDING = 1
    EXECUTED = 2
    CANCELLED = 3

class TransactionType(Enum):
    DEPOSIT = 1
    WITHDRAWAL = 2
    SCHEDULED_TRANSFER = 3 
    EXECUTED_TRANSFER = 4
    CANCELLED_TRANSFER = 5

class Transaction:
    def __init__(self, id, account_id, transaction_type, amount, time, **kwargs):
        self.id = id
        self.account_id = account_id
        self.type = transaction_type
        self.amount = amount
        self.timestamp = time
        for key, value in kwargs.items():
            setattr(self, key, value)

class Deposit(Transaction):
    def __init__(self, id, account_id, amount, time):
        super().__init__(id, account_id, TransactionType.DEPOSIT, amount, time)

class Withdrawal(Transaction):
    def __init__(self, id, account_id, amount, time):
        super().__init__(id, account_id, TransactionType.WITHDRAWAL, amount, time)

class ScheduledTransfer(Transaction):
    def __init__(self, id, account_id, amount, time, recipient, status):
        super().__init__(id, account_id, TransactionType.SCHEDULED_TRANSFER, amount, time, recipient=recipient, status=status)

class ExecutedTransfer(Transaction):
    def __init__(self, id, account_id, amount, time, scheduled_transaction_id):
        super().__init__(id, account_id, TransactionType.EXECUTED_TRANSFER, amount, time, scheduled_transaction_id=scheduled_transaction_id)

class CancelledTransfer(Transaction):
    def __init__(self, id, account_id, amount, time, scheduled_transaction_id):
        super().__init__(id, account_id, TransactionType.CANCELLED_TRANSFER, amount, time, scheduled_transaction_id=scheduled_transaction_id)

class BankAccount:
    def __init__(self, account_id, holder_name, initial_balance=None, initial_transactions=None):
        self._id = account_id
        self._account_name = holder_name
        self._balance = initial_balance if initial_balance is not None else 0
        self._transactions = initial_transactions if initial_transactions is not None else {}

    def _record_transaction(self, transaction):
        self._transactions[transaction.id] = transaction
    
    def get_id(self):
        return self._id
    
    def get_account_name(self):
        return self._account_name
    
    def get_balance(self):
        return self._balance

    def get_transactions(self):
        return list(self._transactions.values())
    
    def deposit(self, amount):
        self._balance += amount
        transaction = Deposit(len(self._transactions)+1, self._id, amount, datetime.now())
        self._record_transaction(transaction)

    def withdraw(self, amount):
        if amount > self._balance:
            raise ValueError(f'Amount {amount} to be withdrawn exceeds balance {self._balance}.')
        else:
            self._balance -= amount
            transaction = Withdrawal(len(self._transactions)+1, self._id, amount, datetime.now())
            self._record_transaction(transaction)

    def schedule_transfer(self, amount, time, recipient):
        if type(recipient) is not BankAccount:
            raise TypeError('Recipient is not valid BankAccount.')
        elif type(time) is not datetime:
            raise TypeError(f'{time} is not of type datetime.')
        elif amount > self._balance:
            raise ValueError('Not sufficient balance for amount to be transferred.')
        else:
            transaction = ScheduledTransfer(len(self._transactions)+1, self._id, amount, time, recipient, ScheduledTransactionStatus.PENDING)
            self._record_transaction(transaction)

    #TODO: creates three transactions for one transfer, a bit redundant
    def execute_transfer(self, transaction_id):
        if type(self._transactions[transaction_id]) is not ScheduledTransfer:
            raise TypeError('Not ScheduledTransfer transaction.')
        self.withdraw(self._transactions[transaction_id].amount)
        self._transactions[transaction_id].recipient.deposit(self._transactions[transaction_id].amount)
        self._transactions[transaction_id].status = ScheduledTransactionStatus.EXECUTED
        transaction_new = ExecutedTransfer(len(self._transactions)+1, self._id, self._transactions[transaction_id].amount, datetime.now(), self._transactions[transaction_id].id)
        self._record_transaction(transaction_new)

    def cancel_transfer(self, transaction_id):
        self._transactions[transaction_id].status = ScheduledTransactionStatus.CANCELLED
        new_transaction = CancelledTransfer(len(self._transactions)+1, self._id, self._transactions[transaction_id].amount, datetime.now(), self._transactions[transaction_id].id)
        self._record_transaction(new_transaction)

    #TODO: could be generalized to take list of accounts as input
    def merge_accounts(self, other_account):
        pass

def sort_top_k(list_accounts, k=5):
    accounts = {}
    for account in list_accounts:
        if type(account) is not BankAccount:
            raise TypeError(f'{account} is not of type BankAccount!')
        amount = 0
        for transaction in account.get_transactions():
            if transaction.type == TransactionType.WITHDRAWAL:
                amount += transaction.amount
                accounts[account.get_id()] = amount
    sorted_accounts = sorted(accounts.items(), key=lambda x:x[1], reverse=True)[:k]
    return sorted_accounts

#TODO: transaction histories are separate in that every transactions contains the account_id it was made on, tbc if there other ways to maintain separate trans hists
def merge_accounts(list_accounts, new_account_id, new_account_name):
    counter = 0
    initial_balance = 0
    dict_init_trans = {}
    initial_transactions = []
    for account in list_accounts:
        initial_balance += account.get_balance()
        initial_transactions.extend(account.get_transactions())
    initial_transactions.sort(key=lambda x:x.timestamp, reverse=True)
    #TODO: maybe way without needing to add extra loop for building merge dict (do not convert dict into list when returning it or add other function)
    for transaction in initial_transactions:
        counter += 1
        dict_init_trans[counter] = transaction
    return BankAccount(new_account_id, new_account_name, initial_balance, dict_init_trans)

def main():
    a1 = BankAccount(1, 'Max Musterman')
    a2 = BankAccount(2, 'Lisa Maier')
    a1.deposit(150)
    a1.withdraw(20)
    a2.deposit(200)
    a2.withdraw(50)
    k = sort_top_k([a1, a2])
    a1.schedule_transfer(5, datetime.now(), a2)
    a1.schedule_transfer(3, datetime.now(), a2)
    a1.execute_transfer(3)
    a1.cancel_transfer(4)
    a3 = merge_accounts([a1, a2], 3, 'Werner Walter')

if __name__== "__main__":
    main()