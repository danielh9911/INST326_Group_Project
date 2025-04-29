from enum import Enum, auto
from dataclasses import dataclass
from datetime import datetime

class TransactionType(Enum):
    INCOME = auto()
    EXPENSE = auto()

@dataclass
class Transaction:
    date: datetime
    amount: float
    category: str
    description: str = ""
    type: TransactionType