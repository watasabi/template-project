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

    # # load data
    # data_inferenced = pd.read_parquet(args.data_inference)
    # raw_data = pd.read_parquet(args.raw_data)
    # transform_pipe = joblib.load(args.transform_pipeline)

    # # post processing
    # cat_feat = raw_data.select_dtypes(include="object").columns.drop("species")
    
    # num_inversed = (
    #     transform_pipe.named_transformers_["num"]
    #     .named_steps["StandardScaler"]
    #     .inverse_transform(data_inferenced.filter(like="num__", axis=1))
    # )

    # num_inversed = (
    #     transform_pipe.named_transformers_["num"]
    #     .named_steps["Imputer"]
    #     .inverse_transform(num_inversed)
    # )

    # cat_encoded = data_inferenced.filter(like="cat__", axis=1)
    # ohe = transform_pipe.named_transformers_["cat"].named_steps["OneHotEncoder"]
    # cat_inversed = ohe.inverse_transform(cat_encoded)
    # cat_inversed = pd.DataFrame(cat_inversed, columns=cat_feat)
    # cat_inversed = cat_inversed[:, :2]

    # inversed_transform = pd.DataFrame(
    #     np.hstack([num_inversed, cat_inversed]),
    #     columns=num_feat.tolist() + cat_feat.tolist(),
    # )
    # inversed_transform["species"] = data_inferenced["species"].values
