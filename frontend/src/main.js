import "./style.css";

const signUpButton = document.getElementById("signUp");
const signInButton = document.getElementById("signIn");
const container = document.getElementById("container");
const signInForm = document.getElementById("sign-in-form");
const signUpForm = document.getElementById("sign-up-form");

// Обработка слайда формы регистрации/авторизации
signUpButton.addEventListener("click", () => {
  container.classList.add("right-panel-active");
});

signInButton.addEventListener("click", () => {
  container.classList.remove("right-panel-active");
});

// Обработка формы регистрации
signInForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const login = document.getElementById("register-login").value;
  const username = document.getElementById("register-name").value;
  const password = document.getElementById("register-password").value;
  const responseElement = document.getElementById("register-response");
  responseElement.textContent = "Загрузка..."

  try {
    const response = await fetch("/api/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ login, username, password }),
    });

// Обработка формы авторизации
signInForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const login = document.getElementById("login-login").value;
  const password = document.getElementById("login-password").value;
  const responseElement = document.getElementById("login-response");
  responseElement.textContent = "Загрузка..."

  try {
    const response = await fetch("/api/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ login, password }),
    });
  const data = await response.json();
  responseElement.textContent = data.message || data.detail || "Успех!";
  responseElement.style.color = data.message ? "green" : "red";
} catch (error) {
  responseElement.textContent = "Ошибка: " + error.message;
  responseElement.style.color = "red";
}
});