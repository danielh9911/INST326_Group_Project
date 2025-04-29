from typing import List
from datetime import datetime
from .models import Transaction

class FinanceTracker:
    
    def __init__(self):
        self.transactions = []                    # Initializes empty list if none provided
    def add_transaction(self, transaction):
        """adds transactions to history"""
        self.transactions.append(transaction)      # Stores in memory
    
    def get_monthly_summary(self, month, year):
        """calculates the monthly totals"""
        income = 0         # Initializes counters
        expenses = 0       # Initializes counters
        for t in self.transactions:              # Loops through all transactions
            if t.date.month == month and t.date.year == year:   # Filters by date
                if t.type == 'income':
                    income += t.amount
                else:
                    expenses += t.amount
        return {'income': income, 'expenses': expenses, 'savings': income - expenses}    # Returns formatted dict