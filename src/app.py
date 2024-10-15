from fastapi import FastAPI
from src.routing import client
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

app.include_router(client.router, prefix="/clients", tags=["client"])

@app.get("/")
def read_root():
    return {"message": "Hello World"}