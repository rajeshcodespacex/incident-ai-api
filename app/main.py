from fastapi import FastAPI
from .database import engine, Base
from .routers import auth, incidents, admin, users

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI-Powered IT Incident Support Assistant API",
    description="Automatically analyze IT incidents and get AI-powered resolution suggestions based on real enterprise experience",
    version="1.0.0"
)

@app.get("/healthy")
def health_check():
    return {"status": "Healthy"}

app.include_router(auth.router)
app.include_router(incidents.router)
app.include_router(admin.router)
app.include_router(users.router)