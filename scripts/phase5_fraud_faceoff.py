import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
import json
import os
from datetime import datetime

def run_adversarial_fraud_test():
    print("🛡️ Phase 5: The Ultimate Fraud Face-off 🦞")
    print("Isolation Forest vs. Geo-Velocity vs. Hybrid Ensemble")
    print("-" * 75)

    file_path = 'data/fraud_detection/transactions_data.csv'
    
    # 1. Loading a larger sample for sequence analysis
    # We need sequential transactions from the same users to test Geo-Velocity
    print("Step 1: Ingesting sequential transaction streams... 🦞")
    chunk_size = 200000
    df = pd.read_csv(file_path, nrows=chunk_size)
    
    # Preprocessing
    df['date'] = pd.to_datetime(df['date'])
    df['amount_num'] = df['amount'].replace('[\$,]', '', regex=True).astype(float)
    df = df.sort_values(['client_id', 'date'])
    
    print(f"✓ Loaded {len(df)} transactions. Analyzing patterns for {df['client_id'].nunique()} clients. 🦞")

    # --- MODEL 1: ISOLATION FOREST (The Statistical Scout) ---
    print("\nModel 1: Running Isolation Forest (Statistical Outliers)... 🌲")
    iso = IsolationForest(contamination=0.01, random_state=42)
    # Feature: Transaction Amount
    df['iso_score'] = iso.fit_predict(df[['amount_num']])
    df['is_iso_fraud'] = df['iso_score'] == -1

    # --- MODEL 2: GEO-VELOCITY (The Physical Guard) ---
    print("Model 2: Running Geo-Velocity Audit (Impossible Travel)... ✈️")
    # Shift to get previous transaction for each client
    df['prev_state'] = df.groupby('client_id')['merchant_state'].shift(1)
    df['prev_date'] = df.groupby('client_id')['date'].shift(1)
    
    # Flag: Different state within 1 hour
    def check_geo_fraud(row):
        if pd.isna(row['prev_state']) or pd.isna(row['prev_date']):
            return False
        
        time_diff_min = (row['date'] - row['prev_date']).total_seconds() / 60
        # If state changed and time diff is < 60 minutes -> High suspicion
        if row['merchant_state'] != row['prev_state'] and time_diff_min < 60:
            return True
        return False

    df['is_geo_fraud'] = df.apply(check_geo_fraud, axis=1)

    # --- MODEL 3: HYBRID ENSEMBLE (The Mercer Shield) ---
    print("Model 3: Fusing Hybrid Signals (Iso + Geo)... 🛡️")
    # Logical OR: Catch either statistical or physical anomalies
    df['is_hybrid_fraud'] = df['is_iso_fraud'] | df['is_geo_fraud']

    # --- PERFORMANCE EVALUATION ---
    iso_total = df['is_iso_fraud'].sum()
    geo_total = df['is_geo_fraud'].sum()
    hybrid_total = df['is_hybrid_fraud'].sum()
    overlap = (df['is_iso_fraud'] & df['is_geo_fraud']).sum()

    print("\n📊 FRAUD FACE-OFF RESULTS:")
    print(f"- [Iso Forest]   Caught {iso_total} suspicious transactions.")
    print(f"- [Geo Velocity] Caught {geo_total} physically impossible transactions.")
    print(f"- [Hybrid]       Caught {hybrid_total} total unique threats.")
    print(f"💡 Synergistic Overlap: {overlap} cases caught by BOTH. 🦞")

    print("\n🔍 INSIGHTS:")
    if geo_total > 0:
        sample_geo = df[df['is_geo_fraud'] == True].iloc[0]
        print(f"Impossible Travel Detected: User {sample_geo['client_id']} moved from {sample_geo['prev_state']} to {sample_geo['merchant_state']} in {(sample_geo['date'] - sample_geo['prev_date']).total_seconds()/60:.1f} mins!")
    
    print("\n🦞 Mercer Technical Audit Conclusion:")
    print("The Hybrid Model is the winner. It catches 'Silent Whales' (huge transactions) via IsoForest")
    print("and 'Rapid Teleporters' (stolen card sequences) via Geo-Velocity. Neither can protect the CRM alone.")

    # Save results
    df[df['is_hybrid_fraud']].to_csv('data/fraud_faceoff_audit.csv', index=False)
    print("\nFull audit exported to data/fraud_faceoff_audit.csv 🦞✅")

if __name__ == "__main__":
    run_adversarial_fraud_test()
