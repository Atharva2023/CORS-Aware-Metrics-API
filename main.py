
import os
import time
import uuid
from statistics import mean

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

EMAIL = "25f1002516@ds.study.iitm.ac.in"
ALLOWED_ORIGIN = "https://dash-t4u9qh.example.com"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[ALLOWED_ORIGIN],
    allow_credentials=False,
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["*"],
)

@app.middleware("http")
async def response_headers(request: Request, call_next):
    start = time.perf_counter()
    request_id = str(uuid.uuid4())

    try:
        response = await call_next(request)
    except Exception:
        response = JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"},
        )

    elapsed = max(0.0, time.perf_counter() - start)
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time"] = f"{elapsed:.6f}"
    return response

@app.get("/stats")
async def get_stats(values: str = Query(...)):
    try:
        nums = [int(v.strip()) for v in values.split(",")]
        if not nums or any(v == "" for v in values.split(",")):
            raise ValueError
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="values must be comma-separated integers",
        )

    return {
        "email": EMAIL,
        "count": len(nums),
        "sum": sum(nums),
        "min": min(nums),
        "max": max(nums),
        "mean": mean(nums),
    }

