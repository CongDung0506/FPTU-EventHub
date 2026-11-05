/* FPTU EventHub: Modern Client-Side Controller */

document.addEventListener("DOMContentLoaded", function () {
  // 1. Dark Mode Management
  initTheme();

  // 2. Countdown Timer
  initCountdown();

  // 3. Instant Live Search
  initLiveSearch();
});

// --- Dark Mode ---------------------------------------------------------------
function initTheme() {
  const toggleBtn = document.getElementById("theme-toggle-btn");
  const themeIcon = document.getElementById("theme-icon");
  const currentTheme = localStorage.getItem("feh-theme") || "light";

  setTheme(currentTheme);

  if (toggleBtn) {
    toggleBtn.addEventListener("click", function () {
      const activeTheme = document.documentElement.getAttribute("data-theme") || "light";
      const newTheme = activeTheme === "dark" ? "light" : "dark";
      setTheme(newTheme);
    });
  }
}

function setTheme(theme) {
  const themeIcon = document.getElementById("theme-icon");
  if (theme === "dark") {
    document.documentElement.setAttribute("data-theme", "dark");
    localStorage.setItem("feh-theme", "dark");
    if (themeIcon) {
      themeIcon.className = "fa-solid fa-sun text-warning";
    }
  } else {
    document.documentElement.removeAttribute("data-theme");
    localStorage.setItem("feh-theme", "light");
    if (themeIcon) {
      themeIcon.className = "fa-solid fa-moon";
    }
  }
}

// --- Countdown Timer --------------------------------------------------------
function initCountdown() {
  const countdownEl = document.getElementById("feh-countdown");
  if (!countdownEl) return;

  const targetDateStr = countdownEl.getAttribute("data-target-time");
  if (!targetDateStr) return;

  const targetDate = new Date(targetDateStr).getTime();

  function updateTimer() {
    const now = new Date().getTime();
    const distance = targetDate - now;

    if (distance <= 0) {
      countdownEl.innerHTML = "<div class='text-warning' style='font-weight:700;'>Sự kiện đang diễn ra!</div>";
      return;
    }

    const days = Math.floor(distance / (1000 * 60 * 60 * 24));
    const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((distance % (1000 * 60)) / 1000);

    const elDays = document.getElementById("cd-days");
    const elHours = document.getElementById("cd-hours");
    const elMins = document.getElementById("cd-mins");
    const elSecs = document.getElementById("cd-secs");

    if (elDays) elDays.innerText = days < 10 ? "0" + days : days;
    if (elHours) elHours.innerText = hours < 10 ? "0" + hours : hours;
    if (elMins) elMins.innerText = minutes < 10 ? "0" + minutes : minutes;
    if (elSecs) elSecs.innerText = seconds < 10 ? "0" + seconds : seconds;
  }

  updateTimer();
  setInterval(updateTimer, 1000);
}

// --- Instant Live Search ----------------------------------------------------
function initLiveSearch() {
  const searchInput = document.getElementById("live-search-input");
  if (!searchInput) return;

  searchInput.addEventListener("input", function (e) {
    const keyword = e.target.value.toLowerCase().trim();
    const cards = document.querySelectorAll(".feh-event-item");
    let matchCount = 0;

    cards.forEach(function (card) {
      const title = card.getAttribute("data-title") || "";
      const venue = card.getAttribute("data-venue") || "";
      const speaker = card.getAttribute("data-speaker") || "";
      const cat = card.getAttribute("data-category") || "";

      if (title.includes(keyword) || venue.includes(keyword) || speaker.includes(keyword) || cat.includes(keyword)) {
        card.style.display = "";
        matchCount++;
      } else {
        card.style.display = "none";
      }
    });

    const noResultEl = document.getElementById("live-no-results");
    if (noResultEl) {
      noResultEl.style.display = matchCount === 0 ? "block" : "none";
    }
  });
}

// --- Confetti Effect (Uses canvas-confetti) ----------------------------------
function triggerConfetti() {
  if (typeof confetti === "function") {
    confetti({
      particleCount: 80,
      spread: 70,
      origin: { y: 0.6 }
    });
  }
}
