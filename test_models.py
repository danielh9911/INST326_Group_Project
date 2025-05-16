from datetime import datetime
from models import Transaction, TransactionType

def test_transaction_creation():
    tx = Transaction(
        date=datetime(2025, 5, 1),
        amount=100.0,
        category='Food',
        description='Groceries',
        type=TransactionType.EXPENSE
    )
    assert tx.amount == 100.0
    assert tx.category == 'Food'
    assert tx.description == 'Groceries'
    assert tx.type == TransactionType.EXPENSE