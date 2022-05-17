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
import tracemalloc
import time
import csv
import sys
csv.field_size_limit(2147483647)
default_limit = 100000
sys.setrecursionlimit(default_limit*10)

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""
def inicializarCatalogo():
    return model.inicializarCatalogo()

# Funciones para la carga de datos
def loadArtists(catalogo, tamanioArchivo):
    tagsfile = cf.data_dir + 'Spotify/spotify-artists-utf8-'+tamanioArchivo+'.csv'
    input_file = csv.DictReader(open(tagsfile, encoding='utf-8'))
    for artist in input_file:
        listaArtistas=model.addArtistsId(catalogo, artist)
        model.addArtistsName(catalogo, artist)
        model.addArtistaPopularidad(catalogo, artist)
    return listaArtistas

def loadCanciones(catalogo, tamanioArchivo):
    tagsfile = cf.data_dir + 'Spotify/spotify-tracks-utf8-'+tamanioArchivo+'.csv'
    input_file = csv.DictReader(open(tagsfile, encoding='utf-8'))
    for cancion in input_file:
        listaCanciones=model.addCancionId(catalogo, cancion)
        model.addCancionesPopularidad(catalogo, cancion)
        model.addCancionesPaises(catalogo, cancion)
        model.addCancionesAlbumId(catalogo, cancion)
    return listaCanciones
       
def loadAlbumes(catalogo, tamanioArchivo):
    tagsfile = cf.data_dir + 'Spotify/spotify-albums-utf8-'+tamanioArchivo+'.csv'
    input_file = csv.DictReader(open(tagsfile, encoding='utf-8'))
    for album in input_file:
        listaAlbumes=model.addAlbumId(catalogo, album)
        model.addAlbumAnio(catalogo, album)
        model.addArtistaAlbumes(catalogo, album)
        model.addAlbumesPaises(catalogo, album)
    return listaAlbumes

def loadData(catalogo, tamanioArchivos):
    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()
    listaArtistas=loadArtists(catalogo, tamanioArchivos)
    listaCanciones=loadCanciones(catalogo, tamanioArchivos)
    listaAlbumes=loadAlbumes(catalogo, tamanioArchivos)
    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()
    delta_time = deltaTime(stop_time, start_time)
    delta_memory = deltaMemory(stop_memory, start_memory)
    return delta_time,delta_memory, listaArtistas, listaAlbumes, listaCanciones

# Funciones de ordenamiento
def listaOrdenadaAlbumesAnio(catalogo,anio):
    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()
    lista=model.listaOrdenadalbumesAnio(catalogo,anio)
    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()
    delta_time = deltaTime(stop_time, start_time)
    delta_memory = deltaMemory(stop_memory, start_memory)
    return lista, delta_time, delta_memory

def listaOrdenadaArtistasPopularidad(catalogo, popularidad):
    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()
    lista=model.listaOrdenadaArtistasPopularidad(catalogo,popularidad)
    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()
    delta_time = deltaTime(stop_time, start_time)
    delta_memory = deltaMemory(stop_memory, start_memory)
    return lista, delta_time, delta_memory
    
def listaOrdenadaCancionesPopularidad(catalogo, popularidad):
    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()
    lista=model.listaOrdenadaCancionesPopularidad(catalogo, popularidad)
    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()
    delta_time = deltaTime(stop_time, start_time)
    delta_memory = deltaMemory(stop_memory, start_memory)
    return lista, delta_time, delta_memory
def listaOrdenadaPaisCanciones(catalogo, codigoPais):
    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()
    lista=model.listaOrdenadaPaisCanciones(catalogo, codigoPais)
    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()
    delta_time = deltaTime(stop_time, start_time)
    delta_memory = deltaMemory(stop_memory, start_memory)
    return lista, delta_time, delta_memory
def listaOrdenadaPaisAlbumes(catalogo, codigoPais):
    return model.listaOrdenadaPaisAlbumes(catalogo, codigoPais)
def listaAlbumesArtista(catalogo, nombre):
    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()
    lista=model.listaAlbumesArtista(catalogo, nombre)
    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()
    delta_time = deltaTime(stop_time, start_time)
    delta_memory = deltaMemory(stop_memory, start_memory)
    return lista, delta_time, delta_memory

    return model.listaAlbumesArtista(catalogo, nombre)

# Funciones de consulta sobre el catálogo


def artistasSize(catalogo):
    return model.artistsSize(catalogo)
def cancionesSize(catalogo):
    return model.cancionesSize(catalogo)
def albumesSize(catalogo):
    return model.albumesSize(catalogo)

#funciones caracteristicas especiales
def cancionPopularArtistaPais(catalogo, listaCancionesPais, artista):
    return model.cancionPopularArtistaPais(catalogo, listaCancionesPais, artista)
def listaAlbumesArtistaPais(catalogo, listaAlbumesPais, artista):
    return model.listaAlbumesArtistaPais(catalogo, listaAlbumesPais, artista)
def numeroCancionesAlbum(catalogo, albumId):
    return model.numeroCancionesAlbum(catalogo, albumId)
def nombreArtistaId(catalogo, artistId):
    return model.nombreArtistaId(catalogo, artistId)
def nombreCancionId(catalogo, trackId):
    return model.nombreCancionId(catalogo, trackId)
def nombreAlbumId(catalogo, albumId):
    return model.nombreAlbumId(catalogo,albumId)
def nombreVariosArtistasId(catalogo, artistsId):
    return model.nombreVariosArtistasId(catalogo, artistsId)
def tipoAlbumesArtista(listaAlbumesArtista):
    return model.tipoAlbumesArtista(listaAlbumesArtista)
def cancionPopularAlbum(catalogo, albumId):
    return model.cancionPopularAlbum(catalogo, albumId)
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
