import { fireEvent, screen, waitFor } from '@testing-library/dom';
import { JSDOM } from 'jsdom';

// Имитируем DOM
const dom = new JSDOM(`
  <!DOCTYPE html>
  <html>
    <body>
      <button id="signUp">Sign Up</button>
      <button id="signIn">Sign In</button>
      <div id="container"></div>
      <form id="sign-up-form" data-testid="sign-up-form">
        <input id="register-login" value="testuser" />
        <input id="register-name" value="Test User" />
        <input id="register-password" value="pass123" />
        <select id="register-role">
          <option value="user">User</option>
        </select>
        <div id="register-response"></div>
      </form>
      <form id="sign-in-form" data-testid="sign-in-form">
        <input id="login-login" value="testuser" />
        <input id="login-password" value="pass123" />
        <div id="login-response"></div>
      </form>
    </body>
  </html>
`);

// Устанавливаем глобальный объект window
global.window = dom.window;
global.document = dom.window.document;

// Импортируем main.js после настройки DOM
beforeAll(() => {
  require('../main.js');
  const event = new Event('DOMContentLoaded');
  global.document.dispatchEvent(event);
});

// Мокаем fetch
beforeEach(() => {
  jest.spyOn(global, 'fetch').mockImplementation(() =>
    Promise.resolve({
      ok: true,
      status: 200,
      json: () => Promise.resolve({ message: 'Успех!' }),
    })
  );
});

afterEach(() => {
  jest.restoreAllMocks();
});

describe('Frontend Tests', () => {
  test('Переключение на регистрацию', () => {
    const signUpButton = screen.getByText('Sign Up');
    fireEvent.click(signUpButton);
    expect(document.getElementById('container')).toHaveClass('right-panel-active');
  });

  test('Переключение на авторизацию', () => {
    const signInButton = screen.getByText('Sign In');
    fireEvent.click(signInButton);
    expect(document.getElementById('container')).not.toHaveClass('right-panel-active');
  });

  test('Успешная регистрация', async () => {
    const form = screen.getByTestId('sign-up-form');
    fireEvent.submit(form);
    await waitFor(() => {
      const response = screen.getByText('Регистрация успешна! Вы получили токен.');
      expect(response).toBeInTheDocument();
      expect(response).toHaveStyle('color: green');
    });
  });

  test('Ошибка при регистрации (короткий пароль)', async () => {
    document.getElementById('register-password').value = '123';
    const form = screen.getByTestId('sign-up-form');
    jest.spyOn(global, 'fetch').mockImplementation(() =>
      Promise.resolve({
        ok: false,
        status: 400,
        json: () =>
          Promise.resolve({
            detail: [{ loc: ['password'], msg: 'String should have at least 4 characters' }],
          }),
      })
    );
    fireEvent.submit(form);
    await waitFor(() => {
      const response = screen.getByText('password: Пароль должен содержать минимум 4 символа');
      expect(response).toBeInTheDocument();
      expect(response).toHaveStyle('color: red');
    });
  });

  test('Успешная авторизация', async () => {
    const form = screen.getByTestId('sign-in-form');
    fireEvent.submit(form);
    await waitFor(() => {
      const response = screen.getByText('Успех!');
      expect(response).toBeInTheDocument();
      expect(response).toHaveStyle('color: green');
    });
  });

  test('Ошибка при авторизации', async () => {
    jest.spyOn(global, 'fetch').mockImplementation(() =>
      Promise.resolve({
        ok: false,
        status: 400,
        json: () => Promise.resolve({ message: 'Ошибка авторизации' }),
      })
    );
    const form = screen.getByTestId('sign-in-form');
    fireEvent.submit(form);
    await waitFor(() => {
      const response = screen.getByText('Ошибка авторизации');
      expect(response).toBeInTheDocument();
      expect(response).toHaveStyle('color: red');
    });
  });
});