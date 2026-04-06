from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from database import get_connection, create_tables

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

create_tables()

class Expense(BaseModel):
    date: str
    amount: float
    category: str
    description: str = ""
    source: str = "manual"

@app.get("/expenses")
def get_expenses():
    conn = get_connection()
    expenses = conn.execute("SELECT * FROM expenses ORDER BY date DESC").fetchall()
    conn.close()
    return [dict(e) for e in expenses]

@app.post("/expenses")
def add_expense(expense: Expense):
    conn = get_connection()
    conn.execute(
        "INSERT INTO expenses (date, amount, category, description, source) VALUES (?, ?, ?, ?, ?)",
        (expense.date, expense.amount, expense.category, expense.description, expense.source)
    )
    conn.commit()
    conn.close()
    return {"message": "Expense added successfully"}

@app.get("/expenses/summary")
def get_summary():
    conn = get_connection()
    rows = conn.execute(
        "SELECT category, SUM(amount) as total FROM expenses GROUP BY category"
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]