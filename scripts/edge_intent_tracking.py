import pandas as pd
import json
import psycopg2
import os
import random
from datetime import datetime

# Load DB config
CONFIG_PATH = os.path.expanduser("~/.config/clawdbot/db-config.json")
with open(CONFIG_PATH, 'r') as f:
    db_config = json.load(f)["databases"][0]

def simulate_edge_stream():
    """Simulates a stream of intents from Voice Assistants and Social Media."""
    intents = [
        {"source": "Alexa", "text": "I need to buy more premium ground coffee by tomorrow"},
        {"source": "Siri", "text": "Remind me to check the price of high-end espresso machines"},
        {"source": "TikTok_Shop", "text": "User liked 3 videos of artisanal lobster bisque recipes"},
        {"source": "Google_Home", "text": "Where is the nearest store selling organic sea salt?"},
        {"source": "Instagram", "text": "User commented 'Need this!' on a set of ceramic dinner plates"}
    ]
    
    products = ["Coffee", "Espresso Machine", "Lobster Bisque", "Organic Sea Salt", "Ceramic Plates"]
    
    results = []
    for i, item in enumerate(intents):
        # Mock NLP extraction logic
        raw_text = item["text"].lower()
        product = products[i]
        
        # Calculate Intent Level (0.0 to 1.0)
        # "Need", "Buy", "Tomorrow" increase the score
        score = 0.3
        if "need" in raw_text: score += 0.3
        if "buy" in raw_text: score += 0.3
        if "tomorrow" in raw_text: score += 0.1
        
        is_hot = score >= 0.7
        
        results.append((item["source"], item["text"], product, score, is_hot))
        
    return results

def upload_to_crm(data):
    print("Connecting to Digital Crustacean Warehouse... 🦞")
    conn = psycopg2.connect(
        host=db_config["host"],
        port=db_config["port"],
        database=db_config["database"],
        user=db_config["user"],
        password=db_config["password"]
    )
    cur = conn.cursor()
    
    print(f"Processing {len(data)} Edge Intents... 🦞")
    
    insert_query = """
    INSERT INTO edge_leads (source, raw_intent, extracted_product, intent_level, is_hot_lead)
    VALUES (%s, %s, %s, %s, %s)
    """
    
    cur.executemany(insert_query, data)
    conn.commit()
    
    print("✓ Successfully ingested Edge leads into PostgreSQL! 🦞")
    cur.close()
    conn.close()

if __name__ == "__main__":
    stream_data = simulate_edge_stream()
    upload_to_crm(stream_data)
