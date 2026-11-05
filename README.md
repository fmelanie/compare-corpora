# compare-corpora
The Democrat and Litbank-fr corpora – part of the Propp project – are two corpora of annotated reference strings. The second partly draws on data from the first. It is this overlap that we shall examine and analyse here. In what ways does fr-Litbank constitute a reuse and adaptation of Democrat?

To run the 0_run_all.sh and 1_compare_entites.py files, you need to create a folder called ‘data’ with the corpora - from the 2 projects :
- litbank (https://lattice-8094.github.io/propp/)
- Democrat (https://doi.org/10.82270/democrat/v1.1) 


```
.
├── data_result
│   ├── data-Democrat.json
│   ├── data-Litbank.json
│   ├── data-posDem.json
│   ├── data-posDem_SAUV.json
│   ├── entites_freqEgal_DL.csv
│   ├── tableau_difference_D-L_partCorps.csv
│   ├── tableau_difference_D-L_pronoms.csv
│   └── tableau_difference_D-L_withPosP.csv
├── img
│   ├── 1_heatmap_recouvrement.png
│   ├── 2_nuage_recouvrement.png
│   ├── 4_histogramme_zscores.png
│   └── heatmap_parties_corps.png
├── lst_files.csv
├── README.md
├── result
│   └── taux_recouvrement_par_oeuvre.csv
└── src
    ├── 0_run_all.sh
    ├── 1_compare_entites.py
    ├── 2_recouvrement.py
    ├── 3-1_vizu_recouvrement.py
    ├── 3-2_vizu_body-part.py
    ├── DemocratXMLToBrat_class.py
    └── DemocratXMLToBrat.py

```

<a rel="license" href="https://creativecommons.org/licenses/by-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by/4.0/88x31.png" /></a>
