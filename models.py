from enum import Enum, auto
from dataclasses import dataclass
from datetime import datetime

class TransactionType(Enum):
    """Enumeration for the type of transaction"""
    INCOME = auto()
    EXPENSE = auto()

@dataclass
class Transaction:
    """Represents a financial transaction entry"""
    date: datetime
    amount: float
    category: str
    type: TransactionType
    description: str = ""