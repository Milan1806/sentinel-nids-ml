import sys
import os
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score

# 1. Setup Paths (So Python finds your files)
# Get the directory where THIS script is located
current_dir = os.path.dirname(os.path.abspath(__file__))
# Get the Project Root (2 levels up)
project_root = os.path.abspath(os.path.join(current_dir, '../../'))
sys.path.append(project_root)

# Import the "Brain" (Preprocessing logic)
try:
    from src.common.preprocessing import load_and_preprocess
except ImportError:
    print("Error: Could not find 'src/common/preprocessing.py'. Did you create it?")
    sys.exit(1)

def train():
    print("Starting Training Pipeline...")

    # Define paths to the data you just downloaded
    train_path = os.path.join(project_root, "data/raw/KDDTrain+.txt")
    test_path = os.path.join(project_root, "data/raw/KDDTest+.txt")

    # 2. Check if data exists
    if not os.path.exists(train_path):
        print(f"Error: File not found at {train_path}")
        return

    # 3. Load and Preprocess
    print("   Loading Training Data... (This prepares the data)")
    X_train, y_train = load_and_preprocess(train_path, train=True)

    print("   Loading Test Data...")
    X_test, y_test = load_and_preprocess(test_path, train=False)

    # 4. Train Model
    print("   Training Random Forest Model... (Please wait...)")
    model = RandomForestClassifier(n_estimators=100, n_jobs=-1, random_state=42)
    model.fit(X_train, y_train)

    # 5. Evaluate
    print("   Evaluating Model...")
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"\nModel Trained! Test Accuracy: {accuracy:.4f}")
    
    # 6. Save the Model
    model_dir = os.path.join(project_root, "models")
    os.makedirs(model_dir, exist_ok=True)
    save_path = os.path.join(model_dir, "rf_model.pkl")
    joblib.dump(model, save_path)
    print(f"Model saved to: {save_path}")

if __name__ == "__main__":
    train()