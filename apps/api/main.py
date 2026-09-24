from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import social, marketplace

app = FastAPI(
    title="TAKEUP API",
    description="Backend API for TAKEUP social marketplace",
    version="1.0.0"
)

# CORS setup for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For dev, allow all to avoid Next.js issues
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(social.router)
app.include_router(marketplace.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to TAKEUP API"}
