#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 28 22:41:14 2022

@author: helenenouveau
"""
from django import forms

class Prop(forms.Form):
    
    prop = forms.CharField(label = "Votre réponse", max_length=100)
    

# class Abandon(forms.Form):
    
#     abandon = forms.BooleanField(label = "abandon", required=False)
    

# class Hint(forms.Form):
    
#     hint = forms.BooleanField(label = "indice", required=False)