from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from typing import List

from app.database import get_session
from app.models.expense import Expense

router = APIRouter(prefix="/expenses", tags=["Expenses"])


@router.post("/", response_model=Expense)
def create_expense(expense: Expense, session: Session = Depends(get_session)):
    session.add(expense)
    session.commit()
    session.refresh(expense)
    return expense


@router.get("/", response_model=List[Expense])
def list_expenses(session: Session = Depends(get_session)):
    statement = select(Expense)
    expenses = session.exec(statement).all()
    return expenses
