import json

class BankAccount:
    def __init__(self, account_number, pin, balance=0):
        self.account_number = account_number
        self.pin = pin
        self.balance = balance
    
    def check_balance(self):
        return self.balance
    
    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            return f"Deposit successful! New balance: ${self.balance}"
        return "Invalid deposit amount."
    
    def withdraw(self, amount):
        if amount > self.balance:
            return "Insufficient funds."
        if amount <= 0:
            return "Invalid withdrawal amount."
        self.balance -= amount
        return f"Withdrawal successful! New balance: ${self.balance}"


class ATM:
    def __init__(self):
        self.accounts = self.load_accounts()
    
    def load_accounts(self):
        try:
            with open('accounts.json', 'r') as file:
                data = json.load(file)
                return {acc_num: BankAccount(acc_num, acc['pin'], acc['balance']) for acc_num, acc in data.items()}
        except (FileNotFoundError, json.JSONDecodeError):
            return {
                "1234": BankAccount("1234", "4321", 1000),
                "5678": BankAccount("5678", "8765", 2000)
            }
    
    def save_accounts(self):
        data = {acc_num: {"pin": acc.pin, "balance": acc.balance} for acc_num, acc in self.accounts.items()}
        with open('accounts.json', 'w') as file:
            json.dump(data, file)
    
    def authenticate(self, account_number, pin):
        account = self.accounts.get(account_number)
        if account and account.pin == pin:
            return account
        return None
    
    def run(self):
        print("Welcome to the ATM!")
        account_number = input("Enter your account number: ")
        pin = input("Enter your PIN: ")
        account = self.authenticate(account_number, pin)
        
        if account:
            print("Authentication successful!")
            while True:
                print("\n1. Check Balance\n2. Deposit\n3. Withdraw\n4. Exit")
                choice = input("Choose an option: ")
                
                if choice == '1':
                    print(f"Your balance is: ${account.check_balance()}")
                elif choice == '2':
                    amount = float(input("Enter deposit amount: "))
                    print(account.deposit(amount))
                    self.save_accounts()
                elif choice == '3':
                    amount = float(input("Enter withdrawal amount: "))
                    print(account.withdraw(amount))
                    self.save_accounts()
                elif choice == '4':
                    print("Thank you for using the ATM. Goodbye!")
                    self.save_accounts()
                    break
                else:
                    print("Invalid option. Please try again.")
        else:
            print("Authentication failed. Invalid account number or PIN.")



if __name__ == '__main__':
    atm = ATM()
    atm.run()
