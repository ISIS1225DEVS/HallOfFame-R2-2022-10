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
from DISClib.Algorithms.Sorting import mergesort as merge
assert cf

def newCatalog():
    catalog = {'albums': None,
               'albums_years': None,
               'albums_artists': None,
               'albums_ids': None,
               'artists': None,
               'artists_names': None,
               'artists_ids': None,
               'artists_popularity': None,
               'tracks': None,
               'tracks_ids': None,
               'tracks_popularity': None,
               'tracks_album': None}

    catalog['albums'] = lt.newList('ARRAY_LIST')

    """
    Este indice crea un map cuya llave es el año de publicacion
    """
    catalog['albums_years'] = mp.newMap(260,
                                 maptype='PROBING',
                                 loadfactor=0.5)
    
    catalog['albums_artists'] = mp.newMap(56126,
                                    maptype='PROBING',
                                    loadfactor=0.5)
    
    catalog['albums_ids'] = mp.newMap(101939,
                                    maptype='PROBING',
                                    loadfactor=0.5)

    catalog['artists'] = lt.newList('ARRAY_LIST')

    catalog['artists_names'] = mp.newMap(56126,
                                  maptype='PROBING',
                                  loadfactor=0.5)
    
    catalog['artists_ids'] = mp.newMap(56126,
                                  maptype='PROBING',
                                  loadfactor=0.5)
    
    catalog['artists_popularity'] = mp.newMap(101,
                                       maptype='PROBING',
                                       loadfactor=0.5)

    catalog['tracks'] = lt.newList('ARRAY_LIST')
    
    catalog['tracks_popularity'] = mp.newMap(101,
                                       maptype='PROBING',
                                       loadfactor=0.5)

    catalog['tracks_ids'] = mp.newMap(75503,
                                       maptype='PROBING',
                                       loadfactor=0.5)
    
    catalog['tracks_artist'] = mp.newMap(56126,
                                    maptype='PROBING',
                                    loadfactor=0.5)
                                
    catalog['tracks_album'] = mp.newMap(75503,
                                    maptype='PROBING',
                                    loadfactor=0.5)

    return catalog

# ==============================
# Add info functions (Lists)
# ==============================

def addAlbum(catalog, album):

    date = album['release_date']

    if len(album['release_date']) == 10:
        album['release_date'] = int(album['release_date'].split('-')[0])
    elif len(album['release_date']) == 4:
        album['release_date'] = int(album['release_date'])
    else:
        album['release_date'] = int('19' + album['release_date'].split('-')[1])
    
    album['available_markets'] = album['available_markets'].split(',')
    album['available_markets'] = list(album['available_markets'])
    for i in range (0, len(album['available_markets'])):
        album['available_markets'][i] = album['available_markets'][i].replace('[', '')
        album['available_markets'][i] = album['available_markets'][i].replace(']', '')
        album['available_markets'][i] = album['available_markets'][i].replace('\'', '')
        album['available_markets'][i] = album['available_markets'][i].replace(' ', '')
        album['available_markets'][i] = album['available_markets'][i].replace('\"', '')

    new_album = newAlbum(album['id'], album['track_id'], album['total_tracks'], album['external_urls'], album['album_type'], album['available_markets'], album['artist_id'], album['release_date'], album['name'], date)

    lt.addLast(catalog['albums'], new_album)
    addAlbumYear(catalog, new_album)
    addAlbumArtist(catalog, new_album)
    
