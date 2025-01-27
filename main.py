import mysql.connector
import sys


class ATMMachine:
    def __init__(self, pin):
        self.pin = pin
        try:
            self.db = mysql.connector.connect(
                host="sundram0py.mysql.pythonanywhere-services.com",  # Update with your PythonAnywhere hostname
                user="sundram0py",  # Your PythonAnywhere username
                password="Mysql@123",  # MySQL database password
                database="sundram0py$atm_db"  # Format: username$databasename
            )
            self.cursor = self.db.cursor()
            print("Database connected successfully!")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            sys.exit()

    def authenticate_user(self):
        query = "SELECT * FROM users WHERE pin = %s"
        self.cursor.execute(query, (self.pin,))
        result = self.cursor.fetchone()
        if result:
            self.user_id = result[0]
            self.name = result[1]
            self.balance = result[3]
            print(f"Welcome, {self.name}!")
            return True
        else:
            print("Invalid PIN. Please try again.")
            return False

    def check_balance(self):
        print(f"Your current balance is: ${self.balance}")

    def withdraw(self, amount):
        if amount > self.balance:
            print("Insufficient funds.")
        else:
            self.balance -= amount
            self.update_balance()
            print(f"Withdrawal of ${amount} successful. New balance: ${self.balance}")

    def deposit(self, amount):
        self.balance += amount
        self.update_balance()
        print(f"Deposit of ${amount} successful. New balance: ${self.balance}")

    def update_balance(self):
        query = "UPDATE users SET balance = %s WHERE id = %s"
        self.cursor.execute(query, (self.balance, self.user_id))
        self.db.commit()

    def main_menu(self):
        while True:
            print("\n--- ATM Main Menu ---")
            print("1. Check Balance")
            print("2. Withdraw")
            print("3. Deposit")
            print("4. Exit")
            choice = input("Enter your choice: ")

            if choice == "1":
                self.check_balance()
            elif choice == "2":
                amount = float(input("Enter amount to withdraw: "))
                self.withdraw(amount)
            elif choice == "3":
                amount = float(input("Enter amount to deposit: "))
                self.deposit(amount)
            elif choice == "4":
                print("Thank you for using the ATM. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")


if __name__ == "__main__":
    pin = input("Enter your 4-digit PIN: ")
    atm = ATMMachine(pin)
    if atm.authenticate_user():
        atm.main_menu()
