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


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as m
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
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
            'artistsUnique':None,
            'songsUnique':None}

    catalog['songs'] = lt.newList(datastructure='SINGLE_LINKED')

    catalog['artistsUnique'] = om.newMap(omaptype='BST')

    catalog['songsUnique'] = om.newMap(omaptype='BST')

    return catalog

# Funciones para agregar informacion al catalogo

def addSong(catalog, song):
    lt.addLast(catalog['songs'],song)
    updateArtistsUnique(catalog['artistsUnique'],song)
    updateSongsUnique(catalog['songsUnique'],song)

def updateArtistsUnique(map, song):
    artist = song['artist_id']
    exists = om.get(map,artist)

    if exists is None:
        list = lt.newList(datastructure="SINGLE_LINKED")
        lt.addLast(list, song)
        om.put(map,artist,list)

    else:
        existingList = me.getValue(exists)
        lt.addLast(existingList,song)

def updateSongsUnique(map, song):
    track = song['track_id']
    exists = om.get(map, track)

    if exists is None:
        list = lt.newList(datastructure="SINGLE_LINKED")
        lt.addLast(list, song)
        om.put(map,track,list)

    else:
        existingList = me.getValue(exists)
        lt.addLast(existingList,song)


# Funciones para creacion de datos

# Funciones de consulta

def songsSize(catalog):
    return lt.size(catalog['songs'])

def artistsSize(catalog):
    return om.size(catalog['artistsUnique'])

def uniqueSongsSize(catalog):
    return om.size(catalog['songsUnique'])

# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento
