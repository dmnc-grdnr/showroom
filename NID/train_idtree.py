# Trainiert das IntruDTree Modell.
# Benötigt Ergebnisse der Hyperparameter suche im Ordner search.
from common import Identifier
from common import print_info
from common import get_modifications
from common_cart import prune_tree
from common_idtree import get_selected_features
from sklearn.model_selection import train_test_split
import pandas as pd
import pickle


def get_selected_params():
    with open(f"search/grid_{id_.as_file()}.pkl", "rb") as file:
        result = pickle.load(file)
        return result.best_params_


if __name__ == '__main__':
    id_ = Identifier()
    id_.title = "netflow_sample"
    id_.name = "idtree"
    df = pd.read_parquet(f"data/{id_.title}.parquet")
    for mod in get_modifications():
        id_.mod = mod
        print_info(f"Pruning model {id_}.")
        data = df[get_selected_features(id_)]
        labels = df["Attack"]
        X_train, X_test, y_train, y_test = train_test_split(data, labels, random_state=35, shuffle=True, train_size=0.8)
        params = get_selected_params()
        model = prune_tree(id_, X_train, y_train, params, skip_pruning=False)
        print_info(f"{id_.name} result: {model.score(X_test, y_test)}.")
    print_info("Done.")