def addTrack(catalog, track):
    track['artists_id'] = track['artists_id'].split(',')
    track['artists_id'] = list(track['artists_id'])
    for i in range (0, len(track['artists_id'])):
        track['artists_id'][i] = track['artists_id'][i].replace('[', '')
        track['artists_id'][i] = track['artists_id'][i].replace(']', '')
        track['artists_id'][i] = track['artists_id'][i].replace('\'', '')
        track['artists_id'][i] = track['artists_id'][i].replace(' ', '')
    
    if track['lyrics'] == '-99':
        track['lyrics'] = 'Lyrics no available'
    else:
        track['lyrics'] = track['lyrics'][0:50]
    
    track['available_markets'] = track['available_markets'].split(',')
    track['available_markets'] = list(track['available_markets'])
    for i in range (0, len(track['available_markets'])):
        track['available_markets'][i] = track['available_markets'][i].replace('[', '')
        track['available_markets'][i] = track['available_markets'][i].replace(']', '')
        track['available_markets'][i] = track['available_markets'][i].replace('\'', '')
        track['available_markets'][i] = track['available_markets'][i].replace(' ', '')
        track['available_markets'][i] = track['available_markets'][i].replace('\"', '')
    
    album_name = track['album_id']

    new_track = newTrack(track['id'], track['href'], track['album_id'], track['available_markets'], track['artists_id'], track['popularity'], track['name'], track['duration_ms'], track['lyrics'], track['preview_url'], album_name)

    lt.addLast(catalog['tracks'], track)
    addTracksPopularity(catalog, track)
    addTracksArtist(catalog, new_track)
    addTracksAlbum(catalog, track)

def addArtist(catalog, artist):
    lt.addLast(catalog['artists'], artist)
    addArtistsPopularity(catalog, artist)

# ==============================
# Add info functions (Hash Tables)
# ==============================

def addAlbumYear(catalog, album):
    try:
        years = catalog['albums_years']
        pub_year = int(album['release_date'])
        exist_year = mp.contains(years, pub_year)
        if exist_year:
            entry = mp.get(years, pub_year)
            year = me.getValue(entry)
        else:
            year = newYear(pub_year)
            mp.put(years, pub_year, year)
        lt.addLast(year['albums'], album)
    except Exception:
        return None

def addAlbumArtist(catalog, album):
    try:
        artist_albums = catalog['albums_artists']
        artist_id = album['artist_id']
        exist_artist = mp.contains(artist_albums, artist_id)
        if exist_artist:
            entry = mp.get(artist_albums, artist_id)
            albums = me.getValue(entry)
        else:
            albums = newAlbumArtist(artist_id)
            mp.put(artist_albums, artist_id, albums)
        lt.addLast(albums['albums'], album)
    except Exception:
        return None
        
def addArtistsPopularity(catalog, artist):
    popularities = catalog['artists_popularity']
    artist_popularity = float(artist['artist_popularity'])
    exist_popularity = mp.contains(popularities, artist_popularity)
    if exist_popularity:
        entry = mp.get(popularities, artist_popularity)
        popularity = me.getValue(entry)
    else:
        popularity = newArtistPopularity(artist_popularity)
        mp.put(popularities, artist_popularity, popularity)
    lt.addLast(popularity['artists'], artist)

def addTracksPopularity(catalog, track):
    popularities = catalog['tracks_popularity']
    track_popularity = float(track['popularity'])
    exist_popularity = mp.contains(popularities, track_popularity)
    if exist_popularity:
        entry = mp.get(popularities, track_popularity)
        popularity = me.getValue(entry)
    else: 
        popularity = newTrackPopularity(track_popularity)
        mp.put(popularities, track_popularity, popularity)
    lt.addLast(popularity['tracks'], track)

def addTracksArtist(catalog, track):
    tracks_artist = catalog['tracks_artist']
    if len(track['artists_id']) > 1:
        for artist_id in track['artists_id']:
            exist_artist = mp.contains(tracks_artist, artist_id)
            if exist_artist:
                entry = mp.get(tracks_artist, artist_id)
                track_id = me.getValue(entry)
            else:
                track_id = newTrackArtist(artist_id)
                mp.put(tracks_artist, artist_id, track_id)
            lt.addLast(track_id['tracks'], track)
    else:
        artist_id = track['artists_id'][0]
        exist_artist = mp.contains(tracks_artist, artist_id)
        if exist_artist:
            entry = mp.get(tracks_artist, artist_id)
            track_id = me.getValue(entry)
        else:
            track_id = newTrackArtist(artist_id)
            mp.put(tracks_artist, artist_id, track_id)
        lt.addLast(track_id['tracks'], track)


