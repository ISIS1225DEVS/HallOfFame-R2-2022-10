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
from DISClib.Algorithms.Sorting import mergesort as sa
assert cf
from datetime import datetime

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# =======================
# Construccion de modelos
# =======================

def newCatalog():
    catalog = {'albums': None,
                'songs': None,
                'artists': None,
                'id_artists': None,
                'id_albums': None,
                'years': None,
               'popularity': None,
               'artists_name': None,
               'genres': None}

    catalog['albums'] = lt.newList('ARRAY_LIST')
    catalog['songs'] = lt.newList('ARRAY_LIST')
    catalog['artists'] = lt.newList('ARRAY_LIST')

    catalog['id_artists'] = mp.newMap(56126,
                                   maptype='CHAINING',
                                   loadfactor=4,
                                   comparefunction=cmpMapName)
    catalog['id_albums'] = mp.newMap(75503,
                                   maptype='CHAINING',
                                   loadfactor=4,
                                   comparefunction=cmpMapName)
    catalog['years'] = mp.newMap(120,
                                   maptype='PROBING',
                                   loadfactor=0.5,
                                   comparefunction=cmpMapInt)
    catalog['popularity'] = mp.newMap(101,
                                   maptype='PROBING',
                                   loadfactor=0.5,
                                   comparefunction=cmpMapInt)
    catalog['artists_name'] = mp.newMap(56126,
                                maptype='CHAINING',
                                loadfactor=4,
                                comparefunction=cmpMapName)             
    return catalog

def createCountryMap():
    CountryMap = mp.newMap(79,
                            maptype='PROBING',
                            loadfactor=0.5,
                            comparefunction=cmpMapName)
    return CountryMap

# ============================
# Funciones para remover mapas
# ============================

def removeMapIdAlbums(catalog):
    catalog['id_albums'] = None

def removeMapIdArtists(catalog):
    catalog['id_artists'] = None

# ==============================
# Funciones de creación de datos
# ==============================

def newArtist(id):
    artist = {'id': id, 'artist_popularity': 0, 'genres': lt.newList('SINGLE_LINKED'), 'followers': 0, 'track_id': None, 
        'name': None, 'relevant_song_name': None, 'albums': lt.newList('ARRAY_LIST'), 'album_single': 0, 
        'album_compilation': 0, 'album_typealbum': 0}
    return artist

def newAlbum(id):
    album = {'id': id, 'release_date': None, 'available_markets': lt.newList('ARRAY_LIST'), 'total_tracks': 0, 
        'album_type': None, 'name': None, 'artist_id': None, 'external_urls': None , 'artist_album_name': None, 
        'songs': lt.newList('ARRAY_LIST')}
    return album

def newSong(id):
    song = {'id': id, 'lyrics': None, 'album_id': None, 'artists_id': None, 'disc_number': 0, 'popularity': 0,
        'available_markets': lt.newList('ARRAY_LIST'), 'available_markets_num': 0, 'track_number': 0, 
        'name': None, 'duration_ms': 0, 'href': None, 'preview_url': None , 'release_date': None, 
        'album_name': None, 'album_type': None, 'artist_names': lt.newList('ARRAY_LIST')}
    return song

# ==============================
# Funciones para filtro de datos
# ==============================

def FilterArtist(Data):
    artist = newArtist(Data['id'])
    artist['artist_popularity'] =  int(float(Data['artist_popularity']))
    artist['genres'] = ArrangeLst(Data['genres'])
    artist['followers'] = int(float(Data['followers']))
    artist['track_id'] = Data['track_id']
    artist['name'] = Data['name'].strip('""')
    return artist

def FilterAlbum(Data):
    album = newAlbum(Data['id'])
    album['release_date'] = DateFix(Data['release_date'])
    album['available_markets'] = ArrangeLst(Data['available_markets'])
    album['total_tracks'] = int(float(Data['total_tracks']))
    album['album_type'] = Data['album_type']
    album['name'] = Data['name'].strip('""')
    album['artist_id'] = Data['artist_id']
    album['external_urls'] = UrlFix(Data['external_urls'])
    return album

