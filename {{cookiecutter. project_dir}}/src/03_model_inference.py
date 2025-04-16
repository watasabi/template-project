import seaborn as sns
import pandas as pd
import sklearn
import matplotlib.pyplot as plt
import numpy as np
import argparse
from azureml.core import Run

from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from sklearn.model_selection import cross_val_score

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--data_transformed",
        type=str,
        required=True,
        help="Path to the dataset",
        dest="data_transformed",
    )
    parser.add_argument(
        "--data_inference",
        type=str,
        required=True,
        help="Path to save the transformed dataset",
        dest="data_inference",
    )
    args = parser.parse_args()
    run = Run.get_context()

    dummy_model = RandomForestClassifier()
    new_data = pd.read_parquet(args.data_transformed)
    dummy_model.fit(new_data.drop("species", axis=1), new_data["species"].values)
    y_pred = dummy_model.predict(new_data.drop("species", axis=1))
    df_report = pd.DataFrame(
        classification_report(new_data["species"].values, y_pred, output_dict=True)
    )

    df_report.to_parquet(args.data_inference, index=False)

    run.flush()
    run.complete()
