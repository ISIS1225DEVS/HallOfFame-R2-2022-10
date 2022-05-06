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
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Sorting import mergesort as ms
assert cf
import datetime
import pycountry

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

def newCatalog():

    catalog = {"artists": None,
               "albums": None,
               "tracks": None,
               "genres": None,
               "popularityByTracks": None,
               "AlbumID": None,
               "ArtistID": None,
               "NameArtist":None}

    catalog["artists"] = mp.newMap(8000,
                                   maptype='PROBING',
                                   loadfactor=0.5)

    catalog["albums"] = mp.newMap(8000,
                                   maptype='PROBING',
                                   loadfactor=0.5)

    catalog["tracks"] = mp.newMap(8000,
                                   maptype='PROBING',
                                   loadfactor=0.5)

    catalog["genres"] = mp.newMap(8000,
                                   maptype='PROBING',
                                   loadfactor=0.5)
    
    catalog["album_year"] = mp.newMap(8000,
                                   maptype='PROBING',
                                   loadfactor=0.5)

    catalog["artist_popularity"] = mp.newMap(8000,
                                   maptype='PROBING',
                                   loadfactor=0.5)

    catalog["artists_name"] = mp.newMap(8000,
                                   maptype='PROBING',
                                   loadfactor=0.5)

    catalog["album_artist"] = mp.newMap(8000,
                                   maptype='PROBING',
                                   loadfactor=0.5)

    catalog["track_album"] = mp.newMap(8000,
                                   maptype='PROBING',
                                   loadfactor=0.5)

     #CAMBIOS ANDERSON                              
    catalog["popularityByTracks"] =mp.newMap(100,
                                   maptype='PROBING',
                                   loadfactor=0.5)
    catalog["AlbumID"] =mp.newMap(500,
                                   maptype='PROBING',
                                   loadfactor=0.5)
    catalog["ArtistID"] =mp.newMap(500,
                                   maptype='PROBING',
                                   loadfactor=0.5)
    catalog["NameArtist"] =mp.newMap(500,
                                   maptype='PROBING',
                                   loadfactor=0.5)   

    catalog["artists_position"] = mp.newMap(8000,
                                   maptype='PROBING',
                                   loadfactor=0.5)

    catalog["albums_position"] = mp.newMap(8000,
                                   maptype='PROBING',
                                   loadfactor=0.5)

    catalog["tracks_position"] = mp.newMap(8000,
                                   maptype='PROBING',
                                   loadfactor=0.5)

    return catalog

# Funciones para agregar informacion al catalogo

def addArtist(catalog, artist):
    mp.put(catalog["artists"], artist["id"], artist)
    mp.put(catalog["genres"], artist["genres"], artist)
    mp.put(catalog["artists_name"], artist["name"], artist)
    
    popularity = artist["artist_popularity"]
    if not mp.contains(catalog["artist_popularity"], popularity):
        list = lt.newList(datastructure="ARRAY_LIST")
        lt.addLast(list, artist)
        mp.put(catalog["artist_popularity"], popularity, list)

    else:
        entry = mp.get(catalog["artist_popularity"], popularity)
        list = me.getValue(entry)
        if artist not in list["elements"]:
            lt.addLast(list, artist)
            mp.put(catalog["artist_popularity"], popularity, list) 

    #CAMBIOS ANDERSON
    InfoArtist = newArtist()
    InfoArtist["artist"] = artist
    mp.put(catalog["ArtistID"], artist["id"], InfoArtist)
    mp.put(catalog["NameArtist"], artist["name"].upper(), artist["id"])

    mp.put(catalog["artists_position"], mp.size(catalog["artists_position"])+1, artist)


def addAlbum(catalog, album):

    mp.put(catalog["albums"], album["id"], album)
    mp.put(catalog["AlbumID"], album["id"], album)

    if album["release_date_precision"] == "day":
        fecha = datetime.datetime.strptime(album["release_date"], "%Y-%m-%d")
        year = int(fecha.year)

    elif album["release_date_precision"] == "year":
        year = int(album["release_date"])

    elif album["release_date_precision"] == "month":
        fecha1 = datetime.datetime.strptime(album["release_date"], "%b-%y")
        year = int(fecha1.year)

    if not mp.contains(catalog["album_year"], year):
        list = lt.newList(datastructure="ARRAY_LIST")
        lt.addLast(list, album)
        mp.put(catalog["album_year"], year, list)

    else:
        entry = mp.get(catalog["album_year"], year)
        list = me.getValue(entry)
        if album not in list["elements"]:
            lt.addLast(list, album)
            mp.put(catalog["album_year"], year, list)   

    artist_id = album["artist_id"]
    if not mp.contains(catalog["album_artist"], artist_id):
        list = lt.newList(datastructure="ARRAY_LIST")
        lt.addLast(list, album)
        mp.put(catalog["album_artist"], artist_id, list)

    else:
        entry = mp.get(catalog["album_artist"], artist_id)
        list = me.getValue(entry)
        if album not in list["elements"]:
            lt.addLast(list, album)
            mp.put(catalog["album_artist"], artist_id, list) 

    mp.put(catalog["albums_position"], mp.size(catalog["albums_position"])+1, album)     

def addTrack(catalog, track):
    mp.put(catalog["tracks"], track["id"], track)

    album_id = track["album_id"]
    if not mp.contains(catalog["track_album"], album_id):
        list = lt.newList(datastructure="ARRAY_LIST")
        lt.addLast(list, track)
        mp.put(catalog["track_album"], album_id, list)

    else:
        entry = mp.get(catalog["track_album"], album_id)
        list = me.getValue(entry)
        if track not in list["elements"]:
            lt.addLast(list, track)
            mp.put(catalog["track_album"], album_id, list) 
    
    mp.put(catalog["tracks_position"], mp.size(catalog["tracks_position"])+1, track)

    addTrackByPopularity(catalog, track)
    listID = str(track["artists_id"])
    artists = listID.replace("[","")
    artists = listID.replace("]","")
    artists = listID.replace("'","")
    Lartists = artists.split(", ")
    for artist in Lartists:
        b = artist.replace("[","")
        b = artist.replace("]","")
        addTrackArtist(catalog, b.strip(), track) 

