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


from platform import architecture
import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as shell
from DISClib.Algorithms.Sorting import insertionsort as insertion
from DISClib.Algorithms.Sorting import mergesort as merge
assert cf
from datetime import datetime as dt

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos
#our_prime = 977
#our_prime = 2147483647
our_prime = 12345678910987654321
our_loadfactor = 0.1

def newCatalog():
    catalog = {
        "tracks" : None,
        "albums" : None, 
        "artists": None, 
        #================[lab7]================
        "genres":  None,
        #================[id]==================
        "id_tracks": None,
        "id_albums": None,
        "id_artists": None,

        #=================[R1]=================
        "albums_per_year": None,
        #=================[R2]=================
        'artists_per_popularity' : None,
        #=================[R3]=================
        "tracks_by_popularity": None,
        #=================[R4]=================
        'tracks_by_artist': None,
        #=================[R5]=================
        "albums_by_artist": None,
        "tracks_in_album" : None
    }
    catalog["tracks"] = lt.newList("ARRAY_LIST")
    catalog["albums"] = lt.newList("ARRAY_LIST")
    catalog["artists"] = lt.newList("ARRAY_LIST")
    #================[ids]=====================
    
    catalog['id_tracks'] = mp.newMap(numelements = 101939, 
                        prime = our_prime,
                        maptype= 'PROBING',
                        loadfactor = our_loadfactor,
                        )

    catalog['id_albums'] = mp.newMap(numelements = 75503, 
                        prime = our_prime,
                        maptype= 'PROBING',
                        loadfactor = our_loadfactor,
                        )

    catalog['id_artists'] = mp.newMap(numelements = 56126, 
                        prime = our_prime,
                        maptype= 'PROBING',
                        loadfactor = our_loadfactor,
                        )
    
    #=================[R1]=================
    catalog["albums_per_year"] = mp.newMap(numelements= 88, 
                        prime= our_prime,
                        maptype="PROBING",
                        loadfactor=our_loadfactor,
                        )

    #=================[R2]=================
    catalog['artists_per_popularity'] = mp.newMap(numelements= 100,
                        prime = our_prime,
                        maptype='PROBING',
                        loadfactor= our_loadfactor,
                        )
                        
    #=================[R3]=================
    catalog["tracks_by_popularity"] = mp.newMap(numelements = 100,
                        prime = our_prime,
                        maptype='PROBING',
                        loadfactor= our_loadfactor,
                        )

    #=================[R4 & R6]=================
    catalog['tracks_by_artist'] = mp.newMap(numelements = 56126, 
                        prime = our_prime,
                        maptype= 'PROBING',
                        loadfactor = our_loadfactor,
                        )

    #================[R5]===================
    catalog["albums_by_artist"] = mp.newMap(numelements = 56200, 
                        prime = our_prime,
                        maptype= 'PROBING',
                        loadfactor = our_loadfactor,
                        )

    catalog["tracks_in_album"] = mp.newMap(numelements = 76000, 
                        prime = our_prime,
                        maptype= 'PROBING',
                        loadfactor = our_loadfactor,
                        )
    
    return catalog


# Funciones para agregar información al catalogo
#####################################################################################
def addTrack(catalog, track):
    
    lt.addLast(catalog["tracks"], track)
    #=================[Id]====================
    mp.put(catalog['id_tracks'], track['id'], track)

    #=================[R3]==================
    
    track_rating = str(round(float(track["popularity"])))
    exist_track_rating = mp.get(catalog["tracks_by_popularity"], track_rating)
    if exist_track_rating:
        insort_right_r3(exist_track_rating["value"], track, lo=1, hi=None)

    else:
        mp.put(catalog["tracks_by_popularity"],track_rating, lt.newList("ARRAY_LIST"))
        exists_track_rating = mp.get(catalog["tracks_by_popularity"], track_rating)
        lt.addLast(exists_track_rating["value"], track)

    #=================[R4]=====================
    tracks_byArtist(catalog, track)

    #=================[R5]=====================
    album_name_for_key = mp.get(catalog["id_albums"], track["album_id"])
    
    if album_name_for_key != None:
        album_name_for_key = album_name_for_key["value"]["name"]
    
    if album_name_for_key == None:
        pass
    else:
        list_album_tracks = mp.get(catalog["tracks_in_album"], album_name_for_key)

        if list_album_tracks:
            insort_right_r5_2(list_album_tracks["value"], track, lo=1,hi=None)
        
        else:
            mp.put(catalog["tracks_in_album"], album_name_for_key , lt.newList("ARRAY_LIST"))
            list_album_tracks = mp.get(catalog["tracks_in_album"], album_name_for_key)
            lt.addLast(list_album_tracks["value"], track)

    #=================[R6]=====================
    available_markets = track['available_markets']
    str_lista_markets = available_markets[2:(len(available_markets)-2)]
    lista_markets = str_lista_markets.split("', '")
    

    distribution = len(lista_markets)
    track['distribution'] = distribution
    
    
