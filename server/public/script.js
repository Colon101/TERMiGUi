const toggleCheckbox = document.getElementById("toggle-theme");
const body = document.body;

// Function to set a cookie with a given name, value, and expiration date
function setCookie(name, value, days) {
  const date = new Date();
  date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
  const expires = "expires=" + date.toUTCString();
  document.cookie = name + "=" + value + ";" + expires + ";path=/";
}

// Function to get the value of a cookie with a given name
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

// Function to check if a cookie with a given name exists
function cookieExists(name) {
  return document.cookie.split(";").some((cookie) => cookie.trim().startsWith(name + "="));
}

toggleCheckbox.addEventListener("change", function() {
  if (toggleCheckbox.checked) {
    body.classList.add("light-theme");
    setCookie("theme", "light", 365); // Set the "theme" cookie with a value of "light" that expires in 365 days
  } else {
    body.classList.remove("light-theme");
    setCookie("theme", "dark", 365); // Set the "theme" cookie with a value of "dark" that expires in 365 days
  }
});

// Check if the "theme" cookie exists and set the theme accordingly
if (cookieExists("theme")) {
  const theme = getCookie("theme");
  if (theme === "light") {
    toggleCheckbox.checked = true;
    body.classList.add("light-theme");
  }
}
