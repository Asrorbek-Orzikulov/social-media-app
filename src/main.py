from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routers import auth, users, posts, votes, videos
from src.database import lifespan


app = FastAPI(lifespan=lifespan)
origins = [
    "http://localhost:8000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
all_modules = [auth, users, posts, votes, videos]
for module in all_modules:
    app.include_router(module.router)


@app.get("/")
async def root():
    return {"message": "Backend application is running, I swear!"}