def FilterSong(Data):
    song = newSong(Data['id'])
    song['lyrics'] = lyricsFix(Data['lyrics'])
    song['album_id'] = Data['album_id']
    song['artists_id'] = ArrangeLst(Data['artists_id'])
    song['disc_number'] = int(float(Data['disc_number']))
    song['popularity'] = int(float(Data['popularity']))
    song['available_markets'] = ArrangeLst(Data['available_markets'])
    song['available_markets_num'] = lt.size(song['available_markets'])
    song['track_number'] = int(float(Data['track_number']))
    song['name'] = Data['name'].strip('""')
    song['duration_ms'] = int(float(Data['duration_ms']))
    song['href'] = Data['href']
    song['preview_url'] = Data['preview_url']
    return song

# ======================================
# Funciones para agregar datos (General)
# ======================================

def addSong(catalog, infoSong):
    Song = FilterSong(infoSong) 
    lt.addLast(catalog['songs'], Song)
    addMap(catalog['popularity'], Song['popularity'], Song, newEntryDoubleList, addValueSecondList)
    addMap(catalog['id_albums'], Song['album_id'], Song, newEntry, addValueMap)
    for artistid in lt.iterator(Song['artists_id']):
        addMap(catalog['id_artists'], artistid, Song, newEntryDoubleList, addValueFirstList)     

def addAlbum(catalog, infoAlbum):
    Album = FilterAlbum(infoAlbum)
    lt.addLast(catalog['albums'], Album)
    date = Album['release_date']
    addMap(catalog['years'], int(date[:4]), Album, newEntry, addValueMap)
    getInMap(catalog['id_albums'], Album['id'], Album, addSongAlbum)
    addMap(catalog['id_artists'], Album['artist_id'], Album, newEntryDoubleList, addValueSecondList)

def addArtist(catalog, infoArtist):
    Artist = FilterArtist(infoArtist)
    lt.addLast(catalog['artists'], Artist)
    addMap(catalog['popularity'], Artist['artist_popularity'], Artist, newEntryDoubleList, addValueFirstList)
    Albums = getInMap(catalog['id_artists'], Artist['id'], Artist, addReferences)
    if Albums:
        countryMap = addMap(catalog['artists_name'], Artist['name'], Artist, newEntryNameArtist, addArtistIdMap)
        for Album in lt.iterator(Albums):
            for country in lt.iterator(Album['available_markets']):
                addMap(countryMap, country, Album, newEntryCountry, addABCountSGCountry)

# ========================================
# Funciones para agregar datos a los Mapas
# ========================================

def addMap(Map, keyname, data, funcEntry, lstaction):
    try:
        if mp.contains(Map, keyname):
            pair_kv = mp.get(Map, keyname)
            mpvalue = me.getValue(pair_kv)
        else:
            mpvalue = funcEntry(keyname)
            mp.put(Map, keyname, mpvalue)
        return lstaction(mpvalue['info'], data)
    except Exception:
        return None

def getInMap(Map, keyname, data, lstaction):
    try:
        if mp.contains(Map, keyname):
            pair_kv = mp.get(Map, keyname)
            mpvalue = me.getValue(pair_kv)
            return lstaction(mpvalue['info'], data)
        return None
    except Exception:
        return None

# ==========================================
# Funciones para nueva entradas valores Mapa
# ==========================================

def newEntry(key):
    entry = {'key': key, 'info': None}
    entry['info'] = lt.newList('ARRAY_LIST')
    return entry

def newEntryDoubleList(key):
    entry = {'key': key, 'info': None}
    entry['info'] = lt.newList('ARRAY_LIST')
    firstList = lt.newList('ARRAY_LIST')
    secondList = lt.newList('ARRAY_LIST')
    lt.addLast(entry['info'], firstList)
    lt.addLast(entry['info'], secondList)
    return entry

def newEntryNameArtist(key):
    entry = {'key': key, 'info': None}
    entry['info'] = lt.newList('ARRAY_LIST') 
    artist = lt.newList('ARRAY_LIST')  #COLLISIONCHECKER
    countryMap = createCountryMap()
    lt.addLast(entry['info'], artist)
    lt.addLast(entry['info'], countryMap)
    return entry

