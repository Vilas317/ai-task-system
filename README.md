# AI Task & Knowledge Management System

An AI-powered system for task and document management with semantic search.

## Tech Stack
- **Backend**: FastAPI + Uvicorn
- **Database**: MySQL + SQLAlchemy
- **Auth**: JWT + bcrypt
- **AI Search**: sentence-transformers + FAISS

## Features
- JWT Authentication with Admin & User roles
- Document upload and AI semantic search
- Task management with assignment
- Activity logging and analytics

## Setup Instructions

### 1. Clone the repo
git clone https://github.com/Vilas317/ai-task-system.git
cd ai-task-system

### 2. Create virtual environment
python -m venv venv
venv\Scripts\activate

### 3. Install dependencies
pip install -r requirements.txt

### 4. Create MySQL database
CREATE DATABASE ai_task_db;

### 5. Create .env file
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/ai_task_db
SECRET_KEY=mysupersecretkey123

### 6. Run the server
uvicorn app.main:app --reload

### 7. Open API docs
http://localhost:8000/docs

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /auth/register | Register user |
| POST | /auth/login | Login |
| GET | /tasks | List tasks |
| POST | /tasks | Create task |
| PATCH | /tasks/{id} | Update task status |
| GET | /documents | List documents |
| POST | /documents/upload | Upload document |
| POST | /search | AI semantic search |
| GET | /analytics | Dashboard stats |

## How AI Search Works
1. Admin uploads a .txt document
2. Text is split into chunks
3. Each chunk is converted to embeddings using sentence-transformers
4. Embeddings stored in FAISS vector database
5. Search query converted to embedding
6. FAISS finds most similar chunks
7. Results returned with relevance score
