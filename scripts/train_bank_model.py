import pandas as pd
import psycopg2
import json
import os
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.preprocessing import LabelEncoder

# Load DB config
CONFIG_PATH = os.path.expanduser("~/.config/clawdbot/db-config.json")
with open(CONFIG_PATH, 'r') as f:
    db_config = json.load(f)["databases"][0]

def train_model():
    print("Connecting to database to fetch bank data... 🦞")
    conn = psycopg2.connect(
        host=db_config["host"],
        port=db_config["port"],
        database=db_config["database"],
        user=db_config["user"],
        password=db_config["password"]
    )
    
    # Load data from PostgreSQL
    query = "SELECT * FROM bank_marketing"
    df = pd.read_sql(query, conn)
    conn.close()
    
    print(f"Fetched {len(df)} records. Starting preprocessing... 🦞")
    
    # Drop 'id' column as it's not a feature
    if 'id' in df.columns:
        df = df.drop('id', axis=1)
    
    # Preprocessing: Encode categorical variables
    categorical_cols = df.select_dtypes(include=['object']).columns
    le = LabelEncoder()
    
    for col in categorical_cols:
        df[col] = le.fit_transform(df[col])
    
    # Target variable is 'y'
    X = df.drop('y', axis=1)
    y = df['y']
    
    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Training Random Forest Classifier... 🦞")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Predictions
    y_pred = model.predict(X_test)
    
    # Evaluation
    acc = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)
    
    print(f"✓ Model Accuracy: {acc:.2f} 🦞")
    print("\nClassification Report:")
    print(report)
    
    # Feature Importance
    plt.figure(figsize=(10, 6))
    feat_importances = pd.Series(model.feature_importances_, index=X.columns)
    feat_importances.nlargest(10).plot(kind='barh', color='teal')
    plt.title('Top 10 Important Features for Term Deposit Subscription')
    plt.tight_layout()
    plt.savefig('data/bank_feature_importance.png')
    
    # Save metrics to a file
    with open('data/bank_model_results.txt', 'w') as f:
        f.write(f"Accuracy: {acc:.4f}\n\n")
        f.write("Classification Report:\n")
        f.write(report)
    
    print("✓ Analysis complete. Chart saved to data/bank_feature_importance.png 🦞")

if __name__ == "__main__":
    train_model()
