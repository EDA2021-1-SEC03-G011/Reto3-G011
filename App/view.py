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

# ====================
# Menu principal
# ====================

def printMenu():
    print("\n/-/-/-/-/-/-/-/-/-/-/-/-/-/-/")
    print("Bienvenido")
    print("1- Inicializar el catalogo")
    print("2- Cargar información en el catálogo")
    print("3- Caracterizar las reproducciones")
    print("5- Encontrar musica para estudiar")
    print("6- Estudiar los generos musicales")
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
        controller.loadData(catalog, contextfile,usertrack)


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
            print("Reproducciones totales: "+str(answer[0])+" Artistas unicos: "+str(answer[1]))
        else:
            print("Los rangos ingresados no son validos o la categoria ingresada no existe")

    elif int(inputs[0]) == 5:
        #REQ 3
        loInstru = float(input("Digite el valor minimo para la instrumentalidad: "))
        hiInstru = float(input("Digite el valor maximo para la instrumentalidad: "))
        loTempo = float(input("Digite el valor minimo para el tempo: "))
        hiTempo = float(input("Digite el valor maximo para el tempo: "))
        correctInstru = controller.verifyRanges(loInstru,hiInstru)
        correctTempo = controller.verifyRanges(loTempo,hiTempo)
        if correctInstru and correctTempo:
            tempoMap = catalog['trackTempoMap']
            tempoList = controller.createTempoList(tempoMap, loTempo, hiTempo)
            instruList = controller.createInstruList(tempoList,loInstru,hiInstru)
            controller.printReqThree(instruList,loInstru,hiInstru,loTempo,hiTempo)
        else:
            print("Los rangos ingresados no son validos")

    elif int(inputs[0]) == 6:
        #REQ 4
        genreList = controller.askGenre(catalog)
        tempoMap = catalog['tempoMap']
        totalReproductions = 0
        genreResults = {}
        for genre in genreList:
            loTempo = catalog['genres'][genre][0]
            hiTempo = catalog['genres'][genre][1]
            tempoList = controller.createTempoList(tempoMap, loTempo, hiTempo)
            eventList = controller.createSubList(tempoList, 10)
            artistsMap = controller.createArtistMap(tempoList)
            reproductions = lt.size(tempoList)
            totalReproductions += reproductions
            genreResults[genre]={'tempo':(loTempo,hiTempo),'reproductions':reproductions,'artists':artistsMap, 'list':eventList}

        controller.printReqFour(genreResults,totalReproductions)
            
    else:
        sys.exit(0)
sys.exit(0)
