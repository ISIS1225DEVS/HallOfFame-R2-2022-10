"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrollado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
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
 * along withthis program.If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import model
import time
import tracemalloc
import csv

csv.field_size_limit(2147483647)

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo Spotify

def newController():
    """
    Llama la funcion de inicializacion del catalogo del modelo.
    """

    control = {'model': None}
    control['model'] = model.newCatalog()
    return control

# Funciones para la carga de datos

def loadData(control):
    """
    Carga los datos de los archivos y cargar los datos en la
    estructura de datos
    """
    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()
    catalog = control['model']
    albums = loadAlbums(catalog)
    artists = loadArtists(catalog)
    tracks = loadTracks(catalog)
    print('Ajustando artistas, espere un momento...')
    model.namesakeManagement(catalog)
    print('Organizando información, espere un momento...')
    model.sortSpotifyLists(catalog)
    print('Fusionando información, espere un momento...')
    model.connectFullData(catalog)
    print('Creando mapas, espere un momento...')
    model.mapsCreator(catalog)
    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()
    delta_time = deltaTime(stop_time, start_time)
    delta_memory = deltaMemory(stop_memory, start_memory)
    print('Time: ', delta_time)
    print('Memory: ', delta_memory)
    return albums, artists, tracks

def loadAlbums(catalog, suffix = '-large.csv'):
    """
    Carga los albumes del archivo.
    """
    albumsfile = cf.data_dir + 'Spotify/spotify-albums-utf8' + suffix
    input_file = csv.DictReader(open(albumsfile, encoding ='utf-8'))
    for album in input_file:
        model.addAlbum(catalog, album)
    return model.albumsSize(catalog)

def loadArtists(catalog, suffix = '-large.csv'):
    """
    Carga los albumes del archivo.
    """
    artistsfile = cf.data_dir + 'Spotify/spotify-artists-utf8' + suffix
    input_file = csv.DictReader(open(artistsfile, encoding ='utf-8'))
    for artist in input_file:
        model.addArtist(catalog, artist)
    return model.artistsSize(catalog)

def loadTracks(catalog, suffix = '-large.csv'):
    """
    Carga los albumes del archivo.
    """
    tracksfile = cf.data_dir + 'Spotify/spotify-tracks-utf8' + suffix
    input_file = csv.DictReader(open(tracksfile, encoding ='utf-8'))
    for track in input_file:
        model.addTrack(catalog, track)
    return model.tracksSize(catalog)

# Funciones de ordenamiento

def sortpopularityartist(catalog):
    return model.sortpopularityartist(catalog)

# Funciones de consulta sobre el catálogo

#=^..^=   =^..^=   =^..^=    =^..^=  [Requerimiento 1]  =^..^=    =^..^=    =^..^=    =^..^=
def albumsByReleaseYear(catalog, year):
    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()
    answerLstreq = model.albumsByReleaseYear(catalog, year)
    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()
    delta_time = deltaTime(stop_time, start_time)
    delta_memory = deltaMemory(stop_memory, start_memory)
    return answerLst(answerLstreq), model.lt.size(answerLstreq), delta_time, delta_memory

#=^..^=   =^..^=   =^..^=    =^..^=  [Requerimiento 2]  =^..^=    =^..^=    =^..^=    =^..^=

def artistByPopularity(catalog, popularity):
    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()
    answerLstreq = model.artistByPopularity(catalog, popularity)
    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()
    delta_time = deltaTime(stop_time, start_time)
    delta_memory = deltaMemory(stop_memory, start_memory)
    return answerLst(answerLstreq), model.lt.size(answerLstreq), delta_time, delta_memory

#=^..^=   =^..^=   =^..^=    =^..^=  [Requerimiento 3]  =^..^=    =^..^=    =^..^=    =^..^=
def tracksByPopularity(catalog, popularity):
    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()
    answerLstreq = model.tracksByPopularity(catalog, popularity)
    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()
    delta_time = deltaTime(stop_time, start_time)
    delta_memory = deltaMemory(stop_memory, start_memory)
    return answerLst(answerLstreq), model.lt.size(answerLstreq), delta_time, delta_memory

#=^..^=   =^..^=   =^..^=    =^..^=  [Requerimiento 4]  =^..^=    =^..^=    =^..^=    =^..^=
def popularTrackByArtist(catalog, artistName, countryCode):
    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()
    answerLstreq, albumsSize, sizeSongs = model.popularTrackByArtist(catalog, artistName, countryCode)
    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()
    delta_time = deltaTime(stop_time, start_time)
    delta_memory = deltaMemory(stop_memory, start_memory)
    return answerLst(answerLstreq), model.lt.size(answerLstreq), delta_time, delta_memory, albumsSize, sizeSongs

