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

from functools import total_ordering
import config as cf
import model
import csv
import time
import tracemalloc


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros

def newController():
    """
    Crea una instancia del modelo
    """
    control = {
        'model': None
    }
    control['model'] = model.newCatalog()
    return control


# Funciones para la carga de datos

def loadData(control, file):
    """
    Carga los datos de los archivos y cargar los datos en la
    estructura de datos
    """
    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()


    catalog = control['model']
    artists, genres, artistpopularity, artistsname = loadArtists(catalog, file)
    albums, albumyear, albumartist = loadAlbums(catalog, file)
    tracks, trackalbum = loadTracks(catalog, file)

    firstartists = model.getFirstArtists(catalog)
    firstalbums = model.getFirstAlbums(catalog)
    firsttracks = model.getFirstTracks(catalog)

    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = deltaTime(stop_time, start_time)
    delta_memory = deltaMemory(stop_memory, start_memory)

    return artists, albums, albumyear, tracks, genres, artistpopularity, artistsname, albumartist, trackalbum, firstartists, firstalbums, firsttracks, delta_time, delta_memory

def loadArtists(catalog, file):
    """
    Carga los libros del archivo.  Por cada libro se toman sus autores y por
    cada uno de ellos, se crea en la lista de autores, a dicho autor y una
    referencia al libro que se esta procesando.
    """
    artistsfile = cf.data_dir + 'spotify-artists-utf8-' + file + '.csv'
    input_file = csv.DictReader(open(artistsfile, encoding='utf-8'))
    for artist in input_file:
        model.addArtist(catalog, artist)
    return model.artistsSize(catalog), model.genresSize(catalog), model.artistpopularitySize(catalog), model.artistsnameSize(catalog)

def loadAlbums(catalog, file):
    """
    Carga todos los tags del archivo y los agrega a la lista de tags
    """
    albumfile = cf.data_dir + 'spotify-albums-utf8-' + file + '.csv'
    input_file = csv.DictReader(open(albumfile, encoding='utf-8'))
    for album in input_file:
        model.addAlbum(catalog, album)
    return model.albumsSize(catalog), model.albumyearSize(catalog), model.albumartistSize(catalog)

def loadTracks(catalog, file):
    """
    Carga la información que asocia tags con libros.
    """
    trackfile = cf.data_dir + 'spotify-tracks-utf8-' + file + '.csv'
    input_file = csv.DictReader(open(trackfile, encoding='utf-8'))
    for track in input_file:
        model.addTrack(catalog, track)
    return model.tracksSize(catalog), model.trackalbumSize(catalog)


# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo

def AlbumsinCertainYear(year, catalog):

    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()

    primero, segundo, tercero, antepenultimo, penultimo, ultimo, size = model.AlbumsinCertainYear(year, catalog)

    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()
    delta_time = deltaTime(stop_time, start_time)
    delta_memory = deltaMemory(stop_memory, start_memory)

    return primero, segundo, tercero, antepenultimo, penultimo, ultimo, size, delta_time, delta_memory

def ArtistswithCertainPopularity(popularity, catalog):

    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()

    primero, segundo, tercero, antepenultimo, penultimo, ultimo, size = model.ArtistswithCertainPopularity(popularity, catalog)

    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()
    delta_time = deltaTime(stop_time, start_time)
    delta_memory = deltaMemory(stop_memory, start_memory)

    return primero, segundo, tercero, antepenultimo, penultimo, ultimo, size, delta_time, delta_memory

def TrackByPopularity(popularity, catalog):
    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()
    ListTracks = model.TracksByPopularity(popularity, catalog)
    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()
    total ={}
    delta_time = deltaTime(stop_time, start_time)
    delta_memory = deltaMemory(stop_memory, start_memory)
    total["resultado"] = ListTracks
    total["tiempo"] = delta_time
    total["memoria"] = delta_memory   
    return total

def MostPopularArtistSong(name, country, catalog):
    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()
    MostPopularArtistSong = model.MostPopularArtistSong(name, country, catalog)
    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()
    delta_time = deltaTime(stop_time, start_time)
    delta_memory = deltaMemory(stop_memory, start_memory)
    total ={}
    total["resultado"] = MostPopularArtistSong
    total["tiempo"] = delta_time
    total["memoria"] = delta_memory 
    return total

def ArtistDiscography(name, catalog):

    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()

    single_albums, compilation_albums, album_albums, total_albums, primero, segundo, tercero, antepenultimo, penultimo, ultimo, popular_songs = model.ArtistDiscography(name, catalog)

    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()
    delta_time = deltaTime(stop_time, start_time)
    delta_memory = deltaMemory(stop_memory, start_memory)

    return single_albums, compilation_albums, album_albums, total_albums, primero, segundo, tercero, antepenultimo, penultimo, ultimo, popular_songs, delta_time, delta_memory

def Bonus(name, country, top, catalog):
    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()
    Bonus = model.Bonus(name, country, top, catalog)
    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()
    total ={}
    delta_time = deltaTime(stop_time, start_time)
    delta_memory = deltaMemory(stop_memory, start_memory)
    total["resultado"] = Bonus
    total["tiempo"] = delta_time
    total["memoria"] = delta_memory 
    return total

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