from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI()

# CORS middleware with specific origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://example.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define a route for the root endpoint "/"
@app.get("/")
def read_root():
    data = [{"id": 1, "name": "Jayantha BS", "Profession": "Fullstack Developer", "Experience": "5 Years",
            "company": ["EFI", "Risk Advisors Inc", "Medilenz", "CamcomAI","hobi":"Cricket"]
            }]
    return JSONResponse(content=data, headers={"Custom-Header": "value"})
