import argparse

CHOICES = ["download", "etl"]


def _parse_args():
    parser = argparse.ArgumentParser(
        description="Execute COVID-19 JHU data collection pipeline.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "step",
        choices=CHOICES,
        help=("Choose a step: 0) `download`, 1) `etl` to get all data and DS ready file."),
    )
    parser.add_argument(
        "-s",
        "--skip-download",
        action="store_true",
        help="Skip downloading files from the JHU repository",
    )
    args = parser.parse_args()
    return args