def addTrackArtist(catalog, artistID, track):
    c =artistID.replace("]","")
    c= artistID.replace("[","")
    ArtistMap = catalog["ArtistID"]
    existArtist = mp.contains(ArtistMap, c)
    if existArtist:
        entry = mp.get(ArtistMap, c)
        valores = me.getValue(entry)
        ListTracks = valores["Tracks"]
    else: 
        valores = newArtist()
        ListTracks = valores["Tracks"]
        mp.put(ArtistMap, c, valores)
    lt.addLast(ListTracks, track)

def newArtist():
    info = {"Tracks": None,
        "artist": None}
    info["Tracks"] = lt.newList()
    return info
def addTrackByPopularity(catalog, track):
    Popularity= catalog["popularityByTracks"]
    Npopularity = float(track["popularity"])
    existpopularity = mp.contains(Popularity, Npopularity)
    if not existpopularity:
        listTracks = newTrack()
        lt.addLast(listTracks, track)
        mp.put(catalog["popularityByTracks"],Npopularity, listTracks)

    else:
        entry = mp.get(Popularity,Npopularity)
        listTracks = me.getValue(entry)
        if track not in listTracks["elements"]:
            lt.addLast(listTracks, track)
            mp.put(catalog["popularityByTracks"], Npopularity, listTracks)
        
        

def newTrack():
    Track= lt.newList("ARRAY_LIST")
    return Track

# Funciones para creacion de datos

# Funciones de consulta

def artistsSize(catalog):
    return mp.size(catalog['artists'])

def albumsSize(catalog):
    return mp.size(catalog['albums'])

def tracksSize(catalog):
    return mp.size(catalog['tracks'])

def genresSize(catalog):
    return mp.size(catalog['genres'])

def albumyearSize(catalog):
    return mp.size(catalog["album_year"])

def artistpopularitySize(catalog):
    return mp.size(catalog["artist_popularity"])

def albumartistSize(catalog):
    return mp.size(catalog["album_artist"])

def artistsnameSize(catalog):
    return mp.size(catalog["artists_name"])

def trackalbumSize(catalog):
    return mp.size(catalog["track_album"])

def getFirstTracks(catalog):

    first = me.getValue(mp.get(catalog["tracks_position"], 1))
    second = me.getValue(mp.get(catalog["tracks_position"], 2))
    third = me.getValue(mp.get(catalog["tracks_position"], 3))
    fourth = me.getValue(mp.get(catalog["tracks_position"], mp.size(catalog["tracks_position"])-2))
    fifth = me.getValue(mp.get(catalog["tracks_position"], mp.size(catalog["tracks_position"])-1))
    last = me.getValue(mp.get(catalog["tracks_position"], mp.size(catalog["tracks_position"])))

    
    album_id = first["album_id"]
    entryalbum1 = mp.get(catalog["albums"], album_id)
    album1 = "Unknown"
    if entryalbum1 != None:
        valuealbum1 = me.getValue(entryalbum1)
        album1 = valuealbum1["name"]

    listadelistas = []
    lista1 = [first["name"], first["popularity"], album1, first["disc_number"], first["track_number"],first["duration_ms"]]
    listadelistas.append(lista1)

    album_id = second["album_id"]
    entryalbum1 = mp.get(catalog["albums"], album_id)
    album1 = "Unknown"
    if entryalbum1 != None:
        valuealbum1 = me.getValue(entryalbum1)
        album1 = valuealbum1["name"]

    lista2 = [second["name"], second["popularity"], album1, second["disc_number"], second["track_number"], second["duration_ms"]]
    listadelistas.append(lista2)

    album_id = third["album_id"]
    entryalbum1 = mp.get(catalog["albums"], album_id)
    album1 = "Unknown"
    if entryalbum1 != None:
        valuealbum1 = me.getValue(entryalbum1)
        album1 = valuealbum1["name"]

    lista3 = [third["name"], third["popularity"], album1, third["disc_number"], third["track_number"], third["duration_ms"]]
    listadelistas.append(lista3)

    album_id = fourth["album_id"]
    entryalbum1 = mp.get(catalog["albums"], album_id)
    album1 = "Unknown"
    if entryalbum1 != None:
        valuealbum1 = me.getValue(entryalbum1)
        album1 = valuealbum1["name"]

    lista4 = [fourth["name"], fourth["popularity"], album1, fourth["disc_number"], fourth["track_number"], fourth["duration_ms"]]
    listadelistas.append(lista4)

    album_id = fifth["album_id"]
    entryalbum1 = mp.get(catalog["albums"], album_id)
    album1 = "Unknown"
    if entryalbum1 != None:
        valuealbum1 = me.getValue(entryalbum1)
        album1 = valuealbum1["name"]

    lista5 = [fifth["name"], fifth["popularity"], album1, fifth["disc_number"], fifth["track_number"], fifth["duration_ms"]]
    listadelistas.append(lista5)

    album_id = last["album_id"]
    entryalbum1 = mp.get(catalog["albums"], album_id)
    album1 = "Unknown"
    if entryalbum1 != None:
        valuealbum1 = me.getValue(entryalbum1)
        album1 = valuealbum1["name"]

    lista6 = [last["name"], last["popularity"], album1, last["disc_number"], last["track_number"], last["duration_ms"]]
    listadelistas.append(lista6)

    return listadelistas

