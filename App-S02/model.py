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

from importlib.metadata import entry_points
import config as cf
import time
import datetime
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import mergesort as mgs
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

def newCatalog():
    """
    Inicializa el catálogo de Spotify Profiling. Crea una lista vacia para guardar
    todos los albums, adicionalmente, crea una lista vacia para los artistas y una
    lista vacia para los tracks. Retorna el catalogo inicializado.
    """
    catalog = {'albums': None, 'artists': None, 'tracks': None, 'albumsByYear': None}

    catalog['albums'] = lt.newList('ARRAY_LIST')
    catalog['artists'] = lt.newList('ARRAY_LIST')
    catalog['tracks'] = lt.newList('ARRAY_LIST')
    catalog['artistsByGenres'] = mp.newMap(maptype = 'PROBING', numelements = 4210, loadfactor = 0.5)
    catalog['albumsByYear'] = mp.newMap(maptype = 'PROBING', numelements = 74, loadfactor = 0.5)
    catalog['artistsByPopularity'] = mp.newMap(maptype = 'PROBING', numelements = 99, loadfactor = 0.5)
    catalog['artistsByName'] = mp.newMap(maptype = 'CHAINING', numelements = 56126, loadfactor = 0.5)
    catalog['albumsMap'] = mp.newMap(maptype = 'CHAINING', numelements = 75503, loadfactor = 4.0)
    catalog['artistsMap'] = mp.newMap(maptype = 'CHAINING', numelements = 56126, loadfactor = 4.0)
    catalog['tracksMap'] = mp.newMap(maptype = 'CHAINING', numelements = 101939, loadfactor = 4.0)
    catalog['tracksByPopularity'] = mp.newMap(maptype = 'CHAINING', numelements = 100, loadfactor = 4.0)
    catalog['artistsWithNamesake'] = mp.newMap(maptype = 'PROBING', numelements = 150, loadfactor = 0.5)
    return catalog

# Funciones para agregar informacion al catalogos

def addAlbum(catalog, album):
    'El album se añade a la lista de albums'
    try:
        album['year'] = int(album['release_date'][:4].strip())
    except:
        album['year'] = int('19' + album['release_date'][-2:])
    album['tracks'] = lt.newList('ARRAY_LIST')
    album['total_tracks'] = 0
    album['inicial_track_name'] = "No track"
    album['artist_name'] = "Unknown"
    album['most_Popular'] = "No track"
    lt.addLast(catalog['albums'], album)
    return catalog

def addArtist(catalog, artist):
    'El artista se añade a la lista de artistas'
    artist['albums'] = lt.newList('ARRAY_LIST')
    artist['tracks'] = lt.newList('ARRAY_LIST')
    artist['tracksMaps'] = mp.newMap(maptype = 'PROBING', numelements = 50, loadfactor = 0.5)
    artist['albumsByType'] = mp.newMap(maptype = 'PROBING', numelements = 3, loadfactor = 0.5)
    mp.put(artist['albumsByType'], 'single', 0)
    mp.put(artist['albumsByType'], 'compilation', 0)
    mp.put(artist['albumsByType'], 'album', 0)
    artist['relevant_track_name'] = "Unknown"
    lt.addLast(catalog['artists'], artist)
    return catalog

def addTrack(catalog, track):
    'El track se añade a la lista de tracks'
    track['artists_names'] = ''
    if track['lyrics'] == '-99':
        track['lyrics'] = 'La letra NO esta disponible'
    track['available_markets'] = strlstdivider(track['available_markets'])
    track['distribution'] = len(track['available_markets'])
    lt.addLast(catalog['tracks'], track)
    return catalog

# Funciones para creacion de datos

def namesakeManagement(catalog):
    catalog['artists'] = sortLst(catalog['artists'], lt.size(catalog['artists']), cmpLstsByName)
    for i in range(1,lt.size(catalog['artists'])):
        if i + 1 <= lt.size(catalog['artists']) and lt.getElement(catalog['artists'], i)['name'].lower() == lt.getElement(catalog['artists'], i + 1)['name'].lower():
            j = i
            count = 1
            originalName = lt.getElement(catalog['artists'], i)['name']
            while originalName.lower() == lt.getElement(catalog['artists'], j)['name'].lower():
                modifiedName = lt.getElement(catalog['artists'], j)['name'] + '-' + str(count)
                lt.getElement(catalog['artists'], j)['name'] = modifiedName
                if mp.contains(catalog['artistsWithNamesake'], originalName):
                    lt.addLast(me.getValue(mp.get(catalog['artistsWithNamesake'], originalName)),modifiedName)
                else:
                    artistsModifiedName = lt.newList('ARRAY_LIST')
                    lt.addLast(artistsModifiedName, modifiedName)
                    mp.put(catalog['artistsWithNamesake'], originalName, artistsModifiedName)
                j += 1
                count += 1

