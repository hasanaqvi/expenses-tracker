# Expense Tracker

A personal expense tracker built with FastAPI, SQLite, and vanilla HTML/JS.
Supports manual expense entry, bank CSV import, and spending visualization by category.

## Tech Stack

- **Backend:** Python, FastAPI, SQLite
- **Frontend:** HTML, CSS, JavaScript, Chart.js
- **Tools:** Git, Uvicorn

## Project Structure

    expense-tracker/
    ├── backend/
    │   ├── main.py        # FastAPI routes
    │   ├── database.py    # SQLite connection and table setup
    │   └── models.py      # Data models
    └── frontend/
        ├── index.html     # Main UI
        ├── app.js         # Frontend logic
        └── style.css      # Styling

## Setup

1. Clone the repository:

    git clone https://github.com/YOUR_USERNAME/expense-tracker.git
    cd expense-tracker

2. Create and activate virtual environment:

    python3 -m venv venv
    source venv/bin/activate

3. Install dependencies:

    pip install fastapi uvicorn python-multipart

## Running the App

Start the backend from inside backend/:

    cd backend
    uvicorn main:app --reload

Start the frontend from inside frontend/ in a new terminal tab:

    cd frontend
    python3 -m http.server 3000

Then open your browser and go to http://localhost:3000

## Features

- Manually add expenses with date, amount, category and description
- Import bank statement CSV files with auto-categorization
- View all expenses in a sortable table
- Spending breakdown chart by category
- Summary totals per category

## CSV Import Format

The importer is configured for Revolut bank statement exports. Only
COMPLETED transactions with negative amounts are imported.
Income and pending transactions are automatically skipped.
