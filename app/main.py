from fastapi import FastAPI
from .api.v1 import websites
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Coll Websites API")

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # or ["*"] for all
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.include_router(websites.router)

app.include_router(
    websites.router, 
    tags=["websites"]
)

@app.get("/")
def root():
    return {"message": "CoolWebsites API is running"}