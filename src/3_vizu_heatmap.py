#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   3-2_vizu_body-part.py
@Time    :   2026/09/26
@Author  :   Frédérique Mélanie
@Version :   1.0
@Contact :   frederique.melanie@ens.psl.eu
'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Les fichiers à analyser
dirData = "data_result/"
listFiles = ["partie-du-corps","pronoms"]

# Analyser les fichiers 1 à 1
for file in listFiles:

    df = pd.read_csv(
        #dirData+"tableau_difference_D-L_partCorps.csv",
        dirData+"tableau_difference_D-L_"+file+".csv",
        encoding="utf-8-sig"
    )

    # La première colonne contient les expressions
    # et les autres colonnes correspondent aux œuvres.
    df = df.set_index(df.columns[0])

    # On enlève la colonne "sum" si elle existe
    colonnes_oeuvres = [
        col for col in df.columns
        if col != "sum"
    ]

    # Conversion en numérique
    df[colonnes_oeuvres] = df[colonnes_oeuvres].apply(
        pd.to_numeric,
        errors="coerce"
    )


    # 2. Trier les expressions
    # Somme des écarts pour chaque expression
    totaux = df[colonnes_oeuvres].sum(axis=1)

    # Trier de la plus grande somme à la plus petite
    df = df.loc[totaux.sort_values(ascending=False).index]

    # 3. Préparer les données pour la heatmap
    # "corp" mis pour "corpus"
    data = df[colonnes_oeuvres]
    data = data.drop(columns=["pos","corp.L", "corp.D"])

    # 4. Créer la heatmap
    fig, ax = plt.subplots(figsize=(14, 15))

    im = ax.imshow(
        data,
        aspect="auto",
        interpolation="nearest"
    )

    # Axe X : œuvres
    ax.set_xticks(range(len(data.columns)))
    ax.set_xticklabels(
        data.columns,
        rotation=55,
        ha="right",
        fontsize=9
    )

    # Axe Y : expressions
    ax.set_yticks(range(len(data.index)))
    ax.set_yticklabels(
        data.index,
        fontsize=9
    )

    ax.set_xlabel("Œuvres")
    ax.set_ylabel(
        #"Entités (partie du corps)"
        "Entités ("+file+")"
    )

    ax.set_title(
        "Différences des contingences : Democrat – Litbank-fr"
    )

    # 5. Afficher les valeurs dans les cases
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):

            value = data.iloc[i, j]

            # Ne rien afficher si la cellule est vide / NaN
            if not pd.isna(value):
                ax.text(
                    j,
                    i,
                    f"{int(value)}",
                    ha="center",
                    va="center",
                    fontsize=7
                )

    # 6. la légende 
    fig.colorbar(
        im,
        ax=ax,
        label="Écart D–L"
    )

    plt.tight_layout()

    # 7. Enregistrer
    plt.savefig(
        #"img/heatmap_parties_corps.png",
        "img/heatmap_"+file+".png",
        dpi=200,
        bbox_inches="tight"
    )

    #plt.show()