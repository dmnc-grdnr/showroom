# Wandelt die Klassifikation auf CIC-DDoS2019 in binäres Spektrum um (für Abbildung 5.9)
# Benötigte Dateien:
#   model/model_*.pkl (alle Modelle)
#   data/netflow_sample.parquet
# Ausgabe im Ordner scores
from common import print_info
from common import load_model
from common import Identifier
from common import rename_attack_ddos2019
from common import get_modifications
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.preprocessing import LabelEncoder
import pandas as pd
import pickle


def save_matrix(result):
    print_info("Pickling matrix.")
    with open(f"scores/binary_matrix_{data_set}_{id_.as_file()}.pkl", "wb") as file:
        pickle.dump(result, file)


def save_report(result):
    print_info("Pickling report.")
    with open(f"scores/binary_report_{data_set}_{id_.as_file()}.pkl", "wb") as file:
        pickle.dump(result, file)


def rename_attack_binary(value):
    return "Benign" if value == "Benign" else "Attack"


if __name__ == '__main__':
    id_ = Identifier()
    id_.title = "netflow_sample"
    df = pd.read_parquet(f"data/{id_.title}.parquet")

    # for xgboost
    le = LabelEncoder().fit(df["Attack"])

    labels = ["Benign", "Attack"]

    data_set = "cicddos2019"

    X_true = pd.read_csv("data/transformation/cicddos2019_labeled.csv")
    y_true = X_true["Label"].apply(rename_attack_ddos2019)

    for name in ["cart", "idtree", "extra", "idforest", "xgboost"]:
        id_.name = name
        for mod in get_modifications():
            id_.mod = mod
            print_info(f"Validating {id_} on {data_set}")
            model = load_model(id_)

            y_pred = model.predict(X_true[model.feature_names_in_])

            if id_.name == "xgboost":
                y_pred = le.inverse_transform(y_pred)

            #Binary
            y_pred = [rename_attack_binary(x) for x in y_pred]
            y_true = [rename_attack_binary(x) for x in y_true]

            matrix = confusion_matrix(y_true, y_pred, labels=labels, normalize=None)
            #print(matrix)
            save_matrix((labels, matrix))

            report = classification_report(y_true, y_pred, labels=labels, output_dict=True, zero_division=0)
            save_report(report)
            #print(report)

    print_info("Done.")