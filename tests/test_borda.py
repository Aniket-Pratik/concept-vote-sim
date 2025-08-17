from api.tally import borda
def test_borda_basic():
    options = ["A","B","C"]
    rankings = [["A","B","C"],["B","A","C"],["A","C","B"]]
    scores, winners = borda(options, rankings)
    assert winners == ["A"] and scores["A"] > scores["B"] > scores["C"]
