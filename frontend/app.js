const API = "http://127.0.0.1:8000"
let spendingChart = null

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
    renderChart(summary)
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

async function importCSV() {
    const fileInput = document.getElementById("csv-file")
    const file = fileInput.files[0]
    
    if (!file) {
      alert("Please select a CSV file first")
      return
    }
    
    const formData = new FormData()
    formData.append("file", file)
    
    const res = await fetch(`${API}/expenses/import`, {
      method: "POST",
      body: formData
    })
    
    const result = await res.json()
    alert(result.message)
    loadExpenses()
    loadSummary()
  }

  function renderChart(summary) {
    const labels = summary.map(s => s.category)
    const data = summary.map(s => s.total)
    const colors = [
      "#4e79a7", "#f28e2b", "#e15759",
      "#76b7b2", "#59a14f", "#edc948"
    ]
  
    if (spendingChart) {
      spendingChart.destroy()
    }
  
    const ctx = document.getElementById("spending-chart").getContext("2d")
    spendingChart = new Chart(ctx, {
      type: "bar",
      data: {
        labels: labels,
        datasets: [{
          label: "Spending by Category (€)",
          data: data,
          backgroundColor: colors.slice(0, labels.length)
        }]
      },
      options: {
        responsive: true,
        plugins: {
          legend: { display: false }
        },
        scales: {
          y: {
            beginAtZero: true,
            ticks: {
              callback: value => `€${value}`
            }
          }
        }
      }
    })
  }