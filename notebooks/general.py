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
import joblib


from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from sklearn.model_selection import cross_val_score


#step1
data_raw = sns.load_dataset("penguins")

#step2
num_feat = data_raw.select_dtypes(include=np.number).columns
cat_feat = data_raw.select_dtypes(include="object").columns.drop("species")

cat_pipeline = Pipeline(
    [
        ("inputer", SimpleImputer(strategy="constant", fill_value="unknown", add_indicator=True)),
        ("OneHotEncoder", OneHotEncoder())
    ]
)

num_pipeline = Pipeline(
    [
        ("Imputer", SimpleImputer(strategy="mean", add_indicator=True)),
        ("StandardScaler", StandardScaler())
    ]
)

transform = ColumnTransformer(
    [
        ("cat", cat_pipeline, cat_feat),
        ("num", num_pipeline, num_feat)
    ]
)

# save transform
data_preprocessed = transform.fit_transform(data_raw)
data_preprocessed = pd.DataFrame(data_preprocessed, columns=transform.get_feature_names_out())
data_preprocessed["species"] = data_raw["species"].values


#step3 - model inference
dummy_model = RandomForestClassifier()
dummy_model.fit(data_preprocessed.drop("species", axis=1), data_raw["species"].values)
y_pred = dummy_model.predict(data_preprocessed.drop("species", axis=1))

df_report = data_preprocessed.drop("species", axis=1)
df_report["species"] = y_pred

# Modified step4 - postProcessing

# For numerical features
num_inversed = transform.named_transformers_["num"].named_steps["StandardScaler"].inverse_transform(
    df_report.filter(like="num__", axis=1)
)
num_inversed = transform.named_transformers_["num"].named_steps["Imputer"].inverse_transform(
    num_inversed
)

# For categorical features - we need to handle this differently
# First inverse the one-hot encoding
cat_encoded = df_report.filter(like="cat__", axis=1)
ohe = transform.named_transformers_["cat"].named_steps["OneHotEncoder"]
cat_inversed = ohe.inverse_transform(cat_encoded)
cat_inversed = cat_inversed[:, :2]  # Get the first column of the inverse transformed data

cat_inversed = pd.DataFrame(cat_inversed, columns=cat_feat)

# Combine results
inversed_transform = pd.DataFrame(
    np.hstack([num_inversed, cat_inversed]),
    columns=num_feat.tolist() + cat_feat.tolist()
)
inversed_transform["species"] = df_report["species"].values