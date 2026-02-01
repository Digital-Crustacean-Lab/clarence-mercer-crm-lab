import pandas as pd
import psycopg2
import json
import os
from datetime import datetime

# Load DB config
CONFIG_PATH = os.path.expanduser("~/.config/clawdbot/db-config.json")
with open(CONFIG_PATH, 'r') as f:
    db_config = json.load(f)["databases"][0]

def import_data():
    file_path = 'data/Online Retail.xlsx'
    print(f"Reading {file_path}... This may take a minute. 🦞")
    
    # Read Excel
    df = pd.read_excel(file_path)
    
    # Basic cleaning
    # Drop rows without CustomerID for CRM analysis (standard practice)
    df = df.dropna(subset=['CustomerID'])
    
    # Ensure InvoiceDate is datetime object (not int/bigint)
    # Convert to standard datetime, handle potential errors
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    
    # Crucial: Convert timestamps to string format that PostgreSQL understands easily
    # This prevents the 'bigint' mismatch error during batch insertion
    df['InvoiceDate'] = df['InvoiceDate'].dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # Connect to DB
    conn = psycopg2.connect(
        host=db_config["host"],
        port=db_config["port"],
        database=db_config["database"],
        user=db_config["user"],
        password=db_config["password"]
    )
    cur = conn.cursor()
    
    print(f"Starting batch import of {len(df)} records... 🦞")
    
    # Use execute_values or fast batch insert
    from psycopg2.extras import execute_values
    
    # Convert dataframe to list of tuples
    records = df.to_records(index=False).tolist()
    
    # Clear table first to avoid duplicates if re-running
    cur.execute("TRUNCATE TABLE retail_transactions;")
    
    insert_query = """
    INSERT INTO retail_transactions (InvoiceNo, StockCode, Description, Quantity, InvoiceDate, UnitPrice, CustomerID, Country)
    VALUES %s
    """
    
    execute_values(cur, insert_query, records)
    
    conn.commit()
    print(f"✓ Successfully imported {len(df)} records into PostgreSQL! 🦞")
    
    cur.close()
    conn.close()

if __name__ == "__main__":
    import_data()