def getFirstAlbums(catalog):

    first = me.getValue(mp.get(catalog["albums_position"], 1))
    second = me.getValue(mp.get(catalog["albums_position"], 2))
    third = me.getValue(mp.get(catalog["albums_position"], 3))
    fourth = me.getValue(mp.get(catalog["albums_position"], mp.size(catalog["albums_position"])-2))
    fifth = me.getValue(mp.get(catalog["albums_position"], mp.size(catalog["albums_position"])-1))
    last = me.getValue(mp.get(catalog["albums_position"], mp.size(catalog["albums_position"])))

    
    artist_id1 = first["artist_id"]
    entryartist1 = mp.get(catalog["artists"], artist_id1)
    artist1 = "Unknown"
    if entryartist1 != None:
        valueartist1 = me.getValue(entryartist1)
        artist1 = valueartist1["name"]
    
    track_id = first["track_id"]
    entrytrack1 = mp.get(catalog["tracks"], track_id)
    track1 = "Unknown"
    if entrytrack1 != None:
        valuetrack1 = me.getValue(entrytrack1)
        track1 = valuetrack1["name"]

    listadelistas = []
    lista1 = [first["name"], first["release_date"], track1, artist1, first["total_tracks"], first["album_type"]]
    listadelistas.append(lista1)

    artist_id1 = second["artist_id"]
    entryartist1 = mp.get(catalog["artists"], artist_id1)
    artist1 = "Unknown"
    if entryartist1 != None:
        valueartist1 = me.getValue(entryartist1)
        artist1 = valueartist1["name"]
    
    track_id = second["track_id"]
    entrytrack1 = mp.get(catalog["tracks"], track_id)
    track1 = "Unknown"
    if entrytrack1 != None:
        valuetrack1 = me.getValue(entrytrack1)
        track1 = valuetrack1["name"]

    lista2 = [second["name"], second["release_date"], track1, artist1, second["total_tracks"], second["album_type"]]
    listadelistas.append(lista2)

    artist_id1 = third["artist_id"]
    entryartist1 = mp.get(catalog["artists"], artist_id1)
    artist1 = "Unknown"
    if entryartist1 != None:
        valueartist1 = me.getValue(entryartist1)
        artist1 = valueartist1["name"]

    track_id = third["track_id"]
    entrytrack1 = mp.get(catalog["tracks"], track_id)
    track1 = "Unknown"
    if entrytrack1 != None:
        valuetrack1 = me.getValue(entrytrack1)
        track1 = valuetrack1["name"]

    lista3 = [third["name"], third["release_date"], track1, artist1, third["total_tracks"], third["album_type"]]
    listadelistas.append(lista3)

    artist_id1 = fourth["artist_id"]
    entryartist1 = mp.get(catalog["artists"], artist_id1)
    artist1 = "Unknown"
    if entryartist1 != None:
        valueartist1 = me.getValue(entryartist1)
        artist1 = valueartist1["name"]

    track_id = fourth["track_id"]
    entrytrack1 = mp.get(catalog["tracks"], track_id)
    track1 = "Unknown"
    if entrytrack1 != None:
        valuetrack1 = me.getValue(entrytrack1)
        track1 = valuetrack1["name"]

    lista4 = [fourth["name"], fourth["release_date"], track1, artist1, fourth["total_tracks"], fourth["album_type"]]
    listadelistas.append(lista4)

    artist_id1 = fifth["artist_id"]
    entryartist1 = mp.get(catalog["artists"], artist_id1)
    artist1 = "Unknown"
    if entryartist1 != None:
        valueartist1 = me.getValue(entryartist1)
        artist1 = valueartist1["name"]

    track_id = fifth["track_id"]
    entrytrack1 = mp.get(catalog["tracks"], track_id)
    track1 = "Unknown"
    if entrytrack1 != None:
        valuetrack1 = me.getValue(entrytrack1)
        track1 = valuetrack1["name"]

    lista5 = [fifth["name"], fifth["release_date"], track1, artist1, fifth["total_tracks"], fifth["album_type"]]
    listadelistas.append(lista5)

    artist_id1 = last["artist_id"]
    entryartist1 = mp.get(catalog["artists"], artist_id1)
    artist1 = "Unknown"
    if entryartist1 != None:
        valueartist1 = me.getValue(entryartist1)
        artist1 = valueartist1["name"]

    track_id = last["track_id"]
    entrytrack1 = mp.get(catalog["tracks"], track_id)
    track1 = "Unknown"
    if entrytrack1 != None:
        valuetrack1 = me.getValue(entrytrack1)
        track1 = valuetrack1["name"]

    lista6 = [last["name"], last["release_date"], track1, artist1, last["total_tracks"], last["album_type"]]
    listadelistas.append(lista6)

    return listadelistas

def getFirstArtists(catalog):

    first = me.getValue(mp.get(catalog["artists_position"], 1))
    second = me.getValue(mp.get(catalog["artists_position"], 2))
    third = me.getValue(mp.get(catalog["artists_position"], 3))
    fourth = me.getValue(mp.get(catalog["artists_position"], mp.size(catalog["artists_position"])-2))
    fifth = me.getValue(mp.get(catalog["artists_position"], mp.size(catalog["artists_position"])-1))
    last = me.getValue(mp.get(catalog["artists_position"], mp.size(catalog["artists_position"])))

    
    track_id = first["track_id"]
    entrytrack1 = mp.get(catalog["tracks"], track_id)
    track1 = "Unknown"
    if entrytrack1 != None:
        valuetrack1 = me.getValue(entrytrack1)
        track1 = valuetrack1["name"]

    listadelistas = []
    lista1 = [first["name"], first["artist_popularity"], first["followers"], track1, first["genres"]]
    listadelistas.append(lista1)

    track_id = second["track_id"]
    entrytrack1 = mp.get(catalog["tracks"], track_id)
    track1 = "Unknown"
    if entrytrack1 != None:
        valuetrack1 = me.getValue(entrytrack1)
        track1 = valuetrack1["name"]

    lista2 = [second["name"], second["artist_popularity"], second["followers"], track1, second["genres"]]
    listadelistas.append(lista2)

    track_id = third["track_id"]
    entrytrack1 = mp.get(catalog["tracks"], track_id)
    track1 = "Unknown"
    if entrytrack1 != None:
        valuetrack1 = me.getValue(entrytrack1)
        track1 = valuetrack1["name"]

    lista3 = [third["name"], third["artist_popularity"], third["followers"], track1, third["genres"]]
    listadelistas.append(lista3)

    track_id = fourth["track_id"]
    entrytrack1 = mp.get(catalog["tracks"], track_id)
    track1 = "Unknown"
    if entrytrack1 != None:
        valuetrack1 = me.getValue(entrytrack1)
        track1 = valuetrack1["name"]

    lista4 = [fourth["name"], fourth["artist_popularity"], fourth["followers"], track1, fourth["genres"]]
    listadelistas.append(lista4)

    track_id = fifth["track_id"]
    entrytrack1 = mp.get(catalog["tracks"], track_id)
    track1 = "Unknown"
    if entrytrack1 != None:
        valuetrack1 = me.getValue(entrytrack1)
        track1 = valuetrack1["name"]

    lista5 = [fifth["name"], fifth["artist_popularity"], fifth["followers"], track1, fifth["genres"]]
    listadelistas.append(lista5)

    track_id = last["track_id"]
    entrytrack1 = mp.get(catalog["tracks"], track_id)
    track1 = "Unknown"
    if entrytrack1 != None:
        valuetrack1 = me.getValue(entrytrack1)
        track1 = valuetrack1["name"]

    lista6 = [last["name"], last["artist_popularity"], last["followers"], track1, last["genres"]]
    listadelistas.append(lista6)

    return listadelistas



