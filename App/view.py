"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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
import sys
import controller
from DISClib.ADT import list as lt
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""
# ====================
# Ruta a los archivos
# ====================

contextfile = 'subsamples-small/context_content_features-small.csv'
usertrack = 'subsamples-small/user_track_hashtag_timestamp-small.csv'
sentiment = 'subsamples-small/sentiment_values.csv'

# ====================
# Menu principal
# ====================

def printMenu():
    print("\n/-/-/-/-/-/-/-/-/-/-/-/-/-/-/")
    print("Bienvenido")
    print("1- Inicializar el catalogo")
    print("2- Cargar información en el catálogo")
    print("3- Caracterizar las reproducciones")
    print("4- Encontrar musica para festejar")
    print("5- Encontrar musica para estudiar")
    print("6- Estudiar los generos musicales")
    print("7- Indicar el género musical más escuchado en el tiempo")
    print("/-/-/-/-/-/-/-/-/-/-/-/-/-/-/\n")

catalog = None


"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar: ')
    if int(inputs[0]) == 1:
        print("Inicializando ....")
        catalog = controller.init()

    elif int(inputs[0]) == 2:
        print("\nCargando información de los archivos ....")
        resources=controller.loadData(catalog, contextfile,usertrack,sentiment)
        artists = controller.artistsSize(catalog)
        tracks = controller.tracksSize(catalog)
        events = controller.eventsSize(catalog)
        print("La cantidad de artistas caragados es: "+str(artists))
        print("La cantidad de tracks caragados es: "+str(tracks))
        print("La cantidad de eventos caragados es: "+str(events))
        print("Tiempo gastado en la carga de datos : ", resources[0]," ms" )
        print("Memoria usada en la carga de datos : ",resources[1]," kb")


    elif int(inputs[0]) == 3:
        #REQ 1
        characteristic = (input("Bajo que caracteristica desea buscar: ")).lower()
        loValue = float(input("Digite el valor minimo de la caracteristica del contenido: "))
        hiValue = float(input("Digite el valor maximo de la caracteristica del contenido: "))
        correctValue = controller.verifyRanges(loValue,hiValue)
        correctChar = characteristic in catalog['characteristics']
        if correctValue and correctChar:
            answer = controller.filterByChar(catalog, characteristic, loValue,hiValue)
            print("\n+++++++ Resultados Req No. 1 +++++++")
            print(characteristic + " entre " + str(loValue)+" - "+str(hiValue))
            print("Reproducciones totales: "+str(answer[0][0])+" Artistas unicos: "+str(answer[0][1]))
            print("Tiempo gastado : ", answer[1]," ms")
            print("Memoria consumida : ", answer[2]," kb")
        else:
            print("Los rangos ingresados no son validos o la categoria ingresada no existe")


    elif int(inputs[0])==4:
        #REQ2

        lovalueE=float(input("Digite el rango minimo para energía: "))
        hivalueE=float(input("Digite el rango maximo para energía: "))
        lovalueD=float(input("Digite el rango minimo para danceabilidad: "))
        hivalueD=float(input("Digite el rango maximo para danceabilidad: "))
        correctValue=controller.verifyRanges(lovalueE,hivalueE) and controller.verifyRanges(lovalueD,hivalueD)
        if correctValue:
            answer=controller.filterByFeatures(catalog,lovalueE,hivalueE,lovalueD,hivalueD)
            print("\n+++++++ Resultados Reto No. 2 ++++++")
            print("Energia entre : ",lovalueE," - ",hivalueE)
            print("Danceabilidad entre: ",lovalueD," - ",hivalueD)
            controller.printReqTwo(answer[0])
            print("Tiempo usado: ",answer[1]," ms")
            print("Memoria consumida: ",answer[2]," kb")
        else:
            print("Los rangos ingresados no son validos")

        
    elif int(inputs[0]) == 5:
        #REQ 3
        loInstru = float(input("Digite el valor minimo para la instrumentalidad: "))
        hiInstru = float(input("Digite el valor maximo para la instrumentalidad: "))
        loTempo = float(input("Digite el valor minimo para el tempo: "))
        hiTempo = float(input("Digite el valor maximo para el tempo: "))
        correctInstru = controller.verifyRanges(loInstru,hiInstru)
        correctTempo = controller.verifyRanges(loTempo,hiTempo)
        if correctInstru and correctTempo:
            tempoMap = catalog['tempoMap']
            instruList = controller.createTempoInstruList(tempoMap,loTempo, hiTempo,loInstru,hiInstru)
            controller.printReqThree(instruList[0],loInstru,hiInstru,loTempo,hiTempo)
            
        else:
            print("Los rangos ingresados no son validos")

    elif int(inputs[0]) == 6:
        #REQ 4
        genreList = controller.askGenre(catalog)
        tempoMap = catalog['tempoMap']
        totalReproductions = 0
        genreResults = {}
        tiempo =0
        memoria = 0
        for genre in genreList:
            loTempo = catalog['genres'][genre][0]
            hiTempo = catalog['genres'][genre][1]
            tempoList = controller.createTempoList(tempoMap, loTempo, hiTempo)
            eventList = controller.createSubList(tempoList[0], 10)
            artists = controller.createArtistMap(tempoList[0])
            reproductions = lt.size(tempoList[0])
            totalReproductions += reproductions
            genreResults[genre]={'tempo':(loTempo,hiTempo),'reproductions':reproductions,'artists':artists[0], 'list':eventList}
            tiempo += tempoList[1]
            tiempo += artists[1]
            memoria += tempoList[2]
            memoria += artists[2]

        controller.printReqFour(genreResults,totalReproductions)
        print("Tiempo usado: ",tiempo," ms")
        print("Memoria consumida: ",memoria," kb")

    elif int(inputs[0]) == 7:
        #REQ 5
        counter = 1
        sumation = 0
        loHour = input("Digite el valor minimo de la hora del dia con formato (HH:MM:SS): ")
        hiHour = input("Digite el valor maximo de la hora del dia con formato (HH:MM:SS): ")
        loHourSec = controller.timeInSeconds(loHour)
        hiHourSec = controller.timeInSeconds(hiHour)
        if True:
            timeMemory = controller.memoryTime(True,0,0)
            genresDict = controller.filterByTime(catalog['timeMap'],loHourSec,hiHourSec,catalog)
            print("\n+++++++ Resultados Req No. 5 +++++++")
            print("====================== TOP REPRODUCCIONES GENEROS ======================")
            stepOne = controller.findTopGenre(genresDict[0],genresDict[1])
            for genre in stepOne[0].keys():
                print('TOP ',counter,': ',genre,' con ',stepOne[0][genre],' reproducciones')
                counter += 1
                sumation += stepOne[0][genre]
            print("\nHay un total de: ",sumation," reproducciones entre ",loHour, " y ",hiHour)
            print("El genero mas escuchado fue: ",stepOne[1],' con ',stepOne[0][stepOne[1]],' reproducciones\n')
            stepTwo = controller.findTenTracks(genresDict[0][stepOne[1]],stepOne[1],stepOne[2],catalog)
            timeMemory = controller.memoryTime(False,timeMemory[0],timeMemory[1])
            print("Tiempo usado: ",timeMemory[0]," ms")
            print("Memoria consumida: ",timeMemory[1]," kb")
        else: 
            print("Los rangos ingresados no son validos")
        
        
    
sys.exit(0)
