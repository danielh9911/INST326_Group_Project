import csv
from pathlib import Path
from datetime import datetime
from models import Transaction, TransactionType

class CSVHandler:
    def __init__(self, filepath):
        self.filepath = Path(filepath)
        self._ensure_file()
        
    def _ensure_file(self):
        # Create parent directory if it doesn't exist
        self.filepath.parent.mkdir(parents=True, exist_ok=True)

        # Create CSV file with headers if it doesn't exist or is empty
        if not self.filepath.exists() or self.filepath.stat().st_size == 0:
            with open(self.filepath, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=['date', 'amount', 'category', 'description', 'type'])
                writer.writeheader()

    def load(self):
        if not self.filepath.exists():
            return []

        with open(self.filepath, newline='') as f:
            return [
                Transaction(
                    date=datetime.strptime(row['date'], '%Y-%m-%d'),
                    amount=float(row['amount']),
                    category=row['category'],
                    description=row.get('description', ''),
                    type=TransactionType[row['type'].upper()]
                ) for row in csv.DictReader(f)
            ]
    
    def save(self, transactions):
        with open(self.filepath, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['date', 'amount', 'category', 'description', 'type'])
            writer.writeheader()
            for t in transactions:
                writer.writerow({
                    'date': t.date.strftime('%Y-%m-%d'),
                    'amount': t.amount,
                    'category': t.category,
                    'description': t.description,
                    'type': t.type.name  # saves as 'INCOME' or 'EXPENSE'
                })