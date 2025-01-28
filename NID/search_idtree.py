#Führt eine Hyperparametersuche für IntruDTree durch pro Feature-Konfiguration.
#Benötigte Dateien:
#   search/rank_idtree_*.pkl (zwecks Featureselektion)
#   data/netflow_sample.parquet
from common import print_info
from common import Identifier
from common import get_modifications
from common_cart import get_grid_ranges
from common_idtree import get_selected_features
from pathlib import Path
import pandas as pd
import pickle
from sklearn import tree
from sklearn.model_selection import RandomizedSearchCV
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import train_test_split


def randomsearch():
    ranges = get_grid_ranges()
    print_info(f"Ranges: {ranges}.")
    parameters = {"min_samples_leaf": ranges,
                  "min_samples_split": ranges,
                  "min_impurity_decrease": ranges}
    model = tree.DecisionTreeClassifier(random_state=35)
    skf = StratifiedKFold(n_splits=10, shuffle=True, random_state=35)
    runs = 20
    search = RandomizedSearchCV(model, parameters, scoring="accuracy", n_iter=runs, n_jobs=6, cv=skf, verbose=10,
                       random_state=32)
    search.fit(X_train, y_train)
    print_info("Saving results.")
    Path("search").mkdir(parents=True, exist_ok=True)
    with open(f"search/grid_{id_.as_file()}.pkl", "wb") as file:
        pickle.dump(search, file)
    print_info(f"Best parameters for {id_}: {search.best_params_}")


if __name__ == '__main__':
    id_ = Identifier()
    id_.title = "netflow_sample"
    id_.name = "idtree"
    df = pd.read_parquet(f"data/{id_.title}.parquet")
    for mod in get_modifications():
        id_.mod = mod
        print_info(f"Starting search for {id_}.")
        data = df[get_selected_features(id_)]
        print(get_selected_features(id_))
        print_info(f"Selected {len(data.columns)}: data.columns")
        labels = df["Attack"]
        X_train, X_test, y_train, y_test = train_test_split(data, labels, random_state=35, shuffle=True, train_size=0.8)
        print_info(f"Final column {data.columns[-1]}.")
        randomsearch()
    print_info("Done.")