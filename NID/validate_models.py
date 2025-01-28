# Erzeugt die Konfusionsmatrizen und Klassifikationsergebnisse der Modelle auf den Validierungsdatensätzen und den Testdaten.
# Benötigte Dateien:
#   model/model_*.pkl (alle Modelle)
#   data/netflow_sample.parquet
#   data/transformation/cicddos2019_labeled.csv
#   data/transformation/cicids2017_labeled.csv
#   data/transformation/fhswfcnl_labeled.csv
# Ausgabe im Ordner scores
from common import print_info
from common import load_model
from common import Identifier
from common import rename_attack_ids2017
from common import rename_attack_ddos2019
from common import get_modelnames
from common import get_modifications
from common import rename_attack_fhswfcnl
from common import rename_attack
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import pandas as pd
import pickle


def save_matrix(result):
    print_info("Pickling matrix.")
    with open(f"scores/matrix_{data_set}_{id_.as_file()}.pkl", "wb") as file:
        pickle.dump(result, file)


def save_report(result):
    print_info("Pickling report.")
    with open(f"scores/report_{data_set}_{id_.as_file()}.pkl", "wb") as file:
        pickle.dump(result, file)


if __name__ == '__main__':
    id_ = Identifier()
    id_.title = "netflow_sample"
    df = pd.read_parquet(f"data/{id_.title}.parquet")

    # for xgboost
    le = LabelEncoder().fit(df["Attack"])

    all_attacks = sorted([rename_attack(x) for x in df["Attack"].unique()])

    for data_set in ["test", "cicddos2019", "cicids2017", "fhswfcnl"]:

        X_true = y_true = None

        if data_set == "test":
            _, X_true, _, y_true = train_test_split(df, df["Attack"], random_state=35, shuffle=True, train_size=0.8)
            y_true = [rename_attack(x) for x in y_true]
        elif data_set == "cicddos2019":
            X_true = pd.read_csv("data/transformation/cicddos2019_labeled.csv")
            y_true = X_true["Label"].apply(rename_attack_ddos2019)
        elif data_set == "cicids2017":
            X_true = pd.read_csv("data/transformation/cicids2017_labeled.csv")
            y_true = X_true["Label"].apply(rename_attack_ids2017)
        elif data_set == "fhswfcnl":
            X_true = pd.read_csv("data/transformation/fhswfcnl_labeled.csv")
            y_true = X_true["Label"].apply(rename_attack_fhswfcnl)

        for name in get_modelnames():
            id_.name = name
            for mod in get_modifications():
                id_.mod = mod
                print_info(f"Validating {id_} on {data_set}")
                model = load_model(id_)
                labels = sorted(set(y_true))
                y_pred = model.predict(X_true[model.feature_names_in_])

                if id_.name == "xgboost":
                    y_pred = le.inverse_transform(y_pred)
                y_pred = [rename_attack(x) for x in y_pred]

                matrix = confusion_matrix(y_true, y_pred, labels=all_attacks, normalize=None)
                #print(matrix)
                save_matrix((all_attacks, matrix))

                report = classification_report(y_true, y_pred, labels=labels, output_dict=True, zero_division=0)
                save_report(report)
                #print(report)

    print_info("Done.")