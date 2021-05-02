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

def loadData(catalog, contextfile,usertrack):
    usertrack = cf.data_dir + usertrack
    input_file = csv.DictReader(open(usertrack, encoding = 'utf-8'), delimiter=",") 
    for song in input_file:
        model.addUserTrack(catalog, song)
    
    context = cf.data_dir + contextfile
    input_file = csv.DictReader(open(context, encoding = 'utf-8'), delimiter=",") 
    for event in input_file:
        model.eventInUserTrackMap(catalog, event)

    return catalog

# Funciones de ordenamiento

# ================================
# Funciones para creacion de datos
# ================================

def createArtistMap(charList):
    # FUNCION REQ 4
    return model.createArtistMap(charList)

def createTempoList(tempoMap, loTempo, hiTempo):
    # FUNCION REQ 3, REQ 4
    return model.createTempoList(tempoMap, loTempo, hiTempo)

def createInstruList(tempoList,loInstru,hiInstru):
    # FUNCION UNICA REQ 3
    return model.createInstruList(tempoList,loInstru,hiInstru)

def createSubList(list, rank):
    # FUNCION REQ 4
    return model.createSubList(list, rank)

def filterByChar(catalog, characteristic, loValue,hiValue):
    # FUNCION UNICA REQ 1
    return model.filterByChar(catalog, characteristic, loValue,hiValue)

# ========================================
# Funciones de consulta sobre el catálogo
# ========================================

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

# ====================================
# Funciones creacion datos por usuario
# ====================================

def askGenre(catalog):
    # FUNCION UNICA REQ 4
    return model.askGenre(catalog)

def verifyRanges(loRange,hiRange):
    # FUNCION REQ1, REQ 3, REQ 4
    return model.verifyRanges(loRange,hiRange)

# =======================
# Funciones para imprimir
# =======================

def printReqThree(list,loInstru,hiInstru,loTempo,hiTempo):
    # FUNCION UNICA REQ 3
    model.printReqThree(list,loInstru,hiInstru,loTempo,hiTempo)

def printReqFour(genreResults,totalReproductions):
    # FUNCION UNICA REQ 4
    model.printReqFour(genreResults,totalReproductions)