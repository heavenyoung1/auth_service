import "./style.css";

const form = document.getElementById("login-form");
const usernameInput = document.getElementById("username");
const passwordInput = document.getElementById("password");
const responseElement = document.getElementById("response");
const submitButton = form.querySelector("button");

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  // Отключаем форму во время запроса
  usernameInput.disabled = true;
  passwordInput.disabled = true;
  submitButton.disabled = true;
  submitButton.textContent = "Loading...";
  responseElement.textContent = "";

  try {
    const response = await fetch("/api/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        username: usernameInput.value,
        password: passwordInput.value,
      }),
    });
    const data = await response.json();
    responseElement.textContent = data.message || data.detail || "Success!";
    responseElement.style.color = data.message ? "green" : "red";
  } catch (error) {
    responseElement.textContent = "Error: " + error.message;
    responseElement.style.color = "red";
  } finally {
    // Включаем форму обратно
    usernameInput.disabled = false;
    passwordInput.disabled = false;
    submitButton.disabled = false;
    submitButton.textContent = "Sign In";
  }
});