from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class ExpenseBase(SQLModel):
    title: str
    amount: float
    category: str


class Expense(ExpenseBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ExpenseCreate(ExpenseBase):
    pass


class ExpenseUpdate(ExpenseBase):
    pass
