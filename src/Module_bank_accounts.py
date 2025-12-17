class BalanceException(Exception):
    pass

class BankAccount:
    def __init__(self, initialAmount, accName):
        self.balance = initialAmount
        self.name = accName
        print(f"Account {self.name} created with balance {self.balance}")

    def getBalance(self):
        print(f"\nAccount '{self.name}' balance = ${self.balance:.2f}")

    def deposit(self, amount):
        self.balance = self.balance + amount
        print(f"\nDeposit Complete.\nAccount '{self.name}' balance = ${self.balance:.2f}")
        self.getBalance()

    def viableTransaction(self, amount):
        if self.balance >= amount:
            return
        else:
            raise BalanceException(f"\n Sorry, account '{self.name}' only has a balance of ${self.balance:.2f}")

    def withdraw(self, amount):
        try:
            self.viableTransaction(amount)
            self.balance = self.balance - amount
            print("\nWithdraw complete.")
            self.getBalance()
        except BalanceException as error:
            print(f'\nWithdraw interrupted: {error}')
            
#now also define for the transfer method for the money transfer 

    def transfer(self, amount, account):
        try:
            print('\n********\n\nBeginning transfer...\n\n')
            self.viableTransaction(amount)        # raise if not enough balance
            self.balance -= amount               # perform withdraw without calling withdraw() (avoids duplicate messages)
            account.deposit(amount)
            print('\nTransfer complete.\n\n********')
        except BalanceException as error:
            print(f'\nTransfer interrupted: {error}')
