import seaborn as sns
import pandas as pd
import sklearn
import matplotlib.pyplot as plt
import numpy as np
import argparse
from azureml.core import Run
import joblib

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
        "--data_inference",
        type=str,
        required=True,
        help="Path to the dataset",
        dest="data_inference",
    )
    parser.add_argument(
        "--transform_pipeline",
        type=str,
        required=True,
        help="Path to the transform pipeline",
        dest="transform_pipeline",
    )
    parser.add_argument(
        "--raw_data",
        type=str,
        required=True,
        help="Path to the raw data",
        dest="raw_data",
    )

    args = parser.parse_args()
    run = Run.get_context()
    pass