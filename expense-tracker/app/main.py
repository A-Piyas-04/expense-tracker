from fastapi import FastAPI
from app.database import create_db_and_tables
from app.routers.expense import router as expense_router

app = FastAPI(title="Expense Tracker")


@app.on_event("startup")
def on_startup():
    create_db_and_tables()



@app.get("/")
def root():
    return {"status": "ok"}

    
app.include_router(expense_router)