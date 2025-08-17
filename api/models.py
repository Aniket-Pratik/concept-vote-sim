from pydantic import BaseModel, Field, conint, field_validator
from typing import List, Literal, Optional, Dict

Mode = Literal["forced_choice","approval","ranking"]
Rule = Literal["plurality","approval","borda","condorcet"]
PersonaSource = Literal["synthetic","personahub","genz_synthetic"]

class VoteRequest(BaseModel):
    question: str = Field(..., min_length=5, description="e.g., Which color for the new drink brand?")
    brief: str = Field(..., min_length=40, description="Brand/product brief, target audience, constraints.")
    options: List[str] = Field(..., min_items=2, description="Choice labels, e.g., ['Yellow','Red','Blue']")
    mode: Mode = "forced_choice"
    rule: Rule = "plurality"
    n_voters: conint(ge=5, le=500) = 100
    persona_source: PersonaSource = "synthetic"
    persona_filter: Optional[str] = None    # if using PersonaHub
    temperature: float = 0.6
    seed: Optional[int] = None

    @field_validator("temperature")
    @classmethod
    def _temp_range(cls, v):
        if not (0.0 <= v <= 1.0): raise ValueError("temperature must be in [0,1]")
        return v

class VoterResult(BaseModel):
    id: str
    selection: List[str]             # forced_choice: [best]; approval: [approved...]; ranking: full order
    scores: Dict[str, float] = {}    # per-option 0..1 utility (optional)
    justification: str
    confidence: float                # 0..1

class VoteResponse(BaseModel):
    question: str
    options: List[str]
    rule: Rule
    mode: Mode
    sample: int
    generated_at: str
    winner: Optional[str] = None
    winners: Optional[List[str]] = None
    tallies: Dict[str, float]
    details: Dict[str, object]
    voters: List[VoterResult]
    notes: Optional[str] = None
