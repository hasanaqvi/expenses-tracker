import csv
import io
from fastapi import File, UploadFile

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

@app.post("/expenses/import")
async def import_csv(file: UploadFile = File(...)):
    contents = await file.read()
    decoded = contents.decode("utf-8")
    reader = csv.DictReader(io.StringIO(decoded))

    # Auto-categorize based on keywords in the description
    def categorize(description: str) -> str:
        description = description.lower()
        if any(word in description for word in ["restaurant", "cafe", "coffee", "food", "pizza", "burger", "sushi", "chaikhana"]):
            return "Food"
        elif any(word in description for word in ["uber", "bolt", "taxi", "train", "metro", "bus", "flight", "ryanair"]):
            return "Transport"
        elif any(word in description for word in ["netflix", "spotify", "amazon", "apple", "steam", "cinema"]):
            return "Entertainment"
        elif any(word in description for word in ["pharmacy", "doctor", "gym", "health"]):
            return "Health"
        elif any(word in description for word in ["rent", "electricity", "gas", "internet", "insurance"]):
            return "Housing"
        else:
            return "Other"

    conn = get_connection()
    imported = 0

    for row in reader:
        # Skip non-completed or non-expense transactions
        if row.get("State", "").strip() != "COMPLETED":
            continue
        
        amount = float(row.get("Amount", 0))
        if amount >= 0:
            continue  # Skip income, only import expenses

        # Clean up the date — strip the time portion
        raw_date = row.get("Started Date", "")
        date = raw_date.split(" ")[0] if " " in raw_date else raw_date

        description = row.get("Description", "").strip()

        conn.execute(
            "INSERT INTO expenses (date, amount, category, description, source) VALUES (?, ?, ?, ?, ?)",
            (
                date,
                abs(amount),  # Store as positive number
                categorize(description),
                description,
                "csv"
            )
        )
        imported += 1

    conn.commit()
    conn.close()
    return {"message": f"{imported} expenses imported successfully"}