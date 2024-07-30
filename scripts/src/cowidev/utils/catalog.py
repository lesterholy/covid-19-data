from owid import catalog
from typing import List, Literal


def load_table_from_catalog(namespace: str, dataset: str, table: str, channels: List[Literal["meadow", "garden", "grapher"]] = ["garden"]) -> catalog.Table:
    cat = catalog.RemoteCatalog(channels=channels)
    tb = cat.find_latest(namespace=namespace, dataset=dataset, table=table)
    return tb
