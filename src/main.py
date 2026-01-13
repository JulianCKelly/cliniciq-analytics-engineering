from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
from typing import Optional
import io

app = FastAPI(
    title="ClinicIQ Backend Core",
    description="Backend API for uploading EMR CSV data and basic login auth",
    version="0.1.0"
)

# CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to frontend URL in production env
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simulated user database (replace with PostgreSQL later)
users = {
    "admin@cliniciq.com": {
        "password": "secure123",
        "name": "Admin User"
    }
}


# Login model
class LoginRequest(BaseModel):
    email: str
    password: str


# Login endpoint
@app.post("/login")
def login(credentials: LoginRequest):
    user = users.get(credentials.email)
    if not user or user["password"] != credentials.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {
        "message": f"Welcome back, {user['name']}!",
        "email": credentials.email
    }


# EMR upload endpoint
@app.post("/upload-emr/")
async def upload_emr(file: UploadFile = File(...)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are accepted.")

    content = await file.read()
    try:
        df = pd.read_csv(io.BytesIO(content))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"CSV read error: {str(e)}")

    return {
        "message": "File uploaded successfully.",
        "columns": df.columns.tolist(),
        "preview": df.head(3).to_dict(orient="records")
    }


# Health check
@app.get("/")
def root():
    return {"message": "ClinicIQ Backend is live."}