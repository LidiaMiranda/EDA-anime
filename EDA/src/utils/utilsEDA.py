# Librerías

import numpy as np
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
from scipy.stats import mannwhitneyu
import statsmodels.api as sm

# Evitar warnings

import warnings
warnings.filterwarnings('ignore')

                                               ### FUNCIONES DE LIMPIEZA ###

# Función para eliminar las columnas que no necesitamos

def delete(anime):
    '''
    Función que elimina las columnas especificadas en la variable "anime_delete".
    Para más información, ver carpeta utils.
    ''' 
    anime_delete = anime[["ID", "Synonyms", "Japanese", "Synopsis", "End_Aired", "Broadcast", "Producers", "Licensors", 
                          "Premiered","Popularity", "Members", "Favorites"]]
    anime = anime.drop(anime_delete.columns, axis=1)
    return anime

#Rellenamos los NaN con la media de la columna en las columnas seleccionadas

def fill_nan(anime):
    '''
    Función que rellena los NaN con la media de la columna en las columnas especificadas en la variable "anime_fill_mean".
    Para más información, ver carpeta utils.
    '''
    anime_fill_mean = {"Score": anime["Score"].mean(), "Scored_Users": anime["Scored_Users"].mean(),
                       "Episodes": anime["Episodes"].mean(), "Duration_Minutes": anime["Duration_Minutes"].mean()}
    anime = anime.fillna(value=anime_fill_mean)
    return anime

# Ordenamos al columna "Ranked". La convertimos en índice y determinamos que sea una sucesión numérica que empiece en 1.
def ranking(anime):
    '''
    Función que ordena el DataFrame en base a la columna "Ranked".
    Al ranking le faltan números, por lo que lo convertimos a una sucesión numérica que empiece en 1.
    Finalmente, determinamos que el ranking sea el índice.
    Para más información, ver carpeta utils.
    '''
    anime_sorted = anime.sort_values(by=["Ranked"])
    anime_sorted.set_index("Ranked", inplace=True)
    anime_sorted.reset_index(drop=True, inplace=True)
    anime_sorted.index = anime_sorted.index + 1
    return anime_sorted

# Para las columnas tipo object eliminamos todos los "Unknown". Tras verificar los Unknowns en varias columnas, se determina que no son relevantes.
def delete_unknown(anime):
    '''
    Función que elimina los valores "Unknown" de todas las columnas tipo object excepto "Start_Aired".
    '''
    anime_unk = anime.select_dtypes(include="object")
    for col in anime_unk:
        if col != "Start_Aired":
            anime = anime.drop(anime[anime[col] == "Unknown"].index)
    return anime


# def update_start_aired(anime):
#     '''
#     Función que busca todas las fechas que siguen siendo string, hace un split cuando encuentre un guión y, si el número tras el guión es 
#     menos o igual a 24, le sumamos 2000. En caso contrario, sumamos 1900.

#     DATO IMPORTANTE: Partiendo de la base de que el anime comenzó el 1917 con un cortometraje que no está en la base de datos, podemos decir 
#     sin equivocarnos que todo lo que sea menor de 24 será de los años 2000.
#     Ejemplo: 04-16 se le va a sumar 2000
#     Ejemplo2: 05-78 se le va a sumar 1900
#     '''
#     updated_anime = anime.copy()
#     errors = pd.DataFrame()
    
#     for pos in range(len(updated_anime["Start_Aired"])):
#         try:
#             if type(updated_anime["Start_Aired"].iloc[pos]) == str:
#                 aniored = int(updated_anime["Start_Aired"].iloc[pos].split("-")[-1])
#                 if aniored <= 24:
#                     anio = 2000 + aniored
#                 else:
#                     anio = 1900 + aniored          
#                 updated_anime["Start_Aired"].iloc[pos] = anio
#         except:
#             x = updated_anime["Start_Aired"].iloc[pos]
#             errors = errors.append([[pos, x]])
            
#     return updated_anime, errors

#Para las filas con más de un género / tema, se determina el primer género como principal. Se elimina el resto y se suma al principal.def clean_genre(genre_string):
def clean_col(col_string):
    '''
    Función que elimina los strings donde hay varias categorías. Cuando la fila tiene varias palabras (Ejemplo-> Genre: Historical, Military, 
    Mythology), se queda solo con la primera palabra porque entiende que es la categoría principal.

    '''
    return col_string.split(',')[0].strip()





                                               ### FUNCIONES DE VISUALIZACIÓN ###

#Función para graficar todas las columnas tipo object con un gráfico de barras.
def barra_uni(anime):
    '''
    Función que grafica todas las columnas tipo object en una grafica de barras. 
    Se excluyen las columnas "Title" y "English", por tener valores individuales únicos.
    Si la columna tiene más de 10 categorías, se mostrarán solo las 10 primeras para que el gráfico sea más claro.
    '''
    cuant_col = anime.select_dtypes(include=['object'])
    exclude_cols = ["Title", "English"]
    for col in cuant_col:
        if col not in exclude_cols:
            order = cuant_col[col].value_counts().index.tolist()
            plt.figure(figsize=(25,10))
            sns.countplot(x=cuant_col[col], order=order[:10])
        else:
            pass
    return anime

#Función para graficar la densidad de  todas las columnas numéricas con un gráfico lineal
def dens_uni(anime):
    '''
    Función que grafica la densidad de todas las columnas numéricas con un gráfico lineal. 
    '''
    num_cols = anime.select_dtypes(include=["int64", "float64"])
    for col in num_cols:
        sns.kdeplot(anime[col], shade=True)
        sns.color_palette("husl",5)
        plt.xlabel(col)
        plt.show()
    return anime

#Función para graficar la densidad de  todas las columnas numéricas con un boxplot
def boxp_uni(anime):
    '''
    Función que grafica la densidad de todas las columnas numéricas con un boxplot. 
    '''
    num_cols = anime.select_dtypes(include=["int64", "float64"]).columns
    for col in num_cols:
        plt.figure(figsize=(8,5))
        sns.boxplot(x=anime[col])
        sns.color_palette("husl",5)
        plt.xlabel(col)
        plt.gca().set_ylabel("Densidad")
        plt.show()
    return anime

