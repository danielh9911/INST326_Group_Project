import tempfile
from storage import CSVHandler, RecurringCSVHandler
from models import Transaction, TransactionType
from datetime import datetime

def test_csvhandler_save_and_load():
    with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as tmp:
        handler = CSVHandler(tmp.name)
        tx = Transaction(datetime(2025, 5, 1), 200.0, 'Rent', TransactionType.EXPENSE, 'Monthly rent')
        handler.save([tx])

        loaded = handler.load()
        assert len(loaded) == 1
        assert loaded[0].category == 'Rent'
        assert loaded[0].amount == 200.0

def test_recurringcsvhandler_save_and_load():
    with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as tmp:
        handler = RecurringCSVHandler(tmp.name)
        entries = [{'day': '5', 'amount': '50.0', 'category': 'Subscription', 'description': 'Netflix'}]
        handler.save(entries)

        loaded = handler.load()
        assert len(loaded) == 1
        assert loaded[0]['category'] == 'Subscription'