def addTracksAlbum(catalog, track):
    tracks_album = catalog['tracks_album']
    album_id = track['album_id']
    exist_album_id = mp.contains(tracks_album, album_id)
    if exist_album_id:
        entry = mp.get(tracks_album, album_id)
        tracks = me.getValue(entry)
    else:
        tracks = newTrackAlbum(album_id)
        mp.put(tracks_album, album_id, tracks)
    lt.addLast(tracks['tracks'], track)

def addArtistName(catalog, name, artist):
    mp.put(catalog['artists_names'], name, artist)

def addArtistId(catalog, id, artist):
    mp.put(catalog['artists_ids'], id, artist)

def addTrackId(catalog, id, track):
    mp.put(catalog['tracks_ids'], id, track)

def addAlbumId(catalog, id, album):
    mp.put(catalog['albums_ids'], id, album)

# ==============================
# Creating data functions
# ==============================

def newAlbum(id, track_id, total_tracks, external_urls, album_type, available_markets, artist_id, release_date, name, date):
    album = {'id': '', 'track_id': '', 'total_tracks': '', 'external_urls': '', 'album_type': '', 'available_markets': '', 'artist_id': '', 'release_date': '', 'name': '', 'date': ''}

    album['id'] = id
    album['track_id'] = track_id
    album['total_tracks'] = total_tracks
    album['external_urls'] = external_urls
    album['album_type'] = album_type
    album['available_markets'] = available_markets
    album['artist_id'] = artist_id
    album['release_date'] = release_date
    album['name'] = name
    album['date'] = date

    return album

def newTrack(id, href, album_id, available_markets, artists_id, popularity, name, duration_ms, lyrics, preview_url, album_name):
    track = {'id': '', 'href': '', 'album_id': '', 'available_markets': '', 'artists_id': '', 'popularity': '', 'name': '', 'duration_ms': '', 'lyrics': '', 'preview_url': '', 'album_name': ''}

    track['id'] = id
    track['href'] = href
    track['album_id'] = album_id
    track['available_markets'] = available_markets
    track['artists_id'] = artists_id
    track['popularity'] = popularity
    track['name'] = name
    track['duration_ms'] = duration_ms
    track['lyrics'] = lyrics
    track['preview_url'] = preview_url
    track['album_name'] = album_name

    return track

def newYear(pub_year):
    entry = {'year': "", "albums": None}
    entry['year'] = pub_year
    entry['albums'] = lt.newList('ARRAY_LIST', compareElements)
    return entry

def newAlbumArtist(artist_id):
    entry = {'artist_id': "", 'albums': None}
    entry['artist_id'] = artist_id
    entry['albums'] = lt.newList('ARRAY_LIST', compareElements)
    return entry

def newArtistPopularity(artist_popularity):
    entry = {'popularity': '', 'artists': None}
    entry['popularity'] = artist_popularity
    entry['artists'] = lt.newList('ARRAY_LIST', compareElements)
    return entry

def newTrackPopularity(track_popularity):
    entry = {'popularity': '', 'tracks': None}
    entry['popularity'] = track_popularity
    entry['tracks'] = lt.newList('ARRAY_LIST', compareElements)
    return entry

def newTrackArtist(track_artist):
    entry = {'artist': '', 'tracks': None}
    entry['artist'] = track_artist
    entry['tracks'] = lt.newList('ARRAY_LIST', compareElements)
    return entry

def newTrackAlbum(album_id):
    entry = {'album': '', 'tracks': None}
    entry['album'] = album_id
    entry['tracks'] = lt.newList('ARRAY_LIST', compareElements)
    return entry

# ==============================
# Cmp functions
# ==============================

def compareElements(element1, element2):
    if (element1) == (element2):
        return 0
    elif (element1) > (element2):
        return 1
    else:
        return 0

def cmpArtistsByPopularity(artist1, artist2):
    if float(artist1['followers']) > float(artist2['followers']):
        return True
    elif float(artist1['followers']) == float(artist2['followers']):
        if str(artist1['name']) > str(artist2['name']):
            return True
        else: 
            return False
    else:
        return False

