from fastapi import FastAPI

app = FastAPI(title="Expense Tracker")

@app.get("/")
def root():
    return {"status": "ok"}
