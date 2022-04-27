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
import time
import tracemalloc
import config as cf
import model
import csv
csv.field_size_limit(2147483647)

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""
# ===========================
# Inicialización del catálogo
# ===========================

def newController():
    control = {'model': None}
    control['model'] = model.newCatalog()
    return control

# ================================
# Funciones para la carga de datos
# ================================

def loadData(control):
    catalog = control['model']
    songs = loadSongs(catalog)
    albums = loadAlbums(catalog)
    model.removeMapIdAlbums(catalog)
    artists = loadArtists(catalog)
    model.removeMapIdArtists(catalog)
    printAT = cleanerArtists(catalog, artists)
    printAB = cleanerAlbums(catalog, albums)
    printSG = cleanerSongs(catalog, songs)
    return printAB, printSG, printAT

def loadArtists(catalog):
    artistsfile = cf.data_dir + 'spotify-artists-utf8-large.csv'
    input_file = csv.DictReader(open(artistsfile, encoding='utf-8'))
    for artist in input_file:
        model.addArtist(catalog, artist)
    return model.LSTSize(catalog['artists'])

def loadAlbums(catalog):
    albumsfile = cf.data_dir + 'spotify-albums-utf8-large.csv'
    input_file = csv.DictReader(open(albumsfile, encoding='utf-8'))
    for album in input_file:
        model.addAlbum(catalog, album)
    return model.LSTSize(catalog['albums'])

def loadSongs(catalog):
    songsfile = cf.data_dir + 'spotify-tracks-utf8-large.csv'
    input_file = csv.DictReader(open(songsfile, encoding='utf-8'))
    for song in input_file:
        model.addSong(catalog, song)
    return model.LSTSize(catalog['songs'])

def cleanerArtists(catalog, size):
    if size == 0:
        return 0, None
    artists = model.get3FirstandLast(catalog['artists'], size)
    return size, model.cleanerArtists(artists)

def cleanerAlbums(catalog, size):
    if size == 0:
        return 0, None
    albums = model.get3FirstandLast(catalog['albums'], size)
    return size, model.cleanerAlbums(albums)

def cleanerSongs(catalog, size):
    if size == 0:
        return 0, None
    songs = model.get3FirstandLast(catalog['songs'], size)
    return size, model.cleanerSongs(songs)
    
# =======================================
# Funciones de consulta sobre el catálogo
# =======================================

def getAlbumsYear(cntrl, year):
    size, albums = model.getAlbumsYear(cntrl['model'], year)
    if size == 0:
        return 0 , None
    return size, model.cleanerAlbums(albums)

def getArtistPopurality(cntrl, number):
    size, artists = model.getPopularity(cntrl['model'], number, 1, model.cmpATFollowsName)
    if size == 0:
        return 0 , None
    return size, model.cleanerArtists(artists)

def getSongPopurality(cntrl, number):
    size, songs = model.getPopularity(cntrl['model'], number, 2, model.cmpSGDurationName)
    if size == 0:
        return 0 , None
    return size, model.cleanerSongs(songs)

def getSGByArtistCountry(cntrl, name, country):
    sizeAB, sizeSG, song = model.getSGByArtistCountry(cntrl['model'], name, country)
    if sizeSG == 0 and sizeAB == 0:
        return 0, 0, None
    elif sizeSG == 0:
        return sizeAB, 0, None
    return sizeAB, sizeSG, model.cleanerSongs(song)

def getDiscography(cntrl, name):
    ABSingle, ABCompilation, ABAlbum, albums, songs = model.getDiscography(cntrl['model'], name)
    if albums == None:
        return 0, 0, 0, None
    return ABSingle, ABCompilation, ABAlbum, model.cleanerAlbums(albums), model.cleanerSongs(songs)

def getSGArtistCountryTOP(cntrl, name, country, number):
    sizeSG, song = model.getSGByArtistCountryTOP(cntrl['model'], name, country, number)
    if sizeSG == 0:
        return 0, None
    return sizeSG, model.cleanerSongs(song)

# ========================
# Funciones de Laboratorio
# ========================

def loadMapGenre(cntrl, type, fc):
    model.configMapGenre(cntrl['model'], type, fc)
    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()
    size = model.LoadMapGenre(cntrl['model'])
    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()
    delta_time = deltaTime(stop_time, start_time)
    delta_memory = deltaMemory(stop_memory, start_memory)
    return size, delta_time, delta_memory

def getTime():
    return float(time.perf_counter()*1000)

def deltaTime(end, start):
    elapsed = float(end - start)
    return elapsed

def getMemory():
    return tracemalloc.take_snapshot()

def deltaMemory(stop_memory, start_memory):
    memory_diff = stop_memory.compare_to(start_memory, "filename")
    delta_memory = 0.0
    for stat in memory_diff:
        delta_memory = delta_memory + stat.size_diff
    delta_memory = delta_memory/1024.0
    return delta_memory
