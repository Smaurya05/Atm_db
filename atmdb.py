import mysql.connector

class ATMMachine:
    def __init__(self, pin):
        self.pin = pin
        self.user_id = None
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",  # Replace with your MySQL username
            password="Sundram@12345",  # Replace with your MySQL password
            database="atm_db"
        )
        self.cursor = self.db.cursor()
        self.transaction_history = []

    def setup_database(self):
        self.cursor.execute("CREATE DATABASE IF NOT EXISTS ATM_DB")
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                pin VARCHAR(10) NOT NULL,
                balance DOUBLE DEFAULT 0
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                transaction_type VARCHAR(50),
                amount DOUBLE,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        self.db.commit()

    def load_user(self):
        self.cursor.execute("SELECT id, balance FROM users WHERE pin = %s", (self.pin,))
        user = self.cursor.fetchone()
        if user:
            self.user_id, self.balance = user
        else:
            self.cursor.execute("INSERT INTO users (pin) VALUES (%s)", (self.pin,))
            self.db.commit()
            self.user_id = self.cursor.lastrowid
            self.balance = 0

    def check_pin(self):
        entered_pin = input("Enter your PIN: ")
        return entered_pin == self.pin

    def account_balance_inquiry(self):
        if self.check_pin():
            print(f"Your current balance is: ${self.balance:.2f}")
            self.transaction_history.append("Balance inquiry")
        else:
            print("PIN verification failed. Cannot perform balance inquiry.")

    def cash_withdrawal(self):
        if self.check_pin():
            amount = float(input("Enter amount to withdraw: $"))
            if amount > self.balance:
                print("Insufficient balance.")
            else:
                self.balance -= amount
                self.cursor.execute("UPDATE users SET balance = %s WHERE id = %s", (self.balance, self.user_id))
                self.cursor.execute("INSERT INTO transactions (user_id, transaction_type, amount) VALUES (%s, %s, %s)", 
                                    (self.user_id, "Withdraw", amount))
                self.db.commit()
                print(f"${amount:.2f} withdrawn successfully.")
        else:
            print("PIN verification failed. Cannot perform cash withdrawal.")

    def cash_deposit(self):
        if self.check_pin():
            amount = float(input("Enter amount to deposit: $"))
            self.balance += amount
            self.cursor.execute("UPDATE users SET balance = %s WHERE id = %s", (self.balance, self.user_id))
            self.cursor.execute("INSERT INTO transactions (user_id, transaction_type, amount) VALUES (%s, %s, %s)", 
                                (self.user_id, "Deposit", amount))
            self.db.commit()
            print(f"${amount:.2f} deposited successfully.")
        else:
            print("PIN verification failed. Cannot perform cash deposit.")

    def change_pin(self):
        if self.check_pin():
            new_pin = input("Enter your new PIN: ")
            self.pin = new_pin
            self.cursor.execute("UPDATE users SET pin = %s WHERE id = %s", (new_pin, self.user_id))
            self.db.commit()
            self.transaction_history.append("PIN changed")
            print("PIN changed successfully.")
        else:
            print("PIN verification failed. Cannot change PIN.")

    def show_transaction_history(self):
        self.cursor.execute("SELECT transaction_type, amount FROM transactions WHERE user_id = %s", (self.user_id,))
        transactions = self.cursor.fetchall()
        print("Transaction History:")
        for transaction in transactions:
            print(f"{transaction[0]}: ${transaction[1]:.2f}")

    def start(self):
        self.setup_database()
        self.load_user()
        while True:
            print("\n1. Account Balance Inquiry")
            print("2. Cash Withdrawal")
            print("3. Cash Deposit")
            print("4. Change PIN")
            print("5. Transaction History")
            print("6. Exit")

            choice = input("Choose an option: ")

            if choice == '1':
                self.account_balance_inquiry()
            elif choice == '2':
                self.cash_withdrawal()
            elif choice == '3':
                self.cash_deposit()
            elif choice == '4':
                self.change_pin()
            elif choice == '5':
                self.show_transaction_history()
            elif choice == '6':
                print("Thank you for using the ATM. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")

# Example usage
atm = ATMMachine(pin="1234")
atm.start()
