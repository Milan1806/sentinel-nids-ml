import joblib
import pandas as pd
from sklearn.metrics import confusion_matrix, classification_report
import seaborn as sns
import matplotlib.pyplot as plt

# Load model
model = joblib.load("models/random_forest.pkl")

# Load test data
df = pd.read_csv("data/NSL_KDD_test.csv")
X = df.drop("label", axis=1)
y = df["label"]

y_pred = model.predict(X)

print(classification_report(y, y_pred))

cm = confusion_matrix(y, y_pred)
sns.heatmap(cm, annot=True, fmt="d")
plt.title("Confusion Matrix")
plt.show()