def tracks_byArtist(catalog, track):
    artists_id = track["artists_id"].strip("[").strip('"').strip("]").strip('[').replace("'","").split(",")
    
    for artist_id in artists_id:
        artist_id = artist_id.strip(" ")
        if artist_id == '':
            pass 
        else:
            artist = mp.get(catalog['id_artists'], artist_id)['value']
            artist_name = artist['name']
            exist_name = mp.get(catalog['tracks_by_artist'], artist_name)
            
            
            if exist_name:
                insort_right_r4(exist_name["value"], track, lo=1, hi=None)
                
            else:           #Si no existe el id, crear la lista
                mp.put(catalog['tracks_by_artist'], artist_name, lt.newList('ARRAY_LIST'))
                exists_name = mp.get(catalog["tracks_by_artist"], artist_name)
                lt.addLast(exists_name["value"], track)
                    
                


####################################################################################################
def addAlbum(catalog, album):
    album['total_tracks'] = int(float(album['total_tracks']))
    lt.addLast(catalog["albums"], album)

    #=================[Id]====================
    mp.put(catalog['id_albums'], album['id'], album)

    #=================[R1]=================
    album["release_date"] = str_to_date(album["release_date"], album["release_date_precision"])
    anio_album = str(album["release_date"])[:4]
    exists_year = mp.get(catalog["albums_per_year"], anio_album)

    if exists_year:
        insort_right_r1(exists_year["value"], album, lo=1,hi=None)

    else:
        mp.put(catalog["albums_per_year"], anio_album, lt.newList("ARRAY_LIST"))
        exists_year = mp.get(catalog["albums_per_year"], anio_album)
        lt.addLast(exists_year["value"], album)
    #======================================

    #=================[R5]=================
    artist_name_for_key = mp.get(catalog["id_artists"], album["artist_id"])
    
    if artist_name_for_key != None:
        artist_name_for_key = artist_name_for_key["value"]["name"]
    
    if artist_name_for_key == None:
        pass
    else:
        list_artist_albums = mp.get(catalog["albums_by_artist"], artist_name_for_key)

        if list_artist_albums:
            insort_right_r5(list_artist_albums["value"],album, lo=1,hi=None)
        
        else:
            mp.put(catalog["albums_by_artist"], artist_name_for_key, lt.newList("ARRAY_LIST"))
            list_artist_albums = mp.get(catalog["albums_by_artist"], artist_name_for_key)
            lt.addLast(list_artist_albums["value"], album)

######################################################################################################
def addArtist(catalog, artist):
    artist['artist_popularity'] = int(float(artist['artist_popularity']))
    artist['followers'] = int(float(artist['followers']))
    lt.addLast(catalog["artists"], artist)

    #=================[Id]====================
    mp.put(catalog['id_artists'], artist['id'], artist)
    
    #==================[R2]===================
    art_popularity = str(artist['artist_popularity'])
    exist_pop = mp.get(catalog['artists_per_popularity'], art_popularity)

    if exist_pop:
        insort_right_r2(exist_pop['value'], artist, lo = 1, hi = None)
    else:
        mp.put(catalog['artists_per_popularity'], art_popularity, lt.newList('ARRAY_LIST'))
        exists_pop = mp.get(catalog["artists_per_popularity"], art_popularity) 
        lt.addLast(exists_pop["value"], artist)


    


