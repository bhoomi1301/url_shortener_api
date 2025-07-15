from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from . import models, schemas, database, utils
from sqlalchemy.future import select

app = FastAPI()

# Add CORS middleware to avoid "Failed to fetch" issues
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, use specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Redirect root ("/") to Swagger docs ("/docs")
@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")

@app.get("/health", include_in_schema=False)
async def health():
    return {"message": "URL Shortener API is running"}

# Create DB tables on startup
@app.on_event("startup")
async def startup():
    async with database.engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)

# POST endpoint to shorten URLs
@app.post("/shorten", response_model=schemas.URLInfo)
async def shorten_url(url: schemas.URLCreate, db: AsyncSession = Depends(database.get_db)):
    short_code = utils.generate_short_code()
    new_url = models.URL(original_url=url.original_url, short_code=short_code)
    db.add(new_url)
    await db.commit()
    await db.refresh(new_url)
    return {"short_url": f"http://localhost:8000/{short_code}"}

# GET endpoint to redirect shortened URLs
@app.get("/{short_code}")
async def redirect_url(short_code: str, db: AsyncSession = Depends(database.get_db)):
    result = await db.execute(select(models.URL).where(models.URL.short_code == short_code))
    url = result.scalars().first()
    if url:
        return RedirectResponse(url.original_url)
    raise HTTPException(status_code=404, detail="URL not found")

