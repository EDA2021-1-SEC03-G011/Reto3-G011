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
from DISClib.ADT import map as mp
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
    catalog = {'eventList':None,
            'artists':None,
            'tracks':None,
            'tempoMap':None,
            'genres':None}



    #catalog['eventList'] = lt.newList(datastructure='SINGLE_LINKED')

    #catalog['trackList'] = lt.newList(datastructure='SINGLE_LINKED')

    catalog['trackMap'] = om.newMap(omaptype='BST')

    catalog['eventMap'] = om.newMap(omaptype='BST')

    #catalog['artistMap'] = om.newMap(omaptype='BST')

    catalog['tempoMap'] = om.newMap(omaptype='RBT')

    catalog['genres'] = {'reggae':(60,90),'down-tempo':(70,100),'chill-out':(90,120),'hip-hop':(85,115),
                         'jazz and funk':(120,125),'pop':(100,130),"r&b":(60,80),'rock':(110,140),'metal':(100,160)}

    return catalog

# ==============================================
# Funciones para agregar informacion al catalogo
# ==============================================

def addUserTrack(catalog, usertrack):
    #updateArtists(catalog['artistMap'],song)
    updateUserTrack(usertrack,catalog['trackMap'])
    #updateTracks(song,catalog['trackList'],catalog['trackMap'])

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

def updateUserTrack(usertrack,trackMap):
    event = (usertrack['user_id'],usertrack['track_id'],usertrack['created_at'])
    
    om.put(trackMap,event, usertrack)

def eventInTrackMap(catalog, event):
    id_event =(event['user_id'],event['track_id'],event['created_at'])

    if om.contains(catalog['trackMap'],id_event):
        om.put(catalog['eventMap'],id_event,event)

        if om.contains(catalog['tempoMap'],float(event['tempo'])):
            couple = om.get(catalog['tempoMap'],float(event['tempo']))
            list = me.getValue(couple)
            lt.addLast(list,event)

        else:
            list = lt.newList(datastructure='SINGLE_LINKED')
            lt.addLast(list,event)
        om.put(catalog['tempoMap'],float(event['tempo']),list)
        

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

"""
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
"""
def createArtistMap(tempoList):
    map = mp.newMap(maptype='PROBING')

    iterator = slit.newIterator(tempoList)
    while slit.hasNext(iterator):
        event = slit.next(iterator)
        
        artist = event['artist_id']
        mp.put(map,artist,event)
    return mp.size(map)

def createTempoMap(catalog, track_event):
    tempoMap = om.newMap(omaptype='RBT')
    songsList = catalog[track_event]

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
    answerMap = mp.newMap(maptype='CHAINING',loadfactor=1.0,numelements=28000)

    iteratorLists = slit.newIterator(listOfLists)
    while slit.hasNext(iteratorLists):
        list = slit.next(iteratorLists)

        iteratorSongs = slit.newIterator(list)
        while slit.hasNext(iteratorSongs):
            song = slit.next(iteratorSongs)
            id = song['user_id'],song['track_id'],song['created_at']
            mp.put(answerMap, id, song)
    
    return mp.valueSet(answerMap)
"""
def createInstruList(tempoList,loInstru,hiInstru):
    instruList = lt.newList(datastructure="SINGLE_LINKED")

    iterator = slit.newIterator(tempoList)
    while slit.hasNext(iterator):
        song = slit.next(iterator)

        if float(song['instrumentalness'])>= loInstru and float(song['instrumentalness'])<= hiInstru:
            lt.addLast(instruList, song)

    return instruList
"""
def createSubList(list, rank):
    sublist = lt.subList(list,1,rank)
    return sublist


def filterByChar(catalog, characteristic, loValue,hiValue):
    list = om.valueSet(catalog['eventMap'])
    answerMap = mp.newMap(maptype='PROBNG', numelements=1800)
    counter = 0

    for event in lt.iterator(list):
        if float(loValue) <= float(event[characteristic]) <= float(hiValue):
            counter += 1
            mp.put(answerMap, event['artist_id'],event)
    
    return (counter, mp.size(answerMap))



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

# ====================================
# Funciones creacion datos por usuario
# ====================================

def askGenre(catalog):
    continuing = True
    genreList = []
    genreDictionary = catalog['genres']

    while continuing == True:
        print("\nLos generos disponibles son")
        print("\nGenero\tBMP Tipico")
        for genre in genreDictionary.keys():
            print(str(genre)+"\t"+str(genreDictionary[genre]))
        print("\nQue accion desea realizar:\n")
        print(">1< Agregar un nuevo genero al diccionario")
        print(">2< Agregar un genero a la lista de busqueda")
        print(">3< Finalizar proceso y comenzar a buscar")
        action = int(input("\nDigite el numero de la accion deseada: "))

        if action == 1:
            newGenreName = input("Ingrese el nombre unico para el nuevo genero musical: ")
            loTempo = int(input("Digite el valor entero minimo del tempo del nuevo genero musical: "))
            hiTempo = int(input("Digite el valor entero maximo del tempo del nuevo genero musical: "))
            genreDictionary[newGenreName] = (loTempo,hiTempo)

        elif action == 2:
            print("La lista de busqueda que tiene es la siguiente "+str(genreList))
            existingGenre = input("Ingrese el nombre del genero que desea agregar a la busqueda: ")
            if existingGenre in genreDictionary:
                genreList.append(existingGenre)
            else:
                print("\n>>>El genero deseado no existe en el diccionario<<<")
        
        elif action == 3:
            print("La lista de busqueda que tiene es la siguiente "+str(genreList))
            continuing = False
    
    return genreList


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

def printReqFour(genreResults,totalReproductions):
    print("\n+++++++ Resultados Req No. 4 +++++++")
    print("Total de reproducciones: "+str(totalReproductions))
    for genre in genreResults.keys():
        tempo = genreResults[genre]['tempo']
        reproductions = genreResults[genre]['reproductions']
        artists = genreResults[genre]['artists']
        list = genreResults[genre]['list']
        print("\n\n======== "+genre.upper()+" ========")
        print("Para "+genre+" el tempo esta entre "+str(tempo[0])+" y "+str(tempo[1])+" BPM")
        print("El total de reproducciones de "+genre+" son: "+str(reproductions)+" con "+str(artists) +" diferentes artistas")
        print("Algunos artistas para "+genre)

        iterator = slit.newIterator(list)
        counter = 1

        while slit.hasNext(iterator):
            event = slit.next(iterator)
            print("Artista "+str(counter)+": "+event['artist_id'])
