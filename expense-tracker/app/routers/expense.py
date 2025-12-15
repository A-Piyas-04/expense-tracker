from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from sqlalchemy import func
from typing import List
from datetime import date,datetime


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




@router.get("/summary/monthly")
def monthly_summary(
    year: int,
    month: int,
    session: Session = Depends(get_session)
):
    start_date = datetime(year, month, 1)

    if month == 12:
        end_date = datetime(year + 1, 1, 1)
    else:
        end_date = datetime(year, month + 1, 1)

    # Total amount for the month
    total = session.exec(
        select(func.sum(Expense.amount))
        .where(Expense.created_at >= start_date)
        .where(Expense.created_at < end_date)
    ).one()

    total_amount = total or 0.0

    # Category-wise breakdown
    results = session.exec(
        select(Expense.category, func.sum(Expense.amount))
        .where(Expense.created_at >= start_date)
        .where(Expense.created_at < end_date)
        .group_by(Expense.category)
    ).all()

    by_category = {
        category: amount for category, amount in results
    }

    return {
        "year": year,
        "month": month,
        "total_amount": total_amount,
        "by_category": by_category
    }
