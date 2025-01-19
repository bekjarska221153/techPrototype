// Функција за прикажување податоци во табелата
function displayData(data) {
    const tableBody = document.getElementById("dataTable");
    tableBody.innerHTML = ""; // Исчисти ја табелата
    data.forEach(row => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
      <td>${row.issuer}</td>
      <td>${row.date}</td>
      <td>${row.lastTransaction}</td>
      <td>${row.max}</td>
      <td>${row.min}</td>
      <td>${row.avgPrice}</td>
      <td>${row.change}</td>
      <td>${row.quantity}</td>
    `;
        tableBody.appendChild(tr);
    });
}

function loadInitialData() {
    fetch('/api/data')
        .then(response => response.json())
        .then(data => {
            displayData(data);
        })
        .catch(error => console.error("Error fetching initial data:", error));
}


// Филтер функција
function filterData() {
  const issuerCode = document.getElementById("issuerCode").value.toUpperCase();
  const dateFrom = document.getElementById("dateFrom").value;
  const dateTo = document.getElementById("dateTo").value;

  // AJAX повик до Flask API
  fetch(`/api/data?issuerCode=${issuerCode}&dateFrom=${dateFrom}&dateTo=${dateTo}`)
    .then(response => response.json())
    .then(data => {
      displayData(data);
    })
    .catch(error => console.error("Error fetching data:", error));
}

window.onload = loadInitialData;
function fetchAnalysis() {
    const issuerCode = document.getElementById("issuerCode").value.toUpperCase();
    const dateFrom = document.getElementById("dateFrom").value;
    const dateTo = document.getElementById("dateTo").value;

    fetch(`/api/analysis?issuerCode=${issuerCode}&dateFrom=${dateFrom}&dateTo=${dateTo}`)
        .then(response => response.json())
        .then(data => {
            const graphImage = document.getElementById("graphImage");
            graphImage.src = data.graph;
        })
        .catch(error => console.error("Error fetching analysis data:", error));
}
