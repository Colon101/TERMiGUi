const toggleCheckbox = document.getElementById("toggle-theme");
const body = document.body;

function setCookie(name, value, days) {
  const date = new Date();
  date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
  const expires = "expires=" + date.toUTCString();
  document.cookie = name + "=" + value + ";" + expires + ";path=/";
}

function getCookie(name) {
  const cookieName = name + "=";
  const cookies = document.cookie.split(";");
  for (let i = 0; i < cookies.length; i++) {
    let cookie = cookies[i];
    while (cookie.charAt(0) === " ") {
      cookie = cookie.substring(1);
    }
    if (cookie.indexOf(cookieName) === 0) {
      return cookie.substring(cookieName.length, cookie.length);
    }
  }
  return "";
}

function cookieExists(name) {
  return document.cookie.split(";").some((cookie) => cookie.trim().startsWith(name + "="));
}

toggleCheckbox.addEventListener("change", function() {
  if (toggleCheckbox.checked) {
    body.classList.add("light-theme");
    setCookie("theme", "light", 365);
  } else {
    body.classList.remove("light-theme");
    setCookie("theme", "dark", 365);
  }
});

if (cookieExists("theme")) {
  const theme = getCookie("theme");
  if (theme === "light") {
    toggleCheckbox.checked = true;
    body.classList.add("light-theme");
  }
}

let loading = false;
let offset = 0;

function loadLeaderboard() {
  if (loading) return;
  loading = true;
  const leaderboardContainer = document.getElementById('leaderboard-container');
  const loadingSpinner = document.getElementById('loading-spinner');

  loadingSpinner.style.display = 'block';

  fetch(`/leaderboard?offset=${offset}`)
    .then((response) => response.json())
    .then((data) => {
      if (data.length === 0) {
        loadingSpinner.style.display = 'none';
        return;
      }

      const table = leaderboardContainer.querySelector('table');
      data.forEach((row, index) => {
        const newRow = document.createElement('tr');
        newRow.innerHTML = `
          <td>${offset + index + 1}</td>
          <td>${row.username}</td>
          <td>${row.score}</td>
        `;
        table.appendChild(newRow);
      });

      offset += data.length;
      loading = false;
      loadingSpinner.style.display = 'none';
;
    })
    .catch((error) => {
      console.error('Error loading leaderboard: ', error);
      loading = false;
      loadingSpinner.style.display = 'none';
    });
}

loadLeaderboard();

window.addEventListener('scroll', () => {
  if (window.innerHeight + window.scrollY >= document.body.offsetHeight - 100) {
    loadLeaderboard();
  }
});