def cmpTracksByPopularity(track1, track2):
    if float(track1['popularity']) > float(track2['popularity']):
        return True
    elif float(track1['popularity']) == float(track2['popularity']):
        if float(track1['duration_ms']) > float(track2['duration_ms']):
            return True
        elif float(track1['duration_ms']) == float(track2['duration_ms']):
            if str(track1['name']) > str(track2['name']):
                return True
            else: 
                return False
        else:
            return False
    else:
        return False

def cmpTracksByMarket(track1, track2):
    if float(track1['popularity']) > float(track2['popularity']):
        return True
    elif float(track1['popularity']) == float(track2['popularity']):
        if float(track1['duration_ms']) > float(track2['duration_ms']):
            return True
        elif float(track1['duration_ms']) == float(track2['duration_ms']):
            if str(track1['name']) > str(track2['name']):
                return True
            else: 
                return False
        else:
            return False
    else:
        return False

def cmpAlbumsByDate(album1, album2):
    if float(album1['release_date']) > float(album2['release_date']):
        return True
    elif float(album1['release_date']) == float(album2['release_date']):
        if str(album1['name']) > str(album2['name']):
            return True
        else: 
            return False
    else:
        return False

def cmpAlbumsByName(album1, album2):
    if album1['name'] > album2['name']:
        return True
    else:
        return False

#==========================================
# Generic functions
#==========================================

def sortList(list, cmp_function):
    sorted_list = merge.sort(list, cmp_function)
    return sorted_list

def sizeList(list):
    return lt.size(list)

def subList(list, pos, len):
    return lt.subList(list, pos, len)

def sizeMap(map):
    return mp.size(map)

#==========================================
# Other functions
#==========================================

def sortTracks(tracks):
    return sortList(tracks, cmpTracksByMarket)

def sortTracksByAlbum(tracks):
    return sortList(tracks, cmpTracksByPopularity)

#==========================================
# Get info functions with lists
#==========================================

def getAlbumsByYear(catalog, year):
    albums_year = mp.get(catalog['albums_years'], year)
    if albums_year:
        albums = me.getValue(albums_year)['albums']
        for album in lt.iterator(albums):
            artist_name = getArtistName(catalog, album['artist_id'])
            if artist_name == None:
                album['artist_id'] = 'UNKNOWN'
            else:
                album['artist_id'] = artist_name
        sorted_albums = sortList(albums, cmpAlbumsByName)
        return sorted_albums
    return None

def getAlbumsByArtist(catalog, artist_name):
    artist_id = getArtistId(catalog, artist_name)
    albums_artist = mp.get(catalog['albums_artists'], artist_id)
    type_album = 0
    type_compilation = 0
    type_single = 0
    if albums_artist:
        albums = me.getValue(albums_artist)['albums']
        for album in lt.iterator(albums):
            if album['album_type'] == 'album':
                type_album += 1
            elif album['album_type'] == 'compilation':
                type_compilation += 1
            else:
                type_single += 1
        sorted_albums = sortList(albums, cmpAlbumsByDate)

        return sorted_albums, type_album, type_compilation, type_single
    return None

def getAlbumsAvailable(albums, country_code):
    available_albums = lt.newList('ARRAY_LIST')
    for album in lt.iterator(albums):
        for country in album['available_markets']:
            if country == country_code:
                lt.addLast(available_albums, album)
    return available_albums

def getAlbumById(catalog, id):
    album = mp.get(catalog['albums_ids'], id)
    if album:
        album_info = me.getValue(album)
        return album_info
    return None

def getArtistsByPopularity(catalog, popularity):
    artists_popularity = mp.get(catalog['artists_popularity'], popularity)
    if artists_popularity:
        artists = me.getValue(artists_popularity)['artists']
        sorted_artists = sortList(artists, cmpArtistsByPopularity)
        for artist in lt.iterator(artists):
            track_name = getTrackName(catalog, artist['track_id'])
            if track_name == None:
                artist['track_id'] = 'UNKNOWN'
            else:
                artist['track_id'] = track_name
        return sorted_artists
    return None

