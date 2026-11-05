#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   2_recouvrement.py
@Time    :   2026/09/26
@Author  :   Frédérique Mélanie
@Version :   1.0
@Contact :   frederique.melanie@ens.psl.eu
'''

import json
import pandas as pd

# 1. Import the dictionnaries / JSON files
folder_data = "data_result/"
# data_D = Democrat / data_L = Propp
with open(folder_data+"data-Democrat.json", "r", encoding="utf-8") as f:
    data_D = json.load(f)

with open(folder_data+"data-Litbank.json", "r", encoding="utf-8") as f:
    data_L = json.load(f)

# 2. Calculer les taux de recouvrement pour chaque œuvre
resultats = []

# Union des œuvres
oeuvres = sorted(set(data_D.keys()) | set(data_L.keys()))

for oeuvre in oeuvres:

    # Vocabulaire de chaque annotation pour cette œuvre
    vocab_D = set(data_D.get(oeuvre, {}).keys())
    vocab_L = set(data_L.get(oeuvre, {}).keys())

    # Vocabulaire commun
    vocab_commun = vocab_D & vocab_L

    # Nombre de vocables
    nb_vocab_D = len(vocab_D)
    nb_vocab_L = len(vocab_L)
    nb_commun = len(vocab_commun)

    # Recouvrement
    if nb_vocab_D > 0:
        recouvrement_data_D = 100 * nb_commun / nb_vocab_D
    else:
        recouvrement_data_D = 0

    if nb_vocab_L > 0:
        recouvrement_data_L = 100 * nb_commun / nb_vocab_L
    else:
        recouvrement_data_L = 0

    resultats.append({
        "oeuvre": oeuvre,
        "voc_data_D": nb_vocab_D,
        "voc_data_L": nb_vocab_L,
        "voc_communs": nb_commun,
        "recouvrement_data_D_par_data_L (%)": recouvrement_data_D,
        "recouvrement_data_L_par_data_D (%)": recouvrement_data_L,
    })

# 3. Créer le tableau
df = pd.DataFrame(resultats)

# Arrondir à 2 chiffres apres virgule
df["recouvrement_data_D_par_data_L (%)"] = \
    df["recouvrement_data_D_par_data_L (%)"].round(1)

df["recouvrement_data_L_par_data_D (%)"] = \
    df["recouvrement_data_L_par_data_D (%)"].round(1)


# 4. Calcul du recouvrement TOTAL

# Constituer ici le vocabulaire global de chaque annotation.
# Un mot est compté une seule fois, même s'il apparaît dans plusieurs œuvres.

vocab_global_data_D = set()
vocab_global_data_L = set()

for oeuvre in data_D:
    vocab_global_data_D.update(data_D[oeuvre].keys())

for oeuvre in data_L:
    vocab_global_data_L.update(data_L[oeuvre].keys())

# Vocabulaire commun global
vocab_global_commun = (
    vocab_global_data_D & vocab_global_data_L
)

# Nombres de vocables globaux
nb_global_data_D = len(vocab_global_data_D)
nb_global_data_L = len(vocab_global_data_L)
nb_global_commun = len(vocab_global_commun)

# Taux de recouvrement globaux
if nb_global_data_D > 0:
    recouvrement_global_data_D = (
        100 * nb_global_commun / nb_global_data_D
    )
else:
    recouvrement_global_data_D = 0

if nb_global_data_L > 0:
    recouvrement_global_data_L = (
        100 * nb_global_commun / nb_global_data_L
    )
else:
    recouvrement_global_data_L = 0

# 5. Ajouter la ligne TOTAL au tableau

ligne_total = pd.DataFrame([{
    "oeuvre": "TOTAL",
    "voc_data_D": nb_global_data_D,
    "voc_data_L": nb_global_data_L,
    "voc_communs": nb_global_commun,
    "recouvrement_data_D_par_data_L (%)":
        round(recouvrement_global_data_D, 1),
    "recouvrement_data_L_par_data_D (%)":
        round(recouvrement_global_data_L, 1),
}])

df = pd.concat(
    [df, ligne_total],
    ignore_index=True
)


print(df.to_string(index=False))

df.to_csv(
    "result/taux_recouvrement_par_oeuvre.csv",
    index=False,
    encoding="utf-8-sig"
)

