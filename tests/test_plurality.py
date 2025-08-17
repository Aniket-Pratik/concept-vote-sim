from api.tally import plurality
def test_plurality_basic():
    options = ["Yellow","Red","Blue"]
    votes = [["Yellow"],["Yellow"],["Red"],["Blue"],["Yellow"]]
    tallies, winners = plurality(options, votes)
    assert tallies["Yellow"] == 3 and winners == ["Yellow"]