def connectFullData(catalog):
    #Se recorre la lista de tracks para añadir cada tracks a su artista y album correspondiente
    for track in lt.iterator(catalog['tracks']):
        album = lt.getElement(catalog['albums'], binarySearch(catalog['albums'], track['album_id'], 'id'))
        artistOfAlbum = lt.getElement(catalog['artists'], binarySearch(catalog['artists'], album['artist_id'], 'id'))
        album['artist'] = artistOfAlbum
        album['artist_name'] = artistOfAlbum['name']
        if album['most_Popular'] == "No track":
            album['most_Popular'] = track
        else:
            if album['most_Popular']['popularity'] < track['popularity']:
                album['most_Popular'] = track
        track['album'] = album
        track['album_name'] = album['name']
        track['album_type'] = album['album_type']
        track['release_date'] = int(album['year'])
        artistsIds = strlstdivider(track['artists_id'])
        if track['id'] == album['track_id']:
            album['inicial_track_name'] = track['name']

        for artistId in artistsIds:
            artist = lt.getElement(catalog['artists'], binarySearch(catalog['artists'], artistId, 'id'))
            if artist['track_id'] == track['id']:
                artist['relevant_track_name'] =  track['name']
            if track['artists_names'] == '':
                track['artists_names'] =  artist['name']
            else:
                track['artists_names'] += ' - ' + artist['name']
            lt.addLast(artist['tracks'], track)
            if not mp.contains(artist['tracksMaps'], album['id']):
                lt.addLast(artist['albums'], album)
                mp.put(artist['tracksMaps'], album['id'], album)
                albumType = album['album_type']
                conteo = me.getValue(mp.get(artist['albumsByType'],albumType)) + 1
                mp.put(artist['albumsByType'],albumType,conteo)
        lt.addLast(album['tracks'], track)
        album['total_tracks'] += 1

def mapsCreator(catalog):
    'Maps by artists:'
    for artist in lt.iterator(catalog['artists']):
        artist['tracks'] = sortLst(artist['tracks'], lt.size(artist['tracks']), cmpTracksByPopularity)
        artist['albums'] = sortLst(artist['albums'],lt.size(artist['albums']),cmpAlbumsByYear)
        loadArtistByGenreMap(catalog, artist)
        loadArtistOrTrackByPopularityMap(catalog['artistsByPopularity'], artist, 'artist_popularity')
        loadArtistsByNameMap(catalog, artist['name'], artist)
    'Maps by Albums'
    for album in lt.iterator(catalog['albums']):
        album['tracks'] = sortLst(album['tracks'],lt.size(album['tracks']),cmpTracksByPopularity)
        loadAlbumsByYearMap(catalog, album['year'], album)
    'Maps by Tracks'
    for track in lt.iterator(catalog['tracks']):
        loadArtistOrTrackByPopularityMap(catalog['tracksByPopularity'], track, 'popularity')

def loadArtistByGenreMap(catalog, artist):
    for genre in artist['genres']:
        if mp.contains(catalog['artistsByGenres'], genre):
            lt.addLast(me.getValue(mp.get(catalog['artistsByGenres'], genre)), artist) # me.getValue(mp.get(catalog['artistsByGenres'], genre)) = UNA LISTA XDXD
        else:
            artists = lt.newList('ARRAY_LIST')
            lt.addLast(artists, artist)
            mp.put(catalog['artistsByGenres'], genre, artists)

def loadArtistOrTrackByPopularityMap(mapBy, spotifyBy, key):
    if mp.contains(mapBy, int(float(spotifyBy[key]))):
        lt.addLast(me.getValue(mp.get(mapBy, int(float(spotifyBy[key])))), spotifyBy) # me.getValue(mp.get(catalog['artistsByGenres'], genre)) = UNA LISTA XDXD
    else:
        lstBy = lt.newList('ARRAY_LIST')
        lt.addLast(lstBy, spotifyBy)
        mp.put(mapBy, int(float(spotifyBy[key])), lstBy)

def loadAlbumsByYearMap(catalog, year, album):
    if mp.contains(catalog['albumsByYear'], year):
        lt.addLast(me.getValue(mp.get(catalog['albumsByYear'], year)),album) # me.getValue(mp.get(catalog['artistsByGenres'], genre)) = UNA LISTA XDXD
    else:
        albums = lt.newList('ARRAY_LIST')
        lt.addLast(albums, album)
        mp.put(catalog['albumsByYear'], year, albums)

