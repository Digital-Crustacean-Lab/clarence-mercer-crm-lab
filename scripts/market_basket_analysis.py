import pandas as pd
import psycopg2
import json
import os
from mlxtend.frequent_patterns import apriori, association_rules

# Load DB config
CONFIG_PATH = os.path.expanduser("~/.config/clawdbot/db-config.json")
with open(CONFIG_PATH, 'r') as f:
    db_config = json.load(f)["databases"][0]

def perform_mba():
    print("Connecting to database for Market Basket Analysis... 🦞")
    conn = psycopg2.connect(
        host=db_config["host"],
        port=db_config["port"],
        database=db_config["database"],
        user=db_config["user"],
        password=db_config["password"]
    )
    
    # We'll focus on France first as it's a manageable subset for demonstration
    query = "SELECT InvoiceNo, Description, Quantity FROM retail_transactions WHERE Country = 'France'"
    df = pd.read_sql(query, conn)
    conn.close()
    
    print(f"Fetched {len(df)} records for France. Preprocessing... 🦞")
    
    # 1. Clean descriptions (remove whitespace)
    # Note: PostgreSQL returns lowercase column names
    df['description'] = df['description'].str.strip()
    
    # 2. Pivot the data to create a basket format
    basket = (df.groupby(['invoiceno', 'description'])['quantity']
              .sum().unstack().reset_index().fillna(0)
              .set_index('invoiceno'))
    
    # 3. Convert quantities to 1 (bought) or 0 (not bought)
    def encode_units(x):
        if x <= 0:
            return 0
        if x >= 1:
            return 1
    
    # Use map instead of applymap for newer pandas
    basket_sets = basket.map(encode_units)
    
    # 4. Generate frequent itemsets
    print("Generating frequent itemsets (min_support=0.07)... 🦞")
    frequent_itemsets = apriori(basket_sets, min_support=0.07, use_colnames=True)
    
    # 5. Generate association rules
    print("Generating association rules... 🦞")
    rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1)
    
    # 6. Filter and sort rules
    top_rules = rules.sort_values('lift', ascending=False).head(10)
    
    print("\n✓ Top 10 Association Rules Found:")
    print(top_rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']])
    
    # Save to file
    top_rules.to_csv('data/market_basket_rules.csv', index=False)
    
    with open('data/mba_summary.txt', 'w') as f:
        f.write("--- Market Basket Analysis Summary (France) ---\n")
        f.write(f"Total Transactions analyzed: {len(basket_sets)}\n\n")
        f.write("Top Rules:\n")
        f.write(top_rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']].to_string())
        
    print("\n✓ Analysis complete. Results saved to data/market_basket_rules.csv 🦞")

if __name__ == "__main__":
    perform_mba()
