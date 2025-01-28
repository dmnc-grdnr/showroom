# Erzeugt Abbildungen der normaisilerten Konfusionsmatrizen aus Kapitel 5.2
# Benötigte Dateien:
#   model/model_*.pkl (alle Modelle)
#   data/netflow_sample.parquet
# Ausgabe im Ordner img
from common import Identifier
from common import rename_attack
from common import get_modelnames
from common import get_modifications
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pickle
import seaborn as sns


def load_matrices():
    matrices = dict()
    print(id_)
    for mod in get_modifications():
        id_.mod = mod
        with open(f"scores/matrix_test_{id_.as_file()}.pkl", "rb") as file:
            _, matrix = pickle.load(file)
            matrix = matrix / sum(sum(matrix)) # Normalisieren
            matrix = np.floor(matrix * 1000) / 10 # Umwandlung in Prozent
            matrices[mod] = matrix
    return matrices


def save_image(matrices):
    f, axes = plt.subplots(nrows=4, ncols=1, figsize=(12, 15), sharey=True)

    for ax, (key, matrix) in zip(axes, matrices.items()):
        sns.heatmap(matrix, annot=True, annot_kws={'color': "black"}, ax=ax,
                    cmap=sns.light_palette("red"), vmin=7, vmax=12,
                    yticklabels=all_attacks, xticklabels=all_attacks, cbar_kws={'format': '%.0f%%'})

        ax.text(-0.1, 1.1, key, transform=ax.transAxes, size=18, weight='bold')

    plt.subplots_adjust(wspace=0.1, hspace=0.5)
    plt.savefig(f'img/{dataset}/confusion_{id_.name}.png', bbox_inches='tight')


if __name__ == "__main__":
    df = pd.read_parquet("data/netflow_sample.parquet")
    all_attacks = sorted([rename_attack(x) for x in df["Attack"].unique()])

    dataset = "test_mod"
    dataset_title = "Test data set"

    Path("img").mkdir(parents=True, exist_ok=True)
    Path(f"img/{dataset}").mkdir(parents=True, exist_ok=True)

    for name, name_title in get_modelnames().items():
        id_ = Identifier()
        id_.title = "netflow_sample"
        id_.name = name

        result = load_matrices()
        save_image(result)