def loadArtistsByNameMap(catalog, name, artist):
    artist['tracksByCountry'] = mp.newMap(numelements = 193, maptype = 'PROBING', loadfactor = 0.5)
    for track in lt.iterator(artist['tracks']):
        for countryCode in track['available_markets']:
            if mp.contains(artist['tracksByCountry'], hyperStrip(countryCode)):
                lt.addLast(me.getValue(mp.get(artist['tracksByCountry'], hyperStrip(countryCode))), track)
            else:
                tracks = lt.newList('ARRAY_LIST')
                lt.addLast(tracks, track)
                mp.put(artist['tracksByCountry'], hyperStrip(countryCode), tracks)

    mp.put(catalog['artistsByName'], name, artist)

def strlstdivider(artistStr):
    artistsList = artistStr.replace('[','').replace(']','').replace("'",'').split(',')
    return artistsList

def listsFusion(lst1, lst2):
    fusionList = lt.newList('ARRAY_LIST')
    for element in lt.iterator(lst1):
        lt.addLast(fusionList, element)
    for element in lt.iterator(lst2):
        lt.addLast(fusionList, element)
    return fusionList

#=^..^=   =^..^=   =^..^=    =^..^=  [Requerimiento 1]  =^..^=    =^..^=    =^..^=    =^..^=
def albumsByReleaseYear(catalog, year):
    entry = mp.get(catalog['albumsByYear'], year)
    if entry:
        albumsByReleaseYear = me.getValue(entry)
        albumsByReleaseYear = sortLst(albumsByReleaseYear, lt.size(albumsByReleaseYear), cmpLstsByName)
        return albumsByReleaseYear
    return lt.newList()

#=^..^=   =^..^=   =^..^=    =^..^=  [Requerimiento 2]  =^..^=    =^..^=    =^..^=    =^..^=
def artistByPopularity(catalog, popularity):
    entry = mp.get(catalog['artistsByPopularity'], popularity)
    if entry:
        artistByPopularitylt = me.getValue(entry)
        artistByPopularitylt = sortLst(artistByPopularitylt,lt.size(artistByPopularitylt), cmpArtistsByPopularity)
        return artistByPopularitylt
    return lt.newList()

#=^..^=   =^..^=   =^..^=    =^..^=  [Requerimiento 3]  =^..^=    =^..^=    =^..^=    =^..^=
def tracksByPopularity(catalog, popularity):
    entry = mp.get(catalog['tracksByPopularity'], popularity)
    if entry:
        tracksByPopularity = me.getValue(entry)
        tracksByPopularity = sortLst(tracksByPopularity, lt.size(tracksByPopularity), cmpTracksByPopularity)
        return tracksByPopularity
    return lt.newList()

#=^..^=   =^..^=   =^..^=    =^..^=  [Requerimiento 4]  =^..^=    =^..^=    =^..^=    =^..^=
def popularTrackByArtist(catalog, artistName, countryCode):
    albums = lt.newList('ARRAY_LIST')
    entryArt = mp.get(catalog['artistsByName'], artistName)
    if entryArt:
        artist = me.getValue(entryArt)
        entryDataHelper = mp.get(artist['tracksByCountry'], countryCode)
        if entryDataHelper:
            songs = me.getValue(entryDataHelper)
            songs = sortLst(songs, lt.size(songs), cmpTracksByPopularityOldV)
            for song in lt.iterator(songs):
                if not lt.isPresent(albums, song['album_name']):
                    lt.addLast(albums, song['album_name'])
            return lt.subList(songs, 1, 1), lt.size(albums), lt.size(songs)
    return lt.newList(), 0, 0
#=^..^=   =^..^=   =^..^=    =^..^=  [Requerimiento 5]  =^..^=    =^..^=    =^..^=    =^..^=
def albumInfo(catalog, artistName):
    entry = mp.get(catalog['artistsByName'], artistName)
    if entry:
        artist = me.getValue(entry)
        sizeAlbumsArtist = lt.size(artist['albums'])
        countSingles = me.getValue(mp.get(artist['albumsByType'], 'single'))
        countRecopilations = me.getValue(mp.get(artist['albumsByType'], 'compilation'))
        countAlbums = me.getValue(mp.get(artist['albumsByType'], 'album'))
        countByType = (countSingles, countRecopilations, countAlbums)
        albumssorted = sortLst(artist['albums'], lt.size(artist['albums']), cmpAlbumsByYear)

        trackArray = lt.newList('ARRAY_LIST')
        for albumpop in lt.iterator(albumssorted):
            maximumTrack = albumpop['most_Popular']
            lt.addLast(trackArray,maximumTrack)
        return sizeAlbumsArtist, countByType, albumssorted, trackArray
    default = lt.newList()
    return 0, (0,0,0), default, default


