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
from datetime import datetime
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""
# ======================
# Creacion del catalogo
# ======================

def newCatalog():
    catalog = {'user-track-createdMap':None,
               'eventMap':None,
               'tempoMap':None,
               'genres':None,
               'characteristics':None,
               'sentiment_values':None
               }

    catalog['user-track-createdMap'] = mp.newMap(maptype='PROBING',numelements=80000) #se cambio a tabla de hash para acceder mas rapido a sus valores

    catalog['eventMap'] = mp.newMap(maptype='PROBING',numelements=60000, loadfactor=0.5)

    catalog['tempoMap'] = om.newMap(omaptype='RBT')

    catalog['trackMap'] = om.newMap(omaptype='BST')

    catalog["danceability"]=om.newMap(omaptype='RBT')

    catalog['timeMap'] = om.newMap(omaptype='RBT')

    catalog['artists'] = mp.newMap(maptype='CHAINING',numelements=5000,loadfactor=1.0)

    catalog['tracks'] = mp.newMap(maptype='CHAINING',numelements=31000,loadfactor=1.0)

    catalog['genres'] = {'reggae':(60,90),'down-tempo':(70,100),'chill-out':(90,120),'hip-hop':(85,115),
                         'jazz and funk':(120,125),'pop':(100,130),"r&b":(60,80),'rock':(110,140),'metal':(100,160)}

    catalog['characteristics'] = ['instrumentalness','liveness','speechiness','danceability',
                                  'valence','acousticness','energy']
    catalog['sentiment_values']=mp.newMap(numelements=5300,loadfactor=1.0)



    return catalog

# ==============================================
# Funciones para agregar informacion al catalogo
# ==============================================

def addUserTrack(catalog, usertrack):
    """
    Durante la carga del archivo user-track se guarda en el mapa 'user-track-createdMap'
    un evento unico identificado por (user+track+created)
    """
    usertrack['hashtag']=usertrack['hashtag'].lower()
    userTrackMap = catalog['user-track-createdMap']
    event = (usertrack['user_id'],usertrack['track_id'],usertrack['created_at'])
    mp.put(userTrackMap,event, usertrack)


def eventInUserTrackMap(catalog, event):
    id_event =(event['user_id'],event['track_id'],event['created_at'])
    danceability=float(event['danceability'])
    track_id = event['track_id']

    time = datetime.strptime(event['created_at'],"%Y-%m-%d %H:%M:%S")
    seconds = time.hour*3600 + time.minute*60 +time.second
    """
    Para cada evento que se repite en los dos archivos se agrega a un RBT que los
    clasifica por Tempo
    Ademas se filtra por track_id para luego meter los tracks segun el Tempo en 
    otro RBT
    """
    #Creando los mapas mirando si el evento se repite en ambos archivos

    if mp.contains(catalog['user-track-createdMap'],id_event):
        mp.put(catalog['eventMap'],id_event,event)

        #creando mapa para los artistas
        if not mp.contains(catalog['tracks'],event['track_id']):
            trackmap=mp.newMap(numelements=10,loadfactor=1.0)
        else:
            couple=mp.get(catalog["tracks"],event["track_id"])
            trackmap=me.getValue(couple)

        mp.put(trackmap,id_event,event)
        mp.put(catalog["tracks"],event["track_id"],trackmap)


        mp.put(catalog['artists'],event['artist_id'],event)
        

        #Creando el mapa 'tempoMap' segun eventos (user+track+created) unicos

        if om.contains(catalog['tempoMap'],float(event['tempo'])):
            couple = om.get(catalog['tempoMap'],float(event['tempo']))
            list = me.getValue(couple)
            lt.addLast(list,event)

        else:
            list = lt.newList(datastructure='SINGLE_LINKED')
            lt.addLast(list,event)
        om.put(catalog['tempoMap'],float(event['tempo']),list)

        #Agrega el evento a un RBT segun su danceabilidad
       
        if om.contains(catalog["danceability"],danceability):
            couple=om.get(catalog["danceability"],danceability)
            map=me.getValue(couple)
        else:
            map=mp.newMap(maptype="PROBING",numelements=20) #TODO Verificar para el tiempo de carga de datos

        mp.put(map,id_event,event)
        om.put(catalog["danceability"],danceability,map)

        #Creando el mapa 'timeMap' segun las horas pasadas a segundos

        if om.contains(catalog['timeMap'],seconds):
            keyValue = om.get(catalog['timeMap'],seconds)
            timeList = me.getValue(keyValue)
            lt.addLast(timeList,event)

        else:
            timeList = lt.newList(datastructure='SINGLE_LINKED')
            lt.addLast(timeList,event)
        om.put(catalog['timeMap'],seconds,timeList)

        #Creando el mapa 'trackMap' por track_id con valores listas con los eventos de ese track_id

        if om.contains(catalog['trackMap'],track_id):
            trackCouple = om.get(catalog['trackMap'],track_id)
            trackList = me.getValue(trackCouple)
            lt.addLast(trackList,event)

        else:
            trackList = lt.newList(datastructure='SINGLE_LINKED')
            lt.addLast(trackList,event)
        om.put(catalog['trackMap'],track_id,trackList)

