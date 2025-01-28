from common import print_error
from common import print_info
from common import save_model
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import GridSearchCV
import pickle

# Führt das Pruning der Modelle CART und IntruDTree aus
def compute_alphas(model, X_train, y_train):
    path = model.cost_complexity_pruning_path(X_train, y_train)
    ccp_alphas, _ = path.ccp_alphas, path.impurities
    print_info(f"Computing {len(ccp_alphas)} alphas.")
    skf = StratifiedKFold(n_splits=10, shuffle=True, random_state=35)
    search = GridSearchCV(model, {"ccp_alpha":ccp_alphas}, scoring="accuracy", n_jobs=6, cv=skf, verbose=10)
    search.fit(X_train, y_train)
    return search


def save_alphas(id_, alphas):
    print_info("Saving results.")
    with open(f"search/alphas_{id_.as_file()}.pkl", "wb") as file:
        pickle.dump(alphas, file)

# Ermittelt den Alphawert mit dem höchsten Score
def select_alpha(alphas):
    max_score = max([x[1] for x in alphas])
    return [x[0] for x in alphas if x[1] == max_score][0]

# Trainiert CART mit übergebenen Parametern mit anschließendem Pruning
def prune_tree(id_, X_train, y_train, params, skip_pruning=False):
    if skip_pruning:
        print_error(f"Skipping Pruning.")
        with open(f"search/alphas_{id_.as_file()}.pkl", "rb") as file:
            alpha_params = pickle.load(file).best_params_
        for key, value in alpha_params.items():
            print(key, value)
            params[key] = value
        print(params)
        model = DecisionTreeClassifier(random_state=35, **params)
        model = model.fit(X_train, y_train)
        save_model(id_, model)
        return model
    print_info(f"Pruning model.")
    model = DecisionTreeClassifier(random_state=35, **params)
    model = model.fit(X_train, y_train)
    alphas = compute_alphas(model, X_train, y_train)
    save_alphas(id_, alphas)
    alpha_params = alphas.best_params_
    for key, value in alpha_params.items():
        print(key, value)
        params[key] = value
    print_info(f"Retraining model with parameters: {params}.")
    model = DecisionTreeClassifier(random_state=35, **params)
    model = model.fit(X_train, y_train)
    save_model(id_, model)
    return model


def get_grid_ranges():
    return [0.000001, 0.000005, 0.00001, 0.00005, 0.0001, 0.0005, 0.001, 0.005, 0.01, 0.05, 0.1]


def as_percentage(value):
    value = value * 100
    if value >= 1:
        value = int(value)
    return str(value) + "%"
