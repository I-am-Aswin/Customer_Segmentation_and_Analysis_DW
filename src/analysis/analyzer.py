import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.impute import SimpleImputer

from sqlalchemy import create_engine

from ..db_connection import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME

# Database connection
engine = create_engine(f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

# Load customer summary data
df = pd.read_sql("SELECT * FROM customer_summary", engine)

# RFM Scoring
df['R'] = pd.qcut(df['recency'], 4, labels=[3, 2, 1, 0], duplicates="drop")  # Higher recency = lower score
df['F'] = pd.qcut(df['total_transactions'], 4, labels=[0, 1, 2], duplicates="drop")  # Higher frequency = higher score
df['M'] = pd.qcut(df['total_spent'], 4, labels=[0, 1, 2, 3], duplicates="drop")  # Higher monetary = higher score

# Combine RFM Scores
df['RFM_Score'] = df['R'].astype(str) + df['F'].astype(str) + df['M'].astype(str)

def rfm_level(df):
    if df['RFM_Score'][1:] in ['33', '23', '13', '03']:
        return 'Champions'
    elif df['RFM_Score'][1:] in ['32', '22', '12', '02']:
        return 'Potential Loyalists'
    elif df['RFM_Score'][1:] in ['31', '21', '11', '01']:
        return 'At Risk Customers'
    elif df['RFM_Score'][1:] in ['30', '20', '10', '00']:
        return 'Hibernating'
    else:
        return 'Other'

df['Customer_Segment'] = df.apply(rfm_level, axis=1)

# Save to CSV
# rfm_csv_path = r'E:\Programs\CustomerSegmentation_DW\src\visualizer\exports\rfm_segments.csv'
# df.to_csv(rfm_csv_path, index=False)
# print(f"RFM data saved to {rfm_csv_path}")


# Prepare features and target for churn prediction
X = df[['recency', 'total_transactions', 'total_spent']]
y = df['churn_flag']

imputer = SimpleImputer(strategy='mean')  # You can also use 'median' or 'most_frequent'
X = imputer.fit_transform(X)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train logistic regression model
model = LogisticRegression()
model.fit(X_train, y_train)

# Predict churn
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Churn Prediction Model Accuracy: {accuracy * 100:.2f}%")

# Save churn predictions to CSV
df['churn_prediction'] = model.predict(X)
# churn_csv_path = r'E:\Programs\CustomerSegmentation_DW\src\visualizer\exports\churn_predictions.csv'
# df.to_csv(churn_csv_path, index=False)
# print(f"Churn predictions saved to {churn_csv_path}")


# Estimate CLV using a basic model
df['predicted_clv'] = df['total_spent'] * (df['total_transactions'] / (df['recency'] + 1))

df = df.dropna()
# Save CLV data to CSV
clv_csv_path = r'E:\Programs\CustomerSegmentation_DW\src\visualizer\exports\clv_estimations.csv'
df.to_csv(clv_csv_path, index=False)
print(f"CLV estimations saved to {clv_csv_path}")