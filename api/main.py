import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from .models import VoteRequest, VoteResponse
from .vote import run_vote

load_dotenv()
app = FastAPI(title="Concept Vote Simulator")
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

@app.get("/healthz")
def healthz(): return {"ok": True}

@app.post("/v1/concept/vote", response_model=VoteResponse)
def concept_vote(req: VoteRequest):
    if "OPENAI_API_KEY" not in os.environ:
        raise HTTPException(500, "Missing OPENAI_API_KEY")
    return run_vote(req)
