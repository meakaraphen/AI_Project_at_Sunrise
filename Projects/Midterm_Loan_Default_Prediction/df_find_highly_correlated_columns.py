
import pandas as pd
import numpy as np

def find_highly_correlated_columns(df, threshold=0.9):
    """
    Identify highly correlated columns and suggest ones to drop.

    Parameters:
    df (pd.DataFrame): DataFrame with numeric columns only.
    threshold (float): Correlation threshold (default = 0.9).

    Returns:
    to_drop (set): Set of column names to drop.
    high_corr_pairs (list): List of tuples of highly correlated column pairs.

    | Correlation Coefficient | Interpretation               | Typical Action                 |
    | ----------------------- | ---------------------------- | ------------------------------ |
    | 0.0 - 0.5               | Weak to moderate correlation | Usually keep both features     |
    | 0.5 - 0.85              | Moderate to strong           | Consider domain knowledge      |
    | **> 0.85 - 0.95**       | **Strong correlation**       | **Often drop one of the pair** |
    | **> 0.95**              | **Very strong correlation**  | **Almost always drop one**     |

    """
    # Compute the correlation matrix
    corr_matrix = df.corr().abs()
    
    # Take upper triangle of the correlation matrix
    upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
    
    # Identify pairs and mark columns to drop
    to_drop = set()
    high_corr_pairs = []

    for col in upper.columns:
        for row in upper.index:
            corr_value = upper.loc[row, col]
            if pd.notnull(corr_value) and corr_value > threshold:
                high_corr_pairs.append((row, col))
                to_drop.add(col)  # drop the later column in the pair

    return to_drop, high_corr_pairs