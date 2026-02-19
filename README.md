# Competitive Intelligence Tracker

A production-grade competitive intelligence tool that tracks SaaS pricing pages, changelogs, and documentation. It detects meaningful content changes, filters out noise (timestamps, navigation), and uses AI to generate strategic insights.

## 🚀 Live Demo
[Insert Railway Link Here]

## ✨ Key Features

- **Strategic Noise Filtering**: Intelligent preprocessing removes dynamic content like "14 hours ago", vote counts, and navigation menus to focus on *actual* product updates.
- **Smart Diffing**: Paragraph-level comparison tailored for SaaS documentation, ignoring trivial whitespace or order changes.
- **AI-Powered Insights**: Uses GPT-3.5-Turbo to categorize changes into:
  - 💰 **Pricing Updates**
  - 🚀 **New Features**
  - 📢 **Positioning Changes**
  - 🧠 **Strategic Implications**
- **Visual Dashboard**: A clean, modern UI to track competitors and view historical snapshots.
- **System Health**: A dedicated status dashboard to monitor backend, database, and AI service health.

## 🛠️ Tech Stack

- **Backend**: FastAPI (Python 3.11)
- **Database**: PostgreSQL (Async SQLAlchemy)
- **AI Engine**: OpenAI API
- **Frontend**: Server-Side Rendered (Jinja2) + Modern CSS (No heavyweight JS frameworks)
- **Infrastructure**: Docker & Docker Compose

## 📦 Deployment Instructions

### Option 1: Railway (Recommended)

1. Fork this repository.
2. Login to [Railway.app](https://railway.app/).
3. Create a **New Project** → **Deploy from GitHub repo**.
4. Railway will automatically detect the `Dockerfile`.
5. Add a **PostgreSQL** database service within the Railway project.
6. Set the following **Environment Variables** in the Service settings:
   - `DATABASE_URL`: (Connect to the PostgreSQL service you just added)
   - `OPENAI_API_KEY`: `sk-...`
   - `PORT`: `8000`
7. The app will deploy, and you'll get a public URL.

### Option 2: Local Development (Docker)

1. Clone the repository:
   ```bash
   git clone https://github.com/Ujjuanku/Intelligence_Tracker_Backend.git
   cd Intelligence_Tracker_Backend
   ```

2. Create a `.env` file:
   ```bash
   cp .env.example .env
   # Add your OPENAI_API_KEY in the .env file
   ```

3. Run with Docker Compose:
   ```bash
   docker compose up --build
   ```

4. Access the app:
   - Dashboard: `http://localhost:8000`
   - System Status: `http://localhost:8000/system-status`
   - API Docs: `http://localhost:8000/docs`

## 📁 Project Structure

```
├── app/
│   ├── main.py            # Application entrypoint & routes
│   ├── database.py        # Database connection & session management
│   ├── models.py          # SQLAlchemy database models
│   ├── schemas.py         # Pydantic data schemas
│   ├── services/
│   │   ├── fetcher.py     # HTML fetching & cleaning logic
│   │   ├── preprocess.py  # Regex-based noise reduction
│   │   ├── diff_service.py # Logic for text comparison
│   │   └── llm_service.py # OpenAI integration for summarization
│   ├── templates/         # Jinja2 HTML templates
│   └── static/            # CSS and assets
├── Dockerfile             # Production container definition
├── docker-compose.yml     # Local development orchestration
└── requirements.txt       # Python dependencies
```

## 🛡️ Design Decisions

1. **Why Async?**: We use `asyncpg` and `httpx` to handle multiple competitor checks concurrently without blocking the main thread, ensuring the dashboard remains responsive.
2. **Why Server-Side Rendering?**: For this use case, a separate React frontend would add unnecessary complexity. Jinja2 templates allow for rapid iteration and a single deployment unit, perfect for an MVP.
3. **Data Integrity**: We store the *processed* text, not just the raw HTML, ensuring that our historical diffs remain valid even if our cleaning logic changes in the future.
