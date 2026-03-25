import { useState } from "react";
import axios from "axios";

const API = "http://127.0.0.1:8000";

export default function App() {
  const [token, setToken] = useState("");

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const [file, setFile] = useState(null);

  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);

  const [tasks, setTasks] = useState([]);

  // ✅ REMOVE DUPLICATES (keep best score)
  const uniqueResults = Object.values(
    results.reduce((acc, r) => {
      if (!acc[r.document_id] || r.score < acc[r.document_id].score) {
        acc[r.document_id] = r;
      }
      return acc;
    }, {})
  );

  // LOGIN
  const login = async () => {
    try {
      const res = await axios.post(`${API}/auth/login`, {
        username,
        password,
      });
      setToken(res.data.access_token);
      alert("Login success");
    } catch (err) {
      alert("Login failed");
    }
  };

  // UPLOAD
  const upload = async () => {
    if (!file) return alert("Select file");

    const formData = new FormData();
    formData.append("file", file);

    try {
      await axios.post(`${API}/documents/upload`, formData, {
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "multipart/form-data",
        },
      });
      alert("Uploaded successfully");
    } catch {
      alert("Upload failed");
    }
  };

  // SEARCH
  const search = async () => {
    try {
      const res = await axios.post(
        `${API}/search`,
        { query, top_k: 5 },
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );
      setResults(res.data);
    } catch {
      alert("Search failed");
    }
  };

  // GET TASKS
  const loadTasks = async () => {
    try {
      const res = await axios.get(`${API}/tasks`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setTasks(res.data);
    } catch {
      alert("Failed to load tasks");
    }
  };

  return (
    <div style={{ padding: 20, fontFamily: "Arial" }}>
      <h1>AI Task System</h1>

      {/* LOGIN */}
      <h2>Login</h2>
      <input placeholder="Username" onChange={(e) => setUsername(e.target.value)} />
      <input type="password" placeholder="Password" onChange={(e) => setPassword(e.target.value)} />
      <button onClick={login}>Login</button>

      <hr />

      {/* UPLOAD */}
      <h2>Upload Document</h2>
      <input type="file" onChange={(e) => setFile(e.target.files[0])} />
      <button onClick={upload}>Upload</button>

      <hr />

      {/* SEARCH */}
      <h2>Search</h2>
      <input placeholder="Search query" onChange={(e) => setQuery(e.target.value)} />
      <button onClick={search}>Search</button>

      <ul>
        {uniqueResults.map((r, i) => (
          <li key={i}>
            <b>{r.filename}</b>
            <p>{r.excerpt}</p>
            <small>Score: {r.score}</small>
          </li>
        ))}
      </ul>

      <hr />

      {/* TASKS */}
      <h2>Tasks</h2>
      <button onClick={loadTasks}>Load Tasks</button>

      <ul>
        {tasks.map((t) => (
          <li key={t.id}>
            {t.title} - {t.status}
          </li>
        ))}
      </ul>
    </div>
  );
}