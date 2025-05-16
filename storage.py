import csv
from pathlib import Path
from datetime import datetime
from models import Transaction, TransactionType

# Normal Payment Handler

class CSVHandler:
    def __init__(self, filepath):
        self.filepath = Path(filepath)
        self._ensure_file()

    def _ensure_file(self):
        """Checks if transactions.csv with the correct headers exists, if it doesn't, creates new CSV with headers"""

        self.filepath.parent.mkdir(parents = True, exist_ok = True)
        if not self.filepath.exists() or self.filepath.stat().st_size == 0:
            with open(self.filepath, 'w', newline = '') as f:
                writer = csv.DictWriter(f, fieldnames = ['date', 'amount', 'category', 'description', 'type'])
                writer.writeheader()

    def load(self):
        """Loads transactions from transactions.csv
        
        Returns:
            List: List of Transactions objects loaded from models.py
        """
        
        if not self.filepath.exists():
            return []

        with open(self.filepath, newline = '') as f:
            return [
                Transaction(
                    date = datetime.strptime(row['date'], '%Y-%m-%d'),
                    amount = float(row['amount']),
                    category = row['category'],
                    description = row.get('description', ''),
                    type = TransactionType[row['type'].upper()]
                    )

                for row in csv.DictReader(f)
            ]

    def save(self, transactions):
        """Saves list of Transaction objects to transactions.csv

        Args:
            transactions (list): The list of transactions to write to the file
        """
        with open(self.filepath, 'w', newline = '') as f:
            writer = csv.DictWriter(f, fieldnames = ['date', 'amount', 'category', 'description', 'type'])
            writer.writeheader()
            for t in transactions:
                writer.writerow({
                    'date': t.date.strftime('%Y-%m-%d'),
                    'amount': t.amount,
                    'category': t.category,
                    'description': t.description,
                    'type': t.type.name
                })


# Recurring Payment Handler

class RecurringCSVHandler:
    def __init__(self, filepath):
        self.filepath = Path(filepath)
        self._ensure_file()

    def _ensure_file(self):
        """Checks if recurring.csv with the correct headers exists, if it doesn't, creates new CSV with headers"""

        self.filepath.parent.mkdir(parents = True, exist_ok = True)
        if not self.filepath.exists() or self.filepath.stat().st_size == 0:
            with open(self.filepath, 'w', newline = '') as f:
                writer = csv.DictWriter(f, fieldnames = ['day', 'amount', 'category', 'description'])
                writer.writeheader()

    def load(self):
        """Loads recurring payments from recurring.csv
        
        Returns:
            List: List of recurring payments from recurring.csv
        """

        if not self.filepath.exists():
            return []
        with open(self.filepath, newline = '') as f:
            return list(csv.DictReader(f))

    def save(self, entries: list[dict]):
        """Saves list of recurring payments to recurring.csv
        
        Args:
            entries (list): List of recurring payments to write to the file
        """
        with open(self.filepath, 'w', newline = '') as f:
            writer = csv.DictWriter(f, fieldnames = ['day', 'amount', 'category', 'description'])
            writer.writeheader()
            for row in entries:
                writer.writerow(row)