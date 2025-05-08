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
signUpForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const login = document.getElementById("register-login").value;
  const fullname = document.getElementById("register-name").value;
  const password = document.getElementById("register-password").value;
  const role = document.getElementById("register-role").value;
  const responseElement = document.getElementById("register-response");
  const inputs = signUpForm.querySelectorAll("input, select");
  responseElement.textContent = "Загрузка..."

  try {
    const response = await fetch("/api/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ login, fullname, password, role }),
    });
    const data = await response.json();
    console.log("Ответ от сервера:", data); // Отладка

    if (response.ok) {
      responseElement.textContent = "Регистрация успешна! Вы получили токен.";
      responseElement.style.color = "green";
    } else {
      if (data.detail) {
        if (Array.isArray(data.detail)) {
          const errorMessages = data.detail.map((error) => {
            const field = error.loc[error.loc.length - 1];
            let message = error.msg;
            // Локализация сообщений
            if (message.includes("String should have at least 6 characters")) {
              message = "Логин должен содержать минимум 6 символов";
            } else if (message.includes("String should have at least 4 characters")) {
              message = "Пароль должен содержать минимум 4 символа";
            } else if (message === "value is not a valid enumeration member") {
              message = "Недопустимая роль";
            }
            return `${field}: ${message}`;
          });
          responseElement.textContent = errorMessages.join("; ");
        } else {
          responseElement.textContent = data.detail;
        }
      } else {
        responseElement.textContent = "Ошибка регистрации";
      }
      responseElement.style.color = "red";
    }
  } catch (error) {
    responseElement.textContent = "Ошибка: " + error.message;
    responseElement.style.color = "red";
  }
  });

// Обработка формы авторизации
signInForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const username = document.getElementById("login-login").value;
  const password = document.getElementById("login-password").value;
  const responseElement = document.getElementById("login-response");
  responseElement.textContent = "Загрузка..."

  try {
    const response = await fetch("/api/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    });
  const data = await response.json();
  responseElement.textContent = data.message || data.detail || "Успех!";
  responseElement.style.color = data.message ? "green" : "red";
} catch (error) {
  responseElement.textContent = "Ошибка: " + error.message;
  responseElement.style.color = "red";
}
});