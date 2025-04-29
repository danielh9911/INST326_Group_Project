import csv
from pathlib import Path
from .models import Transaction

class CSVHandler:
    def __init__(self, filepath):
        self.filepath = Path(filepath)
        
    def load(self):
        """Load transactions from CSV"""
        if not self.filepath.exists():
            return []
            
        with open(self.filepath) as f:
            return [
                Transaction(
                    date=datetime.strptime(row['date'], '%Y-%m-%d'),
                    amount=float(row['amount']),
                    category=row['category'],
                    description=row['description'],
                    type=row['type']
                ) for row in csv.DictReader(f)
            ]
    
    def save(self, transactions):
        """Save transactions to CSV"""
        with open(self.filepath, 'w') as f:
            writer = csv.DictWriter(f, fieldnames=['date','amount','category','description','type'])
            writer.writeheader()
            writer.writerows({
                'date': t.date.strftime('%Y-%m-%d'),
                'amount': t.amount,
                'category': t.category,
                'description': t.description,
                'type': t.type
            } for t in transactions)