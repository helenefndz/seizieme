#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  4 10:43:08 2022
@author: helenenouveau
"""



import pandas as pd

from quiestce16.models import Mystere, Image, Indice

def run():
    deputes = pd.read_csv('docs/élus2022_début.csv', index_col=[0])

    Mystere.objects.all().delete()

    for line in deputes.index:
        solution = "{} {}".format(deputes.at[line,'Prénom'], deputes.at[line,'Nom'])
      
        prénom = "Son prénom est " + deputes.at[line, 'Prénom'] + "."
        # groupe = "Groupe : " + deputes.at[line, 'Groupe politique (complet)'] + "."
        département = "Département / Français de l'étranger : "+ deputes.at[line, 'Département']
        
        #indice "initiale ou particule"
        i = deputes.at[line, 'Nom'][0]
        if i.isupper():
            initiale = "L'initiale de son nom de famille est "+ i
        else:
            initiale = "Vous cherchez un nom à particule"
        
        #indice sortant/sortante
        if deputes.at[line, 'sortant.e'] == True:
            if deputes.at[line, 'Genre'] == 'F':
                is_sortant = "C'est une sortante"
            else:
                is_sortant = "C'est un sortant"
        else:
            if deputes.at[line, 'Genre'] == 'F':
                is_sortant = "C'est une nouvelle élue"
            else:
                is_sortant = "C'est un nouvel élu"
        
        imgURL = "https://www2.assemblee-nationale.fr/static/tribun/16/photos/" + str(line) + ".jpg"
        
        w = Mystere(individu=solution)

        w.save()
        w.image_set.create(image=imgURL)
        
        # w.indice_set.create(ind_p=prénom, ind_gpe=groupe, ind_dpt=département, ind_initiale=initiale)
        w.indice_set.create(ind_p=prénom, ind_sortant=is_sortant, ind_dpt=département, ind_initiale=initiale)
 
            