from sklearn import tree
from sklearn.model_selection import GridSearchCV, StratifiedKFold, train_test_split

import pandas as pd


# Berechnet die Gini Importance gemäß Kapitel 3.1.2
def gini_delta(impurities, samples):
    delta = impurities[0] * samples[0] / samples[0]
    delta -= impurities[1] * samples[1] / samples[0]
    delta -= impurities[2] * samples[2] / samples[0]
    return delta

# Erzeugt das Feature-Ranking für IntruDTree
# Führt das Ranking der Feature durch
def feature_ranking(data, labels, random_state=35, shuffle=True, train_size=0.8):
    X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=train_size, random_state=random_state)
    features = X_train.columns
    impurities_ranking = []
    X_train_mod = X_train.copy()
    for i in range(len(features)):
        print(f"Round {i + 1} / {len(features)}")
        # Es wird ein Entscheidungsbaumstumpf trainiert
        model = tree.DecisionTreeClassifier(random_state=random_state, max_depth=1)
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
    print("Adding Sets.")
    ranked_features = list(result["Feature"])
    # Untermengen werden erzeugt, indem ein Feature, gemäß des Rankings, nach und nach hinzugefügt wird.
    result["Set"] = [ranked_features[:i + 1] for i in range(len(ranked_features))]
    print("Adding Scores")
    feature_subset_scores = []
    # Pro Untermenge wird die Accuracy auf einem Entscheidungsbaum mit Standardeinstellungen berechnet
    for feature_subset in result["Set"]:
        model = tree.DecisionTreeClassifier(random_state=random_state)
        model = model.fit(X_train[feature_subset], y_train)
        score = model.score(X_test[feature_subset], y_test)
        feature_subset_scores.append(score)

    result["Score"] = feature_subset_scores
    return result


# Führt das Pruning der Modelle CART und IntruDTree aus
def compute_alphas(model, X_train, y_train, random_state=35):
    path = model.cost_complexity_pruning_path(X_train, y_train)
    ccp_alphas, _ = path.ccp_alphas, path.impurities
    print(f"Computing {len(ccp_alphas)} alphas.")
    skf = StratifiedKFold(n_splits=10, shuffle=True, random_state=random_state)
    search = GridSearchCV(model, {"ccp_alpha":ccp_alphas}, scoring="accuracy", n_jobs=6, cv=skf, verbose=10)
    search.fit(X_train, y_train)
    return search

# Ermittelt den Alphawert mit dem höchsten Score
def select_alpha(alphas):
    max_score = max([x[1] for x in alphas])
    return [x[0] for x in alphas if x[1] == max_score][0]
