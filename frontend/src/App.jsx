import { useEffect, useState } from "react";
import "./App.css";

function App() {
  const [message, setMessage] = useState("");

  useEffect(() => {
    fetch("/api/test")
      .then((response) => response.json())
      .then((data) => setMessage(data.message))
      .catch((error) => console.error("Ошибка:", error));
  }, []);

  return (
    <div>
      <h1>Привет от React!</h1>
      <p>Сообщение от бэкенда: {message}</p>
    </div>
  );
}

export default App;