def getElementsBySize(catalog, size):

    if size >= 6:
        primero = lt.getElement(catalog, 1)
        segundo = lt.getElement(catalog, 2)
        tercero = lt.getElement(catalog, 3)
        antepenultimo = lt.getElement(catalog, size-2)
        penultimo = lt.getElement(catalog, size-1)
        ultimo = lt.getElement(catalog, size)
        return primero, segundo, tercero, antepenultimo, penultimo, ultimo
    else:
        if size == 5:
            primero = lt.getElement(catalog, 1)
            segundo = lt.getElement(catalog, 2)
            tercero = lt.getElement(catalog, 3)
            penultimo = lt.getElement(catalog, size-1)
            ultimo = lt.getElement(catalog, size)
            return primero, segundo, tercero, penultimo, ultimo
        elif size == 4:
            primero = lt.getElement(catalog, 1)
            segundo = lt.getElement(catalog, 2)
            tercero = lt.getElement(catalog, 3)
            ultimo = lt.getElement(catalog, size)
            return primero, segundo, tercero, ultimo
        elif size == 3:
            primero = lt.getElement(catalog, 1)
            segundo = lt.getElement(catalog, 2)
            tercero = lt.getElement(catalog, 3)
            return primero, segundo, tercero
        elif size == 2:
            primero = lt.getElement(catalog, 1)
            segundo = lt.getElement(catalog, 2)
            return primero, segundo
        elif size == 1:
            primero = lt.getElement(catalog, 1)
            return primero
        else: 
            return None

