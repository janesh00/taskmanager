# TaskFlow — FastAPI Task Manager

A full-stack task management application with JWT authentication, built with **FastAPI + SQLite + vanilla JS frontend**.

## Live Demo

> 🔗 [https://your-app-name.onrender.com](https://your-app-name.onrender.com)  
> 📖 API Docs: [https://your-app-name.onrender.com/docs](https://your-app-name.onrender.com/docs)

*(Update these links after deployment)*

---

## Features

- ✅ User registration & login (JWT + bcrypt)
- ✅ Create, view, update, delete tasks
- ✅ Mark tasks as completed
- ✅ Filter by status (`?completed=true/false`)
- ✅ Pagination support
- ✅ Users only see their own tasks
- ✅ Interactive frontend (HTML/CSS/JS, no framework)
- ✅ Pytest test suite (14 tests)
- ✅ Dockerfile + docker-compose
- ✅ Clean folder structure

---

## Project Structure

```
taskmanager/
├── backend/
│   ├── app/
│   │   ├── api/              # Route handlers
│   │   │   ├── auth.py
│   │   │   ├── tasks.py
│   │   │   └── dependencies.py
│   │   ├── core/             # Config & security
│   │   │   ├── config.py
│   │   │   └── security.py
│   │   ├── db/               # Database setup
│   │   │   └── database.py
│   │   ├── models/           # SQLAlchemy models
│   │   │   ├── user.py
│   │   │   └── task.py
│   │   ├── schemas/          # Pydantic schemas
│   │   │   ├── user.py
│   │   │   └── task.py
│   │   ├── services/         # Business logic
│   │   │   ├── auth_service.py
│   │   │   └── task_service.py
│   │   └── main.py
│   ├── tests/
│   │   └── test_main.py      # 14 pytest tests
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
├── frontend/
│   └── index.html            # Single-page app
├── docker-compose.yml
└── README.md
```

---

## API Endpoints

### Authentication
| Method | Endpoint    | Description         |
|--------|-------------|---------------------|
| POST   | `/register` | Register a new user |
| POST   | `/login`    | Login, get JWT token |

### Tasks (require `Authorization: Bearer <token>`)
| Method | Endpoint        | Description             |
|--------|-----------------|-------------------------|
| POST   | `/tasks`        | Create a task           |
| GET    | `/tasks`        | List tasks (paginated)  |
| GET    | `/tasks/{id}`   | Get a specific task     |
| PUT    | `/tasks/{id}`   | Update / complete task  |
| DELETE | `/tasks/{id}`   | Delete a task           |

**Query parameters for `GET /tasks`:**
- `page` (int, default 1)
- `page_size` (int, default 10)
- `completed` (bool, optional) — filter by status

---

## Environment Variables

Copy `.env.example` to `.env` and fill in your values:

```env
SECRET_KEY=your-super-secret-key-change-this
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL=sqlite:///./taskmanager.db
```

> ⚠️ Never commit `.env` to version control.

---

## Local Setup

### Prerequisites
- Python 3.11+
- pip

### Steps

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/taskmanager.git
cd taskmanager/backend

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate        # Linux/Mac
# venv\Scripts\activate         # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment
cp .env.example .env
# Edit .env and set a strong SECRET_KEY

# 5. Run the server
uvicorn app.main:app --reload --port 8000
```

Backend will be at: http://localhost:8000  
API docs: http://localhost:8000/docs  
Frontend: Open `frontend/index.html` in your browser (or serve via Live Server)

---

## Running Tests

```bash
cd backend
pytest tests/ -v
```

Expected: **14 tests passing**

---

## Docker

```bash
# Build and run with Docker Compose
docker-compose up --build

# Or build backend image directly
cd backend
docker build -t taskmanager .
docker run -p 8000:8000 -e SECRET_KEY=mysecret taskmanager
```

---

## Deployment (Render — Free Tier)

1. Push repo to GitHub
2. Go to [render.com](https://render.com) → **New Web Service**
3. Connect your GitHub repo
4. Set these options:
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Add **Environment Variables**:
   - `SECRET_KEY` → a long random string
   - `DATABASE_URL` → `sqlite:///./taskmanager.db`
6. Deploy!

### Serving the frontend on Render

After the backend deploys, copy `frontend/index.html` into `backend/static/index.html` — the app auto-serves it at `/`.

Or run a **second Render Static Site** pointing to the `frontend/` folder and set `API` in `index.html` to your Render backend URL.

---

## Tech Stack

| Layer     | Technology                      |
|-----------|---------------------------------|
| Backend   | FastAPI, Python 3.11            |
| ORM       | SQLAlchemy 2.0                  |
| Database  | SQLite (dev) / PostgreSQL (prod)|
| Auth      | JWT (python-jose) + bcrypt      |
| Validation| Pydantic v2                     |
| Testing   | pytest + httpx                  |
| Frontend  | HTML5, CSS3, Vanilla JS         |
| Container | Docker + docker-compose         |
