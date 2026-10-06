from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import social, marketplace, auth, users, categories, services, packages, seller, orders, messaging, notifications, buyer, admin
from core.config import settings

app = FastAPI(
    title="TAKEUP API",
    description="Backend API for TAKEUP social marketplace",
    version="1.0.0"
)

# CORS setup for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in settings.CORS_ORIGINS.split(",")], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include Routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(categories.router)
app.include_router(services.router)
app.include_router(packages.router)
app.include_router(seller.router)
app.include_router(orders.router)
app.include_router(messaging.router)
app.include_router(notifications.router)
app.include_router(buyer.router)
app.include_router(admin.router)
app.include_router(social.router)
app.include_router(marketplace.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to TAKEUP API"}
