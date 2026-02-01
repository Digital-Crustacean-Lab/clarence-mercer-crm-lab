import pandas as pd
import psycopg2
import json
import os
from psycopg2.extras import execute_values

# Load DB config
CONFIG_PATH = os.path.expanduser("~/.config/clawdbot/db-config.json")
with open(CONFIG_PATH, 'r') as f:
    db_config = json.load(f)["databases"][0]

def import_bank_data():
    file_path = 'data/bank_marketing/bank-full.csv'
    print(f"Reading {file_path}... 🦞")
    
    # Read CSV with semicolon delimiter
    df = pd.read_csv(file_path, sep=';')
    
    # Connect to DB
    conn = psycopg2.connect(
        host=db_config["host"],
        port=db_config["port"],
        database=db_config["database"],
        user=db_config["user"],
        password=db_config["password"]
    )
    cur = conn.cursor()
    
    # Create Table Schema
    create_table_query = """
    CREATE TABLE IF NOT EXISTS bank_marketing (
        id SERIAL PRIMARY KEY,
        age INT,
        job VARCHAR(50),
        marital VARCHAR(20),
        education VARCHAR(20),
        "default" VARCHAR(10),
        balance INT,
        housing VARCHAR(10),
        loan VARCHAR(10),
        contact VARCHAR(20),
        day INT,
        month VARCHAR(10),
        duration INT,
        campaign INT,
        pdays INT,
        previous INT,
        poutcome VARCHAR(20),
        y VARCHAR(10)
    );
    TRUNCATE TABLE bank_marketing;
    """
    cur.execute(create_table_query)
    
    print(f"Starting batch import of {len(df)} records into bank_marketing... 🦞")
    
    # Convert dataframe to list of tuples
    records = df.to_records(index=False).tolist()
    
    insert_query = """
    INSERT INTO bank_marketing (age, job, marital, education, "default", balance, housing, loan, contact, day, month, duration, campaign, pdays, previous, poutcome, y)
    VALUES %s
    """
    
    execute_values(cur, insert_query, records)
    
    conn.commit()
    print(f"✓ Successfully imported {len(df)} bank records! 🦞")
    
    cur.close()
    conn.close()

if __name__ == "__main__":
    import_bank_data()
