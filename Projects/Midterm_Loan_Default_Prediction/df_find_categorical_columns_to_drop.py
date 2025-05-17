
import pandas as pd
from sklearn.feature_selection import mutual_info_classif
from sklearn.preprocessing import LabelEncoder

def find_categorical_columns_to_drop(df, target_col=None, high_card_thresh=0.9, similarity_thresh=0.95, low_info_thresh=0.01):
    """
    Dynamically identifies categorical columns to drop based on:
    - Low variance (1 unique value)
    - High cardinality
    - Redundant/similar features
    - (Optionally) Low predictive value with target

    Parameters:
    df (pd.DataFrame): Input DataFrame
    target_col (str): Name of target column (optional)
    high_card_thresh (float): Threshold for high cardinality (e.g. 0.9 * len(df))
    similarity_thresh (float): Value similarity threshold to detect duplicate features
    low_info_thresh (float): Minimum mutual information score (if target_col is used)

    Returns:
    dict: Dictionary with reasons and list of columns to drop

    *** Customize Thresholds:
        - high_card_thresh=0.9: drop if >90% of values are unique
        - similarity_thresh=0.95: drop if >95% values match another column
        - low_info_thresh=0.01: drop if feature has low mutual info with target

    """
    drop_report = {
        "low_variance": [],
        "high_cardinality": [],
        "redundant": [],
        "low_predictive_value": [],
    }

    cat_cols = df.select_dtypes(include=['object', 'category']).columns
    n_rows = len(df)

    # 1. Low variance
    for col in cat_cols:
        if df[col].nunique() == 1:
            drop_report["low_variance"].append(col)

    # 2. High cardinality
    for col in cat_cols:
        if df[col].nunique() > high_card_thresh * n_rows:
            drop_report["high_cardinality"].append(col)

    # 3. Redundant features
    for i, col1 in enumerate(cat_cols):
        for col2 in cat_cols[i+1:]:
            similarity = (df[col1] == df[col2]).mean()
            if similarity > similarity_thresh:
                drop_report["redundant"].append((col1, col2))

    # 4. Low predictive value (optional)
    if target_col:
        X = df[cat_cols].copy()
        y = df[target_col]

        # Label encode for MI calculation
        for col in X.columns:
            X[col] = LabelEncoder().fit_transform(X[col].astype(str))

        mi_scores = mutual_info_classif(X, y, discrete_features=True)
        mi_series = pd.Series(mi_scores, index=X.columns)

        for col, score in mi_series.items():
            if score < low_info_thresh:
                drop_report["low_predictive_value"].append(col)

    return drop_report