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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """

import random
import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as m
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.DataStructures import linkedlistiterator as slit
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""
# ======================
# Creacion del catalogo
# ======================

def newCatalog():
    catalog = {'songs':None,
            'eventList':None,
            'artists':None,
            'tracks':None}

    catalog['songs'] = lt.newList(datastructure='SINGLE_LINKED')

    catalog['eventList'] = lt.newList(datastructure='SINGLE_LINKED')

    catalog['trackList'] = lt.newList(datastructure='SINGLE_LINKED')

    catalog['eventMap'] = om.newMap(omaptype='BST')

    catalog['trackMap'] = om.newMap(omaptype='BST')

    catalog['artistMap'] = om.newMap(omaptype='BST')

    return catalog

# ==============================================
# Funciones para agregar informacion al catalogo
# ==============================================

def addSong(catalog, song):
    lt.addLast(catalog['songs'],song)
    updateArtists(catalog['artistMap'],song)
    updateEvents(song,catalog['eventList'],catalog['eventMap'])
    updateTracks(song,catalog['trackList'],catalog['trackMap'])

def updateArtists(map, song):
    artist = song['artist_id']
    exists = om.get(map,artist)

    if exists is None:
        list = lt.newList(datastructure="SINGLE_LINKED")
        lt.addLast(list, song)
        om.put(map,artist,list)

    else:
        existingList = me.getValue(exists)
        lt.addLast(existingList,song)

def updateEvents(song,eventList,eventMap):
    event = (song['user_id'],song['track_id'],song['created_at'])
    exists_event = om.get(eventMap, event)

    if exists_event is None:
        list = lt.newList(datastructure="SINGLE_LINKED")
        lt.addLast(list, song)
        om.put(eventMap,event,list)
        lt.addLast(eventList, song)

    else:
        existingList = me.getValue(exists_event)
        lt.addLast(existingList,song)

def updateTracks(song,trackList,trackMap):
    track = song['track_id']
    exists_track = om.get(trackMap, track)

    if exists_track is None:
        list = lt.newList(datastructure="SINGLE_LINKED")
        lt.addLast(list, song)
        om.put(trackMap,track,list)
        lt.addLast(trackList, song)

    else:
        existingList = me.getValue(exists_track)
        lt.addLast(existingList,song)

# ================================
# Funciones para creacion de datos
# ================================

def createCharMap(catalog, characteristic):
    uniqueList = catalog['eventList']
    charMap = om.newMap(omaptype='RBT')

    iterator = slit.newIterator(uniqueList)

    while slit.hasNext(iterator):
        song = slit.next(iterator)
        existingValue = om.get(charMap, float(song[characteristic]))

        if existingValue is None: 
            listInKey = lt.newList(datastructure='SINGLE_LINKED')
            lt.addLast(listInKey, song)
            om.put(charMap,float(song[characteristic]),listInKey)
        
        else:
            listInKey = (me.getValue(existingValue))
            lt.addLast(listInKey, song)

    return charMap

def createCharList(charMap,loValue,hiValue):
    listOfLists = om.values(charMap,loValue,hiValue)
    charList = lt.newList(datastructure='SINGLE_LINKED')

    iteratorLists = slit.newIterator(listOfLists)

    while slit.hasNext(iteratorLists):
        list = slit.next(iteratorLists)

        iteratorSongs = slit.newIterator(list)

        while slit.hasNext(iteratorSongs):
            song = slit.next(iteratorSongs)
            lt.addLast(charList,song)
    
    return charList

def createArtistsCharMap(charList):
    map = om.newMap(omaptype='BST')

    iterator = slit.newIterator(charList)

    while slit.hasNext(iterator):
        song = slit.next(iterator)
        artist = song['artist_id']
        exists = om.get(map,artist)

        if exists is None:
            list = lt.newList(datastructure="SINGLE_LINKED")
            lt.addLast(list, song)
            om.put(map,artist,list)

        else:
            existingList = me.getValue(exists)
            lt.addLast(existingList,song)

    return map

def createTempoMap(catalog):
    tempoMap = om.newMap(omaptype='RBT')
    songsList = catalog['trackList']

    iterator = slit.newIterator(songsList)

    while slit.hasNext(iterator):
        song = slit.next(iterator)
        exists = om.get(tempoMap, float(song['tempo']))

        if exists is None:
            listForTempo = lt.newList(datastructure='SINGLE_LINKED')
            lt.addLast(listForTempo, song)
            om.put(tempoMap,float(song['tempo']),listForTempo)
        else:
            existingList = me.getValue(exists)
            lt.addLast(existingList,song)

    return tempoMap

def createTempoList(tempoMap, loTempo, hiTempo):
    listOfLists = om.values(tempoMap, loTempo, hiTempo)
    tempoList = lt.newList(datastructure='SINGLE_LINKED')

    iteratorLists = slit.newIterator(listOfLists)

    while slit.hasNext(iteratorLists):
        list = slit.next(iteratorLists)

        iteratorSongs = slit.newIterator(list)

        while slit.hasNext(iteratorSongs):
            song = slit.next(iteratorSongs)
            lt.addLast(tempoList,song)
    
    return tempoList

def createInstruList(tempoList,loInstru,hiInstru):
    instruList = lt.newList(datastructure="SINGLE_LINKED")

    iterator = slit.newIterator(tempoList)
    while slit.hasNext(iterator):
        song = slit.next(iterator)

        if float(song['instrumentalness'])>= loInstru and float(song['instrumentalness'])<= hiInstru:
            lt.addLast(instruList, song)

    return instruList

# =====================    
# Funciones de consulta
# =====================

def eventsSize(catalog):
    return lt.size(catalog['eventList'])

def artistsSize(catalog):
    return om.size(catalog['artistMap'])

def tracksSize(catalog):
    return om.size(catalog['trackMap'])

def uniqueSongsChar(charList):
    return lt.size(charList)

def mapSize(map):
    return om.size(map)

# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento

# =======================
# Funciones para imprimir
# =======================

def printReqThree(list,loInstru,hiInstru,loTempo,hiTempo):
    randomList = random.sample(range(1, lt.size(list)), 5)
    counter = 1
    print("\n+++++++ Resultados Req No. 1 +++++++")
    print("Instrumentalidad entre: "+ str(loInstru)+" - "+str(hiInstru))
    print("Tempo entre: "+ str(loTempo)+" - "+str(hiTempo))
    print("Total de tracks encontrados: "+str(lt.size(list)))
    print("")
    for i in randomList:
        song = lt.getElement(list, i)
        print("Track "+str(counter)+": "+ song['track_id']+" con instrumentalness de: "+str(song['instrumentalness'])+" y tempo de: "+str(song['tempo']))
        counter +=1
