#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  4 10:43:08 2022
@author: helenenouveau
"""



import pandas as pd

from quiestce16.models import Mystere, Image, Indice

def run():
    deputes = pd.read_csv('docs/revenants16.csv', index_col=[0])

    Mystere.objects.all().delete()

    for line in deputes.index:
        solution = "{} {}".format(deputes.at[line,'Prénom'], deputes.at[line,'Nom'])
      
        prénom = "Son prénom est " + deputes.at[line, 'Prénom'] + "."
        groupe = "Groupe : " + deputes.at[line, 'Groupe politique (complet)'] + "."
        département = "Département / Français de l'étranger : "+ deputes.at[line, 'Département']
        initiale = "L'initiale de son nom de famille est "+ deputes.at[line, 'Nom'][0] 
        
        imgURL = "https://www2.assemblee-nationale.fr/static/tribun/15/photos/" + str(line) + ".jpg"
        
        w = Mystere(individu=solution)

        w.save()
        w.image_set.create(image=imgURL)
        
        w.indice_set.create(ind_p=prénom, ind_gpe=groupe, ind_dpt=département, ind_initiale=initiale)
            
            