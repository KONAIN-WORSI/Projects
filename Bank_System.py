class bank_system():
    def __init__(self, account_name, balance=0):
        self.balance = balance
        self.account_name = account_name
        self.account_id = 12345

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            return f"{amount} Successfully deposited in the account" 
        return "Invalid amount"

    def withdraw(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            return f"Successfully withdrawn {amount}"
        return "You dont have enough balance!"
    
    def show_balance(self):
        return self.balance
    
    
if __name__ == "__main__":
    bank = bank_system("John Doe", 1000)

    while True:
        cmd = input("\nChoose action (deposit, withdraw, show, exit): ").strip().lower()
        if cmd == "deposit":
            try:
                amt = float(input("Amount to deposit: "))
            except ValueError:
                print("Invalid amount")
                continue
            print(bank.deposit(amt))
        elif cmd == "withdraw":
            try:
                amt = float(input("Amount to withdraw: "))
            except ValueError:
                print("Invalid amount")
                continue
            print(bank.withdraw(amt))
        elif cmd == "show":
            print(f"Current Balance: {bank.show_balance():.2f}")
        elif cmd in ("exit", "quit"):
            print("Goodbye.")
            break
        else:
            print("Unknown command")

    
        
        