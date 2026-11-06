# compare-corpora
The Democrat and Litbank-fr corpora – part of the Propp project – are two corpora of annotated reference strings. The second partly draws on data from the first. It is this overlap that we shall examine and analyse here. In what ways does fr-Litbank constitute a reuse and adaptation of Democrat?

The article [... link to coming soon ...]

The 0_run_all.sh and 1_compare_entites.py files run on a folder called ‘data’ which contain the corpora - from the 2 projects :
- litbank (https://lattice-8094.github.io/propp/)
- Democrat (https://doi.org/10.82270/democrat/v1.1) 

The result of this step is in the data_result folder. The data folder isn't in this repository ; the other scripts in the src folder use the data of the data_result.

```
.
├── data_result
│   ├── data-Democrat.json
│   ├── data-Litbank.json
│   ├── data-posDem.json
│   ├── entites_freqEgal_DL.csv
│   ├── tableau_difference_D-L_partie-du-corps.csv
│   ├── tableau_difference_D-L_pronoms.csv
│   └── tableau_difference_D-L_withPosP.csv
├── img
│   ├── heatmap_partie-du-corps.png
│   ├── heatmap_pronoms.png
│   ├── recouvrement_heatmap.png
│   ├── recouvrement_histogramme_zscores.png
│   ├── recouvrement_nuage.png
│   ├── recouvrement_nuage_taille-vocabulaire.png
│   └── recouvrement_zscores.csv
├── result
│   ├── DEMOCRAT-2026-11-06.txm
│   ├── entites_freqEgal_DL.csv
│   └── taux_recouvrement_par_oeuvre.csv
├── src
│   ├── 0_run_all.sh
│   ├── 1_compare_entites.py
│   ├── 2_recouvrement.py
│   ├── 3_vizu_heatmap.py
│   ├── 3_vizu_recouvrement.py
│   ├── DemocratXMLToBrat_class.py
│   └── DemocratXMLToBrat.py
├── files.csv
└──  README.md
```

<a rel="license" href="https://creativecommons.org/licenses/by-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by/4.0/88x31.png" /></a>