#=^..^=   =^..^=   =^..^=    =^..^=  [Bono]  =^..^=    =^..^=    =^..^=    =^..^=
def tracksByDistributionOfArtist(catalog, countryCode, artistName, top):
    default = lt.newList()
    entryArtists = mp.get(catalog['artistsByName'], artistName)
    if entryArtists:
        artist = me.getValue(entryArtists)
        entryDataHelper = mp.get(artist['tracksByCountry'], countryCode)
        if entryDataHelper:
            tracks = me.getValue(entryDataHelper)
            tracks = sortLst(tracks, lt.size(tracks), cmpTracksByPopularityOldV)
            if lt.size(tracks) < top:
                return tracks, lt.size(tracks)
            else:
                topTracks = lt.subList(tracks, 1, top)
                return topTracks, lt.size(tracks)
    return default, 0

# Funciones de consulta

def linealSearch(sortedList,element,parameter):
    pos = None
    while pos == None:
        for album_pos in range(1,lt.size(sortedList)):
            if lt.getElement(sortedList,album_pos)[parameter] == element:
                pos = album_pos
                break
        element += 1
    return pos


def binarySearch(sortedList, element, parameter):
    """
    Busqueda Binaria de un elemento en una lista ordenada ascendentemente
    Resultado: Indice en la lista donde se encuentra el elemento. -1 si no se encuentra.
    """
    i = 0
    f = lt.size(sortedList)
    pos = -1
    found = False
    while i <= f and not found:
        # calcular la posicion de la mitad entre i y f
        m = (i + f) // 2
        if lt.getElement(sortedList, m)[parameter] == element:
            pos = m
            found = True
        elif lt.getElement(sortedList, m)[parameter] > element:
            f = m - 1
        else:
            i = m + 1
    return pos

def binarySearchMin(sortedList, element, parameter):
    m = 0
    i = 0
    f = lt.size(sortedList)
    pos = -1
    found = False
    while i <= f and not found:
        m = (i + f) // 2
        if lt.getElement(sortedList, m)[parameter] == element:
            pos = m
            found = True
        elif lt.getElement(sortedList, m)[parameter] > element:
            f = m - 1
        else:
            i = m + 1
    if found == True:
        while lt.getElement(sortedList, pos - 1)[parameter] == element:
            pos -= 1
    elif lt.getElement(sortedList, m)[parameter] > element:
        pos = m
        while lt.getElement(sortedList, pos - 1)[parameter] > element:
            pos -= 1
    return pos

def binarySearchMax(sortedList, element, parameter):
    m = 0
    i = 0
    f = lt.size(sortedList)
    pos = -1
    found = False
    while i <= f and not found:
        m = (i + f) // 2
        if lt.getElement(sortedList, m)[parameter] == element:
            pos = m
            found = True
        elif lt.getElement(sortedList, m)[parameter] > element:
            f = m - 1
        else:
            i = m + 1
    if found == True:
        while lt.getElement(sortedList, pos + 1)[parameter] == element:
            pos += 1
    elif lt.getElement(sortedList, m)[parameter] < element:
        pos = m
        while lt.getElement(sortedList, pos + 1)[parameter] > element:
            pos += 1
    return pos

albumsSize = lambda catalog: lt.size(catalog['albums'])

artistsSize = lambda catalog: lt.size(catalog['artists'])

tracksSize = lambda catalog: lt.size(catalog['tracks'])

def getLastNum(number, spotifyList):
    """
    Retorna los primeros number
    """
    if number <= lt.size(spotifyList):
        lasts = lt.newList('ARRAY_LIST')
        for cont in range(0, number):
            element = lt.getElement(spotifyList, lt.size(spotifyList) - cont)
            lt.addFirst(lasts, element)
        return lasts
    else:
        return spotifyList

def getFirstNum(number, spotifyList):
    """
    Retorna los ultimos number
    """
    if number <= lt.size(spotifyList):
        firsts = lt.newList('ARRAY_LIST')
        for cont in range(1, number + 1):
            element = lt.getElement(spotifyList, cont)
            lt.addLast(firsts, element)
        return firsts
    else:
        return spotifyList

# Funciones utilizadas para comparar elementos dentro de una lista

def cmpLstsById(element1, element2):
    'Return True if album1 < album2, False otherwise.'
    return element1['id'] < element2['id']

def cmpLstsByName(element1, element2):
    'Return True if album1 < album2, False otherwise.'
    return element1['name'] < element2['name']

