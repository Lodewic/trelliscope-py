import pytest
from io import BytesIO
from datetime import date, timedelta, datetime
import pkgutil

import pandas as pd
import os
import numpy as np

from trelliscope.trelliscope import Trelliscope

DATA_DIR = "external_data"
IRIS_DF_FILENAME = "iris.data"

# def pytest_configure(config):
#     if not os.path.exists(CACHE_DIR):
#         os.makedirs(CACHE_DIR)

@pytest.fixture(scope="session")
def loaded_iris_df() -> pd.DataFrame:
    """
    Loads the iris dataset from a file in the test-data directory.
    """
    iris_path = os.path.join(DATA_DIR, IRIS_DF_FILENAME)

    data = pkgutil.get_data(__name__, iris_path)
    df = pd.read_pickle(BytesIO(data))

    return df

@pytest.fixture
def iris_df(loaded_iris_df : pd.DataFrame):
    """
    Returns a copy of the iris dataset.
    """
    df_copy = loaded_iris_df.copy(deep=True)
    return df_copy

@pytest.fixture
def iris_plus_df(iris_df: pd.DataFrame):
    """
    Returns a copy of the iris dataset with extra columns for id and dates.
    """
    iris_df.insert(0, 'id', range(len(iris_df)))
    # iris_df["id"] = iris_df.apply(lambda row: str(int(row.index) + 1))
    iris_df["date"] = iris_df.apply(lambda row: datetime(2023, 2, 24) + timedelta(days=row["id"], minutes=row["id"]), axis=1)
    iris_df["datetime"] = iris_df.apply(lambda row: row["date"].isoformat(), axis=1)
    iris_df["datestring"] = iris_df.apply(lambda row: row["date"].date().isoformat(), axis=1)
    iris_df["lat"] = np.random.uniform(-90, 90, iris_df.shape[0])
    iris_df["long"] = np.random.uniform(0, 180, iris_df.shape[0])
    iris_df["href"] = iris_df.apply(lambda row: f"https://www.google.com/{row['id']}", axis=1)

    #print(iris_df.head())
    return iris_df

@pytest.fixture
def iris_tr(iris_df: pd.DataFrame):
    tr = Trelliscope(iris_df, name="iris")
    return tr

