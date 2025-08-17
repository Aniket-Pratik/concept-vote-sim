import os, json, random
from datetime import datetime, timezone
from typing import List, Dict
from openai import OpenAI
from .models import VoteRequest, VoteResponse, VoterResult
from .personas import synthetic_panel, personahub_panel, genz_synthetic_panel
from .tally import plurality, approval, borda, condorcet

MODEL = os.getenv("MODEL","gpt-4o-mini")
client = None  # Will be initialized when needed

SYSTEM = (
 "You are a consumer panelist. Use only the provided brand brief and options. "
 "Decide based on alignment with the target audience and the brief. "
 "No web browsing. Return only JSON."
)

def voter_prompt(persona:dict, brief:str, question:str, options:List[str], mode:str):
    persona_text = json.dumps(persona, ensure_ascii=False)
    return f"""
Persona:
{persona_text}

Brand Brief:
{brief}

Question: {question}
Options: {options}

Evaluation rubric (weigh as relevant): shelf visibility, brand personality fit, emotional impact, memorability,
cultural/age appropriateness, readability/accessibility. Penalize options that contradict constraints in the brief.

Task:
- Mode = {mode}
  * forced_choice: pick exactly ONE best option
  * approval: pick ANY number of acceptable options (>=1)
  * ranking: rank ALL options from best to worst with no ties
Also provide:
- per-option utility scores in [0,1] (subjective)
- a 1–2 sentence justification grounded in the brief
- a confidence score in [0,1]

Return STRICT JSON:
{{
  "selection": ["..."],                # forced_choice: [best]; approval: [accepted...]; ranking: full order
  "scores": {{"{options[0]}":0.0}},
  "justification": "",
  "confidence": 0.0
}}
"""

def gen_personas(req:VoteRequest):
    if req.persona_source == "synthetic":
        return synthetic_panel(req.n_voters, req.seed)
    elif req.persona_source == "genz_synthetic":
        return genz_synthetic_panel(req.n_voters, req.seed)
    else:
        return personahub_panel(req.n_voters, req.persona_filter)

def call_model(prompt:str, temperature:float):
    global client
    if client is None:
        if "OPENAI_API_KEY" not in os.environ:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    
    r = client.chat.completions.create(
        model=MODEL,
        temperature=temperature,
        response_format={"type":"json_object"},
        messages=[{"role":"system","content":SYSTEM},{"role":"user","content":prompt}]
    )
    return r.choices[0].message.content

def run_vote(req:VoteRequest) -> VoteResponse:
    personas = gen_personas(req)
    voters=[]
    for p in personas:
        prompt = voter_prompt(p, req.brief, req.question, req.options, req.mode)
        try:
            out = json.loads(call_model(prompt, req.temperature))
            # Validate that all selections are in the original options
            if "selection" in out and out["selection"]:
                valid_selections = [s for s in out["selection"] if s in req.options]
                if not valid_selections:
                    valid_selections = [req.options[0]]  # Fallback to first option
                out["selection"] = valid_selections
        except Exception:
            out = {"selection":[req.options[0]],"scores":{}, "justification":"fallback", "confidence":0.3}
        voters.append(VoterResult(
            id=p.get("id","anon"),
            selection=out.get("selection",[]),
            scores=out.get("scores",{}),
            justification=out.get("justification",""),
            confidence=float(out.get("confidence",0.0))
        ))

    # Aggregate per rule
    if req.rule == "plurality":
        tallies, winners = plurality(req.options, [v.selection[:1] for v in voters])
        winner = winners[0] if len(winners)==1 else None
        details = {"winners": winners}
    elif req.rule == "approval":
        tallies, winners = approval(req.options, [v.selection for v in voters])
        winner = winners[0] if len(winners)==1 else None
        details = {"winners": winners}
    elif req.rule == "borda":
        tallies, winners = borda(req.options, [v.selection for v in voters])
        winner = winners[0] if len(winners)==1 else None
        details = {"winners": winners}
    else:  # condorcet
        pair, winners = condorcet(req.options, [v.selection for v in voters])
        tallies = {"pairwise": pair}
        winner = winners[0] if winners else None
        details = {"winners": winners}

    return VoteResponse(
        question=req.question,
        options=req.options,
        rule=req.rule,
        mode=req.mode,
        sample=len(voters),
        generated_at=datetime.now(timezone.utc).isoformat(),
        winner=winner,
        winners=details.get("winners"),
        tallies=tallies,
        details=details,
        voters=voters,
        notes="Synthetic consumer panel; not representative of real customers."
    )
