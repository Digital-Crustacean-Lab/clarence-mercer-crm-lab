import pandas as pd
import psycopg2
import json
import os
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_curve, auc, RocCurveDisplay
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import SMOTE

# Load DB config
CONFIG_PATH = os.path.expanduser("~/.config/clawdbot/db-config.json")
with open(CONFIG_PATH, 'r') as f:
    db_config = json.load(f)["databases"][0]

def analyze_roc_curve():
    print("Fetching data for ROC analysis... 🦞")
    conn = psycopg2.connect(
        host=db_config["host"],
        port=db_config["port"],
        database=db_config["database"],
        user=db_config["user"],
        password=db_config["password"]
    )
    
    query = "SELECT * FROM bank_marketing"
    df = pd.read_sql(query, conn)
    conn.close()
    
    if 'id' in df.columns:
        df = df.drop('id', axis=1)
    
    # Preprocessing
    categorical_cols = df.select_dtypes(include=['object']).columns
    le = LabelEncoder()
    for col in categorical_cols:
        df[col] = le.fit_transform(df[col])
    
    X = df.drop('y', axis=1)
    y = df['y']
    
    # Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Apply SMOTE
    sm = SMOTE(random_state=42)
    X_res, y_res = sm.fit_resample(X_train, y_train)
    
    # Train Optimized Model
    print("Training models for ROC comparison... 🦞")
    # 1. Optimized Model (SMOTE + Balanced)
    model_opt = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')
    model_opt.fit(X_res, y_res)
    
    # 2. Original Model (for comparison)
    model_orig = RandomForestClassifier(n_estimators=100, random_state=42)
    model_orig.fit(X_train, y_train)
    
    # Get predicted probabilities for the positive class (Class 1)
    y_prob_opt = model_opt.predict_proba(X_test)[:, 1]
    y_prob_orig = model_orig.predict_proba(X_test)[:, 1]
    
    # Compute ROC curve and ROC area for each model
    fpr_opt, tpr_opt, _ = roc_curve(y_test, y_prob_opt)
    roc_auc_opt = auc(fpr_opt, tpr_opt)
    
    fpr_orig, tpr_orig, _ = roc_curve(y_test, y_prob_orig)
    roc_auc_orig = auc(fpr_orig, tpr_orig)
    
    # Plotting
    plt.figure(figsize=(10, 8))
    plt.plot(fpr_opt, tpr_opt, color='darkorange', lw=2, label=f'Optimized Model (AUC = {roc_auc_opt:.2f})')
    plt.plot(fpr_orig, tpr_orig, color='navy', lw=2, linestyle='--', label=f'Original Model (AUC = {roc_auc_orig:.2f})')
    plt.plot([0, 1], [0, 1], color='gray', lw=1, linestyle=':')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate (1 - Specificity)')
    plt.ylabel('True Positive Rate (Sensitivity/Recall)')
    plt.title('ROC Curve: Bank Term Deposit Prediction')
    plt.legend(loc="lower right")
    plt.grid(alpha=0.3)
    
    # Save the plot
    output_path = 'data/bank_roc_curve.png'
    plt.savefig(output_path)
    print(f"✓ ROC Curve saved to {output_path} 🦞")
    print(f"✓ Optimized AUC: {roc_auc_opt:.4f}")
    print(f"✓ Original AUC: {roc_auc_orig:.4f}")

if __name__ == "__main__":
    analyze_roc_curve()
