from core import FinanceTracker
from models import Transaction, TransactionType
from datetime import datetime

def test_add_and_summary():
    tracker = FinanceTracker()
    tracker.add_transaction(Transaction(datetime(2025, 5, 1), 1000, 'Job', TransactionType.INCOME))
    tracker.add_transaction(Transaction(datetime(2025, 5, 2), 200, 'Groceries', TransactionType.EXPENSE))

    summary = tracker.get_monthly_summary(5, 2025)
    assert summary['income'] == 1000
    assert summary['expenses'] == 200
    assert summary['savings'] == 800

def test_recurring_payment_add_and_remove():
    tracker = FinanceTracker()
    tracker.add_recurring_payment(1, 25.0, 'Subscription', 'Test service')
    
    recurring = tracker.recurring_handler.load()
    assert len(recurring) > 0
    
    tracker.remove_recurring_payment(0)
    assert len(tracker.recurring_handler.load()) == 0