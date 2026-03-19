# TaskFlow — FastAPI Task Manager

A full-stack task management application built with **FastAPI + SQLite + vanilla JS frontend**, featuring JWT authentication and a clean dark-themed UI.

## 🔗 Live Demo

> **App**: https://taskmanager-a4d5.onrender.com
> **API Docs**: https://taskmanager-a4d5.onrender.com/docs

---

## ✨ Features

- User registration & login with JWT authentication
- Password hashing with bcrypt
- Create, view, update and delete tasks
- Mark tasks as completed / pending
- Filter tasks by status (`?completed=true/false`)
- Pagination support
- Users can only access their own tasks
- Interactive single-page frontend (no framework)
- Swagger UI at `/docs`
- 16 pytest test cases
- Dockerfile + docker-compose
- Clean layered folder structure

---

## 📁 Project Structure

```
taskmanager/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── auth.py          # /register, /login, /me
│   │   │   ├── tasks.py         # CRUD endpoints
│   │   │   └── dependencies.py  # JWT auth dependency
│   │   ├── core/
│   │   │   ├── config.py        # Settings via pydantic-settings
│   │   │   └── security.py      # JWT + bcrypt
│   │   ├── db/
│   │   │   └── database.py      # SQLAlchemy engine + session
│   │   ├── models/
│   │   │   ├── user.py          # User ORM model
│   │   │   └── task.py          # Task ORM model
│   │   ├── schemas/
│   │   │   ├── user.py          # Pydantic schemas for auth
│   │   │   └── task.py          # Pydantic schemas for tasks
│   │   ├── services/
│   │   │   ├── auth_service.py  # Registration & login logic
│   │   │   └── task_service.py  # Task CRUD logic
│   │   └── main.py              # FastAPI app entry point
│   ├── tests/
│   │   └── test_main.py         # 16 pytest tests
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── pytest.ini
│   └── .env.example
├── frontend/
│   └── index.html               # Single-page app (HTML/CSS/JS)
├── docker-compose.yml
├── render.yaml
└── README.md
```

---

## 🌐 API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/register` | Register a new user |
| POST | `/login` | Login, receive JWT token |
| GET | `/me` | Get current user profile |

### Tasks *(require `Authorization: Bearer <token>`)*
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/tasks` | Create a task |
| GET | `/tasks` | List tasks (paginated + filterable) |
| GET | `/tasks/{id}` | Get a specific task |
| PUT | `/tasks/{id}` | Update / complete a task |
| DELETE | `/tasks/{id}` | Delete a task |

**Query params for `GET /tasks`:**
- `page` (int, default `1`)
- `page_size` (int, default `10`)
- `completed` (bool, optional) — filter by completion status

---

## ⚙️ Environment Variables

Copy `.env.example` to `.env`:

```env
SECRET_KEY=your-super-secret-key-change-this
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL=sqlite:////tmp/taskmanager.db
```

> ⚠️ Never commit `.env` to version control.

---

## 🚀 Local Setup

### Prerequisites
- Python 3.11+

### Steps

```bash
# 1. Clone the repo
git clone https://github.com/janesh00/taskmanager.git
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

- Backend: http://localhost:8000
- API docs: http://localhost:8000/docs
- Frontend: open `frontend/index.html` in your browser

---

## 🧪 Running Tests

```bash
cd backend
pytest tests/ -v
```

Expected output: **16 tests passing**

---

## 🐳 Docker

```bash
# Run with Docker Compose
docker-compose up --build

# Or build backend image directly
cd backend
docker build -t taskmanager .
docker run -p 8000:8000 -e SECRET_KEY=mysecretkey taskmanager
```

---

## ☁️ Deployment (Render)

This project is deployed on [Render](https://render.com) free tier.

### Settings used:
| Field | Value |
|-------|-------|
| Runtime | Python 3.11 |
| Root Directory | `backend` |
| Build Command | `pip install -r requirements.txt && mkdir -p static && cp ../frontend/index.html static/index.html` |
| Start Command | `uvicorn app.main:app --host 0.0.0.0 --port $PORT` |

### Environment variables on Render:
| Key | Value |
|-----|-------|
| `SECRET_KEY` | *(random secret)* |
| `DATABASE_URL` | `sqlite:////tmp/taskmanager.db` |
| `ALGORITHM` | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `30` |

> **Note:** SQLite data resets on each deploy (Render free tier has ephemeral storage). For persistent data, switch `DATABASE_URL` to a PostgreSQL connection string.

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | FastAPI, Python 3.11 |
| ORM | SQLAlchemy 2.0 |
| Database | SQLite (via `/tmp`) |
| Auth | JWT (python-jose) + bcrypt |
| Validation | Pydantic v2 |
| Testing | pytest + httpx (16 tests) |
| Frontend | HTML5, CSS3, Vanilla JS |
| Container | Docker + docker-compose |
| Hosting | Render (free tier) |
