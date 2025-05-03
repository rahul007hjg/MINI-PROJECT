// Navigation between pages (for index.html)
function navigateTo(page) {
  document.querySelectorAll(".container").forEach((el) => el.classList.add("hidden"));
  document.getElementById(`${page}-page`).classList.remove("hidden");

  // If navigating to the history page, fetch previous reports
  if (page === "history") {
    fetchHistory();
  }
}

// From Auto Detect, Extras, or History back to home page
function goBack() {
  document.querySelectorAll(".container").forEach((el) => el.classList.add("hidden"));
  document.getElementById("home-page").classList.remove("hidden");
}

function selectDisease(element) {
  document.querySelectorAll(".disease-option").forEach((el) => (el.style.background = "white"));
  element.style.background = "#e3f2fd";
}

// Show sign-up and login pages
function showSignUp() {
  document.querySelectorAll(".container").forEach((el) => el.classList.add("hidden"));
  document.getElementById("signup-page").classList.remove("hidden");
}

function showLogin() {
  document.querySelectorAll(".container").forEach((el) => el.classList.add("hidden"));
  document.getElementById("login-page").classList.remove("hidden");
}

// Handle login form submission
document.getElementById("login-form").addEventListener("submit", async function(e) {
  e.preventDefault();
  const email = document.getElementById("login-email").value;
  const password = document.getElementById("login-password").value;

  try {
    const res = await fetch("http://localhost:5000/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });
    const result = await res.json();
    if (result.success) {
      localStorage.setItem("userEmail", email);
      document.querySelectorAll(".container").forEach((el) => el.classList.add("hidden"));
      document.getElementById("home-page").classList.remove("hidden");
    } else {
      alert(result.error);
    }
  } catch (error) {
    alert(`Request failed: ${error}`);
  }
});

// Handle sign-up form submission
document.getElementById("signup-form").addEventListener("submit", async function(e) {
  e.preventDefault();
  const email = document.getElementById("signup-email").value;
  const password = document.getElementById("signup-password").value;

  try {
    const res = await fetch("http://localhost:5000/signup", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });
    const result = await res.json();
    if (result.success) {
      alert("Sign up successful! Please log in.");
      showLogin();
    } else {
      alert(result.error);
    }
  } catch (error) {
    alert(`Request failed: ${error}`);
  }
});

// Analysis function to view results (for Auto Detect)
async function viewResults() {
  const textInput = document.querySelector("textarea").value;
  const fileInput = document.querySelector('input[type="file"]').files[0];

  const formData = new FormData();
  formData.append("text", textInput);

  const userEmail = localStorage.getItem("userEmail");
  if (userEmail) {
    formData.append("email", userEmail);
  }
  if (fileInput) formData.append("file", fileInput);

  try {
    const response = await fetch("http://localhost:5000/analyze", {
      method: "POST",
      body: formData,
    });
    const result = await response.json();
    if (result.success) {
      const analysis = result.analysis.replace(/\n/g, "<br>");
      showResultsModal(analysis);
    } else {
      alert(`Error: ${result.error}`);
    }
  } catch (error) {
    alert(`Request failed: ${error}`);
  }
}

function showResultsModal(content) {
  const modal = document.createElement("div");
  modal.className = "modal";
  modal.innerHTML = `
      <div class="modal-content">
        <h2>Analysis Results</h2>
        <div class="analysis-output">${content}</div>
        <button onclick="this.parentElement.parentElement.remove()">Close</button>
      </div>
    `;
  document.body.appendChild(modal);
}

// Fetch history reports from the backend filtered by user email
async function fetchHistory() {
  const userEmail = localStorage.getItem("userEmail");
  try {
    const response = await fetch(`http://localhost:5000/history?email=${encodeURIComponent(userEmail)}`);
    const result = await response.json();
    if (result.success) {
      const container = document.getElementById("reports-container");
      container.innerHTML = "";
      result.reports.forEach((report) => {
        const card = document.createElement("div");
        card.className = "card";
        card.innerHTML = `
            <div class="card-header">
              <span>${report.generated_at}</span>
            </div>
            <div class="card-body">
              <p>${report.report.replace(/\n/g, "<br>")}</p>
            </div>
          `;
        container.appendChild(card);
      });
    } else {
      alert("Error fetching history: " + result.error);
    }
  } catch (error) {
    alert(`Request failed: ${error}`);
  }
}