def getTracksInfo(catalog, Track, n):
    name = Track["name"]
    popularity = Track["popularity"]
    duration = str(float(Track["duration_ms"])  //60000)
    if Track["lyrics"] == "-99":
        lyrics = "Letra de la canción no disponible..."
    else:
        lyrics = Track["lyrics"][:50] + "..."

    existAlbum = mp.contains(catalog["AlbumID"], Track["album_id"])
    if existAlbum:
        entry= mp.get(catalog["AlbumID"], Track["album_id"])
        Album =me.getValue(entry)
        nameAlbum = Album["name"]
        if n == 6 or n == 4:
            Date = Album["release_date"]
    else: 
        nameAlbum = "No se encontro el album de la canción"
    
    ListArtist = []
    ATracks = str(Track["artists_id"])
    BTracks = ATracks.replace("[","")
    BTracks = BTracks.replace("]","")
    BTracks = BTracks.replace("'","")
    ListArtistID = BTracks.split(", ")
    for i in ListArtistID:
        existArtistID = mp.contains(catalog["ArtistID"], i)
        if existArtistID:
            entry1 = mp.get(catalog["ArtistID"], i)
            InfoArtist = me.getValue(entry1)
            artist = InfoArtist["artist"]
            Name = artist["name"]   
        else:
            Name = "No hay informacion del Artista de ID: {}".format(i)
        ListArtist.append(Name)
    ArtistName = str(ListArtist)
    ArtistName = ArtistName.replace("[","")
    ArtistName =  ArtistName.replace("]","")
    ArtistName =  ArtistName.replace("'","")
    
    if n ==3:
        link1 = Track["href"]
        return  name, nameAlbum, ArtistName, popularity,  duration, link1, lyrics
    elif n == 4:
        link = Track["preview_url"]
        return name, nameAlbum, Date, ArtistName, duration, popularity, link, lyrics
    elif n == 6:
        Ncountries = 0
        Countries = str(Track["available_markets"])
        Countries1 =Countries.replace("[","")
        Countries1 =Countries1.replace("]","")
        Countries1 = Countries1.replace("'","")
        Countries2 = Countries1.split(", ")
        for i in Countries2:
            Ncountries += 1
        return name, nameAlbum, Date, ArtistName, str(Ncountries),popularity, duration, lyrics

        
def getTracksByCountry(list, country_code):
    Tracks = lt.newList()
    for i in lt.iterator(list):
        j = str(i["available_markets"])
        h = j.replace("[","")
        h = h.replace("]","")
        h = h.replace("'","")
        h = h.split(", ")
        if country_code in h:
            lt.addLast(Tracks, i)
    return Tracks

def getNoalbums(list):
    totalalbums = mp.newMap(100,
                                   maptype='PROBING',
                                   loadfactor=0.9)
    for i in lt.iterator(list):
        mp.put(totalalbums, i["album_id"], "1")
    N= mp.size(totalalbums)
    return str(N)
#----------------------------------------------------------------------------------------
#                     FUNCIONES DE REQUERIMIENTOS 
# -------------------------------------------------------------------------------------------


def AlbumsinCertainYear(year, catalog):

    entry = mp.get(catalog["album_year"], year)
    AlbumsinCertainYear = me.getValue(entry)
    size = lt.size(AlbumsinCertainYear)
    sortAlbumsByAlphOrder(AlbumsinCertainYear)
 
    primero_SL = lt.getElement(AlbumsinCertainYear, 1)
    segundo_SL = lt.getElement(AlbumsinCertainYear, 2)
    tercero_SL = lt.getElement(AlbumsinCertainYear, 3)
    antepenultimo_SL = lt.getElement(AlbumsinCertainYear, lt.size(AlbumsinCertainYear)-2)
    penultimo_SL = lt.getElement(AlbumsinCertainYear, lt.size(AlbumsinCertainYear)-1)
    ultimo_SL = lt.getElement(AlbumsinCertainYear, lt.size(AlbumsinCertainYear))

    artist_id1 = primero_SL["artist_id"]
    entryartist1 = mp.get(catalog["artists"], artist_id1)
    artist1 = "Unknown"
    if entryartist1 != None:
        valueartist1 = me.getValue(entryartist1)
        artist1 = valueartist1["name"]

    artist_id2 = segundo_SL["artist_id"]
    entryartist2 = mp.get(catalog["artists"], artist_id2)
    artist2 = "Unknown"
    if entryartist2 != None:
        valueartist2 = me.getValue(entryartist2)
        artist2 = valueartist2["name"]

    artist_id3 = tercero_SL["artist_id"]
    entryartist3 = mp.get(catalog["artists"], artist_id3)
    artist3 = "Unknown"
    if entryartist3 != None:
        valueartist3 = me.getValue(entryartist3)
        artist3 = valueartist3["name"]

    artist_id4 = antepenultimo_SL["artist_id"]
    entryartist4 = mp.get(catalog["artists"], artist_id4)
    artist4 = "Unknown"
    if entryartist4 != None:
        valueartist4 = me.getValue(entryartist4)
        artist4 = valueartist4["name"]

    artist_id5 = penultimo_SL["artist_id"]
    entryartist5 = mp.get(catalog["artists"], artist_id5)
    artist5 = "Unknown"
    if entryartist5 != None:
        valueartist5 = me.getValue(entryartist5)
        artist5 = valueartist5["name"]

    artist_id6 = ultimo_SL["artist_id"]
    entryartist6 = mp.get(catalog["artists"], artist_id6)
    artist6 = "Unknown"
    if entryartist6 != None:
        valueartist6 = me.getValue(entryartist6)
        artist6 = valueartist6["name"]

    primero = [primero_SL["name"], primero_SL["release_date"], primero_SL["album_type"],
                 artist1, primero_SL["total_tracks"]]
    segundo = [segundo_SL["name"], segundo_SL["release_date"], segundo_SL["album_type"],
                 artist2, segundo_SL["total_tracks"]]
    tercero = [tercero_SL["name"], tercero_SL["release_date"], tercero_SL["album_type"],
                 artist3, tercero_SL["total_tracks"]]
    antepenultimo = [antepenultimo_SL["name"], antepenultimo_SL["release_date"], antepenultimo_SL["album_type"],
                 artist4, antepenultimo_SL["total_tracks"]]
    penultimo = [penultimo_SL["name"], penultimo_SL["release_date"], penultimo_SL["album_type"],
                 artist5, penultimo_SL["total_tracks"]]
    ultimo = [ultimo_SL["name"], ultimo_SL["release_date"], ultimo_SL["album_type"],
                 artist6, ultimo_SL["total_tracks"]]

    return primero, segundo, tercero, antepenultimo, penultimo, ultimo, size
    

def ArtistswithCertainPopularity(popularity, catalog):

    popularity = str(popularity)
    entry = mp.get(catalog["artist_popularity"], popularity)
    ArtistsPopularity = me.getValue(entry)
    size = lt.size(ArtistsPopularity)
    sortArtistByPopularity(ArtistsPopularity)

    if lt.getElement(ArtistsPopularity, 1) != None:
        primero_TL = lt.getElement(ArtistsPopularity, 1)
        track_id = primero_TL["track_id"]
        entrytrack1 = mp.get(catalog["tracks"], track_id)
        track1 = "Unknown"
        if entrytrack1 != None:
            valuetrack1 = me.getValue(entrytrack1)
            track1 = valuetrack1["name"]

        primero = [primero_TL["name"], primero_TL["artist_popularity"], primero_TL["followers"],
                 primero_TL["genres"], track1]

    if lt.getElement(ArtistsPopularity, 2) != None:
        segundo_TL = lt.getElement(ArtistsPopularity, 2)
        entrytrack2 = mp.get(catalog["tracks"], segundo_TL["track_id"])
        track2 = "Unknown"
        if entrytrack2 != None:
            valuetrack2 = me.getValue(entrytrack2)
            track2 = valuetrack2["name"]

        segundo = [segundo_TL["name"], segundo_TL["artist_popularity"], segundo_TL["followers"],
                 segundo_TL["genres"], track2]

    if lt.getElement(ArtistsPopularity, 3) != None:
        tercero_TL = lt.getElement(ArtistsPopularity, 3)   
        entrytrack3 = mp.get(catalog["tracks"], tercero_TL["track_id"])
        track3 = "Unknown"
        if entrytrack3 != None:
            valuetrack3 = me.getValue(entrytrack3)
            track3 = valuetrack3["name"]

        tercero = [tercero_TL["name"], tercero_TL["artist_popularity"], tercero_TL["followers"],
                 tercero_TL["genres"], track3]

    if lt.getElement(ArtistsPopularity, lt.size(ArtistsPopularity)-2) != None and lt.size(ArtistsPopularity) > 5:
        antepenultimo_TL = lt.getElement(ArtistsPopularity, lt.size(ArtistsPopularity)-2)
        entrytrack4 = mp.get(catalog["tracks"], antepenultimo_TL["track_id"])
        track4 = "Unknown"
        if entrytrack4 != None:
            valuetrack4 = me.getValue(entrytrack4)
            track4 = valuetrack4["name"]

        antepenultimo = [antepenultimo_TL["name"], antepenultimo_TL["artist_popularity"], antepenultimo_TL["followers"],
                 antepenultimo_TL["genres"], track4]

    if lt.getElement(ArtistsPopularity, lt.size(ArtistsPopularity)-1) != None and lt.size(ArtistsPopularity) > 4:
        penultimo_TL = lt.getElement(ArtistsPopularity, lt.size(ArtistsPopularity)-1)
        entrytrack5 = mp.get(catalog["tracks"], penultimo_TL["track_id"])
        track5 = "Unknown"
        if entrytrack5 != None:
            valuetrack5 = me.getValue(entrytrack5)
            track5 = valuetrack5["name"]

        penultimo = [penultimo_TL["name"], penultimo_TL["artist_popularity"], penultimo_TL["followers"],
                 penultimo_TL["genres"], track5]

    if lt.getElement(ArtistsPopularity, lt.size(ArtistsPopularity)) != None and lt.size(ArtistsPopularity) > 3:
        ultimo_TL = lt.getElement(ArtistsPopularity, lt.size(ArtistsPopularity)) 
        entrytrack6 = mp.get(catalog["tracks"], ultimo_TL["track_id"])
        track6 = "Unknown"
        if entrytrack6 != None:
            valuetrack6 = me.getValue(entrytrack6) 
            track6 = valuetrack6["name"]

        ultimo = [ultimo_TL["name"], ultimo_TL["artist_popularity"], ultimo_TL["followers"],
                 ultimo_TL["genres"], track6]

    return primero, segundo, tercero, antepenultimo, penultimo, ultimo, size
    

def TracksByPopularity(popularity, catalog):
    PopularityMap = catalog["popularityByTracks"]
    existpopularity = mp.contains(PopularityMap, popularity)
    if existpopularity:
        entry9 = mp.get(PopularityMap, popularity)
        inordered= me.getValue(entry9)
        listTracks = sortTracksByPopularity(inordered)
        NTracks = lt.size(listTracks)

        if NTracks >= 6:
            primero, segundo, tercero, antepenultimo, penultimo, ultimo = getElementsBySize(listTracks, NTracks)
            primero= getTracksInfo(catalog, primero,3)
            segundo = getTracksInfo(catalog, segundo,3)
            tercero = getTracksInfo(catalog, tercero,3)
            antepenultimo = getTracksInfo(catalog, antepenultimo,3)
            penultimo = getTracksInfo(catalog, penultimo, 3)
            ultimo = getTracksInfo(catalog, ultimo, 3)
            return  NTracks, primero, segundo, tercero, antepenultimo, penultimo, ultimo
        elif NTracks == 5:
            primero, segundo, tercero, penultimo, ultimo = getElementsBySize(listTracks, NTracks)
            primero= getTracksInfo(catalog, primero,3)
            segundo = getTracksInfo(catalog, segundo,3)
            tercero = getTracksInfo(catalog, tercero,3)
            penultimo = getTracksInfo(catalog, penultimo, 3)
            ultimo = getTracksInfo(catalog, ultimo, 3)
            return  NTracks, primero, segundo, tercero, penultimo, ultimo
        elif NTracks == 4:
            primero, segundo, tercero, ultimo = getElementsBySize(listTracks, NTracks)
            primero= getTracksInfo(catalog, primero,3)
            segundo = getTracksInfo(catalog, segundo,3)
            tercero = getTracksInfo(catalog, tercero,3)
            ultimo = getTracksInfo(catalog, ultimo, 3)
            return  NTracks, primero, segundo, tercero, ultimo
        elif NTracks == 3:
            primero, segundo, tercero = getElementsBySize(listTracks, NTracks)
            primero= getTracksInfo(catalog, primero,3)
            segundo = getTracksInfo(catalog, segundo,3)
            tercero = getTracksInfo(catalog, tercero,3)
            return  NTracks, primero, segundo, tercero
        elif NTracks == 2:
            primero, segundo = getElementsBySize(listTracks, NTracks)
            primero= getTracksInfo(catalog, primero,3)
            segundo = getTracksInfo(catalog, segundo,3)
            return  NTracks, primero, segundo
        elif NTracks == 1:
            primero= getElementsBySize(listTracks, NTracks)
            primero= getTracksInfo(catalog, primero,3)
            return  NTracks, primero
        else:
            return None
    else: 
        return None

def MostPopularArtistSong(name, country, catalog):
    list_countries = pycountry.countries.search_fuzzy(str(country))
    country_code = list_countries[0]
    country_code = country_code.alpha_2
    exitsartist = mp.contains(catalog["NameArtist"], name.upper())
    if exitsartist:
        entry1 = mp.get(catalog["NameArtist"], name.upper())
        ArtistID  = me.getValue(entry1)
        exitsArtistID = mp.contains(catalog["ArtistID"], ArtistID)
        if exitsArtistID:
            entry2 = mp.get(catalog["ArtistID"], ArtistID)
            artist = me.getValue(entry2)
            tracks = artist["Tracks"]
            inordered = getTracksByCountry(tracks, country_code)
            TracksByCountry = sortTracksByPopularity(inordered)
            if not lt.isEmpty(TracksByCountry):
                Song = lt.getElement(TracksByCountry,1)
                PopularSong = getTracksInfo(catalog, Song, 4)
                NCanciones = lt.size(TracksByCountry)  
                Nalbums = getNoalbums(TracksByCountry)
                return country_code, NCanciones, Nalbums, PopularSong
        else:
            return None
    else:
        return None

def ArtistDiscography(name, catalog):

    entry = mp.get(catalog["artists_name"], name)
    ArtistInfo = me.getValue(entry)
    id = ArtistInfo["id"]
    entry = mp.get(catalog["album_artist"], id)
    AlbumsInfo = me.getValue(entry)
    sortAlbumsByRecentYear(AlbumsInfo)
    single_albums = 0
    compilation_albums = 0
    album_albums = 0
    total_albums = 0
    popular_tracks = lt.newList("ARRAY_LIST")
    Tracks = lt.newList("ARRAY_LIST")

    for i in lt.iterator(AlbumsInfo):

        if i["album_type"] == "single":
            single_albums += 1
        elif i["album_type"] == "compilation":
            compilation_albums += 1
        elif i["album_type"] == "album":
            album_albums += 1
        
        entry = mp.get(catalog["track_album"], i["id"])
        TracksInfo = me.getValue(entry)
        lt.addLast(Tracks, TracksInfo)

    for i in lt.iterator(Tracks):

        sortTracksByPopularity(i)
        lt.addLast(popular_tracks, lt.getElement(i, 1))

    total_albums = single_albums + compilation_albums + album_albums

    if lt.size(AlbumsInfo) >= 1 and lt.getElement(AlbumsInfo, 1) != None: 
        primero_TL = lt.getElement(AlbumsInfo, 1)

        primero = [primero_TL["release_date"], primero_TL["name"], primero_TL["total_tracks"],
             primero_TL["album_type"], name]

    if lt.size(AlbumsInfo) >= 2 and lt.getElement(AlbumsInfo, 2) != None:
        segundo_TL = lt.getElement(AlbumsInfo, 2)

        segundo = [segundo_TL["release_date"], segundo_TL["name"], segundo_TL["total_tracks"],
             segundo_TL["album_type"], name]

    if lt.size(AlbumsInfo) >= 3 and lt.getElement(AlbumsInfo, 3) != None:
        tercero_TL = lt.getElement(AlbumsInfo, 3)    

        tercero = [tercero_TL["release_date"], tercero_TL["name"], tercero_TL["total_tracks"],
             tercero_TL["album_type"], name]

    if lt.size(AlbumsInfo) >= 4 and lt.getElement(AlbumsInfo, lt.size(AlbumsInfo)-2) != None:
        antepenultimo_TL = lt.getElement(AlbumsInfo, lt.size(AlbumsInfo)-2)

        antepenultimo = [antepenultimo_TL["release_date"], antepenultimo_TL["name"], antepenultimo_TL["total_tracks"],
             antepenultimo_TL["album_type"], name]

    if lt.size(AlbumsInfo) >= 5 and lt.getElement(AlbumsInfo, lt.size(AlbumsInfo)-1) != None:
        penultimo_TL = lt.getElement(AlbumsInfo, lt.size(AlbumsInfo)-1)

        penultimo = [penultimo_TL["release_date"], penultimo_TL["name"], penultimo_TL["total_tracks"],
             penultimo_TL["album_type"], name]

    if lt.size(AlbumsInfo) >= 6 and lt.getElement(AlbumsInfo, lt.size(AlbumsInfo)) != None:
        ultimo_TL = lt.getElement(AlbumsInfo, lt.size(AlbumsInfo))   

        ultimo = [ultimo_TL["release_date"], ultimo_TL["name"], ultimo_TL["total_tracks"],
             ultimo_TL["album_type"], name]

    posicion_i = 1
    popular_songs = []

    for i in lt.iterator(popular_tracks):
        
        if posicion_i in [1,2,3, lt.size(popular_tracks)-2,lt.size(popular_tracks)-1, lt.size(popular_tracks)]:
            artistsintrack = []
            artists_id = str(i["artists_id"])
            artists_id = artists_id.replace("[","")
            artists_id = artists_id.replace("]","")
            artists_id = artists_id.replace("'","")
            list_artists_id = artists_id.split(", ")
            if i["lyrics"] == "-99":
                lyrics = "Letra de la canción no disponible..."
            else:
                lyrics = i["lyrics"][:50] + "..."
            
            for j in list_artists_id:
                entry = mp.get(catalog["artists"], j)
                value = me.getValue(entry)
                artistsintrack.append(value["name"])

            songs_data = [i["name"], str(artistsintrack), i["duration_ms"],
                i["popularity"], i["preview_url"], lyrics]
            popular_songs.append(songs_data)

        posicion_i += 1
    
    return single_albums, compilation_albums, album_albums, total_albums, primero, segundo, tercero, antepenultimo, penultimo, ultimo, popular_songs


def Bonus(name, country, top, catalog):
    list_countries = pycountry.countries.search_fuzzy(str(country))
    country_code = list_countries[0]
    country_code = country_code.alpha_2
    exitsartist = mp.contains(catalog["NameArtist"], name.upper())
    if exitsartist:
        entry1 = mp.get(catalog["NameArtist"], name.upper())
        ArtistID = me.getValue(entry1)
        exitsArtistID = mp.contains(catalog["ArtistID"], ArtistID)
        if exitsArtistID:
            entry2 = mp.get(catalog["ArtistID"], ArtistID)
            artist = me.getValue(entry2)
            Tracks = artist["Tracks"]
            inordered = getTracksByCountry(Tracks, country_code)
            ordered= sortTracksByPopularity(inordered)
            if lt.size(ordered) > top:
                TracksByCountry = lt.subList(ordered, 1, top)
            else:
                TracksByCountry = lt.subList(ordered, 1, lt.size(ordered))
            if not lt.isEmpty(TracksByCountry):
                SizeTracksByCountry  = lt.size(TracksByCountry)
                if SizeTracksByCountry >= 6:
                    primero, segundo, tercero, antepenultimo, penultimo, ultimo = getElementsBySize(TracksByCountry, SizeTracksByCountry)
                    primero= getTracksInfo(catalog, primero, 6)
                    segundo = getTracksInfo(catalog, segundo, 6)
                    tercero = getTracksInfo(catalog, tercero, 6)
                    antepenultimo = getTracksInfo(catalog, antepenultimo, 6)
                    penultimo = getTracksInfo(catalog, penultimo, 6)
                    ultimo = getTracksInfo(catalog, ultimo, 6)
                    return  SizeTracksByCountry, primero, segundo, tercero, antepenultimo, penultimo, ultimo
                elif SizeTracksByCountry == 5:
                    primero, segundo, tercero, penultimo, ultimo = getElementsBySize(TracksByCountry, SizeTracksByCountry)
                    primero= getTracksInfo(catalog, primero, 6)
                    segundo = getTracksInfo(catalog, segundo, 6)
                    tercero = getTracksInfo(catalog, tercero, 6)
                    penultimo = getTracksInfo(catalog, penultimo, 6)
                    ultimo = getTracksInfo(catalog, ultimo, 6)
                    return  SizeTracksByCountry, primero, segundo, tercero, penultimo, ultimo
                elif SizeTracksByCountry == 4:
                    primero, segundo, tercero, ultimo = getElementsBySize(TracksByCountry, SizeTracksByCountry)
                    primero= getTracksInfo(catalog, primero, 6)
                    segundo = getTracksInfo(catalog, segundo, 6)
                    tercero = getTracksInfo(catalog, tercero, 6)
                    ultimo = getTracksInfo(catalog, ultimo, 6)
                    return  SizeTracksByCountry, primero, segundo, tercero, ultimo
                elif SizeTracksByCountry == 3:
                    primero, segundo, tercero = getElementsBySize(TracksByCountry, SizeTracksByCountry)
                    primero= getTracksInfo(catalog, primero, 6)
                    segundo = getTracksInfo(catalog, segundo, 6)
                    tercero = getTracksInfo(catalog, tercero, 6)
                    return  SizeTracksByCountry, primero, segundo, tercero
                elif SizeTracksByCountry == 2:
                    primero, segundo = getElementsBySize(TracksByCountry, SizeTracksByCountry)
                    primero= getTracksInfo(catalog, primero, 6)
                    segundo = getTracksInfo(catalog, segundo, 6)
                    return  SizeTracksByCountry, primero, segundo
                elif SizeTracksByCountry == 1:
                    primero= getElementsBySize(TracksByCountry, SizeTracksByCountry)
                    primero= getTracksInfo(catalog, primero, 6)
                    return  SizeTracksByCountry, primero
                else:
                    return None
            else:
                return None
        else:
            return None
    else:
        return None

# Funciones utilizadas para comparar elementos dentro de una lista

def cmpGenresByName(keyname, genre):

    genreentry = me.getKey(genre)
    if (keyname == genreentry):
        return 0
    elif (keyname > genreentry):
        return 1
    else:
        return -1

def cmpAlbumsByYear(album1, album2):

    comparison = None

    if album1["release_date_precision"] == "day":
        fecha = datetime.datetime.strptime(album1["release_date"], "%Y-%m-%d")
        year1 = fecha.year

    elif album1["release_date_precision"] == "year":
        year1 = int(album1["release_date"])

    elif album1["release_date_precision"] == "month":
        fecha1 = datetime.datetime.strptime(album1["release_date"], "%b-%y")
        year1 = fecha1.year

    if album2["release_date_precision"] == "day":
        fecha2 = datetime.datetime.strptime(album2["release_date"], "%Y-%m-%d")
        year2 = fecha2.year

    elif album2["release_date_precision"] == "year":
        year2 = int(album2["release_date"])

    elif album2["release_date_precision"] == "month":
        fecha2 = datetime.datetime.strptime(album2["release_date"], "%b-%y")
        year2 = fecha2.year

    if year1 < year2:
        comparison = True
    else: 
        comparison = False

    return comparison

def cmpAlbumsByRecentYear(album1, album2):

    comparison = None

    if album1["release_date_precision"] == "day":
        fecha = datetime.datetime.strptime(album1["release_date"], "%Y-%m-%d")
        year1 = fecha.year

    elif album1["release_date_precision"] == "year":
        year1 = int(album1["release_date"])
    
    elif album1["release_date_precision"] == "month":
        fecha1 = datetime.datetime.strptime(album1["release_date"], "%b-%y")
        year1 = fecha1.year

    if album2["release_date_precision"] == "day":
        fecha2 = datetime.datetime.strptime(album2["release_date"], "%Y-%m-%d")
        year2 = fecha2.year

    elif album2["release_date_precision"] == "year":
        year2 = int(album2["release_date"])

    elif album2["release_date_precision"] == "month":
        fecha2 = datetime.datetime.strptime(album2["release_date"], "%b-%y")
        year2 = fecha2.year

    if int(year1) >= int(year2):
        comparison = True

    else: 
        comparison = False

    return comparison


def cmpAlbumsByAlphOrder(album1, album2):

    comparison = None

    if album1["name"] < album2["name"]:
        comparison = True
    
    else: 
        comparison = False

    return comparison

def cmpArtistByPopularity(artist1, artist2):

    comparison = None

    if float(artist1["followers"]) > float(artist2["followers"]):
        comparison = True

    elif float(artist1["followers"]) == float(artist2["followers"]) and artist1["name"] < artist2["name"]:
        comparison = True
    
    else: 
        comparison = False

    return comparison

def cmpTracksByPopularity(track1, track2):

    comparison = None

    if float(track1["popularity"]) > float(track2["popularity"]):
        comparison = True

    elif float(track1["duration_ms"]) > float(track2["duration_ms"]) and float(track1["popularity"]) == float(track2["popularity"]):
        comparison = True

    elif track1["name"] > track2["name"] and float(track1["popularity"]) == float(track2["popularity"]
             and float(track1["duration_ms"])) == float(track2["duration_ms"]):
        comparison == True

    else: 
        comparison = False

    return comparison


def cmpTracksByPopularity(track1, track2):

    comparison = None

    if float(track1["popularity"]) > float(track2["popularity"]):
        comparison = True

    elif float(track1["duration_ms"]) > float(track2["duration_ms"]) and float(track1["popularity"]) == float(track2["popularity"]):
        comparison = True

    elif track1["name"] > track2["name"] and float(track1["popularity"]) == float(track2["popularity"]
             and float(track1["duration_ms"])) == float(track2["duration_ms"]):
        comparison == True

    else: 
        comparison = False

    return comparison
# Funciones de ordenamiento

def sortAlbumsByRecentYear(catalog):
    ms.sort(catalog, cmpAlbumsByYear)

def sortAlbumsByAlphOrder(catalog):

    ms.sort(catalog, cmpAlbumsByAlphOrder)

def sortArtistByPopularity(catalog):

    ms.sort(catalog, cmpArtistByPopularity)

def sortAlbumsByRecentYear(catalog):

    ms.sort(catalog, cmpAlbumsByRecentYear)

def sortTracksByPopularity(catalog):

    ms.sort(catalog, cmpTracksByPopularity)

def sortTracksByPopularity(catalog):
    return ms.sort(catalog, cmpTracksByPopularity)
