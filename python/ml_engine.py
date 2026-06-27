import sys
import json
import warnings
import pandas as pd
import numpy as np

warnings.filterwarnings('ignore')

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import (
    accuracy_score, f1_score,
    mean_squared_error, r2_score
)

# Classification models
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

# Regression models
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR


def badge(score, is_class):
    """Assign badge based on accuracy (classification) or R² (regression)."""
    val = score if not is_class else score
    if val >= 0.85:
        return 'Excellent'
    elif val >= 0.70:
        return 'Good'
    else:
        return 'Fair'


def preprocess(df, target):
    """Drop rows with missing target, fill NaNs, encode categoricals."""
    df = df.dropna(subset=[target])

    # Separate features and target
    X = df.drop(columns=[target])
    y = df[target]

    # Fill missing numeric with median, categorical with mode
    for col in X.columns:
        if X[col].dtype == object:
            X[col] = X[col].fillna(X[col].mode()[0] if not X[col].mode().empty else 'missing')
        else:
            X[col] = X[col].fillna(X[col].median())

    # Encode categoricals in X
    for col in X.columns:
        if X[col].dtype == object:
            le = LabelEncoder()
            X[col] = le.fit_transform(X[col].astype(str))

    # Encode target if classification and it's a string
    if y.dtype == object:
        le_y = LabelEncoder()
        y = le_y.fit_transform(y.astype(str))

    return X, y


def run_classification(X_train, X_test, y_train, y_test):
    models = [
        ('K-Nearest Neighbors', KNeighborsClassifier(n_neighbors=5)),
        ('Naive Bayes', GaussianNB()),
        ('Support Vector Machine', SVC(kernel='rbf', probability=False, max_iter=1000)),
        ('Logistic Regression', LogisticRegression(max_iter=500)),
        ('Decision Tree', DecisionTreeClassifier(random_state=42)),
        ('Random Forest', RandomForestClassifier(n_estimators=100, random_state=42)),
    ]

    results = []
    for name, model in models:
        try:
            model.fit(X_train, y_train)
            preds = model.predict(X_test)
            acc = round(float(accuracy_score(y_test, preds)), 4)
            f1  = round(float(f1_score(y_test, preds, average='weighted', zero_division=0)), 4)
            results.append({
                'name': name,
                'accuracy': acc,
                'f1': f1,
                'rmse': None,
                'r2': None,
                'badge': badge(acc, is_class=True)
            })
        except Exception as e:
            results.append({
                'name': name,
                'accuracy': None,
                'f1': None,
                'rmse': None,
                'r2': None,
                'badge': 'Error',
                'error': str(e)
            })

    return results


def run_regression(X_train, X_test, y_train, y_test):
    models = [
        ('Linear Regression', LinearRegression()),
        ('Ridge Regression', Ridge(alpha=1.0)),
        ('Decision Tree Regressor', DecisionTreeRegressor(random_state=42)),
        ('Random Forest Regressor', RandomForestRegressor(n_estimators=100, random_state=42)),
        ('SVR', SVR(kernel='rbf', max_iter=1000)),
    ]

    results = []
    for name, model in models:
        try:
            model.fit(X_train, y_train)
            preds = model.predict(X_test)
            rmse = round(float(np.sqrt(mean_squared_error(y_test, preds))), 4)
            r2   = round(float(r2_score(y_test, preds)), 4)
            results.append({
                'name': name,
                'accuracy': None,
                'f1': None,
                'rmse': rmse,
                'r2': r2,
                'badge': badge(r2, is_class=False)
            })
        except Exception as e:
            results.append({
                'name': name,
                'accuracy': None,
                'f1': None,
                'rmse': None,
                'r2': None,
                'badge': 'Error',
                'error': str(e)
            })

    return results


def main():
    if len(sys.argv) < 4:
        print(json.dumps({'error': 'Usage: ml_engine.py <csv_path> <target_column> <task_type>'}))
        sys.exit(1)

    csv_path    = sys.argv[1]
    target_col  = sys.argv[2]
    task_type   = sys.argv[3].lower()  # 'classification' or 'regression'

    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        print(json.dumps({'error': f'Failed to read CSV: {str(e)}'}))
        sys.exit(1)

    if target_col not in df.columns:
        print(json.dumps({'error': f'Target column "{target_col}" not found in CSV'}))
        sys.exit(1)

    try:
        X, y = preprocess(df, target_col)
    except Exception as e:
        print(json.dumps({'error': f'Preprocessing failed: {str(e)}'}))
        sys.exit(1)

    if len(X) < 10:
        print(json.dumps({'error': 'Dataset too small (need at least 10 rows after cleaning)'}))
        sys.exit(1)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    if task_type == 'classification':
        model_results = run_classification(X_train, X_test, y_train, y_test)
    elif task_type == 'regression':
        model_results = run_regression(X_train, X_test, y_train, y_test)
    else:
        print(json.dumps({'error': f'Unknown task type: {task_type}'}))
        sys.exit(1)

    output = {
        'task': task_type,
        'rows': int(len(df)),
        'columns': int(len(df.columns)),
        'target': target_col,
        'models': model_results
    }

    print(json.dumps(output))


if __name__ == '__main__':
    main()
