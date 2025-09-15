from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from controllers.user_controller import router

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]

methods = ["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=methods,
    allow_headers=["*"],
)

app.include_router(router=router)


@app.get("")
@app.get("/")
async def root() -> dict[str, Any]:
    return {"detail": "Welcome to the API"}