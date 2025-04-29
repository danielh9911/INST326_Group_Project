"""
Structure

finance-tracker/
├── README.md
├── requirements.txt
├── finance_tracker/
│   ├── __init__.py
│   ├── cli.py          - Command-line interface
│   ├── core.py         - Business logic
│   ├── models.py       - Data models (Transaction, Budget, etc.)
│   ├── storage.py      - CSV persistence
│   ├── utils.py        - Helper functions
│   └── exceptions.py   - Custom exceptions
├── tests/
│   ├── __init__.py
│   ├── test_core.py
│   ├── test_storage.py
│   └── test_cli.py
└── data/               - Default location for CSV files
    └── transactions.csv
  __
"""

import sys
import argparse

class financeTracker:
    
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

def main():
    pass

def parse_args(arglist):

    """ 
    Parse command-line arguments.

    Args:
        arglist (list of str): list of arguments from the command line.

    Returns:
        namespace: the parsed arguments, as returned by
                   argparse.ArgumentParser.parse_args().
    """
    
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="file of financial information")
    return parser.parse_args(arglist)

if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    main(args.path)