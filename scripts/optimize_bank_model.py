import pandas as pd
import psycopg2
import json
import os
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score, recall_score
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import SMOTE

# Load DB config
CONFIG_PATH = os.path.expanduser("~/.config/clawdbot/db-config.json")
with open(CONFIG_PATH, 'r') as f:
    db_config = json.load(f)["databases"][0]

def optimize_model():
    print("Connecting to database to fetch bank data... 🦞")
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
    
    print(f"Original training set distribution: {pd.Series(y_train).value_counts().to_dict()}")
    
    # Apply SMOTE to balance the training data
    print("Applying SMOTE to balance the classes... 🦞")
    sm = SMOTE(random_state=42)
    X_res, y_res = sm.fit_resample(X_train, y_train)
    
    print(f"Resampled training set distribution: {pd.Series(y_res).value_counts().to_dict()}")
    
    # Train Balanced Model
    print("Training Optimized Random Forest Classifier... 🦞")
    model = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')
    model.fit(X_res, y_res)
    
    y_pred = model.predict(X_test)
    
    # Evaluation
    acc = accuracy_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)
    
    print(f"✓ Optimized Model Accuracy: {acc:.2f} 🦞")
    print(f"✓ Optimized Model Recall (Class 1): {rec:.2f} 🦞")
    print("\nClassification Report (Optimized):")
    print(report)
    
    # Save results
    with open('data/bank_model_optimized_results.txt', 'w') as f:
        f.write("--- Optimized Model Results (SMOTE + Balanced Weight) ---\n")
        f.write(f"Accuracy: {acc:.4f}\n")
        f.write(f"Recall (Class 1): {rec:.4f}\n\n")
        f.write("Classification Report:\n")
        f.write(report)
        
    print("✓ Optimization complete. Detailed report saved to data/bank_model_optimized_results.txt 🦞")

if __name__ == "__main__":
    optimize_model()
