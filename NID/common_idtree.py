import pickle


# Berechnet die Gini Importance gemäß Kapitel 3.1.2
def gini_delta(impurities, samples):
    delta = impurities[0] * samples[0] / samples[0]
    delta -= impurities[1] * samples[1] / samples[0]
    delta -= impurities[2] * samples[2] / samples[0]
    return delta


# Lädt die selektierten Feature gemäß der Cut-Off-Nummer in temp_d für jede Feature-Konfiguration.
def get_selected_features(id_):
    temp_d = {"ext":11, "int":11, "red":7, "rex":9}
    with open(f"search/rank_{id_.as_file()}.pkl", "rb") as file:
        ranking = pickle.load(file)
        return ranking["Set"][temp_d[id_.mod]]
    return []