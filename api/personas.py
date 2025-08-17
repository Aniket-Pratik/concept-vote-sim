import random, os
import numpy as np

ARCHETYPES = [
  {"name":"Trendsetter GenZ","age_range":(18,25),"region":"Urban","traits":["bold","playful","novelty-seeking"],"interests":["streetwear","gaming","music festivals"]},
  {"name":"Health-Focused Millennial","age_range":(26,39),"region":"Urban","traits":["clean","fresh","trust"],"interests":["fitness","smoothies","running"]},
  {"name":"Value-Conscious Parent","age_range":(30,50),"region":"Suburban","traits":["practical","family-friendly"],"interests":["groceries","coupons","school runs"]},
  {"name":"Traditionalist","age_range":(35,60),"region":"Tier-2/3","traits":["familiar","safe","low-risk"],"interests":["TV","local fairs","cricket"]},
  {"name":"Design Nerd","age_range":(20,40),"region":"Urban","traits":["aesthetic","minimal","contrast"],"interests":["fonts","branding","UX"]},
  # Enhanced Gen Z personas for your use case
  {"name":"Social Media Influencer GenZ","age_range":(18,25),"region":"Urban","traits":["trendy","social","creative"],"interests":["Instagram","TikTok","fashion","photography"]},
  {"name":"Gaming Enthusiast GenZ","age_range":(18,25),"region":"Urban","traits":["tech-savvy","competitive","immersive"],"interests":["gaming","streaming","esports","tech"]},
  {"name":"Street Culture GenZ","age_range":(18,25),"region":"Urban","traits":["authentic","rebellious","community"],"interests":["hip-hop","street art","sneakers","urban culture"]},
  {"name":"Digital Creator GenZ","age_range":(18,25),"region":"Urban","traits":["innovative","expressive","connected"],"interests":["content creation","digital art","social platforms","trends"]},
  {"name":"Fashion Forward GenZ","age_range":(18,25),"region":"Urban","traits":["stylish","confident","trend-aware"],"interests":["fashion","beauty","lifestyle","brands"]}
]

def synthetic_panel(n:int, seed:int|None=None):
    if seed is not None:
        random.seed(seed); np.random.seed(seed)
    out=[]
    for i in range(n):
        a = random.choice(ARCHETYPES)
        age = int(np.clip(np.random.normal(np.mean(a["age_range"]), 4), a["age_range"][0], a["age_range"][1]))
        out.append({
            "id": f"SYN{i:03d}",
            "archetype": a["name"],
            "age": age,
            "region": a["region"],
            "traits": a["traits"],
            "interests": a["interests"]
        })
    return out

# Enhanced PersonaHub integration for Gen Z targeting
def personahub_panel(n:int, keyword:str|None=None):
    try:
        from datasets import load_dataset
        ds = load_dataset("proj-persona/PersonaHub","persona",split="train",streaming=True)
        res=[]
        
        # Enhanced search for Gen Z personas
        genz_keywords = ["gen z", "gen-z", "18-25", "young adult", "millennial", "social media", "trendy", "bold", "playful", "energetic"]
        
        for row in ds:
            txt = row.get("persona") or str(row)
            txt_lower = txt.lower()
            
            # If keyword is specified, check for it
            if keyword and keyword.lower() not in txt_lower:
                continue
                
            # Prioritize Gen Z personas
            genz_score = sum(1 for kw in genz_keywords if kw in txt_lower)
            
            if genz_score > 0:  # Found Gen Z relevant persona
                res.append({
                    "id": f"PH{len(res):03d}", 
                    "persona_text": txt,
                    "genz_relevance": genz_score,
                    "source": "PersonaHub"
                })
            elif len(res) < n//2:  # Add some other personas for diversity
                res.append({
                    "id": f"PH{len(res):03d}", 
                    "persona_text": txt,
                    "genz_relevance": 0,
                    "source": "PersonaHub"
                })
                
            if len(res) >= n: 
                break
                
        # Sort by Gen Z relevance
        res.sort(key=lambda x: x.get("genz_relevance", 0), reverse=True)
        
        if not res:   # fallback to unfiltered
            ds2 = load_dataset("proj-persona/PersonaHub","persona",split="train",streaming=True)
            for row in ds2:
                txt = row.get("persona") or str(row)
                res.append({
                    "id": f"PH{len(res):03d}", 
                    "persona_text": txt,
                    "genz_relevance": 0,
                    "source": "PersonaHub"
                })
                if len(res) >= n: 
                    break
                    
        return res[:n]
        
    except ImportError:
        print("PersonaHub not available, falling back to synthetic personas")
        return synthetic_panel(n)
    except Exception as e:
        print(f"PersonaHub error: {e}, falling back to synthetic personas")
        return synthetic_panel(n)

# Specialized Gen Z persona generator
def genz_synthetic_panel(n:int, seed:int|None=None):
    """Generate synthetic Gen Z personas specifically for your target audience"""
    if seed is not None:
        random.seed(seed); np.random.seed(seed)
    
    genz_archetypes = [a for a in ARCHETYPES if "GenZ" in a["name"] or a["age_range"][0] <= 25]
    
    out = []
    for i in range(n):
        a = random.choice(genz_archetypes)
        age = random.randint(18, 25)
        
        # Add more Gen Z specific details
        social_platforms = ["Instagram", "TikTok", "Snapchat", "Twitter", "YouTube"]
        genz_interests = ["streetwear", "gaming", "music", "fitness", "travel", "food", "beauty", "tech"]
        
        out.append({
            "id": f"GENZ{i:03d}",
            "archetype": a["name"],
            "age": age,
            "region": a["region"],
            "traits": a["traits"] + ["social-media-savvy", "trend-aware"],
            "interests": a["interests"] + random.sample(genz_interests, 2),
            "social_platforms": random.sample(social_platforms, 2),
            "generation": "Gen Z"
        })
    
    return out
