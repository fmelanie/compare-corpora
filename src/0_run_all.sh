#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   0_run_all.py - used : DemocratXMLToBrat & DemocratXMLToBrat_class
@Time    :   2026/09/26
@Author  :   Frédérique Mélanie, Bruno Boberley, Propp Team 
@Version :   1.0
@Contact :   frederique.melanie@ens.psl.eu
'''

'''
This script converts from XML format to ANN format.
'''

# List of files common to both projects
common_files=("sarrasine" "morteamoureuse" "pauline" "madamedehautefort" "capitainefracasse" "ventredeparis" "bouvardetpecuchet" "mademoisellefifi-1" "mademoisellefifi-2" "mademoisellefifi-3" "rosaliedeconstant" "elisabethseton" "jeanchristophe-1" "jeanchristophe-2" "nemoville" "diableaucorps" "delavilleaumoulin" "doucelumiere")

contains() {
    local elem
    for elem in "${@:2}"; do
        [[ "$elem" == "$1" ]] && return 0
    done
    return 1
}

# Find all .xml files in the folder
for file in data/democrat/xml/*.xml; do
    filename=$(basename "$file" .xml)

    # import the file from this page
    # https://doi.org/10.82270/democrat/v1.1
    if contains "$filename" "${common_files[@]}"; then
        urs_file="data/democrat/xml-urs/${filename}-urs.xml"

        if [[ -f "$urs_file" ]]; then
            echo "Traitement de : $file et $urs_file"
            python src/DemocratXMLToBrat.py "$file" "$urs_file"
        else
            echo "Fichier correspondant manquant : $urs_file"
        fi
    fi
done

