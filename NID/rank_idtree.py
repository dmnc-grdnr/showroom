# Erzeugt das Feature-Ranking für IntruDTree
# benötigte Dateien: netflow_sample.parquet

from common import Identifier
from common import get_features
from common import get_modifications
from common import print_info
from common_idtree import gini_delta
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn import tree
import pandas as pd
import pickle

# Führt das Ranking der Feature durch
def ranking():
    features = X_train.columns
    impurities_ranking = []
    X_train_mod = X_train.copy()
    for i in range(len(features)):
        print_info(f"Round {i + 1} / {len(features)}")
        # Es wird ein Entscheidungsbaumstumpf trainiert
        model = tree.DecisionTreeClassifier(random_state=35, max_depth=1)
        model = model.fit(X_train_mod, y_train)
        impurities = [model.tree_.impurity[i] for i in range(3)]
        nodes = [model.tree_.n_node_samples[i] for i in range(3)]
        # Gini Importance wird berechnet
        delta = gini_delta(impurities, nodes)
        # Column ist das Feature, das für den Stumpf gewählt wurde
        column = model.feature_names_in_[model.feature_importances_.argmax()]
        impurities_ranking.append((column, delta))
        # Das gewählte Feature (Column) wird für den nächsten Vorgang entfernt
        X_train_mod = X_train_mod.drop(column, axis=1)

    result = pd.DataFrame(impurities_ranking, columns=["Feature", "Delta"])
    print_info("Adding Sets.")
    ranked_features = list(result["Feature"])
    # Untermengen werden erzeugt, indem ein Feature, gemäß des Rankings, nach und nach hinzugefügt wird.
    result["Set"] = [ranked_features[:i + 1] for i in range(len(ranked_features))]
    print_info("Adding Scores")
    feature_subset_scores = []
    # Pro Untermenge wird die Accuracy auf einem Entscheidungsbaum mit Standardeinstellungen berechnet
    for feature_subset in result["Set"]:
        model = tree.DecisionTreeClassifier(random_state=35)
        model = model.fit(X_train[feature_subset], y_train)
        score = model.score(X_test[feature_subset], y_test)
        feature_subset_scores.append(score)

    result["Score"] = feature_subset_scores
    return result


# Ergebnisse des Rankings (u.a. Accuracy pro Feature-Menge) werden im Ordner search gespeichert
def save_ranking(result):
    Path("search").mkdir(parents=True, exist_ok=True)
    with open(f"search/rank_{id_.as_file()}.pkl", "wb") as file:
        pickle.dump(result, file)


if __name__ == '__main__':
    id_ = Identifier()
    id_.title = "netflow_sample"
    id_.name = "idtree"
    df = pd.read_parquet(f"data/{id_.title}.parquet")
    for mod in get_modifications():
        id_.mod = mod
        print_info(f"Ranking features for {id_}.")
        data = df[get_features(df.columns, mod)]
        print(data.columns)
        labels = df["Attack"]
        X_train, X_test, y_train, y_test = train_test_split(data, labels, random_state=35, shuffle=True, train_size=0.8)
        df_impurities_ranking = ranking()
        save_ranking(df_impurities_ranking)
    print_info("Done.")
