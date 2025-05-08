import { useState } from "react";
import "./App.css";

function App() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [response, setResponse] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await fetch("/api/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
      });
      const data = await res.json();
      setResponse(data.message || data.detail || "Успех!");
    } catch (error) {
      setResponse("Ошибка: " + error.message);
    }
  };

  return (
    <div>
      <h1>Сервис авторизации</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Имя пользователя: </label>
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
        </div>
        <div>
          <label>Пароль: </label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>
        <button type="submit">Войти</button>
      </form>
      <p>{response}</p>
    </div>
  );
}

export default App;