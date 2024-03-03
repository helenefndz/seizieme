#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  4 10:43:08 2022
@author: helenenouveau

03/24 : runscript de django-extensions ne fonctionnant plus pour des raisons apparemment liées à la puce m1, j'essaye cette nouvelle méthode

"""



import pandas as pd

from django.core.management.base import BaseCommand, CommandError

from quiestce16.models import Mystere, Image, Indice

coms_abr_dvp = {'ETR' : "commission des affaires étrangères",
                'AFFSOC' : "commission des affaires sociales",
                'LOIS' : "commission des lois",
                'ECO' : "commission des affaires économiques",
                'AFFCULT' : "commission des affaires culturelles",
                'FIN' : "commission des finances",
                'DEVDUR' : "commission du développement durable",
                'DEF' : "commission de la défense",
                'ETR' : "commission des affaires étrangères",
                }


class Command(BaseCommand):   

     def handle(self, *args, **options):

        
        deputes = pd.read_csv('docs/deputes_2024-03-02_avec_colonnes_sup.csv', index_col=[0], sep = ",")

        Mystere.objects.all().delete()

        for line in deputes.index:
             
              solution = "{} {}".format(deputes.at[line,'Prénom'], deputes.at[line,'Nom'])
              
              etiquette = deputes.at[line, 'Groupe politique (complet)']
            
              prénom = "Son prénom est " + deputes.at[line, 'Prénom'] + "."
              # print(prénom)
              # groupe = "Groupe : " + deputes.at[line, 'Groupe politique (complet)'] + "."
              
              département = "Son lieu d'élection est : "+ deputes.at[line, 'Département']
              
              #indice "initiale ou particule"
              i = deputes.at[line, 'Nom'][0]
              if i.isupper():
                  initiale = "L'initiale de son nom de famille est "+ i
              else:
                  initiale = "Vous cherchez un nom à particule"
              
              # #indice sortant/sortante
              # if deputes.at[line, 'sortant.e'] == True:
              #     if deputes.at[line, 'Genre'] == 'F':
              #         is_sortant = "C'est une sortante"
              #     else:
              #         is_sortant = "C'est un sortant"
              # else:
              #     if deputes.at[line, 'Genre'] == 'Mme':
              #         is_sortant = "C'est une nouvelle élue"
              #     else:
              #         is_sortant = "C'est un nouvel élu"
                      
              groupe = deputes.at[line, 'Groupe sur la fiche indiv']
              if groupe == "Non inscrit":
                  if deputes.at[line, 'Genre'] == 'Mme':
                      groupe = "C'est une non inscrite"
                  else:
                      groupe = "C'est un non inscrit"
              else:
                  if deputes.at[line, 'Genre'] == 'Mme':
                      groupe = "Elle appartient au groupe " + groupe
                  else:
                      groupe = "Il appartient au groupe " + groupe
                      
              com = deputes.at[line, 'commission le 2024-03-02']
              if deputes.at[line, 'Genre'] == 'Mme':
                  com = "Elle appartient à la " + coms_abr_dvp[com]
              else:
                  com = "Il appartient à la " + coms_abr_dvp[com]
              
              
              imgURL = "https://www2.assemblee-nationale.fr/static/tribun/16/photos/" + str(line) + ".jpg"
              
              
              w = Mystere(individu=solution)
        
              w.save()
        
              w.image_set.create(image=imgURL)
        
              w.nuance_set.create(nuance=etiquette)
        
                # w.indice_set.create(ind_p=prénom, ind_gpe=groupe, ind_dpt=département, ind_initiale=initiale)
              w.indice_set.create(ind_p=prénom,
                                 #ind_sortant=is_sortant,
                                 ind_dpt=département, ind_initiale=initiale,
                                 ind_groupe=groupe, ind_commission=com)


