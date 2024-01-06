from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Create an instance of the FastAPI class
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define a route for the root endpoint "/"
@app.get("/")
def read_root():
    return {"message": "Hello, World!"}
