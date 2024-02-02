"""Collect Cases/Deaths data"""
from cowidev import PATHS
from cowidev.cases_deaths.extract import load_data
from cowidev.cases_deaths.load import export_grapher_file
from cowidev.cases_deaths.transform import process_data
from cowidev.utils.utils import export_timestamp
import pandas as pd


def generate_dataset(logger, server_mode):
    """Generate Cases/Deaths dataset."""
    # Load data
    logger.info("Cases/Deaths: Loading data…")
    df = load_data(server_mode)

    # Process data
    # HOTFIX: Data is only available every 7 days. Fill in the gaps with zeroes
    df = fill_date_gaps(df)

    logger.info("Cases/Deaths: Processing data…")
    df = process_data(df)

    # Export data
    export_grapher_file(df, logger)

    # logger.info("Generating subnational file…")
    # create_subnational()

    # Export timestamp
    export_timestamp(PATHS.DATA_TIMESTAMP_CASES_DEATHS_FILE)


def fill_date_gaps(df):
    """Ensure dataframe has all dates.

    Apparently, in the past the input data had all the dates from start to end.

    Early in 2024 this stopped to be like this, maybe due to a change in how the data is reported by the WHO. Hence, we need to make sure that there are no gaps!
    Source of change might be this: https://github.com/owid/covid-19-data/commit/ed73e7113344caffc9e445946979e1964720348b#diff-cb6c8f3daa43ff50c0cac819d63ce03bedfd4c7cf98ace02cad543a485c9513e

    We do this by:
        - Reindexing the dataframe to have all dates for all locations.
        - Filling in NaNs with zeroes, for daily indicators.
        - Filling in NaNs with the last non-NaN value, for cumulative indicators (forward filling).    
    """
    # Ensure date is of type date
    df["date"] = pd.to_datetime(df["date"])

    # Get set of locations
    locations = set(df["location"])
    # Create index based on all locations and all dates
    complete_dates = pd.date_range(df["date"].min(), df["date"].max())

    # Reindex
    df = df.set_index(["location", "date"])
    new_index = pd.MultiIndex.from_product([locations, complete_dates], names=["location", "date"])
    df = df.reindex(new_index).sort_index()

    # Fill in NaNs
    df[["new_cases", "new_deaths"]] = df[["new_cases", "new_deaths"]].fillna(0)
    df[["total_cases", "total_deaths"]] = df.groupby(level='location')[["total_cases", "total_deaths"]].fillna(method='ffill')

    # Reset index
    df = df.reset_index()
    return df
