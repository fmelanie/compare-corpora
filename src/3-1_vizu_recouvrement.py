#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   3-1_vizu_recouvrement.py
@Time    :   2026/09/26
@Author  :   Frédérique Mélanie
@Version :   1.0
@Contact :   frederique.melanie@ens.psl.eu
'''

from pathlib import Path
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def zscore(series):
    x = pd.to_numeric(series, errors="coerce").astype(float)
    s = x.std(ddof=0)
    if s == 0 or np.isnan(s):
        return pd.Series(np.zeros(len(x)), index=x.index)
    return (x - x.mean()) / s

def main():

    myCsvFile = "taux_recouvrement_par_oeuvre.csv"

    dir_out = "img/"

    #dir_out.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(myCsvFile, encoding="utf-8-sig")

    required = [
        "oeuvre",
        "voc_data_D",
        "voc_data_L",
        "voc_communs",
        "recouvrement_data_D_par_data_L (%)",
        "recouvrement_data_L_par_data_D (%)",
    ]

    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(
            "Colonnes manquantes dans le CSV : " + ", ".join(missing)
        )

    # La ligne TOTAL est retirée des graphiques par œuvre.
    data = df[df["oeuvre"].astype(str).str.upper() != "TOTAL"].copy()

    numeric_cols = [
        "voc_data_D", "voc_data_L", "voc_communs",
        "recouvrement_data_D_par_data_L (%)",
        "recouvrement_data_L_par_data_D (%)",
    ]
    for col in numeric_cols:
        data[col] = pd.to_numeric(data[col], errors="coerce")

    data = data.dropna(
        subset=[
            "recouvrement_data_D_par_data_L (%)",
            "recouvrement_data_L_par_data_D (%)"
        ]
    ).sort_values(
        "recouvrement_data_D_par_data_L (%)"
    ).reset_index(drop=True)

    # Z-scores : utiles pour repérer les œuvres atypiques.
    data["z_recouvrement_d_D"] = zscore(
        data["recouvrement_data_D_par_data_L (%)"]
    )
    data["z_recouvrement_d_L"] = zscore(
        data["recouvrement_data_L_par_data_D (%)"]
    )

    # 1. créer un HEATMAP
    
    heat = data.set_index("oeuvre")[
        [
            "recouvrement_data_D_par_data_L (%)",
            "recouvrement_data_L_par_data_D (%)"
        ]
    ]

    fig, ax = plt.subplots(
        figsize=(7.5, max(6, 0.38 * len(heat) + 1.5))
    )

    im = ax.imshow(heat.values, aspect="auto")

    ax.set_xticks(range(2))
    ax.set_xticklabels([
        "Recouvrement Data D",
        "Recouvrement Data L"
    ])
    ax.set_yticks(range(len(heat)))
    ax.set_yticklabels(heat.index)
    ax.set_title("Recouvrement lexical entre Data D et Data L")

    for i in range(len(heat)):
        for j in range(2):
            value = heat.iloc[i, j]
            ax.text(j, i, f"{value:.1f} %", ha="center", va="center")

    fig.colorbar(im, ax=ax, label="Pourcentage de recouvrement")
    fig.tight_layout()
    fig.savefig(
        "img/1_heatmap_recouvrement.png",
        dpi=300,
        bbox_inches="tight"
    )
    plt.close(fig)

    
    # 2. créer un NUAGE DE POINTS
    
    x = data["recouvrement_data_D_par_data_L (%)"]
    y = data["recouvrement_data_L_par_data_D (%)"]

    # Calcul des couleurs en fonction du z-score
    colors = np.where(np.abs(data["z_recouvrement_d_D"]) > 1, "red", "blue")

    fig, ax = plt.subplots(figsize=(10, 8))
    #ax.scatter(x, y)
    ax.scatter(x, y, c=colors, alpha=0.7)


    ax.set_xlabel("Recouvrement de Data D par Data L (%)")
    ax.set_ylabel("Recouvrement de Data L par Data D (%)")
    ax.set_title("Asymétrie du recouvrement lexical")

    ax.axvline(x.mean(), linestyle="--", linewidth=1)
    ax.axhline(y.mean(), linestyle="--", linewidth=1)

    for _, row in data.iterrows():
        oeuvre = str(row["oeuvre"])
        weight = "normal" #"bold" if oeuvre in {"fifi1", "fifi2"} else "normal"
        ax.annotate(
            oeuvre,
            (
                row["recouvrement_data_D_par_data_L (%)"],
                row["recouvrement_data_L_par_data_D (%)"]
            ),
            xytext=(5, 5),
            textcoords="offset points",
            fontsize=9,
            fontweight=weight
        )


    # Légende pour les couleurs
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor="red", label="|z-score| > 1 (atypique)"),
        Patch(facecolor="blue", label="|z-score| ≤ 1 (typique)")
    ]
    ax.legend(handles=legend_elements, loc="upper right")

    fig.tight_layout()
    fig.savefig(
        "img/2_nuage_recouvrement.png",
        dpi=300,
        bbox_inches="tight"
    )
    plt.close(fig)

    # créer un NUAGE DE POINTS... avec prise en compte du volume lexical
    
    taille = data["voc_data_D"] + data["voc_data_L"]

    if taille.max() > taille.min():
        sizes = 80 + 520 * (
            (taille - taille.min()) / (taille.max() - taille.min())
        )
    else:
        sizes = np.full(len(taille), 250)

    fig, ax = plt.subplots(figsize=(10, 8))
    ax.scatter(x, y, s=sizes, alpha=0.7)

    ax.set_xlabel("Recouvrement de Data D par Data L (%)")
    ax.set_ylabel("Recouvrement de Data L par Data D (%)")
    ax.set_title("Recouvrement lexical et taille du vocabulaire")

    ax.axvline(x.mean(), linestyle="--", linewidth=1)
    ax.axhline(y.mean(), linestyle="--", linewidth=1)

    for _, row in data.iterrows():
        oeuvre = str(row["oeuvre"])
        weight = "normal" #"bold" if oeuvre in {"fifi1", "fifi2",fifi3} else "normal"
        ax.annotate(
            oeuvre,
            (
                row["recouvrement_data_D_par_data_L (%)"],
                row["recouvrement_data_L_par_data_D (%)"]
            ),
            xytext=(5, 5),
            textcoords="offset points",
            fontsize=9,
            fontweight=weight
        )

    for special in ["fifi1", "fifi2"]:
        subset = data[data["oeuvre"].astype(str) == special]
        if not subset.empty:
            row = subset.iloc[0]
            ax.scatter(
                row["recouvrement_data_D_par_data_L (%)"],
                row["recouvrement_data_L_par_data_D (%)"],
                s=180,
                linewidth=2
            )

    fig.tight_layout()
    fig.savefig(
        "img/3_nuage_recouvrement_taille_vocabulaire.png",
        dpi=300,
        bbox_inches="tight"
    )
    plt.close(fig)

    # EXPORT DES Z-SCORES
   
    data[
        [
            "oeuvre",
            "recouvrement_data_D_par_data_L (%)",
            "recouvrement_data_L_par_data_D (%)",
            "z_recouvrement_d_D",
            "z_recouvrement_d_L",
            "voc_data_D",
            "voc_data_L",
            "voc_communs",
        ]
    ].to_csv(
        "img/4_zscores_recouvrement.csv",
        index=False,
        encoding="utf-8-sig"
    )

    #print("Graphiques créés dans :", out.resolve())
    print(" - 1_heatmap_recouvrement.png")
    print(" - 2_nuage_recouvrement.png")
    print(" - 3_nuage_recouvrement_taille_vocabulaire.png")
    print(" - 4_zscores_recouvrement.csv")

    # Exemple : Histogramme des z-scores
    plt.figure(figsize=(10, 6))
    plt.hist(data["z_recouvrement_d_D"], bins=10, alpha=0.5, label="Recouvrement D→L")
    plt.hist(data["z_recouvrement_d_L"], bins=10, alpha=0.5, label="Recouvrement L→D")
    plt.axvline(2, color="red", linestyle="--", label="Seuil |z|=2")
    plt.axvline(-2, color="red", linestyle="--")
    plt.legend()
    plt.title("Distribution des z-scores de recouvrement")
    plt.xlabel("z-score")
    plt.ylabel("Fréquence")
    plt.savefig("img/4_histogramme_zscores.png", dpi=300)
    plt.close()



if __name__ == "__main__":
    main()
