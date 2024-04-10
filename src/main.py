from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import posts, users, votes, auth


app = FastAPI()
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
all_routers = [posts.router, users.router, votes.router, auth.router]
for router in all_routers:
    app.include_router(router)


@app.get("/")
async def root():
    return {"message": "Backend application is running, I swear!"}
