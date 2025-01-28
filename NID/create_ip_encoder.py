# Erzeugt den LabelEncoder für das Nummerieren der IP-Adressen
# benötigt die Dateien:
#   org/org_nfuqnidsv2/NF-UQ-NIDS-v2.csv
#   data/transformation/cicddos2019/cicddos2019_merged.csv (create_cicddos2019.py)
#   data/transformation/cicids2017/cicids2017_merged.csv (create_cicids2017.py)
#   data/transformation/fhswfcnl/fhswfcnl_org.csv (create_fhswfcnl.py)

from common import print_info
from sklearn.preprocessing import LabelEncoder
import dask.dataframe as dd
import os.path
import pandas as pd
import pickle


def extract_columns(input_df, input_values):
    columns = [x for x in input_df.columns if x.startswith("IP")]
    for column in columns:
        input_values = input_values.union(input_df[column].astype("str").unique())
    return input_values


if __name__ == '__main__':
    print_info(f"Creating encoder.")
    values = set()

    # NF-UQ-NIDS-v2
    filename= "org/org_nfuqnidsv2/NF-UQ-NIDS-v2.csv"
    if os.path.isfile(filename):
        print_info(f"Reading from file: {filename}")
        temp_df = dd.read_csv(filename)
        values = extract_columns(temp_df, values)

    # CIC-DDoS2019
    filename = "data/transformation/cicddos2019/cicddos2019_merged.csv"
    if os.path.isfile(filename):
        print_info(f"Reading from file: {filename}")
        temp_df = dd.read_csv(filename)
        values = extract_columns(temp_df, values)

    # CIC-IDS2017
    filename = "data/transformation/cicids2017/cicids2017_merged.csv"
    if os.path.isfile(filename):
        print_info(f"Reading from file: {filename}")
        temp_df = dd.read_csv(filename)
        values = extract_columns(temp_df, values)

    # FH-SWF-CNL
    filename = "data/transformation/fhswfcnl/fhswfcnl_org.csv"
    if os.path.isfile(filename):
        print_info(f"Reading from file: {filename}")
        temp_df = dd.read_csv(filename)
        values = extract_columns(temp_df, values)

    print_info(f"Calculating encoder.")
    le = LabelEncoder().fit(sorted(values))
    le_dict = dict(zip(le.classes_, le.transform(le.classes_)))
    # Speichert das Encoding als CSV-Datei
    pd.DataFrame.from_dict(le_dict, orient='index', columns=['ip']).to_csv("data/ip_encoder_dictionary.csv")
    with open("data/ip_encoder.pkl", "wb") as file:
        # Speichert LabelEncoder als binäre Datei
        pickle.dump(le, file)
    print_info("Completed.")
