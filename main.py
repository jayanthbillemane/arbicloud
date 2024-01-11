from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
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
    data = [{"id":1,"name":"Jayantha BS","Profession":"Fullstack Developer","Experiance":"5 Years",
            "company":["EFI","Risk Advisors Inc","Medilenz","CamcomAI"]
            }]
    return JSONResponse(data)
