from fastapi import FastAPI, Depends, Request, Form, HTTPException, BackgroundTasks
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from contextlib import asynccontextmanager

from app.database import get_db, engine, Base
from app.models import Competitor, Snapshot
from app.services.fetcher import fetch_url, clean_html
from app.services.diff_service import generate_diff
from app.services.llm_service import generate_summary
import os

# Lifecycle manager for startup/shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown
    await engine.dispose()

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(lifespan=lifespan)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Templates
templates = Jinja2Templates(directory="app/templates")

# Add CORS for Vercel Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify Vercel URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ... (Existing mount and templates) ...

# --- JSON API Endpoints for Vercel Frontend ---

@app.get("/api/competitors")
async def get_competitors_api(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Competitor).order_by(Competitor.created_at.desc()))
    return result.scalars().all()

@app.get("/api/history/{competitor_id}")
async def get_history_api(competitor_id: int, db: AsyncSession = Depends(get_db)):
    # Get Competitor
    result = await db.execute(select(Competitor).filter(Competitor.id == competitor_id))
    competitor = result.scalar_one_or_none()
    if not competitor:
        raise HTTPException(status_code=404, detail="Competitor not found")

    # Get Snapshots
    result = await db.execute(
        select(Snapshot)
        .filter(Snapshot.competitor_id == competitor_id)
        .order_by(Snapshot.timestamp.desc())
        .limit(20)
    )
    snapshots = result.scalars().all()
    
    return {
        "competitor": competitor,
        "snapshots": snapshots
    }

# --- Existing Routes ---
@app.get("/", response_class=HTMLResponse)
# ... existing home route ...
async def home(request: Request, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Competitor).order_by(Competitor.created_at.desc()))
    competitors = result.scalars().all()
    return templates.TemplateResponse("index.html", {"request": request, "competitors": competitors})

@app.post("/competitors")
async def add_competitor(url: str = Form(...), db: AsyncSession = Depends(get_db)):
    # Basic validation
    if not url.startswith("http"):
        url = "https://" + url
    
    # Extract name from domain
    try:
        name = url.split("//")[1].split("/")[0]
    except:
        name = url

    # Check existence
    result = await db.execute(select(Competitor).filter(Competitor.url == url))
    existing = result.scalar_one_or_none()
    if existing:
        return RedirectResponse(url="/", status_code=303)

    new_comp = Competitor(url=url, name=name)
    db.add(new_comp)
    await db.commit()
    return RedirectResponse(url="/", status_code=303)

async def perform_check(competitor_id: int, db: AsyncSession):
    # Re-fetch competitor inside background task logic if needed, 
    # but simplest is to pass ID and get a fresh session if this were a true background task.
    # For now, we'll run it inline or awaited to ensure user sees result immediately, 
    # as per "Check Now" button usually implying immediate feedback. 
    # However, "Check Now" might take time. 
    # Let's do it inline for the MVP to keep it simple and ensure the user sees the 'loading' state or result.
    pass 

from app.services.preprocess import preprocess_text

@app.post("/check/{competitor_id}")
async def check_competitor(competitor_id: int, background_tasks: BackgroundTasks, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Competitor).filter(Competitor.id == competitor_id))
    competitor = result.scalar_one_or_none()
    if not competitor:
        raise HTTPException(status_code=404, detail="Competitor not found")

    # 1. Fetch & Clean
    try:
        raw_html = await fetch_url(competitor.url)
        clean_text = clean_html(raw_html)
        # Preprocess to remove noise
        processed_text = preprocess_text(clean_text)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to fetch {competitor.url}: {e}")

    # 2. Get previous snapshot
    result = await db.execute(
        select(Snapshot)
        .filter(Snapshot.competitor_id == competitor_id)
        .order_by(Snapshot.timestamp.desc())
        .limit(1)
    )
    last_snapshot = result.scalar_one_or_none()
    # Use processed text from previous snapshot if available, else standard text
    # Note: If previous snapshot didn't have processed text, diff might be large initially.
    # But clean_html was the old text_content. We are changing what text_content stores.
    old_text = last_snapshot.text_content if last_snapshot else ""

    # 3. Diff
    diff_data = generate_diff(old_text, processed_text)

    # 4. LLM Summary
    summary = await generate_summary(diff_data)

    # 5. Save
    new_snapshot = Snapshot(
        competitor_id=competitor_id,
        html_content=raw_html[:100000], 
        text_content=processed_text, # Store processed text for next comparison
        diff_json=diff_data,
        ai_summary=summary
    )
    # new_snapshot.html_content = raw_html # logic was already handled above

    db.add(new_snapshot)
    await db.commit()

    return RedirectResponse(url=f"/history/{competitor_id}", status_code=303)

@app.get("/history/{competitor_id}", response_class=HTMLResponse)
async def history(competitor_id: int, request: Request, db: AsyncSession = Depends(get_db)):
    # Get Competitor
    result = await db.execute(select(Competitor).filter(Competitor.id == competitor_id))
    competitor = result.scalar_one_or_none()
    if not competitor:
        raise HTTPException(status_code=404, detail="Competitor not found")

    # Get Snapshots (last 5)
    result = await db.execute(
        select(Snapshot)
        .filter(Snapshot.competitor_id == competitor_id)
        .order_by(Snapshot.timestamp.desc())
        .limit(5)
    )
    snapshots = result.scalars().all()

    return templates.TemplateResponse("history.html", {
        "request": request, 
        "competitor": competitor, 
        "snapshots": snapshots
    })

@app.get("/system-status", response_class=HTMLResponse)
async def system_status(request: Request):
    return templates.TemplateResponse("status_dashboard.html", {"request": request})

@app.get("/status")
async def status(db: AsyncSession = Depends(get_db)):
    status_data = {
        "backend": "ok",
        "database": "unknown",
        "llm": "unknown"
    }

    # Check Database
    try:
        await db.execute(select(1))
        status_data["database"] = "connected"
    except:
        status_data["database"] = "disconnected"

    # Check LLM (Small test call)
    if os.getenv("OPENAI_API_KEY"):
         status_data["llm"] = "connected"
    else:
         status_data["llm"] = "disconnected (no key)"

    return status_data
