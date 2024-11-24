# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.16.4
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# # Une première vue d'ensemble des tables à disposition
# \
# Dans ce notebook, on va voir le contenu des tables, leur donner un sens et en extraire les idées importantes.
#
# Cela nous permettra par la suite de mieux savoir comment on veut les manipuler.

import numpy as np
import pandas as pd

# \
# Commençons par la première table : **cities**

df_cities = pd.read_csv('data/cities.csv')
df_cities

# Cette dataframe fait *a priori* la liste des grandes villes du monde, le pays et la région/l'état dans lesquels elles se trouvent. On y lit aussi les codes ISO2 et ISO3 d'identification de leurs pays, ainsi que leurs coordonnées géographiques (latitude et longitude)
# On voit que la première colonne se nomme 'station_id', on peut donc raisonnablement penser que c'est une clé primaire. On peut donc la définir en tant qu'index.

df_cities.set_index('station_id', inplace=True) #on n'a pas besoin de renvoyer
                                                #à nouveau la DF

# Début et fin de la dataframe :

df_cities.head()

df_cities.tail()

# \
# Ici les fonctions comme "describe" ne sont pas pertinentes puisque les seules colonnes contenant des valeurs numériques sont 'longitude' et 'latitude'

# \
# Passons à la table **countries** à présent

df_countries = pd.read_csv('data/countries.csv')
df_countries

# On a la liste des pays du monde, leur nom écrit dans leur langue officielle, leurs codes ISO2 et ISO3 comme dans la table **cities**, leur population, leur superficie, leur capitale avec ses coordonnées géographiques, ainsi que leur région du monde et continent.
#
#
# On peut se demander en premier lieu si toutes les capitales font partie de **cities** :
# pour cela, on peut employer la fonction *isin*, qui renvoie un booléen correspondant à la présence (ou non) des éléments d'une colonne d'une dataframe donnée, dans une colonne d'une autre dataframe.

df_countries['dans_cities'] = df_countries['capital'].isin(df_cities['city_name'])
absents = df_countries[df_countries['dans_cities'] ==  False]

print(absents[['country', 'capital']])

# On remarque que les villes non présentes dans **cities** ne sont pas que des "petites villes", il y a aussi des capitales et/ou mégapoles...
#
# Le choix des villes de **cities** paraît donc assez arbitraire

# \
# Passons enfin à **daily-weather-cities** :

df_weather = pd.read_csv('data/daily-weather-cities.csv')
df_weather

#affichons les villes concernées par les relevés météorologiques
df_weather['city_name'].unique()

# On a donc ici un relevé météorologique de quatre villes (Vienne, Bruxelles, Paris et Berlin) à différentes dates. On remarque que beaucoup de valeurs sont manquantes, soit car certains paramètres n'ont pas pu être mesurés avec les outils dont les scientifiques disposaient à l'époque, soit car on ne les a pas observés le jour de la mesure (c'est vraisemblablement le cas des précipitations ou de la neige en été par exemple).
#
# Nous retrouvons la même colonne *station_id* que sur **cities**, ce qui va pouvoir nous permettre de faire des jointures entre les 3 tables (selon le nom et l'identifiant des villes).
#
# \
# De plus, ici la fonction *describe* peut s'avérer utile puisque l'on a beaucoup de colonnes numériques.

df_weather.describe()

# On remarque cependant un grand nombre de NaN dans cette table : évaluone "l'ampleur des dégâts" pour identifier en quoi ces valeurs manquantes peuvent être problématiques pour une étude de la table

#nombre de NaN par colonne
df_weather.isnull().sum()

#nombre de NaN par colonne, groupé par ville
print(df_weather.groupby('city_name').describe())
df_weather.groupby('city_name').apply(lambda x: x.isnull().sum())

# Les colonnes les plus touchées sont les colonnes relatives à la neige (logique puisqu'il neige très peu de jours dans une année dans ces capitales européennes), le vent et l'ensoleillement. Pour l'ensoleillement, on a tellement de valeurs manquantes qu'il sera difficile de mettre en valeur le peu de mesures effectuées...

# \
# Pour étudier rapidement la dernière table, on va :
#
#
# - vérifier que les dates sont à un format homogène
# - regarder l'étalage des données dans le temps (la plus ancienne, la plus récente)
# - regarder le nombre de mesures par ville

#vérification du format des dates
df_weather['date'].dtypes

# +
#la colonne date ne contient pas des dates à proprement parler, mais est constituée d'“objects“
#pour y remédier, on utilise la fonction to_datetime de pandas

df_weather['date'] = pd.to_datetime(df_weather['date'])
print(df_weather['date'].dtypes)
# -

#on compte le nombre de relevés dans chaque ville
étalage_dates = df_weather['date'].groupby(df_weather['city_name'])
étalage_dates.size()

#maintenant, on affiche un aperçu des données par ville concernée
étalage_dates.describe()

# Pour faire le lien entre les villes, les informations sur les pays et les relevés météoroologiques, on va tenter de réaliser des jointures de tables.
#
# Dans les notebooks suivants, on tentera de modéliser les différentes variables de **daily-weather-cities** avec des graphes par exemple, et les relier aux différentes informations des autres tables.
