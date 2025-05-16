from datetime import datetime
from calendar import monthrange
from models import Transaction, TransactionType
from storage import RecurringCSVHandler

RECURRING_FILE = 'data/recurring.csv'

class FinanceTracker:
    def __init__(self):
        self.transactions = []
        self.recurring_handler = RecurringCSVHandler(RECURRING_FILE)

    def add_transaction(self, transaction: Transaction):
        """Adds a single transaction to the tracker

        Args:
            transaction (Class): The transaction to add
        """

        self.transactions.append(transaction)

    def get_monthly_summary(self, month, year):
        """Summarizes monthly income and expenses for a given month and year
        
        Args: 
            month (int): A number 1-12 to represent each month
            year (int): A number in four digit format to represent the year
        
        Returns:
            dict: Dictionary with keys 'income', 'expenses', and 'savings'
        """

        income = 0
        expenses = 0

        for transaction in self.transactions:
            if transaction.date.month == month and transaction.date.year == year:
                if transaction.type == TransactionType.INCOME:
                    income += transaction.amount
                else:
                    expenses += transaction.amount

        return {'income': income, 'expenses': expenses, 'savings': income - expenses}

    def add_recurring_payment(self, day, amount, category, description = ''):
        """Adds a recurring payment

        Args:
            day (int): A number 1-31 to represent a day of the month
            amount (int or float): Payment amount
            category (str): Category of the recurring payment
            description (str, optional): Description of recurring payment
        """

        entries = self.recurring_handler.load()
        entries.append({
            'day': str(day),
            'amount': str(amount),
            'category': category,
            'description': description
        })
        self.recurring_handler.save(entries)

    def remove_recurring_payment(self, index):
        """Removes a recurring payment from the list
        
        Args:
            index (int): A number that represents which index of recurring payment you wish to remove
        """
        entries = self.recurring_handler.load()
        if 0 <= index < len(entries):
            entries.pop(index)
            self.recurring_handler.save(entries)

    def apply_recurring_payments(self):
        """Applies recurring payments for the current month to the transaction list"""
        
        today = datetime.today()
        current_year = today.year
        current_month = today.month
        last_day = monthrange(current_year, current_month)[1]

        entries = self.recurring_handler.load()
        for entry in entries:
            try:
                day = min(int(entry['day']), last_day)
                date = datetime(current_year, current_month, day)
                amount = float(entry['amount'])
                category = entry['category']
                description = entry.get('description', '')

                transaction = Transaction(
                    date = date,
                    amount = amount,
                    category = category,
                    description = description,
                    type = TransactionType.EXPENSE
                )
                self.transactions.append(transaction)
            except Exception as e:
                print(f'Error applying recurring entry: {entry} — {e}')