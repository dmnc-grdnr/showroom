# Trainiert das XGBoost Modell.
# Benötigt Ergebnisse der Hyperparameter suche im Ordner search.
from common import print_info
from common import Identifier
from common import get_features
from common import get_modifications
from common import save_model
from xgboost import XGBClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import pandas as pd
import pickle


def get_selected_params_grid():
    with open(f"search/grid2_{id_.as_file()}.pkl", "rb") as file:
        result = pickle.load(file)
        return result.best_params_

def get_selected_params_random():
    with open(f"search/random_{id_.as_file()}.pkl", "rb") as file:
        result = pickle.load(file)
        return result.best_params_



if __name__ == '__main__':
    id_ = Identifier()
    id_.title = "netflow_sample"
    id_.name = "xgboost"
    df = pd.read_parquet(f"data/{id_.title}.parquet")

    for mod in get_modifications():
        id_.mod = mod

        params = {**get_selected_params_grid(), **get_selected_params_random()}
        print_info(f"Training {id_} with parameteres: {params}.")

        data = df[get_features(df.columns, mod)]
        labels = df["Attack"]
        labels = LabelEncoder().fit_transform(labels)

        X_train, X_test, y_train, y_test = train_test_split(data, labels, random_state=35, shuffle=True, train_size=0.8)

        model = XGBClassifier(random_state=35, booster="gbtree", tree_method="exact", **params)
        model = model.fit(X_train, y_train)
        save_model(id_, model)
        print_info(f"{id_.name} result: {model.score(X_test, y_test)}.")
    print_info("Done.")