# Funciones utilizadas para comparar elementos
def compareGenres(keygenre, genre):
    genreEntry = me.getKey(genre)
    if keygenre == genreEntry:
        return 0 
    elif keygenre > genreEntry:
        return 1
    else:
        return -1
# Funciones por requerimiento 
#=================[R1]=================
def str_to_date(string, precision):
    if precision == "year":
        return dt.strptime(string,"%Y").date()
    elif precision == "month":
        string= string[:4] + "19" + string[4:]              #Todos los 'month' corresponden con fechas de los 1900' 
        return dt.strptime(string, "%b-%Y").date()                 #Todos son mon-XX por lo que extraemos los XX
    return dt.strptime(string, "%Y-%m-%d").date()

def insort_right_r1(lista, album, lo=1, hi=None):
    """Insert item x in list a, and keep it sorted assuming a is sorted.

    If x is already in a, insert it to the right of the rightmost x.

    Optional args lo (default 0) and hi (default len(a)) bound the
    slice of a to be searched.
    """
    if hi is None:
        hi = lt.size(lista) + 1
    while lo < hi:
        mid = (lo+hi)//2
        if album["release_date"] < lt.getElement(lista, mid)["release_date"]: 
            hi = mid
        
        else:
             lo = mid+1
    lt.insertElement(lista, album, lo)

def answer_r1(catalog, albumes_del_anio):
    """
    Función principal del requerimiento 1
    """
    lista_anio = mp.get(catalog["model"]["albums_per_year"], albumes_del_anio)
    
    if lista_anio == None:
        return None, None, None
    lista_anio = mp.get(catalog["model"]["albums_per_year"], albumes_del_anio)["value"]
    num_albums = mp.size(lista_anio)
    answer_list_r1 = tomar_primeros_ultimos(lista_anio)


    asc_artists = lt.newList('ARRAY_LIST')
    for album in lt.iterator(answer_list_r1):
        asc_art = find_asc_artist(catalog, album)
        lt.addLast(asc_artists, asc_art)

    return answer_list_r1, asc_artists, num_albums

def find_asc_artist(catalog, album):
    id_artist = album['artist_id']
    artist = mp.get(catalog['model']['id_artists'], id_artist)
    if artist:
        return artist['value']['name']
    else:
        return 'Unknown'

#=====================[R2]================================
def answer_r2(catalog, inp_popularity):
    
    lista_popu = mp.get(catalog['model']['artists_per_popularity'], str(inp_popularity))
    if lista_popu == None:
        return None, None, None

    lista_popu = mp.get(catalog['model']['artists_per_popularity'], str(inp_popularity))['value']
    num_artists = lt.size(lista_popu)
    lista_popu_ord = insertion.sort(lista_popu, cmpR2)
    answer_list_r2 = tomar_primeros_ultimos(lista_popu_ord)

    asc_tracks = lt.newList('ARRAY_LIST')
    for artist in lt.iterator(answer_list_r2):
        asc_track = find_asc_track(catalog, artist)
        lt.addLast(asc_tracks, asc_track)

    return answer_list_r2, asc_tracks, num_artists

def cmpR2(artist1, artist2):
    menor = True
    if artist1['followers'] < artist2['followers']:
        menor = False
    elif artist1['followers'] == artist2['followers']:
        if artist1['name'] < artist2['name']:
            menor = False
    return menor

def find_asc_track(catalog, artist):
    id_track = artist['track_id']
    artist = mp.get(catalog['model']['id_tracks'], id_track)
    if artist:
        return artist['value']['name']
    else:
        return 'Unknown'


def insort_right_r2(lista, artist, lo=1, hi=None):
    """Insert item x in list a, and keep it sorted assuming a is sorted.

    If x is already in a, insert it to the right of the rightmost x.

    Optional args lo (default 0) and hi (default len(a)) bound the
    slice of a to be searched.
    """
    if hi is None:
        hi = lt.size(lista) + 1
    while lo < hi:
        mid = (lo+hi)//2
        if artist["followers"] > lt.getElement(lista, mid)["followers"]: 
            hi = mid
        else:
             lo = mid+1
    lt.insertElement(lista, artist, lo)

#=====================[R3]================================

