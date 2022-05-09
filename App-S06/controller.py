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
import sys

default_limit = 1000
sys.setrecursionlimit(default_limit*10)
csv.field_size_limit(2147483647)


def newController():
    control = model.newCatalog()
    return control

# Funciones para la carga de datos

def loadData(control):
    catalog = control
    albums = loadAlbums(catalog)
    tracks = loadTracks(catalog)
    artists = loadArtists(catalog)
    return albums, tracks, artists

# Funciones de ordenamiento

def loadAlbums(catalog):
    albumsfile = cf.data_dir + 'Spotify/spotify-albums-utf8-large.csv'
    input_file = csv.DictReader(open(albumsfile, encoding='utf-8'))
    for album in input_file:
        model.addAlbum(catalog, album)
        model.addAlbumId(catalog, album['id'], album)
    return catalog['albums']

def loadTracks(catalog):
    tracksfile = cf.data_dir + 'Spotify/spotify-tracks-utf8-large.csv'
    input_file = csv.DictReader(open(tracksfile, encoding='utf-8'))
    for track in input_file:
        model.addTrack(catalog, track)
        model.addTrackId(catalog, track['id'], track)
    return catalog['tracks']

def loadArtists(catalog):
    artistsfile = cf.data_dir + 'Spotify/spotify-artists-utf8-large.csv'
    input_file = csv.DictReader(open(artistsfile, encoding='utf-8'))
    for artist in input_file:
        model.addArtist(catalog, artist)
        model.addArtistName(catalog, artist['name'], artist)
        model.addArtistId(catalog, artist['id'], artist)
    return catalog['artists']

# Funciones de consulta sobre el catálogo

def sizeList(list):
    return model.sizeList(list)

def subList(list, pos, len):
    return model.subList(list, pos, len)

def sizeMap(map):
    return model.sizeMap(map)

def sortTracks(tracks):
    return model.sortTracks(tracks)

def sortTracksByAlbum(tracks):
    return model.sortTracksByAlbum(tracks)

#==========================================
# Get info functions
#==========================================

def getAlbumsYear(catalog, year):
    return model.getAlbumsByYear(catalog, year)

def getAlbumsByArtist(catalog, artist_id):
    return model.getAlbumsByArtist(catalog, artist_id)

def getAlbumById(catalog, id):
    return model.getAlbumById(catalog, id)

def getArtistsByPopularity(catalog, popularity):
    return model.getArtistsByPopularity(catalog, popularity)

def getArtistName(catalog, id):
    return model.getArtistName(catalog, id)

def getAlbumsAvailable(albums, country_code):
    return model.getAlbumsAvailable(albums, country_code)

def getTracksByArtist(catalog, artist_id, country_code):
    return model.getTracksByArtist(catalog, artist_id, country_code)

def getTracksByPopularity(catalog, popularity):
    return model.getTracksByPopularity(catalog, popularity)

def getTracksByAlbum(catalog, album_id):
    return model.getTracksByAlbum(catalog, album_id)

def getTrackName(catalog, id):
    return model.getTrackName(catalog, id)

def getAlbumName(catalog, id):
    return model.getAlbumName(catalog, id)

