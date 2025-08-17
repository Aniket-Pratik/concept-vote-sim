from typing import List, Dict
import itertools, math

def plurality(options:List[str], votes:List[List[str]]) -> tuple[Dict[str,int], List[str]]:
    # votes: each is [top_choice]
    counts = {o:0 for o in options}
    for v in votes:
        if v: counts[v[0]] += 1
    maxv = max(counts.values()) if counts else 0
    winners = [o for o,c in counts.items() if c==maxv]
    return counts, winners

def approval(options:List[str], approvals:List[List[str]]) -> tuple[Dict[str,int], List[str]]:
    counts = {o:0 for o in options}
    for a in approvals:
        for o in a:
            if o in counts: counts[o]+=1
    maxv = max(counts.values()) if counts else 0
    winners = [o for o,c in counts.items() if c==maxv]
    return counts, winners

def borda(options:List[str], rankings:List[List[str]]) -> tuple[Dict[str,int], List[str]]:
    # m options; top gets m-1 points
    m=len(options)
    scores = {o:0 for o in options}
    for r in rankings:
        for i,opt in enumerate(r):
            scores[opt] += (m - i - 1)
    maxv = max(scores.values()) if scores else 0
    winners = [o for o,s in scores.items() if s==maxv]
    return scores, winners

def condorcet(options:List[str], rankings:List[List[str]]) -> tuple[Dict[str,Dict[str,int]], List[str]]:
    # pairwise wins
    idx = {o:i for i,o in enumerate(options)}
    pair = {a:{b:0 for b in options if b!=a} for a in options}
    for r in rankings:
        pos = {o:i for i,o in enumerate(r)}
        for a,b in itertools.permutations(options,2):
            if pos[a] < pos[b]:
                pair[a][b]+=1
    # candidate that beats all others
    winners=[]
    for a in options:
        if all(pair[a][b] > pair[b][a] for b in options if b!=a):
            winners.append(a)
    return pair, winners
