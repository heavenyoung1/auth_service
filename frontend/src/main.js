export default function init() {
  const signUpButton = document.getElementById("signUp");
  const signInButton = document.getElementById("signIn");
  const container = document.getElementById("container");
  const signInForm = document.getElementById("sign-in-form");
  const signUpForm = document.getElementById("sign-up-form");

  // Проверка на наличие элементов
  if (!signUpButton || !signInButton || !container || !signInForm || !signUpForm) {
    console.error("One or more DOM elements not found:", {
      signUpButton,
      signInButton,
      container,
      signInForm,
      signUpForm,
    });
    return;
  }

  // Обработка слайда формы регистрации/авторизации
  signUpButton.addEventListener("click", () => {
    container.classList.add("right-panel-active");
  });

  signInButton.addEventListener("click", () => {
    container.classList.remove("right-panel-active");
  });

  // ... остальной код для обработки форм ...
}

if (typeof window !== 'undefined' && window.document) {
  init();
}