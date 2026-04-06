# Expense Tracker

Personal expense tracker built with FastAPI, SQLite, and vanilla HTML/JS.

## Project Structure

```
expenses-tracker/
├── backend/
│   ├── main.py        # FastAPI app — all routes defined here
│   ├── database.py    # SQLite connection and table creation
│   ├── models.py      # (empty — Pydantic models are inlined in main.py)
│   └── expenses.db    # SQLite database file (auto-created on startup)
├── frontend/
│   ├── index.html     # Single-page UI
│   ├── app.js         # All frontend logic (fetch calls, chart rendering)
│   └── style.css      # Styles
└── venv/              # Python virtual environment
```

## Tech Stack

- **Backend**: FastAPI 0.135.3, Uvicorn 0.44.0, Python 3.14
- **Database**: SQLite (via stdlib `sqlite3`)
- **Validation**: Pydantic v2 (inlined in `main.py`)
- **Frontend**: Vanilla HTML/JS, Chart.js 4.4.1 (loaded from CDN)
- **File uploads**: `python-multipart` 0.0.24

## Running the Project

### Backend

```bash
cd backend
source ../venv/bin/activate
uvicorn main:app --reload
```

Runs at `http://127.0.0.1:8000`. Auto-reloads on file changes.

### Frontend

Open `frontend/index.html` directly in a browser — no build step or server needed. The frontend hardcodes the API base URL as `http://127.0.0.1:8000` (see `app.js` line 1).

## Database

SQLite file at `backend/expenses.db`. Created automatically when the backend starts (`create_tables()` is called at module load in `main.py`).

### Schema

```sql
CREATE TABLE IF NOT EXISTS expenses (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    date        TEXT    NOT NULL,
    amount      REAL    NOT NULL,
    category    TEXT    NOT NULL,
    description TEXT,
    source      TEXT    DEFAULT 'manual'
)
```

`source` is either `"manual"` (added via form) or `"csv"` (imported from file).

## API Routes

| Method | Path                  | Description                                      |
|--------|-----------------------|--------------------------------------------------|
| GET    | `/expenses`           | All expenses, ordered by date DESC               |
| POST   | `/expenses`           | Add a single expense (JSON body)                 |
| GET    | `/expenses/summary`   | Total spent per category                         |
| POST   | `/expenses/import`    | Upload a CSV bank statement (multipart/form-data)|

### POST `/expenses` body

```json
{
  "date": "2026-04-06",
  "amount": 12.50,
  "category": "Food",
  "description": "Lunch",
  "source": "manual"
}
```

`description` and `source` are optional (default to `""` and `"manual"`).

### POST `/expenses/import` CSV format

Expects a Revolut-style bank statement CSV with these columns:
- `Started Date` — datetime string; only the date portion is kept
- `Amount` — negative values are expenses, positive values are skipped
- `Description` — used for auto-categorization
- `State` — only rows with `COMPLETED` are imported

### Auto-categorization keywords

| Category      | Keywords                                                          |
|---------------|-------------------------------------------------------------------|
| Food          | restaurant, cafe, coffee, food, pizza, burger, sushi, chaikhana  |
| Transport     | uber, bolt, taxi, train, metro, bus, flight, ryanair             |
| Entertainment | netflix, spotify, amazon, apple, steam, cinema                   |
| Health        | pharmacy, doctor, gym, health                                    |
| Housing       | rent, electricity, gas, internet, insurance                      |
| Other         | (fallback)                                                        |

## Categories

The fixed category list (used in both frontend dropdown and auto-categorization):
`Food`, `Transport`, `Housing`, `Health`, `Entertainment`, `Other`

If you add a new category, update both the `<select>` in `index.html` and the `categorize()` function in `main.py`.

## Conventions

- All routes and business logic live in `backend/main.py`. There is no router split.
- The `Expense` Pydantic model is defined inline in `main.py`; `backend/models.py` is currently empty.
- Database connections are opened and closed per-request (no connection pool).
- CORS is open (`allow_origins=["*"]`) — fine for local development.
- Amounts are stored as positive floats; the CSV importer converts negative bank statement amounts with `abs()`.
- Dates are stored as `TEXT` in `YYYY-MM-DD` format.
- The frontend uses `€` as the currency symbol throughout — hardcoded in `app.js` and `index.html`.