def getTracksByArtist(catalog, artist_name, country_code):
    available_tracks = lt.newList('ARRAY_LIST')
    artist_id = getArtistId(catalog, artist_name)
    artists_tracks = mp.get(catalog['tracks_artist'], artist_id)
    if artists_tracks:
        tracks = me.getValue(artists_tracks)['tracks']
        for track in lt.iterator(tracks):
            for country in track['available_markets']:
                if country == country_code:
                    lt.addLast(available_tracks, track)
        for track in lt.iterator(available_tracks):
            album_name = getAlbumName(catalog, track['album_id'])
            if len(track['artists_id']) == 1:
                artist_id = track['artists_id'][0]
                lista_artists = getArtistName(catalog, artist_id)
                if lista_artists == None:
                    track['artists_id'] = 'UNKOWN'
                else:
                    track['artists_id'] = lista_artists
            else:
                lista_artists = []
                for artist_id in track['artists_id']:
                    artists_name = getArtistName(catalog, artist_id)
                    if artists_name == None:
                        artists_name = 'UNKOWN'
                    lista_artists.append(artists_name)
                    track['artists_id'] = lista_artists
            if album_name == None:
                track['album_name'] = 'UNKNOWN'
            else:
                track['album_name'] = album_name
        sorted_tracks = sortList(available_tracks, cmpTracksByPopularity)
        return sorted_tracks
    return None

def getTracksByPopularity(catalog, popularity):
    tracks_popularity = mp.get(catalog['tracks_popularity'], popularity)
    if tracks_popularity:
        tracks = me.getValue(tracks_popularity)['tracks']
        sorted_tracks = sortList(tracks, cmpTracksByPopularity)
        for track in lt.iterator(tracks):
            album_name = getAlbumName(catalog, track['album_id'])
            if len(track['artists_id']) == 1:
                artist_id = track['artists_id'][0]
                lista_artists = getArtistName(catalog, artist_id)
                if lista_artists == None:
                    track['artists_id'] = 'UNKOWN'
                else:
                    track['artists_id'] = lista_artists
            else:
                lista_artists = []
                for artist_id in track['artists_id']:
                    artists_name = getArtistName(catalog, artist_id)
                    if artists_name == None:
                        artists_name = 'UNKOWN'
                    lista_artists.append(artists_name)
                    track['artists_id'] = lista_artists
            if album_name == None:
                track['album_id'] = 'UNKNOWN'
            else:
                track['album_id'] = album_name
        return sorted_tracks
    return None

def getTracksByAlbum(catalog, album_id):
    tracks_album = mp.get(catalog['tracks_album'], album_id)
    if tracks_album:
        tracks = me.getValue(tracks_album)['tracks']
        for track in lt.iterator(tracks):
            album_name = getAlbumName(catalog, track['album_id'])
            if len(track['artists_id']) == 1:
                artist_id = track['artists_id'][0]
                lista_artists = getArtistName(catalog, artist_id)
                if lista_artists == None:
                    track['artists_id'] = 'UNKOWN'
                else:
                    track['artists_id'] = lista_artists
            else:
                lista_artists = []
                for artist_id in track['artists_id']:
                    artists_name = getArtistName(catalog, artist_id)
                    if artists_name == None:
                        artists_name = 'UNKOWN'
                    lista_artists.append(artists_name)
                    track['artists_id'] = lista_artists
            if album_name == None:
                track['album_id'] = 'UNKNOWN'
            else:
                track['album_id'] = album_name
        return tracks
    return None

#==========================================
# Get inside info functions
#==========================================

def getArtistId(catalog, name):
    artist = mp.get(catalog['artists_names'], name)
    if artist:
        artist_info = me.getValue(artist)['id']
        return artist_info
    return None

def getArtistName(catalog, id):
    artist = mp.get(catalog['artists_ids'], id)
    if artist:
        artist_info = me.getValue(artist)['name']
        return artist_info
    return None

def getTrackName(catalog, id):
    track = mp.get(catalog['tracks_ids'], id)
    if track:
        track_info = me.getValue(track)['name']
        return track_info
    return None

def getAlbumName(catalog, id):
    album = mp.get(catalog['albums_ids'], id)
    if album:
        album_info = me.getValue(album)['name']
        return album_info
    return None
