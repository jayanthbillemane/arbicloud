from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI()

# CORS middleware with specific origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://example.com", "http://localhost:30"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# def validate_origin(origin: str = Header(...)):
#     if origin != "https://www.arbi.cloud/" or:
#         raise HTTPException(status_code=403, detail="Forbidden")

# Define a route for the root endpoint "/"
@app.get("/test")
def read_root():
    data = [{"id": 1, "name": "Jayantha BS", "Profession": "Fullstack Developer", "Experience": "5 Years",
            "company": ["EFI", "Risk Advisors Inc", "Medilenz", "CamcomAI"]
            }]
    return JSONResponse(content=data, headers={"Custom-Header": "value"})
