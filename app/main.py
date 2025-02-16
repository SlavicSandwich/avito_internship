from fastapi import FastAPI
from app.routers import auth, users, items
from app.database import engine, Base

Base.metadata.create_all(bind=engine)



app = FastAPI(
    title="API Avito Shop",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(items.router)