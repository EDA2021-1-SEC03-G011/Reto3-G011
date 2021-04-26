"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import model
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""
# ======================================
# Inicialización del Catálogo
# ======================================

def init():
    catalog = model.newCatalog()
    return catalog

# =================================
# Funciones para la carga de datos
# =================================

def loadData(catalog, musicfile):
    musicfile = cf.data_dir + musicfile
    input_file = csv.DictReader(open(musicfile, encoding = 'utf-8'), delimiter=",") 
    for song in input_file:
        model.addSong(catalog, song)

    return catalog

# Funciones de ordenamiento

# ================================
# Funciones para creacion de datos
# ================================

def createCharMap(catalog, characteristic):
    return model.createCharMap(catalog, characteristic)

def createCharList(charMap,loValue,hiValue):
    return model.createCharList(charMap,loValue,hiValue)

def createArtistsCharMap(charList):
    return model.createArtistsCharMap(charList)

def createTempoMap(catalog):
    return model.createTempoMap(catalog)

def createTempoList(tempoMap, loTempo, hiTempo):
    return model.createTempoList(tempoMap, loTempo, hiTempo)

def createInstruList(tempoList,loInstru,hiInstru):
    return model.createInstruList(tempoList,loInstru,hiInstru)

# Funciones de consulta sobre el catálogo

def eventsSize(catalog):
    return model.eventsSize(catalog)

def artistsSize(catalog):
    return model.artistsSize(catalog)

def tracksSize(catalog):
    return model.tracksSize(catalog)

def uniqueSongsChar(charList):
    return model.uniqueSongsChar(charList)

def mapSize(map):
    return model.mapSize(map)

# =======================
# Funciones para imprimir
# =======================

def printReqThree(list,loInstru,hiInstru,loTempo,hiTempo):
    model.printReqThree(list,loInstru,hiInstru,loTempo,hiTempo)