def insort_right_r3(lista, track, lo=1, hi=None):
    """Insert item x in list a, and keep it sorted assuming a is sorted.

    If x is already in a, insert it to the right of the rightmost x.

    Optional args lo (default 0) and hi (default len(a)) bound the
    slice of a to be searched.
    """
    if hi is None:
        hi = lt.size(lista) + 1
    while lo < hi:
        mid = (lo+hi)//2
        if float(track["duration_ms"]) > float(lt.getElement(lista, mid)["duration_ms"]): 
            hi = mid
        else:
             lo = mid+1
    lt.insertElement(lista, track, lo)

def cmpR3(track1, track2):
    mayor = False
    if float(track1["duration_ms"]) == float(track2["duration_ms"]):
        if track1["name"] > track2["name"]:
            mayor = True
    elif float(track1["duration_ms"]) > float(track2["duration_ms"]):
        mayor = True
    return mayor
    

def answer_R3(catalog, inp_track_popularity):
    list_tracks_with_popularity = mp.get(catalog["model"]["tracks_by_popularity"], inp_track_popularity)
    if list_tracks_with_popularity == None:
        return None, None, None, None
    
    list_tracks_with_popularity =  list_tracks_with_popularity["value"]
    list_tracks_with_popularity_sort = insertion.sort(list_tracks_with_popularity, cmpR3)

    tam_list = lt.size(list_tracks_with_popularity_sort)

    list_resp_R3 = tomar_primeros_ultimos(list_tracks_with_popularity_sort)
    
    names_albums = lt.newList("ARRAY_LIST")
    
    names_artists = lt.newList("ARRAY_LIST")
    a = 1
    for track in lt.iterator(list_resp_R3):
        
        id_album = track["album_id"]
        exist_album = mp.get(catalog["model"]["id_albums"], id_album)

        if exist_album: 
            lt.addLast(names_albums, exist_album["value"]["name"])
        else:
            lt.addLast(names_albums, "Not Found")
        
        artists_ids = track["artists_id"].strip("[").strip('"').strip("]").strip('[').replace("'","").split(",")
        names = lt.newList("ARRAY_LIST")
        for id in artists_ids:
            id = id.strip(" ")
            exists_name = mp.get(catalog["model"]["id_artists"], id)
            if exists_name:
                lt.addLast(names,exists_name["value"]["name"])
            else:
                lt.addLast(names,"Not Found")
        lt.addLast(names_artists, names)
    return tam_list, list_resp_R3, names_albums, names_artists        
        


#====================[R4]=====================================
def answer_r4(catalog, artist_name, country):
    catalog = catalog['model']

    exist_name = mp.get(catalog['tracks_by_artist'], artist_name)
    if exist_name == None:
        return None, None, None
    else:

        list_artist = exist_name['value']
        
        rta_list_havoc = searchCountry(list_artist, country)

        rta_list_ord = insertion.sort(rta_list_havoc, cmpfunction=cmpR4)

        popular_track = lt.getElement(rta_list_ord, 1)
        info_r4(catalog, popular_track)
        num_tracks = uniqueTracks(rta_list_ord)
        num_albums = uniqueAlbums(rta_list_ord)
    


    return popular_track, num_tracks, num_albums

def searchCountry(lista, inp_country):
    rta_list = lt.newList('ARRAY_LIST')

    for track in lt.iterator(lista):
        countries = track["available_markets"].strip("[").strip('"').strip("]").strip('[').replace("'","").split(",")
        
        for country in countries:
            country = country.strip(' ')
            if country == inp_country:
                lt.addLast(rta_list, track)
                break
            
    return rta_list

def cmpR4(track1, track2):
    menor = True
    # De mayor a menor la popularidad
    if track1['popularity'] < track2['popularity']:
        menor = False

    elif track1['popularity'] == track2['popularity']:
        
        # De mayor a menor la duración
        if track1['duration_ms'] < track2['duration_ms']:
            menor = False
        
        elif track1['duration_ms'] == track2['duration_ms']:
            
            if track1['name'] > track2['name']:
                menor = False

    return menor

