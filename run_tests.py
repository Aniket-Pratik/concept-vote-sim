#!/usr/bin/env python3
"""Simple test runner for concept-vote-sim"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_tally_functions():
    """Test the tally functions"""
    print("Testing tally functions...")
    
    from api.tally import plurality, approval, borda, condorcet
    
    # Test plurality
    options = ["Yellow", "Red", "Blue"]
    votes = [["Yellow"], ["Yellow"], ["Red"], ["Blue"], ["Yellow"]]
    tallies, winners = plurality(options, votes)
    assert tallies["Yellow"] == 3
    assert winners == ["Yellow"]
    print("✓ Plurality test passed")
    
    # Test Borda
    rankings = [["A", "B", "C"], ["B", "A", "C"], ["A", "C", "B"]]
    scores, winners = borda(["A", "B", "C"], rankings)
    assert winners == ["A"]
    assert scores["A"] > scores["B"] > scores["C"]
    print("✓ Borda test passed")
    
    print("All tally tests passed!")

def test_personas():
    """Test persona generation"""
    print("Testing persona generation...")
    
    from api.personas import synthetic_panel
    
    personas = synthetic_panel(5, seed=42)
    assert len(personas) == 5
    assert all("id" in p for p in personas)
    print("✓ Persona generation test passed!")

if __name__ == "__main__":
    print("Running concept-vote-sim tests...")
    try:
        test_tally_functions()
        test_personas()
        print("\n🎉 All tests passed! The implementation is working correctly.")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)
