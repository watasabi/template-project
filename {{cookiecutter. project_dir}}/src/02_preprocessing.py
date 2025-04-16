import seaborn as sns
import pandas as pd
import sklearn
import matplotlib.pyplot as plt
import numpy as np
import argparse
import joblib
from azureml.core import Run

from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--data_raw",
        type=str,
        required=True,
        help="Path to the dataset",
        dest="data_raw",
    )

    parser.add_argument(
        "--data_transformed",
        type=str,
        required=True,
        help="Path to save the transformed dataset",
        dest="data_transformed",
    )

    parser.add_argument(
        "--transform_pipeline",
        type=str,
        required=True,
        help="Path to save the transform pipeline",
        dest="transform_pipeline",
    )

    args = parser.parse_args()
    run = Run.get_context()

    data_raw = pd.read_parquet(args.data_raw)

    num_feat = data_raw.select_dtypes(include=np.number).columns
    cat_feat = data_raw.select_dtypes(include="object").columns.drop("species")

    cat_pipeline = Pipeline(
        [
            ("Inputer", SimpleImputer(strategy="constant", fill_value="unknow")),
            ("OneHotEncoder", OneHotEncoder(drop="first")),
        ]
    )

    num_pipeline = Pipeline(
        [
            ("Inputer", SimpleImputer(strategy="mean")),
            ("StandardScaler", StandardScaler()),
        ]
    )

    transform = ColumnTransformer(
        [("cat", cat_pipeline, cat_feat), ("num", num_pipeline, num_feat)]
    )

    # save transform
    new_data = transform.fit_transform(data_raw)
    new_data = pd.DataFrame(new_data, columns=transform.get_feature_names_out())
    new_data["species"] = data_raw["species"].values

    # Save the transformed data and the pipeline
    new_data.to_parquet(args.data_transformed, index=False)
    joblib.dump(transform, args.transform_pipeline)

    run.log("transformed_data_shape", new_data.shape)

    run.flush()
    run.complete()
