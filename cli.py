"""Finance Tracker CLI

Allows users to input through the terminal to interact with our program. Our program allows users to:

- Add one-time payments
- View monthly summaries
- Manage recurring payments
- Apply recurring payments each month
- View recurring payments
"""

from datetime import datetime
from core import FinanceTracker
from models import Transaction, TransactionType
from storage import CSVHandler, RecurringCSVHandler

DATA_FILE = 'data/transactions.csv'
RECURRING_FILE = 'data/recurring.csv'

tracker = FinanceTracker()
transaction_storage = CSVHandler(DATA_FILE)
recurring_storage = RecurringCSVHandler(RECURRING_FILE)

# Load transactions
tracker.transactions = transaction_storage.load()

print("Hello, welcome to your finance tracker.")

while True:
    appinput = input("""
What would you like to do today?
    a) Add transaction
    b) View monthly report
    c) Add recurring payment
    d) View recurring payments
    e) Apply recurring payments for this month
    f) Remove recurring payment
    g) Exit
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
            transaction_storage.save(tracker.transactions)
            print("Transaction added successfully.")

        except ValueError:
            print("Invalid input. Please try again.")

    elif appinput == 'b':
        try:
            month = int(input("Enter month (1-12): "))
            year = int(input("Enter year (e.g. 2025): "))
            summary = tracker.get_monthly_summary(month, year)
            print(f"\nReport for {month}/{year}")
            print(f"Income:  ${summary['income']:.2f}")
            print(f"Expenses: ${summary['expenses']:.2f}")
            print(f"Savings:  ${summary['savings']:.2f}")
        except ValueError:
            print("Invalid input. Please enter numeric values for month and year.")

    elif appinput == 'c':
        try:
            day = int(input("Enter day of the month (1–31): "))
            amount = float(input("Enter recurring amount: "))
            category = input("Enter category: ")
            description = input("Enter description (optional): ")

            tracker.add_recurring_payment(day, amount, category, description)
            print("Recurring payment added.")
        except ValueError:
            print("Invalid input. Please try again.")

    elif appinput == 'd':
        recurring = recurring_storage.load()
        if not recurring:
            print("No recurring payments set.")
        else:
            print("\nRecurring Payments:")
            for i, entry in enumerate(recurring):
                print(f"{i}) Day {entry['day']}: ${entry['amount']} - {entry['category']} ({entry.get('description', '')})")

    elif appinput == 'e':
        tracker.apply_recurring_payments()
        tracker.transactions = transaction_storage.load()
        print("Recurring payments applied for the current month.")

    elif appinput == 'f':
        recurring = recurring_storage.load()
        if not recurring:
            print("No recurring payments to remove.")
            continue

        for i, entry in enumerate(recurring):
            print(f"{i}) Day {entry['day']}: ${entry['amount']} - {entry['category']} ({entry.get('description', '')})")

        try:
            idx = int(input("Enter the index of the recurring payment to remove: "))
            tracker.remove_recurring_payment(idx)
            print("Recurring payment removed.")
        except (ValueError, IndexError):
            print("Invalid index. No recurring payment removed.")

    elif appinput == 'g':
        print("Goodbye!")
        break

    else:
        print("Invalid choice. Please enter a–g.")