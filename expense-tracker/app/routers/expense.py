from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from typing import List
from datetime import date


from app.database import get_session
from app.models.expense import Expense, ExpenseCreate, ExpenseUpdate

router = APIRouter(prefix="/expenses", tags=["Expenses"])

@router.get("/", response_model=List[Expense])
def list_expenses(
    category: str | None = None,
    start_date: date | None = None,
    end_date: date | None = None,
    session: Session = Depends(get_session)
):
    statement = select(Expense)

    if category:
        statement = statement.where(Expense.category == category)

    if start_date:
        statement = statement.where(Expense.created_at >= start_date)

    if end_date:
        statement = statement.where(Expense.created_at <= end_date)

    expenses = session.exec(statement).all()
    return expenses



@router.post("/", response_model=Expense)
def create_expense(
    expense: ExpenseCreate,
    session: Session = Depends(get_session)
):
    db_expense = Expense.model_validate(expense)
    session.add(db_expense)
    session.commit()
    session.refresh(db_expense)
    return db_expense


@router.get("/", response_model=List[Expense])
def list_expenses(session: Session = Depends(get_session)):
    statement = select(Expense)
    expenses = session.exec(statement).all()
    return expenses


@router.put("/{expense_id}", response_model=Expense)
def update_expense(
    expense_id: int,
    expense_data: ExpenseUpdate,
    session: Session = Depends(get_session)
):
    expense = session.get(Expense, expense_id)
    if not expense:
        return {"error": "Expense not found"}

    expense.title = expense_data.title
    expense.amount = expense_data.amount
    expense.category = expense_data.category

    session.add(expense)
    session.commit()
    session.refresh(expense)
    return expense



@router.delete("/{expense_id}")
def delete_expense(
    expense_id: int,
    session: Session = Depends(get_session)
):
    expense = session.get(Expense, expense_id)
    if not expense:
        return {"error": "Expense not found"}

    session.delete(expense)
    session.commit()
    return {"message": "Expense deleted"}