def addSentimentValues(catalog,vader):
    id=vader['hashtag'].lower()
    value=vader['vader_avg']
    mp.put(catalog['sentiment_values'],id,value)
    


        
# ================================
# Funciones para creacion de datos
# ================================

def createArtistMap(tempoList):
    # FUNCION REQ 4
    map = mp.newMap(maptype='PROBING')

    iterator = slit.newIterator(tempoList)
    while slit.hasNext(iterator):
        event = slit.next(iterator)
        
        artist = event['artist_id']
        mp.put(map,artist,event)
    return mp.size(map)


def createTempoList(tempoMap, loTempo, hiTempo):
    # FUNCION REQ 3, REQ 4
    """
    Recibe por parametro un RBT del tempo y los rangos, retorna una lista con 
    los eventos/tracks que estan en ese rango
    """
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


def createTempoInstruList(tempoMap,loTempo, hiTempo,loInstru,hiInstru):
    #FUNCION UNICA REQ 3
    """
    Recibe por parametro un mapa con los tempos y lo convierte a una lista con los tempos filtrados,
    retorna una lista de tracks con la instrumentalidad filtrada dentro de los rangos
    """
    listOfLists = om.values(tempoMap, loTempo, hiTempo)
    answerMap = mp.newMap(maptype='CHAINING',loadfactor=1.0,numelements=28000)

    iteratorLists = slit.newIterator(listOfLists)
    while slit.hasNext(iteratorLists):
        list = slit.next(iteratorLists)

        iteratorSongs = slit.newIterator(list)
        while slit.hasNext(iteratorSongs):
            song = slit.next(iteratorSongs)
            track_id = song['track_id']
            if float(song['instrumentalness'])>= loInstru and float(song['instrumentalness'])<= hiInstru:
                mp.put(answerMap, track_id, song)

    return mp.valueSet(answerMap)

def createSubList(list, rank):
    # FUNCION REQ 4
    sublist = lt.subList(list,1,rank)
    return sublist


def filterByChar(catalog, characteristic, loValue,hiValue):
    # FUNCION UNICA REQ 1
    list = mp.valueSet(catalog['eventMap'])
    answerMap = mp.newMap(maptype='PROBNG', numelements=1800)
    counter = 0


    for event in lt.iterator(list):
        if float(loValue) <= float(event[characteristic]) <= float(hiValue):
            counter += 1
            mp.put(answerMap, event['artist_id'],event)
    
    return (counter, mp.size(answerMap))

def filterByFeatures(catalog,lovalueE,hivalueE,lovalueD,hivalueD):
    # FUNCION UNICA REQ 2

    finalmap=mp.newMap(numelements=2000,maptype='PROBING')
    listValues=om.values(catalog["danceability"],lovalueD,hivalueD)

    for map in lt.iterator(listValues):

        values=mp.valueSet(map)

        for value in lt.iterator(values):
            if float(lovalueE)<=float(value["energy"])<=float(hivalueE):
                mp.put(finalmap,value["track_id"],value)
    return mp.valueSet(finalmap)


