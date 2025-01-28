# Extrahiert Statistiken über die Verteilung der Daten von NF-UQ-NIDS-v2 und netflow_sample (Abbildung 5.1)
# Benötigt netflow_sample.parquet

from common import print_info
import dask.dataframe as dd
from pathlib import Path


def get_statistics(df):
    length = len(df)
    df = df.groupby(by="Attack")["Dataset"].value_counts().compute()
    return round(df/length,4)


def org_statistics():
    path = "org/org_nfuqnidsv2/NF-UQ-NIDS-v2.csv"
    print_info(f"Reading from path: {path}.")
    df = dd.read_csv(path)
    df = get_statistics(df)
    df.to_csv(f"data/netflow_statistics/dataset_statistics_org.csv", index=True)


def sample_statistics():
    path = "data/netflow_sample.parquet"
    print_info(f"Reading from path: {path}.")
    df = dd.read_parquet(path)
    df = get_statistics(df)
    df.to_csv(f"data/netflow_statistics/dataset_statistics_sample.csv", index=True)


if __name__ == '__main__':
    Path("data/netflow_statistics").mkdir(parents=True, exist_ok=True)
    org_statistics()
    sample_statistics()
    print_info("Completed.")