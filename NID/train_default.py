# Trainiert alle Modelle der Arbeit mit Standardeinstellungen.
# Benötigt data/netflow_sample.parquet
from common import print_info
from common import Identifier
from common import get_modifications
from common import get_features
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
import pandas as pd
import pickle


def get_selected_features():
    with open(f"model/idtree_{id_.title}_{id_.mod}.pkl", "rb") as file:
         return pickle.load(file).feature_names_in_


def save_default(id_, model):
    print_info("Pickling model.")
    with open(f"model/{id_.as_file()}_default.pkl", "wb") as file:
        pickle.dump(model, file)


if __name__ == '__main__':
    id_ = Identifier()
    id_.title = "netflow_sample"
    df = pd.read_parquet(f"data/{id_.title}.parquet")

    for mod in get_modifications():
        id_.mod = mod

        data = df[get_features(df.columns, mod)]
        labels = df["Attack"]
        selected_features = get_selected_features()

        X_train, X_test, y_train, y_test = train_test_split(data, labels, random_state=35, shuffle=True, train_size=0.8)

        # CART
        model = DecisionTreeClassifier(random_state=35, criterion="gini")
        id_.name = "cart"
        print_info(f"Selected parameters for {id_}: {model.get_params()}.")
        model = model.fit(X_train, y_train)
        save_default(id_, model)
        print_info(f"{id_.name} result: {model.score(X_test, y_test)}.")

        # IntruDTree
        model = DecisionTreeClassifier(random_state=35, criterion="gini")
        id_.name = "idtree"
        print_info(f"Selected parameters for {id_}: {model.get_params()}.")
        model = model.fit(X_train[selected_features], y_train)
        save_default(id_, model)
        print_info(f"{id_.name} result: {model.score(X_test[selected_features], y_test)}.")

        # ExtraTrees
        model = ExtraTreesClassifier(criterion="gini", random_state=35)
        id_.name = "extra"
        print_info(f"Selected parameters for {id_}: {model.get_params()}.")
        model = model.fit(X_train, y_train)
        save_default(id_, model)
        print_info(f"{id_.name} result: {model.score(X_test, y_test)}.")

        # IntruDForest
        model = RandomForestClassifier(random_state=35, max_features=None, bootstrap=True)
        id_.name = "idforest"
        print_info(f"Selected parameters for {id_}: {model.get_params()}.")
        model = model.fit(X_train[selected_features], y_train)
        save_default(id_, model)
        print_info(f"{id_.name} result: {model.score(X_test[selected_features], y_test)}.")

        # XGBoost
        model = XGBClassifier(random_state=35, booster="gbtree", tree_method="exact")
        id_.name = "xgboost"
        print_info(f"Selected parameters for {id_}: {model.get_params()}.")

        le = LabelEncoder().fit(labels)
        y_train = le.transform(y_train)
        y_test = le.transform(y_test)
        model = model.fit(X_train, y_train)
        save_default(id_, model)
        print_info(f"{id_.name} result: {model.score(X_test, y_test)}.")

    print_info("Done.")