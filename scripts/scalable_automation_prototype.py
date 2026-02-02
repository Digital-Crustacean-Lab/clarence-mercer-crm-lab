import pandas as pd
import psycopg2
import json
import os
import requests
from datetime import datetime

# Load DB config
CONFIG_PATH = os.path.expanduser("~/.config/clawdbot/db-config.json")
with open(CONFIG_PATH, 'r') as f:
    db_config = json.load(f)["databases"][0]

def simulate_reverse_etl():
    """Simulates pushing high-priority model results back to a CRM endpoint (WebHook)."""
    print("Initializing Scalable Automation (Reverse ETL) Prototype... ⚙️ 🦞")
    
    # 1. Fetch High Intent Leads from PostgreSQL (from Direction 1)
    conn = psycopg2.connect(
        host=db_config["host"],
        port=db_config["port"],
        database=db_config["database"],
        user=db_config["user"],
        password=db_config["password"]
    )
    
    query = "SELECT source, raw_intent, extracted_product, intent_level FROM edge_leads WHERE is_hot_lead = TRUE"
    df_hot_leads = pd.read_sql(query, conn)
    conn.close()
    
    print(f"Found {len(df_hot_leads)} Hot Leads to sync... 🦞")
    
    # 2. Sync to 'Mock CRM' (using a public webhook tester or just printing)
    # In a real scenario, this would be RudderStack/Grouparoo pushing to Salesforce/Hubspot
    sync_results = []
    for index, row in df_hot_leads.iterrows():
        lead_payload = {
            "crm_id": f"EXT-{index+100}",
            "status": "High Priority",
            "source": row['source'],
            "intent_note": row['raw_intent'],
            "suggested_product": row['extracted_product'],
            "score": row['intent_level'],
            "action_required": "Immediate Follow-up"
        }
        
        # Simulating API Call
        print(f"Syncing Lead {lead_payload['crm_id']} to Salesforce via Reverse ETL... 🦞")
        sync_results.append(lead_payload)
        
    # Save log
    with open('data/reverse_etl_log.json', 'w') as f:
        json.dump(sync_results, f, indent=4)
        
    print("\n✓ Reverse ETL Sync Complete. Dashboard updated. 🦞")

if __name__ == "__main__":
    simulate_reverse_etl()
