#Führt eine Hyperparametersuche für XGBoost durch pro Feature-Konfiguration.
# Benötigt data/netflow_sample.parquet
from common import print_info
from common import Identifier
from common import get_features
from common import get_modifications
from pathlib import Path
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import RandomizedSearchCV
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import train_test_split
import pandas as pd
import pickle
import xgboost as xgb


def get_selected_params():
    with open(f"search/grid2_{id_.as_file()}.pkl", "rb") as file:
        result = pickle.load(file)
        return result.best_params_


def gridsearch():

    grid_params = get_selected_params()

    model = xgb.XGBClassifier(random_state=35, booster="gbtree", tree_method="exact", **grid_params)

    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=35)

    runs = 20 #number of combindations
    search = RandomizedSearchCV(model, parameters, scoring="accuracy", n_iter=runs, n_jobs=6, cv=skf, verbose=10,
                                random_state=32)
    search.fit(X_train, y_train)
    print_info("Saving results.")
    Path("search").mkdir(parents=True, exist_ok=True)
    with open(f"search/random_{id_.as_file()}.pkl", "wb") as file:
        pickle.dump(search, file)
    print_info(f"Best parameters for {id_}: {search.best_params_}")


if __name__ == '__main__':
    id_ = Identifier()
    id_.title = "netflow_sample"
    id_.name = "xgboost"
    df = pd.read_parquet(f"data/{id_.title}.parquet")

    parameters = {'min_child_weight':[1, 2, 3, 4, 5],
                  'gamma':[0, 0.1, 0.5, 1, 2, 5],
                  'max_depth':[1, 2, 3, 4, 5, 6]}

    for mod in get_modifications():
        id_.mod = mod
        print_info(f"Starting search for {id_}.")

        data = df[get_features(df.columns, mod)]
        labels = df["Attack"]
        # XGBoost benötigt nummerierte Labels (Angriffe)
        le = LabelEncoder()
        labels = le.fit_transform(labels)

        X_train, X_test, y_train, y_test = train_test_split(data, labels, random_state=35, shuffle=True, train_size=0.8)
        gridsearch()
    print_info("Done.")