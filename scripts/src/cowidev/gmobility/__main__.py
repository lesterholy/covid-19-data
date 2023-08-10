from cowidev.gmobility._parser import _parse_args
from cowidev.gmobility.etl import run_etl
from cowidev.gmobility.grapher import run_grapheriser


def run_step(step: str):
    if step == "etl":
        run_etl()
    elif step == "grapher-file":
        run_grapheriser()


if __name__ == "__main__":
    args = _parse_args()
    run_step(args.step)
