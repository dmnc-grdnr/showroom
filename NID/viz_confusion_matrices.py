# Erzeugt Abbildungen der Konfusionsmatrizen auf den Validierungsdaten
# Benötigte Dateien:
#   model/model_*.pkl (alle Modelle)
#   data/netflow_sample.parquet
#   data/transformation/cicddos2019_labeled.csv
#   data/transformation/cicids2017_labeled.csv
#   data/transformation/fhswfcnl_labeled.csv
# Ausgabe im Ordner img
from common import Identifier
from common import rename_attack
from common import get_datasets
from common import get_modelnames
from common import get_modifications
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
import pickle
import seaborn as sns


def load_matrices():
    matrices = dict()
    print(id_)
    for mod in get_modifications():
        id_.mod = mod
        with open(f"scores/matrix_{dataset}_{id_.as_file()}.pkl", "rb") as file:
            _, matrices[mod] = pickle.load(file)
    return matrices


def save_image(matrices):
    f, axes = plt.subplots(nrows=4, ncols=1, figsize=(15, 20), sharey=True)

    for ax, (key, matrix) in zip(axes, matrices.items()):
        matrix_mod = matrix
        sns.heatmap(matrix_mod, annot=True, fmt='g', annot_kws={'color': "black"}, ax=ax,
                    cmap=sns.light_palette("red"), vmin=0, vmax=matrix_mod.mean(),
                    yticklabels=all_attacks, xticklabels=all_attacks)
        if key == "int":
            ax.set_title(f"{dataset_title} classifications by {name_title}")
        ax.text(-0.1, 1.1, key, transform=ax.transAxes, size=15, weight='bold')
    plt.savefig(f'img/{dataset}/{id_.name}_{dataset}.png', bbox_inches='tight')


if __name__ == "__main__":
    Path("img").mkdir(parents=True, exist_ok=True)
    df = pd.read_parquet("data/netflow_sample.parquet")
    all_attacks = sorted([rename_attack(x) for x in df["Attack"].unique()])

    for dataset, dataset_title in get_datasets().items():
        Path(f"img/{dataset}").mkdir(parents=True, exist_ok=True)
        for name, name_title in get_modelnames().items():
            id_ = Identifier()
            id_.title = "netflow_sample"
            id_.name = name

            result = load_matrices()
            save_image(result)

