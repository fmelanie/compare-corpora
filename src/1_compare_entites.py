#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   1_compare_entities.py
@Time    :   2026/09/26
@Author  :   Frédérique Mélanie
@Version :   1.0
@Contact :   frederique.melanie@ens.psl.eu
'''

'''
This script retains only the annotated entities from the following two projects:
- Democrat: the Democrat corpus (D)
- Propp: the fr_Litbank corpus (L)

1/ Create a contingency table for both projects
2/ Merge the two tables into one
3/ Create three selective tables: 
- one containing entities that occur with the same frequency in both projects;
- one containing entities referring to a body part;
- one selecting the most frequent pronouns
'''

import re
import csv
import spacy
import pandas as pd
import json
import numpy as np
import xml.etree.ElementTree as ET

# Files of the corpora / directory
def import_list(myCsv) :
	myFilesD={}
	myFilesP={}

	with open(myCsv, mode='r', newline='', encoding='utf-8') as file:
		
		reader = csv.reader(file, delimiter=',')
		next(reader)
		for row in reader:

			if row[1] != "[no]" :
				if row[1] not in myFilesD:
					if row[2] != "[no]" :
						myFilesD[row[1]]=["[regrp]",row[1],row[4],row[8]]
					else :
						myFilesD[row[1]]=[row[1],row[1],row[4],row[8]]

				myFilesP[row[0]]=[row[2],row[3],row[4],row[8]]

	return myFilesP,myFilesD

# Clean data1 & data2 
def nett_data(data_str):
	# example : anne d’autriche -> anne d'autriche
	data_str_nett = re.sub("’","'",data_str)
	# delete ...
	# apostrophe in the end of the string - example : j' -> j
	data_str_nett = data_str_nett.rstrip("'")
	# the "." in the string
	data_str_nett = re.sub("\.","'",data_str)
	
	data_str_nett = re.sub(",","",data_str)

	return data_str_nett

def recup_xml_pos(filename,borneInf,borneSup):

	myDirXml="data/democrat/xml/"
	
	# Import XML file
	tree = ET.parse(f"{myDirXml}{filename}.xml")
	root = tree.getroot()

	# the namespaces
	namespaces = {
		'tei': 'http://www.tei-c.org/ns/1.0',       # catch <w>, <s>, etc.
		'txm': 'http://textometrie.org/1.0'         # catch <txm:form>, <txm:ana>
	}
	
	mylistPos=[]

	try :
		myBornes = list(range(int(borneInf), int(borneSup)+1))
	
		for i in myBornes:

			w = root.find(f'.//tei:w[@n="{i}"]', namespaces)

			if w is not None:

				frpos_ana = w.find('txm:ana[@type="#frpos"]', namespaces)
				if frpos_ana is not None:
					frpos_text = frpos_ana.text 
					mylistPos.append(frpos_text)
	except :
		mylistPos=["nsp"]
	
	return mylistPos

# Import the ann files - Democrat
def import_ann_data(folder_in,filename,myEntitiesPerBook_D,myCountEntities_D,myEntitiesPos_D,titleSimple,titleXml):
	
	with open(folder_in+"/"+filename+".ann", mode='r', newline='', encoding='utf-8') as file:
		
		print(filename)

		if titleSimple not in myEntitiesPos_D:
			myEntitiesPos_D[titleSimple]=dict()

		if titleSimple not in myEntitiesPerBook_D:
			myEntitiesPerBook_D[titleSimple]=dict()

		reader = csv.reader(file, delimiter='\t')
		for row in reader:
			myEntiteInit = str(row[2]).strip().strip('"').strip("'").lower()
			myEntite = nett_data(myEntiteInit)
							
			if myEntite not in myEntitiesPos_D[titleSimple]:
				# Recuperer le POS
				myEntiteRef = row[1].split()
				# Recuperer les bornes
				myEntiteBorneInf = myEntiteRef[-2]
				myEntiteBorneSup = myEntiteRef[-1]
				myLstPos=recup_xml_pos(titleXml,myEntiteBorneInf,myEntiteBorneSup)
				myEntitiesPos_D[titleSimple][myEntite]=myLstPos

			#GLOBAL
			if myEntite not in myCountEntities_D:
				myCountEntities_D[myEntite]=list()
				myCountEntities_D[myEntite]=[1,[titleSimple]]
			else:
				myNumber = myCountEntities_D[myEntite][0]+1
				myCountEntities_D[myEntite][0]=myNumber
				if titleSimple not in myCountEntities_D[myEntite][1]:
					myCountEntities_D[myEntite][1].append(titleSimple)

			##perBook
			if myEntite not in myEntitiesPerBook_D[titleSimple]:
				myEntitiesPerBook_D[titleSimple][myEntite]=1
				myEntitiesPos_D[titleSimple][myEntite]=myLstPos

			else:
				myNumber = myEntitiesPerBook_D[titleSimple][myEntite]+1
				myEntitiesPerBook_D[titleSimple][myEntite]=myNumber
			

	return myEntitiesPerBook_D, myCountEntities_D, myEntitiesPos_D

# Importer les fichiers entities - Fr-Litbank (Propp)
def import_entities_data(folder_in,filename,myEntitiesPerBook_P,myCountEntities_P,myEntitiesPos_P,titleSimple):
	
	if titleSimple not in myEntitiesPerBook_P:
		myEntitiesPerBook_P[titleSimple]=dict()

	with open(folder_in+"/"+filename+".entities", mode='r', newline='', encoding='utf-8') as file:
		# Créer un lecteur CSV avec tabulation comme séparateur
		reader = csv.reader(file, delimiter='\t')
		# Ignorer la première ligne (en-tête)
		next(reader)
		for row in reader:

			myEntiteInit= str(row[5]).strip().strip('"').strip("'").lower()
			myEntite = nett_data(myEntiteInit)

			#GLOBAL
			if myEntite not in myCountEntities_P:
				myCountEntities_P[myEntite]=list()
				myCountEntities_P[myEntite]=[1,[titleSimple]]
			else:
				myNumber = myCountEntities_P[myEntite][0]+1
				myCountEntities_P[myEntite][0]=myNumber
				if titleSimple not in myCountEntities_P[myEntite][1]:
					myCountEntities_P[myEntite][1].append(titleSimple)

			#perBook
			if myEntite not in myEntitiesPerBook_P[titleSimple]:
				#myEntitiesPerBook_P[titleSimple][myEntite]=list()
				myEntitiesPerBook_P[titleSimple][myEntite]=1
			else:
				myNumber = myEntitiesPerBook_P[titleSimple][myEntite]+1
				myEntitiesPerBook_P[titleSimple][myEntite]=myNumber
			
			if myEntite not in myEntitiesPos_P:
				myEntitiesPos_P[myEntite]=set()
			myEntitiesPos_P[myEntite].add(row[21])

	return myEntitiesPerBook_P, myCountEntities_P,myEntitiesPos_P

def main ():

	folder_res = "data_result/"

	# this files aren't in this git

	# https://doi.org/10.82270/democrat/v1.1
	folder_in_D= "data/democrat/brat/entities"
	myCountEntities_D=dict()
	myEntitiesPerBook_D=dict()
	myEntitiesPos_D=dict()
	# https://lattice-8094.github.io/propp/
	folder_in_P= "data/propp"
	myCountEntities_P=dict()
	myEntitiesPerBook_P=dict()
	myEntitiesPos_P=dict()

	myEntitiesPerBook_PAll=dict()
	myCountEntities_PAll=dict()

	# list of files : 
	myFilesPropp,myFilesDemocrat = import_list("lst_files.csv")
	# 32 files == Listbank-fr (Propp) - the full corpus / 27 files Litbank - fifi more than in Democrat / 18 files Dem

	# IMPORT DATA :
	# Democrat
	for myFile, myCorresp in myFilesDemocrat.items():
		titleSimple = myCorresp[2]
		titleXml = myCorresp[3]
		 
		import_ann_data(folder_in_D,myFile,myEntitiesPerBook_D,myCountEntities_D,myEntitiesPos_D,titleSimple,titleXml)
		

	# Fr-Litbank (PROPP) just the commun files with Democrat
	for myFile, myCorresp in myFilesPropp.items():
		titleSimple = myCorresp[2]
		import_entities_data(folder_in_P,myFile,myEntitiesPerBook_P,myCountEntities_P,myEntitiesPos_P,titleSimple)
		
	# DATA to json files 	
	with open(folder_res + "data-Democrat.json", "w", encoding="utf-8") as f:
	    json.dump(myEntitiesPerBook_D, f, ensure_ascii=False, indent=2)
	with open(folder_res + "data-Litbank.json", "w", encoding="utf-8") as f:
	    json.dump(myEntitiesPerBook_P, f, ensure_ascii=False, indent=2)
	with open(folder_res + "data-posDem.json", "w", encoding="utf-8") as f:
		json.dump(myEntitiesPos_D, f, ensure_ascii=False, indent=2)

	# with open(folder_res + "data-posDem.json", "r", encoding="utf-8") as f:
	#     myEntitePos = json.load(f)
	
	# Entities : Total number of entities per corpus
	print("Numbers entities / size of vocabulary : ")
	print("Democrat :: " + str(len(myCountEntities_D)))
	print("-> nb files  " + str(len(myEntitiesPerBook_D)))
	print("Litbank :: " + str(len(myCountEntities_P)))
	print("-> nb files  " + str(len(myEntitiesPerBook_P)))
	
	#print(myCountEntities_D)

	# contingency tables
	tableConting_D = pd.DataFrame(myEntitiesPerBook_D).fillna(0).astype(int)
	tableConting_P = pd.DataFrame(myEntitiesPerBook_P).fillna(0).astype(int)

	# PRESENT... :
	## ... PAS DANS DEMOCRAT / uniquement dans litbank (Propp)
	non_present_D = tableConting_P.index.difference(tableConting_D.index)
	print("Nb voc present dans P (pas D) : "+ str(len(non_present_D)))
	print(non_present_D)
	## ... PAS DANS PROPP (litbank) / uniquement dans Democrat
	non_present_P = tableConting_D.index.difference(tableConting_P.index)
	print("Nb voc present dans D (pas P) : "+ str(len(non_present_P)))
	print(non_present_P)
	nbOcc_D = sum(liste[0] for liste in myCountEntities_D.values() if liste)
	print("nb occ D : " + str(nbOcc_D))
	nbOcc_P = sum(liste[0] for liste in myCountEntities_P.values() if liste)
	print("nb occ P : " + str(nbOcc_P))
	## COMMUN
	index_communs = tableConting_D.index.intersection(tableConting_P.index).tolist()
	print("Nb voc commun (D et P) : "+ str(len(index_communs)))
	#print(index_communs)

	# Lst des entités : fréquence identiques entre Dem et Propp
	myListFreqEgale = list()
	myListFreqEgale.append(["Entité","nb Occ","Liste oeuvre"])
	for i in index_communs:
		if int(myCountEntities_D[i][0]) == int(myCountEntities_P[i][0]):
			myNbOcc = myCountEntities_D[i][0]
			myEntite = i
			myListeOeuvre = ','.join(myCountEntities_D[i][1])
			# les freq sont identiques
			myTempList = [myEntite,myNbOcc,myListeOeuvre]
			myListFreqEgale.append(myTempList)
	print("---------- lg :" +str(len(myListFreqEgale)))


	with open(folder_res+"entites_freqEgal_DL.csv", "w", newline="", encoding="utf-8") as f:
  		writer = csv.writer(f)
  		writer.writerows(myListFreqEgale)  # Écrit toutes les lignes d'un coup

	# même ensemble de mots et même ensemble d'œuvres
	tableConting_D, tableConting_P = tableConting_D.align(tableConting_P, join="outer", fill_value=0)
	#Pour chaque vocable et chaque œuvre, combien d'occurrences Data 1 a en plus ou en moins que Data 2 ?
	difference = tableConting_D - tableConting_P

	colonnes_oeuvres = difference.columns
	
	# ne pas mettre 0 mais " " (vide / nan) quand les mots ne sont dans aucune des 2 oeuvres
	difference = difference.mask(
		(tableConting_D == 0) & (tableConting_P == 0),
		np.nan
	)

	difference[colonnes_oeuvres] = difference[colonnes_oeuvres].astype("Int64")
	difference["sum"] = difference[colonnes_oeuvres].sum(axis=1)
	# difference.to_csv(folder_res+'tableau_difference_D-P.csv')

	# AJOUTER les POS / comment utiliser, interroger
	resultat = {}

	myEntitePosPos = dict()
	for book,value in myEntitePos.items():
		for myStr, myPos in value.items():
			if myStr not in myEntitePosPos:
				myEntitePosPos[myStr]=myPos
	#print(myEntitePos)

	#myEntitiesPos_P -> à supprimer ?
	for mot, ligne in difference.iterrows():
		myPos = ""
		if mot in myEntitePosPos:
			myPos = myEntitePosPos[mot]
		#if mot in myEntitiesPos_P:
		#	myPos = myEntitiesPos_P[mot]

		resultat[mot] = {
			"pos": myPos
		}

		# in Democrat ("D" = oui) / in Litbank-fr ("L"=oui)
		if mot in non_present_D:
			resultat[mot]["corp.D"] = "non"
		else :
			resultat[mot]["corp.D"] = "oui"

		if mot in non_present_P:
			resultat[mot]["corp.L"] = "non"
		else :
			resultat[mot]["corp.L"] = "oui"

		for oeuvre, valeur in ligne.items():

			if pd.notna(valeur):
				resultat[mot][oeuvre] = int(valeur)

	df = pd.DataFrame.from_dict(resultat, orient="index")

	#df.index.name = "vocable"

	#colonnes_oeuvres = [c for c in df.columns if c != "pos"]
	df[colonnes_oeuvres] = df[colonnes_oeuvres].astype("Int64")
	col = df.pop('sum')
	df["sum"] = col
	df["sum"] = df[colonnes_oeuvres].sum(axis=1)

	df.to_csv(
	    folder_res+"tableau_difference_D-L_withPosP.csv",
	    encoding="utf-8-sig"
	)
	
	# recuperer les annotations de parties du corps
	myDet = ["le","la","les","l'","un","une","des","d'","ce","ces","cet","nos","vos","leur","leurs","mes","tes","ses","mon","ton","son","ma","ta","sa"]
	partie_corps = ["cou", "main", "mains", "oeil","yeux","pied","lèvres","visage","bouche","genou","genoux"]

	pattern = (
	    r"^(?:"
	    + "|".join(map(re.escape, myDet))
	    + r") (?:"
	    + "|".join(map(re.escape, partie_corps))
	    + r")$"
	)

	df_partCorps = df[
	    df.index.str.contains(
	        pattern,
	        case=False,
	        na=False,
	        regex=True
	    )
	].copy()

	#df_partCorps[colonnes_oeuvres] = df_partCorps[colonnes_oeuvres].astype("Int64")
	#df_partCorps["sum"] = df_partCorps[colonnes_oeuvres].sum(axis=1)

	df_partCorps.to_csv(
	    folder_res+"tableau_difference_D-L_partie-du-corps.csv",
	    encoding="utf-8-sig"
	)

	# Pronoms
	# myPron = ["elle","je","son","lui","sa","ses","nous","j","qui","vous","me","mon","ils","l","m","ma","la","on","moi","le","mes","tu","leur","notre","leurs","les","y","dont","te","nos","votre","c","eux","elles","t","qu","toi","que","en","elle-même","l'autre","ton","ta","lui-même","tous","vos","chacun","ce","celui-ci","mienne","laquelle","tes","moi-même","s","sien","mien","miens","quelqu'un","siens","un autre","celui","toutes","un","celle","miennes","tienne","tous ceux","vous-même","ceux","des autres","ça","des miens"]
	myPron = ["elle","je","son","lui","sa","ses","nous","j","vous","me","mon","ils","l","m","la","on","moi","le","mes","tu","leur","notre","leurs","les","te","nos","votre","eux","elles","t","toi","ton","ta","vos","tes"]

	df_pronoms = df[
    	df.index.str.lower().isin([p.lower() for p in myPron])
	].copy()
	
	df_pronoms.to_csv(
			folder_res+"tableau_difference_D-L_pronoms.csv",
			encoding="utf-8-sig"
		)

if __name__ == "__main__":
	main()