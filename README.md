# Concept Vote Simulator

LLM-based concept testing for brand colors, taglines, packaging, names, etc. Uses synthetic personas to simulate consumer voting panels.

## Setup

```bash
# macOS/Linux
python -m venv .venv && source .venv/bin/activate

# Windows
python -m venv .venv && .venv\Scripts\activate

pip install -r requirements.txt
cp env.example .env  # add OPENAI_API_KEY
```

## Run API

```bash
uvicorn api.main:app --reload --port 8000
```

## Try (curl)

```bash
curl -X POST http://localhost:8000/v1/concept/vote \
  -H 'content-type: application/json' \
  -d '{"question":"Which color for the drink brand?","brief":"Audience: Gen Z, bold playful; pop on shelf; avoid diet associations.","options":["Yellow","Red","Blue"],"mode":"ranking","rule":"borda","n_voters":50}'
```

## Run Dashboard

```bash
STREAMLIT_BROWSER_GATHER_USAGE_STATS=false streamlit run app/dashboard.py
```

## Features

- **Voting Modes**: forced choice, approval, ranking
- **Voting Rules**: plurality, approval, Borda count, Condorcet
- **Persona Sources**: synthetic archetypes or PersonaHub integration
- **LLM Voters**: GPT-4 powered consumer panelists
- **Non-political**: Brand/marketing concept testing only
