# 🚀 AI Task & Knowledge Management System

An AI-powered full-stack application for managing tasks and documents with **semantic search using FAISS**.

---

## 🧠 Key Features

- 🔐 JWT Authentication (Admin & User roles - RBAC)
- 📄 Document Upload & AI-based Semantic Search
- 🧠 FAISS + Sentence Transformers for vector search
- ✅ Task Management System (assign, update, track)
- 📊 Activity Logging & Analytics Dashboard
- 🌐 React Frontend for user interaction

---

## 🏗️ Tech Stack

### Backend
- FastAPI + Uvicorn
- MySQL + SQLAlchemy
- JWT (python-jose) + bcrypt

### AI / Search
- sentence-transformers
- FAISS (vector database)

### Frontend
- React (Vite)
- Axios

---

## 📁 Project Structure
ai-task-system/
├── app/ # FastAPI backend
├── frontend/ # React frontend
├── uploads/ # Uploaded documents
├── faiss_index/ # Vector index
├── requirements.txt
├── seed.py
└── .env

---

## ⚙️ Setup Instructions

### 1. Clone the repository
```bash
**git clone https://github.com/Vilas317/ai-task-system.git
cd ai-task-system
🧪 Backend Setup
2. Create virtual environment
python -m venv venv
venv\Scripts\activate
3. Install dependencies
pip install -r requirements.txt
4. Create MySQL database
CREATE DATABASE ai_task_db;
5. Configure environment variables

Create a .env file:

DATABASE_URL=mysql+pymysql://root:YOUR_PASSWORD@localhost:3306/ai_task_db
SECRET_KEY=your_secret_key
6. Run backend server
uvicorn app.main:app --reload

👉 Backend runs on: http://127.0.0.1:8000

👉 API Docs: http://127.0.0.1:8000/docs

🌐 Frontend Setup
7. Run frontend
cd frontend
npm install
npm run dev

👉 Frontend runs on: http://localhost:5173

🔄 How It Works
Admin uploads a document (.txt / .pdf)
Text is split into chunks
Each chunk is converted into embeddings
Stored in FAISS vector index
User searches using natural language
System finds semantically similar content
Returns relevant results with scores
🔌 API Endpoints
Method	Endpoint	Description
POST	/auth/register	Register user
POST	/auth/login	Login
GET	/tasks	List tasks
POST	/tasks	Create task
PATCH	/tasks/{id}	Update task
POST	/documents/upload	Upload document
GET	/documents	List documents
POST	/search	Semantic search
GET	/analytics	Dashboard**