def newEntryCountry(key):
    entry = {'key': key, 'info': None}
    entry['info'] = lt.newList()
    AlbumCount = 0
    SongList = lt.newList('ARRAY_LIST', cmpSGPopDurationName)
    lt.addLast(entry['info'], AlbumCount)
    lt.addLast(entry['info'], SongList)
    return entry

# ============================
# Funciones para agregar datos
# ============================

def addValueMap(LstData, data):
    lt.addLast(LstData, data)

def addValueFirstList(mpvalue, data):
    LstData = lt.getElement(mpvalue, 1)
    lt.addLast(LstData, data)

def addValueSecondList(mpvalue, data):
    LstData = lt.getElement(mpvalue, 2)
    lt.addLast(LstData, data)

def addArtistIdMap(mpvalue, artist):
    artistlist = lt.getElement(mpvalue, 1)
    lt.addLast(artistlist, artist)
    countryMap = lt.getElement(mpvalue, 2)
    return countryMap

def addABCountSGCountry(mpvalue, album):
    AlbumCount = lt.getElement(mpvalue, 1)
    AlbumCount += 1
    SongList = lt.getElement(mpvalue, 2)
    for song in lt.iterator(album['songs']):
        lt.addLast(SongList, song)
    lt.removeFirst(mpvalue)
    lt.addFirst(mpvalue, AlbumCount)
    lt.removeLast(mpvalue)
    lt.addLast(mpvalue, SongList)

# ==================================
# Funciones para agregar referencias
# ==================================

def addSongAlbum(songs, album):
    if not lt.isEmpty(songs):
        for song in lt.iterator(songs):
            song['album_name'] = album['name']
            song['release_date'] = album['release_date']
            song['album_type'] = album['album_type']
            lt.addLast(album['songs'], song)
        sorter(album['songs'], cmpSGPopDurationName)

def addReferences(mpvalue, artist):
    songs = lt.getElement(mpvalue, 1)
    albums = lt.getElement(mpvalue, 2)
    if not lt.isEmpty(albums):
        addAlbumArtist(albums, artist)
    addSongArtist(songs, artist)
    return albums

def addAlbumArtist(albums, artist):
    for album in lt.iterator(albums):
        if album['album_type'] == 'single':
            artist['album_single'] += 1
        elif album['album_type'] == 'compilation':
            artist['album_compilation'] += 1
        elif album['album_type'] == 'album':
            artist['album_typealbum'] += 1
        album['artist_album_name'] = artist['name']
        lt.addLast(artist['albums'], album)
    sorter(artist['albums'], cmpABName)  

def addSongArtist(songs, artist):
    for song in lt.iterator(songs):
        if artist['track_id'] == song['id']:
            artist['relevant_song_name'] = song['name']
        lt.addLast(song['artist_names'], artist['name'])

# ===============================
# Funciones para arreglo de datos
# ===============================

def ArrangeLst(string):
    ArrangeLst = lt.newList('ARRAY_LIST')
    Op = string.strip('""')
    Op2 = Op.strip('][')
    Op3 = Op2.split(', ')
    for i in Op3:
        if i != '':
            lt.addLast(ArrangeLst, i.strip("''"))
    return ArrangeLst

def lyricsFix(string):
    if string == '-99':
        return None
    Op = string.strip('""')
    Op2 = Op.strip(' ')
    Op3 = Op2.strip('\n')
    if len(Op3) > 90:
        Op3 = Op3[:90] + ' ...'
    return Op3

def DateFix(release_date):
    try:
        dateobject = datetime.strptime(release_date, '%b-%y')
        dateformat = dateobject.date()
        datetuple = dateformat.timetuple()
        yeardate = int(datetuple[0])
        if yeardate > 2000:
            yeardate = yeardate - 100
        dateformat.replace(year= yeardate)      
        return dateformat.strftime('%Y-%m')
    except Exception:
        return release_date

def UrlFix(string):
    Op = string.strip('}{')
    Op2 = Op.strip("'spotify': '")
    return Op2

