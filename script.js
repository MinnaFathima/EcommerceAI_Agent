async function send() {
  const input = document.getElementById("userInput").value;

  const res = await fetch("/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message: input })
  });

  const data = await res.json();
  document.getElementById("botReply").innerText = data.reply;

  // Display chart for total sales or ROAS
  if (input.toLowerCase().includes("total sales")) {
    renderChart("Total Sales", parseFloat(data.chartData.match(/₹([\d.]+)/)[1]));
  } else if (input.toLowerCase().includes("roas")) {
    renderChart("ROAS", parseFloat(data.chartData.match(/(\d+(\.\d+)?)/)[0]));
  }
}

function renderChart(label, value) {
  const ctx = document.getElementById("myChart").getContext("2d");
  new Chart(ctx, {
    type: "bar",
    data: {
      labels: [label],
      datasets: [{
        label: label,
        data: [value],
        backgroundColor: ["#4CAF50"]
      }]
    }
  });
}
