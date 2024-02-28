from enum import Enum

class TransactionType(Enum):
    DEPOSIT = 1
    WITHDRAWAL = 2

class Transaction:
    def __init__(self, id, transaction_type, amount):
        self.id = id
        self.type = transaction_type
        self.amount = amount

class BankAccount:
    def __init__(self, account_id, holder_name):
        self._id = account_id
        self._account_name = holder_name
        self._balance = 0 # default amount is 0
        self._transactions = [] # define list for ease of use

    def _record_transaction(self, transaction):
        self._transactions.append(transaction)
    
    def get_id(self):
        return self._id
    
    def get_account_name(self):
        return self._account_name
    
    def get_balance(self):
        return self._balance

    def get_transactions(self):
        return self._transactions

    def deposit(self, amount):
        self._balance += amount
        transaction = Transaction(len(self._transactions)+1, TransactionType.DEPOSIT, amount)
        self._record_transaction(transaction)

    def withdraw(self, amount):
        if amount > self._balance:
            raise ValueError(f'Amount {amount} to be withdrawn exceeds balance {self._balance}.')
        else:
            self._balance -= amount
            transaction = Transaction(len(self._transactions)+1, TransactionType.WITHDRAWAL, amount)
            self._record_transaction(transaction)

    def transfer(self, amount, recipient):
        if type(recipient) is not BankAccount:
            raise TypeError('Recipient is not valid BankAccount.')
        else:
            self.withdraw(amount)
            recipient.deposit(amount)

def sort_top_k(list_accounts, k=5):
    accounts = {}
    for account in list_accounts:
        if type(account) is not BankAccount:
            raise TypeError('{account} is not of type BankAccount!')
        amount = 0
        for transaction in account.get_transactions():
            if transaction.type == TransactionType.WITHDRAWAL:
                amount += transaction.amount
                accounts[account.get_id()] = amount
    sorted_accounts = sorted(accounts.items(), key=lambda x:x[1], reverse=True)[:k]
    return sorted_accounts

def main():
    a1 = BankAccount(1, 'Max Musterman')
    a2 = BankAccount(2, 'Lisa Maier')
    a1.deposit(150)
    a2.deposit(200)
    a1.transfer(100, a2)
    a2.transfer(20, a1)
    a2.transfer(20, a1)
    a2.transfer(20, a1)
    sort_top_k([a1, a2])
    # print(a1.get_transactions())

if __name__== "__main__":
    main()

#TODO: in current transaction history recipient and sender are not included