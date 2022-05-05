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
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp

csv.field_size_limit(2147483647)


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""


tam = "large"
# Inicialización del Creación de Controller

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

def loadData(control):
    """
    Carga los datos de los archivos y cargar los datos en la
    estructura de datos
    """
    catalog = control['model']
    
    tracemalloc.start()

    start_time = getTime()
    start_memory = getMemory()

    artists = loadArtists(catalog)
    albums = loadAlbums(catalog)
    tracks = loadTracks(catalog)


    stop_memory = getMemory()
    stop_time = getTime()
  
    tracemalloc.stop()

    time = deltaTime(stop_time, start_time)
    memory = deltaMemory(stop_memory, start_memory)
    return tracks, albums, artists, time, memory

def loadTracks(catalog):
    """
    Carga todas las canciones del archivo y las agrega a la lista de tracks. 
    """
    tracksfile = cf.data_dir + 'Spotify/spotify-tracks-utf8-{0}.csv'.format(tam)
    input_file = csv.DictReader(open(tracksfile, encoding='utf-8'))
    for track in input_file:
        model.addTrack(catalog, track)
    return lt.size(catalog["tracks"])

def loadAlbums(catalog):
    """
    Carga todos los albums del archivo y los agrega a la lista de albums.
    """
    albumsfile = cf.data_dir + 'Spotify/spotify-albums-utf8-{0}.csv'.format(tam)
    input_file = csv.DictReader(open(albumsfile, encoding='utf-8'))
    for album in input_file:
        model.addAlbum(catalog, album)
    return lt.size(catalog["albums"])

def loadArtists(catalog):
    """
    Carga todas los artistas del archivo y las agrega a la lista de artists.
    """
    artistsfile = cf.data_dir + 'Spotify/spotify-artists-utf8-{0}.csv'.format(tam)
    input_file = csv.DictReader(open(artistsfile, encoding='utf-8'))
    for artist in input_file:
        model.addArtist(catalog, artist)
    return lt.size(catalog["artists"])

#=====================[R1]=======================================
def call_answer_r1(catalog, albumes_del_anio):

    tracemalloc.start()

    start_time = getTime()
    start_memory = getMemory()

    answer_list_r1, asc_artists, num_albums = model.answer_r1(catalog, albumes_del_anio)

    stop_memory = getMemory()
    stop_time = getTime()
    
    tracemalloc.stop()

    time = deltaTime(stop_time, start_time)
    memory = deltaMemory(stop_memory, start_memory)

    if answer_list_r1 == None:
        return None, None, None, None, None
    return answer_list_r1, asc_artists, num_albums, time, memory


#=====================[R2]=======================================
def call_answer_r2(catalog, inp_popularity):

    tracemalloc.start()

    start_time = getTime()
    start_memory = getMemory()

    answer_list_r2, asc_tracks, num_artists = model.answer_r2(catalog, inp_popularity)

    stop_memory = getMemory()
    stop_time = getTime()
    
    tracemalloc.stop()

    time = deltaTime(stop_time, start_time)
    memory = deltaMemory(stop_memory, start_memory)

    if answer_list_r2 == None:
        return None, None, None, None, None
    return answer_list_r2, asc_tracks, num_artists, time, memory



#=====================[R3]=======================================
def call_answer_R3(catalog, inp_track_popularity):
    tracemalloc.start()

    start_time = getTime()
    start_memory = getMemory()
    
    

    tam_list, list_resp_R3, names_albums, names_artists = model.answer_R3(catalog, inp_track_popularity)

    stop_memory = getMemory()
    stop_time = getTime()
    
    tracemalloc.stop()

    time = deltaTime(stop_time, start_time)
    memory = deltaMemory(stop_memory, start_memory)
    if tam_list == None:
        return None, None, None, None, None, None
    return time, memory, tam_list, list_resp_R3, names_albums, names_artists

#===================[R4]==========================================
def call_answer_r4(catalog, artist_name, country):
    tracemalloc.start()

    start_time = getTime()
    start_memory = getMemory()

    popular_track, num_tracks, num_albums = model.answer_r4(catalog, artist_name, country)

    stop_memory = getMemory()
    stop_time = getTime()
    
    tracemalloc.stop()

    time = deltaTime(stop_time, start_time)
    memory = deltaMemory(stop_memory, start_memory)

    if popular_track == None:
        return None, None, None, None, None
    return popular_track, num_tracks, num_albums, time, memory


#=====================[R5]=======================================
def call_answer_R5(catalog, artist_name):
    tracemalloc.start()

    start_time = getTime()
    start_memory = getMemory()
    
    

    album_types, resp_albums, resp_tracks, names_artists = model.answer_R5(catalog, artist_name)

    stop_memory = getMemory()
    stop_time = getTime()
    
    tracemalloc.stop()

    time = deltaTime(stop_time, start_time)
    memory = deltaMemory(stop_memory, start_memory)
    if album_types == None:
        return None, None, None, None, None, None
    return time, memory, album_types, resp_albums, resp_tracks, names_artists



















#=====================[R6]=========================================
def call_answer_r6(catalog, artist_name, country, n):
    tracemalloc.start()

    start_time = getTime()
    start_memory = getMemory()

    answer_tracks, num_tracks = model.answer_r6(catalog, artist_name, country, n)

    stop_memory = getMemory()
    stop_time = getTime()
    
    tracemalloc.stop()

    time = deltaTime(stop_time, start_time)
    memory = deltaMemory(stop_memory, start_memory)

    if answer_tracks == None:
        return None, None, None, None
    return answer_tracks, num_tracks, time, memory







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

