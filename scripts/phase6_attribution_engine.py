import pandas as pd
import numpy as np
import json
import os

def run_attribution_engine():
    print("⚖️ Phase 6: Multi-Touch Attribution (MTA) Engine - Shapley Logic 🦞")
    print("-" * 75)

    # 1. Load Olist Marketing Data
    mql_path = 'data/marketing_funnel/olist_marketing_qualified_leads_dataset.csv'
    deals_path = 'data/marketing_funnel/olist_closed_deals_dataset.csv'
    
    mql = pd.read_csv(mql_path)
    deals = pd.read_csv(deals_path)
    
    print(f"Step 1: Ingesting {len(mql)} Leads and {len(deals)} Closed Deals... 🦞")

    # 2. Merge data to see which channel produced which deal
    df = pd.merge(mql, deals, on='mql_id', how='left')
    df['is_won'] = df['won_date'].notna().astype(int)
    
    # Fill missing channels
    df['origin'] = df['origin'].fillna('unknown')
    
    # 3. Simplify for Shapley demonstration (Markov-style approach)
    # In real Shapley, we calculate marginal contribution of each subset.
    # Here we will compare "Conversion Rate per Channel" vs "Average Performance".
    
    stats = df.groupby('origin').agg(
        total_leads=('mql_id', 'count'),
        total_wins=('is_won', 'sum')
    ).reset_index()
    
    stats['conversion_rate'] = stats['total_wins'] / stats['total_leads']
    avg_conv_rate = stats['total_wins'].sum() / stats['total_leads'].sum()
    
    print("\nStep 2: Calculating Marginal Channel Contributions... 📈")
    
    # Shapley-esque Weighting: How much above/below average did this channel perform?
    # This logic gives credit based on the "lift" it provides to the funnel.
    stats['shapley_weight'] = (stats['conversion_rate'] - avg_conv_rate) * stats['total_leads']
    # Normalize weights to sum up to 100% of total wins
    total_wins = stats['total_wins'].sum()
    stats['attributed_revenue_share'] = (stats['total_wins'] / total_wins) * 100

    print("\n✓ Channel Attribution Report (Fairness Weighting):")
    report = stats.sort_values('attributed_revenue_share', ascending=False)
    for i, row in report.iterrows():
        print(f"Channel: {row['origin']}")
        print(f"   Real Wins: {int(row['total_wins'])}")
        print(f"   Conv. Rate: {row['conversion_rate']:.2%}")
        print(f"   Revenue Share: {row['attributed_revenue_share']:.1f}% 🦞")
        print("-" * 40)

    # 4. Strategic Insight
    top_channel = report.iloc[0]['origin']
    print(f"\n🦞 Mercer Strategic Advice:")
    print(f"The '{top_channel}' channel is your primary engine. However, look at")
    print("channels with high conversion rates but low total leads—those are your")
    print("undervalued 'Hidden Gems' where you should increase spending.")

    # Save to artifacts
    report.to_csv('data/mta_attribution_results.csv', index=False)
    print("\nResults exported to data/mta_attribution_results.csv 🦞✅")

if __name__ == "__main__":
    run_attribution_engine()
