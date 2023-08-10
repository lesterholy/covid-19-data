"""Collect Cases/Deaths data"""
from cowidev import PATHS
from cowidev.cases_deaths.extract import load_data
from cowidev.cases_deaths.load import export_grapher_file
from cowidev.cases_deaths.transform import process_data
from cowidev.utils.utils import export_timestamp


def generate_dataset(logger, server_mode):
    """Generate Cases/Deaths dataset."""
    # Load data
    logger.info("Cases/Deaths: Loading data…")
    df = load_data(server_mode)

    # Process data
    logger.info("Cases/Deaths: Processing data…")
    df = process_data(df)

    # Export data
    export_grapher_file(df, logger)

    # logger.info("Generating subnational file…")
    # create_subnational()

    # Export timestamp
    export_timestamp(PATHS.DATA_TIMESTAMP_CASES_DEATHS_FILE)