def filterByTime(timeMap, loHour, hiHour,catalog):
    listOfLists = om.values(timeMap, loHour, hiHour)
    genres ={}
    track_dict = {}

    for genre in catalog['genres'].keys():
        genres[genre] = mp.newMap(numelements=5000, maptype='PROBING',loadfactor=0.5)
        track_dict[genre] = mp.newMap(numelements=5000, maptype='PROBING',loadfactor=0.5)

    for list in lt.iterator(listOfLists):
        for event in lt.iterator(list):
            id_event =(event['user_id'],event['track_id'],event['created_at'])
            for genre in catalog['genres'].keys():
                if catalog['genres'][genre][0] <= float(event['tempo']) <= catalog['genres'][genre][1]:
                    mp.put(genres[genre],id_event,event )
                    mp.put(track_dict[genre],event['track_id'],event )
            
    return genres, track_dict


def findTopGenre(genresDict,trackDict):
    top = []
    orderedDict = {}
    topGenre = ""
    
    for genreList in genresDict.values():
        top.append(mp.size(genreList))
    top.sort(reverse = True)

    for rep in top:
        for genre in genresDict.keys():
            if mp.size(genresDict[genre]) == rep:
                orderedDict[genre] = rep

    for genre in genresDict.keys():
        if mp.size(genresDict[genre]) == top[0]:
            topGenre = genre

    return orderedDict, topGenre, mp.size(trackDict[topGenre])

def findVaderAvg(catalog,track): #recibe como parametro el id de la canción y retorna la cantidad total de hashtags y su promedio de vader
    counter_mean=0
    quantity=0
    hashtag_map = mp.newMap(numelements=15, maptype='PROBING')
    total_hashtags = mp.newMap(numelements=15, maptype='PROBING')

    couple=mp.get(catalog["tracks"],track)
    eventsForTrack=me.getValue(couple)

    events=mp.valueSet(eventsForTrack)
    
    for event in lt.iterator(events):
        id_event=(event["user_id"],event["track_id"],event["created_at"])
        coupleUserTrack=mp.get(catalog["user-track-createdMap"],id_event)

        eventUserTrack=me.getValue(coupleUserTrack)
        hashtag = eventUserTrack['hashtag']

        contains = mp.contains(catalog["sentiment_values"],hashtag)
        mp.put(total_hashtags,hashtag,1)
        if contains:
            coupleSentiment = mp.get(catalog["sentiment_values"],hashtag)
            vader=me.getValue(coupleSentiment)
            if not mp.contains(hashtag_map,hashtag):
                mp.put(hashtag_map,hashtag,1)
                if vader!="":
                    quantity+=float(vader)
                    counter_mean+=1
    if counter_mean == 0:
        counter_mean = 1
    quantity /= counter_mean

    return mp.size(total_hashtags), quantity

def findTenTracks(map,genre,tracks,catalog):
    list = mp.valueSet(map)
    counter = 1
    answerList = lt.newList(datastructure='SINGLE_LIKED')

    top = 10
    if top > lt.size(list):
        top = lt.size(list)
    randomList = random.sample(range(1, lt.size(list)), top)
    print('========================== ',genre.upper(),' SENTIMENT ANALYSIS =========================')
    print(genre.title(),' tiene ',tracks,' tracks unicos')
    print("\nLos top 10 tracks seleccionados aleatoriamente son: \n")
    for i in randomList:
        event = lt.getElement(list, i)
        lt.addLast(answerList,(findVaderAvg(catalog,event['track_id']),
                               event['track_id']))
    answerList = sa.sort(answerList,cmpfunction= compareHashtag)

    for track in lt.iterator(answerList):
        print('TOP',counter, 'track: ',track[1], 'with' ,track[0][0], 'hashtags and VADER = ',round(track[0][1],2))
        counter +=1 


