from thefuzz import fuzz, process
import pandas as pd
import json
import os

def run_identity_resolution_simple():
    print("Initializing Identity Resolution Lab (Fuzzy Match Edition)... 🆔 🦞")
    
    # Source A: Master Records
    data_a = [
        {"id": 1, "name": "John Smith", "email": "john.smith@gmail.com", "city": "London"},
        {"id": 2, "name": "Alice Wong", "email": "alice.w@yahoo.com", "city": "Hong Kong"},
        {"id": 3, "name": "Robert Mercer", "email": "mercer.r@lab.com", "city": "New York"}
    ]
    
    # Source B: Dirty Records from Social/Voice
    data_b = [
        {"id": 101, "name": "Jon Smith", "email": "john.smith@gmail.com", "city": "Lonon"},
        {"id": 102, "name": "Alice W.", "email": "alice88@wong.com", "city": "HK"},
        {"id": 103, "name": "Bob Mercer", "email": "mercer.r@lab.com", "city": "NYC"}
    ]
    
    results = []
    
    print("Analyzing and Linking Digital Ghosts... 🦞")
    for b in data_b:
        # Strategy: Cross-match name and email
        for a in data_a:
            # Calculate composite similarity
            name_score = fuzz.token_sort_ratio(a['name'], b['name'])
            email_score = 100 if a['email'] == b['email'] else 0
            
            # Weighted Score
            total_score = (name_score * 0.4) + (email_score * 0.6)
            
            if total_score > 60:
                results.append({
                    "master_id": a['id'],
                    "source_id": b['id'],
                    "master_name": a['name'],
                    "source_name": b['name'],
                    "confidence": total_score
                })
                
    print("\n✓ Identity Resolution Results:")
    for res in results:
        print(f"Match: {res['master_name']} <--> {res['source_name']}")
        print(f"Confidence Level: {res['confidence']:.1f}% 🦞")
        print("-" * 30)
        
    # Save to file
    with open('data/identity_linkage_simple.json', 'w') as f:
        json.dump(results, f, indent=4)
        
if __name__ == "__main__":
    run_identity_resolution_simple()