# =========================
# Funciones de ordenamiento
# =========================

def sorter(Lst, cmpfunc):
    if lt.size(Lst) > 1:
        sa.sort(Lst, cmpfunc)

# ======================
# Funciones de consulta
# ======================

def LSTSize(listname):
    return lt.size(listname)

def MPSize(mapname):
    return mp.size(mapname)

def LSTEmpty(listname):
    return lt.isEmpty(listname)

def get3FirstandLast(Lst, sizedata):
    if sizedata == 0:
        return None
    if sizedata < 7:
        return Lst
    Lst_FaL = lt.subList(Lst, 1, 3)
    for i in range(sizedata-2, sizedata+1):
        lt.addLast(Lst_FaL, lt.getElement(Lst,i))
    return Lst_FaL

def getAlbumsYear(catalog, year):
    years = catalog['years']
    if mp.contains(years, year):
        pair_kv = mp.get(years, year)
        mpvalue = me.getValue(pair_kv)
        sizedata = LSTSize(mpvalue['info'])
        sorter(mpvalue['info'], cmpABName)
        PrntElements = get3FirstandLast(mpvalue['info'], sizedata)
        return sizedata, PrntElements
    return 0, None

def getPopularity(catalog, p_value, Dtype, cmpfunction):
    popularity = catalog['popularity']
    if mp.contains(popularity, p_value):
        pair_kv = mp.get(popularity, p_value)
        mpvalue = me.getValue(pair_kv)
        LstData = lt.getElement(mpvalue['info'], Dtype)
        sizedata = LSTSize(LstData)
        sorter(LstData, cmpfunction)
        PrntElements = get3FirstandLast(LstData, sizedata)
        return sizedata, PrntElements
    return 0, None

def getSGByArtistCountry(catalog, name, country):
    sizeAB, sizeSG, songList = getSGMapofMaps(catalog, name, country)
    PrntElements = lt.subList(songList, 1, 1)
    return sizeAB, sizeSG, PrntElements 

def getSGMapofMaps(catalog, name, country):
    artistsNameMap = catalog['artists_name']
    if mp.contains(artistsNameMap, name):
        pair_kv = mp.get(artistsNameMap, name)
        mpvalue = me.getValue(pair_kv)
        countrymap = lt.getElement(mpvalue['info'], 2)
        if mp.contains(countrymap, country):
            pair_kv2 = mp.get(countrymap, country)
            mpvalue2 = me.getValue(pair_kv2)
            sizeAB = lt.getElement(mpvalue2['info'], 1)
            songList = lt.getElement(mpvalue2['info'], 2)
            sizeSG = lt.size(songList)
            sorter(songList, cmpSGPopDurationName)
            return sizeAB, sizeSG, songList
    return 0, 0, None

def getDiscography(catalog, name):
    artistsNameMap = catalog['artists_name']
    if mp.contains(artistsNameMap, name):
        pair_kv = mp.get(artistsNameMap, name)
        mpvalue = me.getValue(pair_kv)
        artistlist = lt.getElement(mpvalue['info'], 1)
        artist = lt.getElement(artistlist, 1)
        ABSingle = artist['album_single']
        ABCompilation = artist['album_compilation']
        ABAlbum = artist['album_typealbum']
        albums = get3FirstandLast(artist['albums'], lt.size(artist['albums']))
        topsongs = lt.newList('ARRAY_LIST')
        try:
            for album in lt.iterator(albums):
                if not lt.isEmpty(album['songs']):
                    song = lt.getElement(album['songs'], 1)
                else:
                    song = None
                lt.addLast(topsongs, song)
        except Exception:
            return 0, 0, 0, None, None
        return ABSingle, ABCompilation, ABAlbum, albums, topsongs
    return 0, 0, 0, None, None

def getSGByArtistCountryTOP(catalog, name, country, number):
    sizeAB, sizeSG, songList = getSGMapofMaps(catalog, name, country)
    if sizeSG <= number:
        return sizeSG, songList
    PrntElements = lt.subList(songList, 1, number)
    sizeAB
    return sizeSG, PrntElements

# ===================================
# Funciones para enviar datos al view
# ===================================

