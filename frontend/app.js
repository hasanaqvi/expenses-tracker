const API = "http://127.0.0.1:8000"

async function loadExpenses() {
  const res = await fetch(`${API}/expenses`)
  const expenses = await res.json()
  const tbody = document.getElementById("tbody")
  tbody.innerHTML = expenses.map(e => `
    <tr>
      <td>${e.date}</td>
      <td>€${e.amount.toFixed(2)}</td>
      <td>${e.category}</td>
      <td>${e.description}</td>
    </tr>
  `).join("")
}

async function loadSummary() {
  const res = await fetch(`${API}/expenses/summary`)
  const summary = await res.json()
  const list = document.getElementById("summary-list")
  list.innerHTML = summary.map(s => `
    <li>${s.category}: €${s.total.toFixed(2)}</li>
  `).join("")
}

async function addExpense() {
  const expense = {
    date: document.getElementById("date").value,
    amount: parseFloat(document.getElementById("amount").value),
    category: document.getElementById("category").value,
    description: document.getElementById("description").value,
    source: "manual"
  }
  await fetch(`${API}/expenses`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(expense)
  })
  loadExpenses()
  loadSummary()
}

loadExpenses()
loadSummary()