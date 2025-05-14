import init from '../src/main.js'; // Удалите фигурные скобки, так как это default export
import { fireEvent } from '@testing-library/dom';

describe('Auth Service', () => {
  let container;

  beforeEach(() => {
    document.body.innerHTML = `
      <div class="container" id="container">
        <div class="form-container sign-up-container">
          <form id="sign-up-form" data-testid="sign-up-form">
            <h1>Регистрация</h1>
            <input type="text" id="register-login" placeholder="Логин" required />
            <input type="text" id="register-name" placeholder="Имя и фамилия" required />
            <input type="password" id="register-password" placeholder="Пароль" required />
            <select id="register-role" required>
              <option value="" disabled selected>Выберите роль</option>
              <option value="user">Пользователь</option>
              <option value="admin">Администратор</option>
            </select>
            <button type="submit">Зарегистрироваться</button>
            <p id="register-response" class="message"></p>
          </form>
        </div>
        <div class="form-container sign-in-container">
          <form id="sign-in-form" data-testid="sign-in-form">
            <h1>Авторизация</h1>
            <input type="text" id="login-login" placeholder="Логин" required/>
            <input type="password" id="login-password" placeholder="Пароль" required />
            <a href="#">Забыли пароль?</a>
            <button type="submit">Войти</button>
            <p id="login-response" class="message"></p>
          </form>
        </div>
        <div class="overlay-container">
          <div class="overlay">
            <div class="overlay-panel overlay-left">
              <h1>Добро пожаловать!</h1>
              <p>Войти со своими учетными данными</p>
              <button class="ghost" id="signIn">Войти</button>
            </div>
            <div class="overlay-panel overlay-right">
              <h1>Привет, друг!</h1>
              <p>Введите свои личные данные и начните свое путешествие вместе с нами</p>
              <button class="ghost" id="signUp">Зарегистрироваться</button>
            </div>
          </div>
        </div>
      </div>
    `;
    container = document.getElementById('container');
    init();
  });

  test('should switch to sign-up form when signUp button is clicked', () => {
    const signUpButton = document.getElementById('signUp');
    fireEvent.click(signUpButton);
    expect(container).toHaveClass('right-panel-active');
  });

  test('should switch to sign-in form when signIn button is clicked', () => {
    const signInButton = document.getElementById('signIn');
    container.classList.add('right-panel-active');
    fireEvent.click(signInButton);
    expect(container).not.toHaveClass('right-panel-active');
  });
});