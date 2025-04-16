import seaborn as sns
import pandas as pd
import sklearn
import matplotlib.pyplot as plt
import numpy as np
import argparse
from azureml.core import Run
import dotenv
dotenv.load_dotenv("../src/config/.env")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--data_raw",
        type=str,
        required=True,
        help="Path to the dataset",
        dest="data_raw",
    )
    args = parser.parse_args()
    run = Run.get_context()

    data_raw = sns.load_dataset("penguins")

    run.log("data shape", str(data_raw.shape))

    # Load the dataset
    data_raw.to_parquet(args.data_raw, index=False)
    run.flush()
    run.complete()
