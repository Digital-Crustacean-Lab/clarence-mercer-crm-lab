import pandas as pd
import numpy as np
from lifetimes import BetaGeoFitter
from lifetimes.utils import calibration_and_holdout_data
import os

def run_offline_backtest():
    print("Step 1: Loading all data... 🦞")
    file_path = 'data/Online Retail.xlsx'
    
    # Load all data but minimize columns to speed up
    df = pd.read_excel(file_path, usecols=['CustomerID', 'InvoiceDate'])
    df = df[df['CustomerID'].notna()]
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    
    # Filter for valid dates (some might be outliers)
    max_date = df['InvoiceDate'].max()
    min_date = df['InvoiceDate'].min()
    
    # Let's take a 6-month calibration and 3-month holdout
    # to ensure we have enough 'history' for the model to learn
    end_date_train = min_date + pd.Timedelta(days=180)
    end_date_holdout = end_date_train + pd.Timedelta(days=90)
    
    print(f"Total rows: {len(df)}")
    print(f"Calibration Period: {min_date.date()} to {end_date_train.date()}")
    print(f"Holdout Period: {end_date_train.date()} to {end_date_holdout.date()} 🦞")

    summary_holdout = calibration_and_holdout_data(
        df, 
        customer_id_col='CustomerID', 
        datetime_col='InvoiceDate',
        calibration_period_end=end_date_train,
        observation_period_end=end_date_holdout
    )
    
    # CLEANING: Remove zero vectors and INF values
    summary_holdout = summary_holdout[summary_holdout['T_cal'] > 0]

    print("Step 2: Training model (BG/NBD)... 🌲")
    bgf = BetaGeoFitter(penalizer_coef=0.1) # Higher penalizer for stability
    bgf.fit(summary_holdout['frequency_cal'], summary_holdout['recency_cal'], summary_holdout['T_cal'])

    print("Step 3: Prediction & Audit... 🔮")
    t = 90
    summary_holdout['predicted'] = bgf.predict(
        t, summary_holdout['frequency_cal'], summary_holdout['recency_cal'], summary_holdout['T_cal']
    )

    actual = summary_holdout['frequency_holdout']
    predicted = summary_holdout['predicted']
    
    # Filter out NaNs for correlation calculation
    mask = ~np.isnan(actual) & ~np.isnan(predicted)
    mae = np.mean(np.abs(actual[mask] - predicted[mask]))
    correlation = np.corrcoef(actual[mask], predicted[mask])[0, 1]

    print("\n" + "="*40)
    print("📊 BACKTESTING PERFORMANCE REPORT:")
    print(f"- Mean Absolute Error (MAE): {mae:.4f}")
    print(f"- Prediction Correlation:    {correlation:.4f} 🦞")
    print("="*40)
    
    if correlation > 0.5:
        print("\n✅ FINAL VERDICT: REAL ENGINE.")
    else:
        print("\n❌ FINAL VERDICT: PAPER TIGER (Requires more behavioral data).")

if __name__ == "__main__":
    run_offline_backtest()