#=^..^=   =^..^=   =^..^=    =^..^=  [Requerimiento 5]  =^..^=    =^..^=    =^..^=    =^..^=
def albumInfo(catalog, artistName):
    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()
    sizeAlbumsArtist, countByType, albumssorted, trackArray = model.albumInfo(catalog, artistName)
    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()
    delta_time = deltaTime(stop_time, start_time)
    delta_memory = deltaMemory(stop_memory, start_memory)
    return sizeAlbumsArtist, countByType, answerLst(albumssorted), answerLst(trackArray), delta_time, delta_memory

#=^..^=   =^..^=   =^..^=    =^..^=  [Bono]  =^..^=    =^..^=    =^..^=    =^..^=
def tracksByDistributionOfArtist(catalog, countryCode, artistName, top):
    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()
    topTracks, tracksSize = model.tracksByDistributionOfArtist(catalog, countryCode, artistName, top)
    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()
    delta_time = deltaTime(stop_time, start_time)
    delta_memory = deltaMemory(stop_memory, start_memory)
    return answerLst(topTracks), tracksSize, delta_time, delta_memory

def getLastNum(number, spotifyList):
    'Retorna los "number" ultimos'
    return model.getLastNum(number, spotifyList)

def getFirstNum(number, spotifyList):
    'Retorna los "number" primeros'
    return model.getFirstNum(number, spotifyList)

# Funciones de analisis

def loadArtistByGenreMap(catalog, artistSize, mapType, loadFactor):
    # inicializa el proceso para medir memoria
    tracemalloc.start()
    # toma de tiempo y memoria al inicio del proceso
    start_time = getTime()
    start_memory = getMemory()
    catalog['artistsByGenres'] = model.resetMap(artistSize, mapType, loadFactor)
    model.loadArtistByGenreMap(catalog)
    # toma de tiempo y memoria al final del proceso
    stop_memory = getMemory()
    stop_time = getTime()
    # finaliza el procesos para medir memoria
    tracemalloc.stop()
    # calculando la diferencia de tiempo y memoria
    delta_time = deltaTime(stop_time, start_time)
    delta_memory = deltaMemory(stop_memory, start_memory)
    return delta_time, delta_memory

def calculator(catalog, mapType, loadFactor):
    print('Espere un momento mientras se hace el promedio del factor de carga ...')
    catalog['artists'] = model.resetList()
    loadArtists(catalog, "-large.csv")

    time1, memory1 = loadArtistByGenreMap(catalog, 4210, mapType, loadFactor)
    print("PRIMERA CARGA: Tiempo [ms]: ", time1, "||","Memoria [kB]: ", str(memory1))

    time2, memory2 = loadArtistByGenreMap(catalog, 4210, mapType, loadFactor)
    print("SEGUNDA CARGA: Tiempo [ms]: ", time2, "||","Memoria [kB]: ", str(memory2))

    time3, memory3 = loadArtistByGenreMap(catalog, 4210, mapType, loadFactor)
    print("TERCERA CARGA: Tiempo [ms]: ", time3, "||","Memoria [kB]: ", str(memory3))
    #print(model.mp.size(catalog['artistsByGenres']))

    averageTime = round(((time1 + time2 + time3) / 3),2)
    averageMemory = round(((memory1 + memory2 + memory3) /3), 2)

    return averageTime, averageMemory

# Funciones auxiliares

def answerLst(spotifyList):
    if model.lt.size(spotifyList) <= 6:
        return spotifyList
    else:
        firsts = getFirstNum(3, spotifyList)
        lasts = getLastNum(3, spotifyList)
        return model.listsFusion(firsts, lasts)

def UEXNamesake(catalog, artistName):
    namesakeCount, artistl = model.UEXNamesake(catalog, artistName)
    return namesakeCount, artistl



# Funciones para medir tiempos de ejecucion

def getTime():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def deltaTime(end, start):
    """
    devuelve la diferencia entre tiempos de procesamiento muestreados
    """
    elapsed = float(end - start)
    return elapsed


# Funciones para medir la memoria utilizada


def getMemory():
    """
    toma una muestra de la memoria alocada en instante de tiempo
    """
    return tracemalloc.take_snapshot()


def deltaMemory(stop_memory, start_memory):
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