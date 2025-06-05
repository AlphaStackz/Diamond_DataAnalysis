class BankAccount:
    def __init__(self, account_holder, balance=0):
        self.account_holder = account_holder
        self.balance = balance

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            print(f"{amount} SEK deposited. New balance: {self.balance} SEK")
        else:
            print("Amount must be positive.")

    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            print(f"{amount} SEK withdrawn. New balance: {self.balance} SEK")
        else:
            print("Too low balance")

my_account = BankAccount("Nour", 500)
print(my_account.account_holder)
print(my_account.balance)
my_account.deposit(100)
my_account.withdraw(100)