def uniqueAlbums(list_tracks):

    my_map = mp.newMap(maptype='PROBING',
                       loadfactor=our_loadfactor,
                       numelements=60)

    for track in lt.iterator(list_tracks):
        album_id = track['album_id']
        mp.put(my_map, album_id, True)
    
    return mp.size(my_map)

def uniqueTracks(list_tracks):

    my_map = mp.newMap(maptype='PROBING',
                       loadfactor=our_loadfactor,
                       numelements=60)

    for track in lt.iterator(list_tracks):
        track_id = track['id']
        mp.put(my_map, track_id, True)
    
    return mp.size(my_map)

def info_r4(catalog, popular_track):
    album_id = popular_track['album_id']
    album = mp.get(catalog['id_albums'], album_id)['value']
    album_name = album['name']
    album_date = album['release_date']
    #1
    popular_track['album_name'] = album_name
    #2
    popular_track['release_date'] = album_date

    artists_id = popular_track["artists_id"].strip("[").strip('"').strip("]").strip('[').replace("'","").split(",")
    
    artists = ''
    for artist_id in artists_id:
        artist_id = artist_id.strip(" ")
        if artist_id == '':
            pass 
        else:
            artist = mp.get(catalog['id_artists'], artist_id)['value']
            artist_name = artist['name']

            artists += artist_name + ', '
    
    #3
    popular_track['artists_name'] = artists

def insort_right_r4(lista, track, lo=1, hi=None):
    """Insert item x in list a, and keep it sorted assuming a is sorted.

    If x is already in a, insert it to the right of the rightmost x.

    Optional args lo (default 0) and hi (default len(a)) bound the
    slice of a to be searched.
    """
    if hi is None:
        hi = lt.size(lista) + 1
    while lo < hi:
        mid = (lo+hi)//2
        if track["popularity"] > lt.getElement(lista, mid)["popularity"]: 
            hi = mid
        else:
             lo = mid+1
    lt.insertElement(lista, track, lo)
#====================[R5]=====================================

def insort_right_r5(lista, album, lo=1, hi=None):
    """Insert item x in list a, and keep it sorted assuming a is sorted.

    If x is already in a, insert it to the right of the rightmost x.

    Optional args lo (default 0) and hi (default len(a)) bound the
    slice of a to be searched.
    """
    if hi is None:
        hi = lt.size(lista) + 1
    while lo < hi:
        mid = (lo+hi)//2
        if album["release_date"] > lt.getElement(lista, mid)["release_date"]: 
            hi = mid
        
        else:
             lo = mid+1
    lt.insertElement(lista, album, lo)

def insort_right_r5_2(lista, track, lo=1, hi=None):
    """Insert item x in list a, and keep it sorted assuming a is sorted.

    If x is already in a, insert it to the right of the rightmost x.

    Optional args lo (default 0) and hi (default len(a)) bound the
    slice of a to be searched.
    """
    if hi is None:
        hi = lt.size(lista) + 1
    while lo < hi:
        mid = (lo+hi)//2
        if float(track["popularity"]) > float(lt.getElement(lista, mid)["popularity"]): 
            hi = mid
        
        else:
             lo = mid+1
    lt.insertElement(lista, track, lo)   

def answer_R5(catalog, artist_name):

    list_albums = mp.get(catalog["model"]["albums_by_artist"], artist_name)

    if list_albums == None:
        return None, None, None, None
    
    list_albums = list_albums["value"]
    album_types = count_album_type(list_albums)

    insertion.sort(list_albums,  albums_by_date)
 
    resp_albums = tomar_primeros_ultimos(list_albums)


    resp_tracks = lt.newList("ARRAY_LIST")
    names_artists = lt.newList("ARRAY_LIST")

    for album in lt.iterator(resp_albums):
        name_album = album["name"]
        tracks_of_album = mp.get(catalog["model"]["tracks_in_album"], name_album)["value"]
        insertion.sort(tracks_of_album ,tracks_by_popularity)
        most_popular_track = lt.getElement(tracks_of_album, 1)
        lt.addLast(resp_tracks, most_popular_track )
        
        artists_ids = most_popular_track["artists_id"].strip("[").strip('"').strip("]").strip('[').replace("'","").split(",")
        
        names = lt.newList("ARRAY_LIST")
        for id in artists_ids: 
            id = id.strip(" ")
            exists_name = mp.get(catalog["model"]["id_artists"], id)
            if exists_name:
                lt.addLast(names, exists_name["value"]["name"])
            else:
                lt.addLast(names, "Not Found")
        lt.addLast(names_artists, names)

    return album_types, resp_albums, resp_tracks, names_artists