def cleanerArtists(artists):
    infoPrint = lt.newList('ARRAY_LIST')
    for artist in lt.iterator(artists):
        data = (artist['name'], artist['artist_popularity'], artist['followers'], artist['relevant_song_name'], artist['genres'])
        lt.addLast(infoPrint, data)
    return infoPrint

def cleanerAlbums(albums):
    infoPrint = lt.newList('ARRAY_LIST')
    for album in lt.iterator(albums):
        data = (album['name'], album['release_date'], album['available_markets'], album['total_tracks'], 
            album['album_type'], album['artist_album_name'], album['external_urls'], album['songs']) 
        lt.addLast(infoPrint, data)
    return infoPrint

def cleanerSongs(songs):
    infoPrint = lt.newList('ARRAY_LIST')
    for song in lt.iterator(songs):
        data = (song['name'], song['release_date'], song['popularity'], song['disc_number'], song['track_number'], 
            song['available_markets'], song['available_markets_num'], song['duration_ms'], song['album_name'],
            song['album_type'], song['artist_names'], song['href'], song['preview_url'], song['lyrics']) 
        lt.addLast(infoPrint, data)
    return infoPrint

# ========================
# Funciones de comparación
# ========================

def cmpMapInt(id, tag):
    tagentry = me.getKey(tag)
    if int(id) == int(tagentry):
        return 0
    elif int(id) > int(tagentry):
        return 1
    else:
        return -1

def cmpMapName(id, tag):
    tagentry = me.getKey(tag)
    if id == tagentry:
        return 0
    elif id > tagentry:
        return 1
    else:
        return -1

def cmpName(info1, info2):
    if info1.lower() >= info2.lower():
        return False
    return True

def cmpInt(info1, info2):
    if int(info1) == int(info2):
        return 0
    elif int(info1) > int(info2):
        return 1
    else:
        return -1

def cmpABName(album1, album2):
    return cmpName(album1['name'], album2['name'])

def cmpATFollowsName(artist1, artist2):
    valueFollows = cmpInt(artist1['followers'], artist2['followers'])
    if valueFollows == 0:
        valueName = cmpName(artist1['name'], artist2['name'])
        return valueName
    elif valueFollows == 1:
        return True
    return False

def cmpSGDurationName(song1, song2):
    valueDuration = cmpInt(song1['duration_ms'], song2['duration_ms'])
    if valueDuration == 0:
        valueName = cmpName(song1['name'], song2['name'])
        return valueName
    elif valueDuration == 1:
        return True
    return False

def cmpSGPopDurationName(song1, song2):
    valuePopularity = cmpInt(song1['popularity'], song2['popularity'])
    if valuePopularity == 0:
        return cmpSGDurationName(song1, song2)
    elif valuePopularity == 1:
        return True
    return False    

# ========================
# Funciones de Laboratorio
# ========================

def configMapGenre(catalog, type, fc):
    catalog['genres'] = mp.newMap(2500,
                            maptype= type,
                            loadfactor= fc,
                            comparefunction=cmpGenres)

def LoadMapGenre(catalog):
    for artist in lt.iterator(catalog['artists']):
        for genre in lt.iterator(artist['genres']):
            if genre:
                addGenreArtist(catalog, artist, genre)
    return MPSize(catalog['genres'])
    
def addGenreArtist(catalog, Artist, genre):
    try:
        genres = catalog['genres']
        existgenre = mp.contains(genres, genre)
        if existgenre:
            pair_kv = mp.get(genres, genre)
            mpvalue = me.getValue(pair_kv)
        else:
            mpvalue = NewGenre(genre)
            mp.put(genres, genre, mpvalue)
        lt.addLast(mpvalue['artists'], Artist)
    except Exception:
        pass

def NewGenre(name):
    entry = {'genre': name, 'artists': None}
    entry['artists'] = lt.newList('SINGLE_LINKED')
    return entry

def cmpGenres(id, tag):
    tagentry = me.getKey(tag)
    if id.lower() == tagentry.lower():
        return 0
    elif id.lower() > tagentry.lower():
        return 1
    else:
        return 0