def cmpArtistsByFollowers(artist1, artist2):
    'Return True if  artist1 < artist2'
    return float(artist1["followers"]) < float(artist2["followers"])

def cmpAlbumsByYear(album1, album2):
    'Return True if album1 < album2, False otherwise.'
    return int(album1['year']) < (album2['year'])

def cmpTracksByYear(track1, track2):
    return track1['release_date'] < track2['release_date']

def cmpTracksByPopularity(track1, track2):
    if float(track1['duration_ms']) > float(track2['duration_ms']):
        return True
    elif float(track1['duration_ms']) == float(track2['duration_ms']):
        if track1['name'] > track2['name']:
            return True
    else:
        return False

def cmpArtistsByPopularity(artistone, artisttwo):
    if float(artistone['followers']) > float(artisttwo['followers']):
        return True
    elif float(artistone['followers']) == float(artisttwo['followers']):
        if artistone['name'] > artisttwo['name']:
            return True
    else:
        return False

def cmpDistribution(element1, element2):

    if int(element1["distribution"]) > int(element2["distribution"]):
            return True
    elif float(element1['distribution']) == float(element2['distribution']):
        if float(element1['popularity']) > float(element2['popularity']):
            return True
        elif float(element1['popularity']) == float(element2['popularity']):
            if element1['name'] > element2['name']:
                return True
    else:
        return False

def cmpTracksByPopularityOldV(track1, track2):
    if float(track1['popularity']) > float(track2['popularity']):
        return True
    elif float(track1['popularity']) == float(track2['popularity']):
        if float(track1['duration_ms']) > float(track2['duration_ms']):
            return True
        elif float(track1['duration_ms']) == float(track2['duration_ms']):
            if track1['name'] > track2['name']:
                return True
    else:
        return False

# Funciones de ordenamiento

def sortLst(lst, size, parameter):
    sub_list = lt.subList(lst, 1, size)
    sorted_list = mgs.sort(sub_list, parameter)
    return sorted_list

def sortSpotifyLists(catalog):
    catalog['albums'] = sortLst(catalog['albums'], lt.size(catalog['albums']), cmpLstsById)
    catalog['artists'] = sortLst(catalog['artists'], lt.size(catalog['artists']), cmpLstsById)
    catalog['tracks'] = sortLst(catalog['tracks'], lt.size(catalog['tracks']), cmpLstsById)

# Funciones Auxiliares
def resetMap(numElements, mapType, loadFactor):
    return mp.newMap(numelements = numElements, maptype = mapType, loadfactor = loadFactor)

def resetList():
    return lt.newList('ARRAY_LIST')

def rangeByDate(listcatalog, min, max, parameter):
    minYear = linealSearch(listcatalog, int(min), parameter)
    #minYear = binarySearchMin(listcatalog, int(min), parameter)
    maxYear = binarySearchMax(listcatalog, int(max), parameter)
    yearRange = maxYear - minYear
    listByYear = lt.subList(listcatalog, minYear, yearRange + 1)
    return listByYear

def getTime():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def deltaTime(start, end):
    """
    devuelve la diferencia entre tiempos de procesamiento muestreados
    """
    elapsed = float(end - start)
    return elapsed

def countAlbumType(TADlist,types):
    type1 = types[0]
    counttype1 = 0
    type2 = types[1]
    counttype2 = 0
    counttype3 = 0
    for album in lt.iterator(TADlist):
        if album['album_type'] == type1:
            counttype1 += 1
        elif album['album_type'] == type2:
            counttype2 += 1
        else:
            counttype3 += 1
    return (counttype1, counttype2, counttype3)

def linealMaxPopularity(listToCount):
    maxiumTrack = lt.getElement(listToCount, 1)
    for track in lt.iterator(listToCount):
        if float(track['popularity']) > float(maxiumTrack['popularity']):
            maxiumTrack = track
        elif float(track['popularity']) == float(maxiumTrack['popularity']):
            if float(track['duration_ms']) > float(maxiumTrack['duration_ms']):
                maxiumTrack = track
            elif float(track['duration_ms']) == float(maxiumTrack['duration_ms']):
                if track['name'] > maxiumTrack['name']:
                    maxiumTrack = track
    return maxiumTrack

hyperStrip = lambda string: string.replace('"',"").replace(' ','').strip()

def UEXNamesake(catalog, artistName):
    namesakeCount = 0
    default = lt.newList()
    entry = mp.get(catalog['artistsWithNamesake'], artistName)
    if entry:
        artistlt = me.getValue(entry)
        namesakeCount = lt.size(artistlt)
        return namesakeCount, artistlt
    return namesakeCount, default