def count_album_type(list_albums):
    singles = 0 
    compilations = 0 
    albumes = 0
    total = lt.size(list_albums)

    for album in lt.iterator(list_albums):
        if album["album_type"] == "single":
            singles += 1
        elif album["album_type"] == "compilation":
            compilations += 1
        elif album["album_type"] == "album":
            albumes += 1

    return (singles, compilations, albumes, total)



def albums_by_date(album1, album2):
    """
    Devuelve verdadero (True) si el año de publicación del album1 es menor que los del album2
    Args:
    album1: informacion del primer album que incluye su fecha en time
    album2: informacion del segundo artista que incluye su fecha en time
    """
    menor = False
    if album1["release_date"] == album2["release_date"]:
        if album1["name"] < album2["name"]:

            menor = True
    else:
        if album1["release_date"] > album2["release_date"]:
            menor = True

    return menor

def tracks_by_popularity(track1, track2):
    menor = False 
    if float(track1['popularity']) == float(track2['popularity']):
        if float(track1["duration_ms"]) == float(track2["duration_ms"]):
            if track1["name"] < track2["name"]:
                menor = True        
        else:
            if float(track1["duration_ms"]) > float(track2["duration_ms"]):
                menor = True
    else:
        if float(track1['popularity']) > float(track2['popularity']):
            menor = True
    return menor

#====================[R6]=====================================
def answer_r6(catalog, artist_name, country, n):
    catalog = catalog['model']

    exist_name = mp.get(catalog['tracks_by_artist'], artist_name)
    if exist_name == None:
        return None, None
    else:

        list_artist = exist_name['value']
        
        rta_list_havoc = searchCountry(list_artist, country)
        rta_list_ord = insertion.sort(rta_list_havoc, cmpfunction=cmpR6)
        num_tracks = lt.size(rta_list_ord)
        
    

    if num_tracks < n:
        top_n = rta_list_ord
    else:
        top_n = lt.subList(rta_list_ord, 1, n)

    answer_list = tomar_primeros_ultimos(top_n)
    info_r6(catalog, answer_list)
    
    return answer_list, num_tracks





def cmpR6(track1, track2):
    menor = True
    # De mayor a menor la popularidad
    if track1['popularity'] < track2['popularity']:
        menor = False

    elif track1['popularity'] == track2['popularity']:
        
        # De mayor a menor la duración
        if track1['duration_ms'] < track2['duration_ms']:
            menor = False
        
        elif track1['duration_ms'] == track2['duration_ms']:
            
            if track1['name'] > track2['name']:
                menor = False

    return menor

def info_r6(catalog, lista):
    for i in lt.iterator(lista):
        info_r4(catalog, i)


#============[para todas]=====================================
def tomar_primeros_ultimos(lista):
    tam = lt.size(lista)
    if tam >= 3:
        answer = lt.newList('ARRAY_LIST')
        a1 = lt.getElement(lista,1)
        a2 = lt.getElement(lista,2)
        a3 = lt.getElement(lista,3)
        a4 = lt.getElement(lista,lt.size(lista)-2)
        a5 = lt.getElement(lista,lt.size(lista)-1)
        a6 = lt.getElement(lista,lt.size(lista))
        
        lt.addLast(answer, a1)
        lt.addLast(answer, a2)
        lt.addLast(answer, a3)
        lt.addLast(answer, a4)
        lt.addLast(answer, a5)
        lt.addLast(answer, a6)
    elif tam == 1:
        answer = lt.newList('ARRAY_LIST')
        a1 = lt.getElement(lista, 1)
        
        lt.addLast(answer, a1)
    elif tam == 2:
        answer = lt.newList('ARRAY_LIST')
        a1 = lt.getElement(lista, 1)
        a2 = lt.getElement(lista,2)

        lt.addLast(answer, a1)
        lt.addLast(answer, a2)

    return answer

