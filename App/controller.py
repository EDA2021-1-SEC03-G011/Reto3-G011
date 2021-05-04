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
import time
import tracemalloc


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
    
    delta_time = -1.0
    delta_memory = -1.0

    tracemalloc.start()

    start_time = getTime()
    start_memory = getMemory()

    usertrack = cf.data_dir + usertrack
    input_file = csv.DictReader(open(usertrack, encoding = 'utf-8'), delimiter=",") 
    for song in input_file:
        model.addUserTrack(catalog, song)
    
    context = cf.data_dir + contextfile
    input_file = csv.DictReader(open(context, encoding = 'utf-8'), delimiter=",") 
    for event in input_file:
        model.eventInUserTrackMap(catalog, event)

    
    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)

    return delta_time,delta_memory

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

def createSubList(list, rank):
    # FUNCION REQ 4
    return model.createSubList(list, rank)

def filterByChar(catalog, characteristic, loValue,hiValue):
    # FUNCION UNICA REQ 1
        
    delta_time = -1.0
    delta_memory = -1.0

    tracemalloc.start()

    start_time = getTime()
    start_memory = getMemory()

    values=model.filterByChar(catalog, characteristic, loValue,hiValue)

    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)

    return values,delta_time,delta_memory


def filterByFeatures(catalog,lovalueE,hivalueE,lovalueD,hivalueD):
    # FUNCION UNICA REQ 2

    delta_time = -1.0
    delta_memory = -1.0

    tracemalloc.start()

    start_time = getTime()
    start_memory = getMemory()

    values=model.filterByFeatures(catalog,lovalueE,hivalueE,lovalueD,hivalueD)

    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)

    return values,delta_time,delta_memory

def createTempoInstruList(tempoMap,loTempo, hiTempo,loInstru,hiInstru):
    # FUNCION UNICA REQ 2
    delta_time = -1.0
    delta_memory = -1.0

    tracemalloc.start()

    start_time = getTime()
    start_memory = getMemory()

    answer =  model.createTempoInstruList(tempoMap,loTempo, hiTempo,loInstru,hiInstru)

    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)

    return answer,delta_time,delta_memory

def filterByTime(timeMap,loHour,hiHour):
    return model.filterByTime(timeMap,loHour,hiHour)


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

def timeInSeconds(hour):
    return model.timeInSeconds(hour)

# =======================
# Funciones para imprimir
# =======================


def printReqTwo(answer):
    # FUNCION UNICA REQ 2
    model.printReqTwo(answer)


def printReqThree(list,loInstru,hiInstru,loTempo,hiTempo):
    # FUNCION UNICA REQ 3
    model.printReqThree(list,loInstru,hiInstru,loTempo,hiTempo)

def printReqFour(genreResults,totalReproductions):
    # FUNCION UNICA REQ 4
    model.printReqFour(genreResults,totalReproductions)

# =======================
# Funciones para calcular tiempo y memoria
# =======================

def getTime():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def getMemory():
    """
    toma una muestra de la memoria alocada en instante de tiempo
    """
    return tracemalloc.take_snapshot()


def deltaMemory(start_memory, stop_memory):
    """
    calcula la diferencia en memoria alocada del programa entre dos
    instantes de tiempo y devuelve el resultado en bytes (ej.: 2100.0 B)
    """
    memory_diff = stop_memory.compare_to(start_memory, "filename")
    delta_memory = 0.0

    # suma de las diferencias en uso de memoria
    for stat in memory_diff:
        delta_memory = delta_memory + stat.size_diff
    # de Byte -> kByte
    delta_memory = delta_memory/1024.0
    return delta_memory
