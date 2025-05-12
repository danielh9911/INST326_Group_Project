from datetime import datetime
from core import FinanceTracker
from models import Transaction, TransactionType
from storage import CSVHandler

DATA_FILE = 'data/transactions.csv'

tracker = FinanceTracker()
storage = CSVHandler(DATA_FILE)

# Load existing transactions
tracker.transactions = storage.load()

print('Hello, welcome to your finance tracker')

while True:
    appinput = input("""
What would you like to do today?
    a) Add transaction
    b) View monthly report
    c) Exit
> """).strip().lower()

    if appinput == 'a':
        try:
            amount = float(input("Enter amount: "))
            category = input("Enter category: ")
            description = input("Enter description (optional): ")
            t_type_input = input("Enter type ('income' or 'expense'): ").strip().lower()
            if t_type_input not in ['income', 'expense']:
                print("Invalid type. Must be 'income' or 'expense'.")
                continue
            t_type = TransactionType.INCOME if t_type_input == 'income' else TransactionType.EXPENSE

            transaction = Transaction(
                date=datetime.today(),
                amount=amount,
                category=category,
                description=description,
                type=t_type
            )

            tracker.add_transaction(transaction)
            storage.save(tracker.transactions)
            print("Transaction added successfully.")

        except ValueError:
            print("Invalid input. Please try again.")

    elif appinput == 'b':
        try:
            month = int(input("Enter month (1-12): "))
            year = int(input("Enter year (e.g. 2025): "))
            summary = tracker.get_monthly_summary(month, year)
            print(f"Report for {month}/{year}")
            print(f"Income: ${summary['income']:.2f}")
            print(f"Expenses: ${summary['expenses']:.2f}")
            print(f"Savings: ${summary['savings']:.2f}")
        except ValueError:
            print("Invalid input. Please enter numeric values for month and year.")

    elif appinput == 'c':
        print("Goodbye!")
        break

    else:
        print("Invalid choice. Please enter a, b, or c.")