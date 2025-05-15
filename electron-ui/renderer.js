// renderer.js

const statusBadge = document.getElementById("statusBadge");
const blinkCountEl = document.getElementById("blinkCount");
const yawnCountEl = document.getElementById("yawnCount");
const modelButtons = document.querySelectorAll("#modelToggle .btn");

// Highlight the active model button
function highlightModelButton(selected) {
  modelButtons.forEach((btn) => {
    btn.classList.toggle("active", btn.getAttribute("data-model") === selected);
  });
}

// Polling function to get status
async function updateStatus() {
  try {
    const res = await fetch("http://localhost:5000/status");
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();

    // Update badge
    if (data.drowsy) {
      statusBadge.textContent = "DROWSY!";
      statusBadge.className = "badge status-badge bg-danger";
    } else {
      statusBadge.textContent = "AWAKE";
      statusBadge.className = "badge status-badge bg-success";
    }

    // Update counts
    blinkCountEl.textContent = data.blink_count ?? 0;
    yawnCountEl.textContent = data.yawn_count ?? 0;

    // Highlight the selected model button
    const selectedModel = data.selected_model || "cnn";
    highlightModelButton(selectedModel);
  } catch (err) {
    console.error("Error fetching status:", err);
    statusBadge.textContent = "ERROR";
    statusBadge.className = "badge status-badge bg-warning";
  }
}

// Handle model toggle clicks
modelButtons.forEach((btn) => {
  btn.addEventListener("click", async () => {
    const model = btn.getAttribute("data-model");
    try {
      const res = await fetch("http://localhost:5000/select_model", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ model }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.message || res.statusText);
      highlightModelButton(data.model);
    } catch (err) {
      console.error("Model selection error:", err);
      statusBadge.textContent = "MODEL ERR";
      statusBadge.className = "badge status-badge bg-warning";
    }
  });
});

// Initial call and interval
updateStatus();
setInterval(updateStatus, 1000);