# =====================    
# Funciones de consulta
# =====================

def eventsSize(catalog):
    return mp.size(catalog['eventMap'])

def artistsSize(catalog):
    return mp.size(catalog['artists'])

def tracksSize(catalog):
    return mp.size(catalog['tracks'])

def uniqueSongsChar(charList):
    return lt.size(charList)

def mapSize(map):
    return om.size(map)


# ================================================================
# Funciones utilizadas para comparar elementos dentro de una lista
# ================================================================

def compareHashtag(genre1,genre2):
    return float(genre1[0][0])>float(genre2[0][0])


# Funciones de ordenamiento

# ====================================
# Funciones creacion datos por usuario
# ====================================

def askGenre(catalog):
    # FUNCION UNICA REQ 4
    continuing = True
    genreList = []
    genreDictionary = catalog['genres']

    while continuing == True:
        print("\nLos generos disponibles son")
        print("\nGenero\tBMP Tipico")
        for genre in genreDictionary.keys():
            print(str(genre)+"\t"+str(genreDictionary[genre]))
        print("\nLa lista con los generos a buscar es: ",genreList)
        print("\nQue accion desea realizar:\n")
        print(">1< Agregar un nuevo genero al diccionario")
        print(">2< Agregar un genero a la lista de busqueda")
        print(">3< Finalizar proceso y comenzar a buscar")
        action = int(input("\nDigite el numero de la accion deseada: "))

        if action == 1:
            newGenreName = input("Ingrese el nombre unico para el nuevo genero musical: ")
            loTempo = int(input("Digite el valor entero minimo del tempo del nuevo genero musical: "))
            hiTempo = int(input("Digite el valor entero maximo del tempo del nuevo genero musical: "))
            correct = verifyRanges(loTempo,hiTempo)
            if correct:
                genreDictionary[newGenreName] = (loTempo,hiTempo)
            else:
                print("Los rangos ingresados no son validos")

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

def verifyRanges(loRange,hiRange):
    # FUNCION REQ 1, REQ 3, REQ4
    """
    Verifica que los rangos proporcionados por el usuario sean validos
    """
    correct = False
    if (loRange <= hiRange) and loRange>=0 and hiRange>=0:
        correct = True
    return correct

def timeInSeconds(hour):
    time = hour.split(":")
    seconds = int(time[0])*3600 + int(time[1])*60 + int(time[2])
    return seconds

# =======================
# Funciones para imprimir
# =======================


def printReqTwo(answer):
    #FUNCIÓN REQ2
    top = 5
    if top > lt.size(answer):
        top = lt.size(answer)
    randomList = random.sample(range(1, lt.size(answer)), top)
    counter = 1
    print("Total de tracks unicos : ",lt.size(answer))
    
    for i in randomList:
        event = lt.getElement(answer, i)
        print("Track",counter,":  ",event["track_id"], " with energy of ", event["energy"] ," and danceability of ", event["danceability"] )
        counter +=1
    

def printReqThree(list,loInstru,hiInstru,loTempo,hiTempo):
    # FUNCION UNICA REQ 3
    top = 5
    if top > lt.size(list):
        top = lt.size(list)
    randomList = random.sample(range(1, lt.size(list)), top)
    counter = 1
    print("\n+++++++ Resultados Req No. 3 +++++++")
    print("Instrumentalidad entre: "+ str(loInstru)+" - "+str(hiInstru))
    print("Tempo entre: "+ str(loTempo)+" - "+str(hiTempo))
    print("Total de tracks encontrados: "+str(lt.size(list)))
    print("")
    for i in randomList:
        song = lt.getElement(list, i)
        print("Track "+str(counter)+": "+ song['track_id']+" con instrumentalness de: "+str(song['instrumentalness'])+" y tempo de: "+str(song['tempo']))
        counter +=1

def printReqFour(genreResults,totalReproductions):
    # FUNCION UNICA REQ 4
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
            counter +=1
def printReqFive(genres):
    pass
    #for genre in genres.keys():