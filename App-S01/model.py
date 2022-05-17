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


from os import name
import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import mergesort as mer
assert cf
import operator
import math as ma

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

# Funciones para agregar informacion al catalogo
def inicializarCatalogo():
    catalog={}
    catalog['canciones'] = mp.newMap(102001, 
                        maptype = 'PROBING',
                        loadfactor = 0.8)
    catalog['artistas'] = mp.newMap(56149, 
                        maptype = 'PROBING',
                        loadfactor = 0.8)
    catalog['artistasLlaveNombre'] = mp.newMap(56149, 
                        maptype = 'PROBING',
                        loadfactor = 0.8)
    catalog['albumes'] = mp.newMap(75521, 
                        maptype = 'PROBING',
                        loadfactor = 0.8)
    catalog['albumesAnio'] = mp.newMap(113, 
                        maptype = 'PROBING',
                        loadfactor = 0.8)
    catalog['artistasPopularidad'] = mp.newMap(113, 
                        maptype = 'PROBING',
                        loadfactor = 0.8)
    catalog['paisCanciones'] = mp.newMap(197, 
                        maptype = 'PROBING',
                        loadfactor = 0.8)
    catalog['paisAlbumes'] = mp.newMap(197, 
                        maptype = 'PROBING',
                        loadfactor = 0.8)
    catalog['cancionesPopularidad'] = mp.newMap(113, 
                        maptype = 'PROBING',
                        loadfactor = 0.8)
    catalog['artistaAlbumes'] = mp.newMap(561490, 
                        maptype = 'PROBING',
                        loadfactor = 0.8)
    catalog['cancionesAlbumId'] =  mp.newMap(75521, 
                        maptype = 'PROBING',
                        loadfactor = 0.8)
    catalog['listaArtistas']=lt.newList('ARRAY_LIST')
    catalog['listaAlbumes']=lt.newList('ARRAY_LIST')
    catalog['listaCanciones']=lt.newList('ARRAY_LIST')
    return catalog

# Funciones para creacion de datos
def addArtistsId(catalogo, artista):
    idArtista=artista['id']
    mp.put(catalogo['artistas'],idArtista, artista )
    listaArtistas=catalogo['listaArtistas']
    lt.addLast(listaArtistas, artista)
    return listaArtistas

def addArtistsName(catalogo, artista):
    nombreArtista=artista['name']
    mp.put(catalogo['artistasLlaveNombre'],nombreArtista, artista )

def addCancionId(catalogo, cancion):
    idCancion=cancion['id']
    mp.put(catalogo['canciones'],idCancion, cancion )
    listaCanciones=catalogo['listaCanciones']
    lt.addLast(listaCanciones, cancion)
    return listaCanciones 

def addAlbumId(catalogo, album):
    idAlbum=album['id']
    mp.put(catalogo['albumes'],idAlbum, album )
    listaAlbumes=catalogo['listaAlbumes']
    lt.addLast(listaAlbumes,album)
    return listaAlbumes

# Funciones de consulta

def artistsSize(catalogo):
    return mp.size(catalogo['artistas'])
def cancionesSize(catalogo):
    return mp.size(catalogo['canciones'])
def albumesSize(catalogo):
    return mp.size(catalogo['albumes'])

#requerimiento 0 carga de datos
def numeroCancionesAlbum(catalogo, albumId):
    llaveValor=mp.get(catalogo['albumes'], albumId)
    album=me.getValue(llaveValor)
    numeroCanciones=album['total_tracks']
    return numeroCanciones


#requerimiento 1
def addAlbumAnio(catalogo, album):
    anio=str(album['release_date'][:4])
    if anio != '':
        if mp.contains(catalogo['albumesAnio'], anio) == False:
            listaAlbumes=lt.newList('ARRAY_LIST')
            lt.addLast(listaAlbumes,album)
            mp.put(catalogo['albumesAnio'], anio, listaAlbumes)
        else:
            llaveValor=mp.get(catalogo['albumesAnio'], anio)
            listaAlbumes=me.getValue(llaveValor)
            lt.addLast(listaAlbumes, album)
    else:
        anio='UNKNWON'
        if mp.contains(catalogo['albumesAnio'], anio) == False:
            listaAlbumes=lt.newList('ARRAY_LIST')
            lt.addLast(listaAlbumes,album)
            mp.put(catalogo['albumesAnio'], anio, listaAlbumes)
        else:
            llaveValor=mp.get(catalogo['albumesAnio'], anio)
            listaAlbumes=me.getValue(llaveValor)
            lt.addLast(listaAlbumes, album)
        
def listaOrdenadalbumesAnio(catalogo, anio):
    llaveValor=mp.get(catalogo['albumesAnio'], anio)
    listaAlbumes=me.getValue(llaveValor)
    mer.sort(listaAlbumes, cmpAlbumesNombre)
    return(listaAlbumes)

def cmpAlbumesNombre(album1, album2):
    return album1['name']<album2['name']

#requerimiento 2
def addArtistaPopularidad(catalogo, artista):
    popularidad=float(artista['artist_popularity'])
    popularidad=ma.trunc(popularidad)
    if mp.contains(catalogo['artistasPopularidad'], popularidad)==False:
        listaArtistas=lt.newList('ARRAY_LIST')
        lt.addLast(listaArtistas, artista )
        mp.put(catalogo['artistasPopularidad'], popularidad,listaArtistas)
    else:
        llaveValor=mp.get(catalogo['artistasPopularidad'], popularidad)
        listaArtistas=me.getValue(llaveValor)
        lt.addLast(listaArtistas, artista)

def listaOrdenadaArtistasPopularidad(catalogo, popularidad):
    llaveValor=mp.get(catalogo['artistasPopularidad'], popularidad)
    listaArtistas=me.getValue(llaveValor)
    listaArtistas=mer.sort(listaArtistas,cmpArtistasFollowers)
    return (listaArtistas)

def cmpArtistasFollowers(artista1, artista2):
    return float(artista1['followers'])>float(artista2['followers'])

#requerimiento 3
def addCancionesPopularidad(catalogo, cancion):
    popularidad=float(cancion['popularity'])
    popularidad=ma.trunc(popularidad)
    if mp.contains(catalogo['cancionesPopularidad'], popularidad) == False:
        listaCanciones=lt.newList('ARRAY_LIST')
        lt.addLast(listaCanciones, cancion)
        mp.put(catalogo['cancionesPopularidad'],popularidad, listaCanciones)
    else:
        llaveValor=mp.get(catalogo['cancionesPopularidad'], popularidad)
        listaCanciones=me.getValue(llaveValor)
        lt.addLast(listaCanciones, cancion)

def listaOrdenadaCancionesPopularidad(catalogo, popularidad):
    llaveValor =mp.get(catalogo["cancionesPopularidad"], popularidad)
    listaCanciones=me.getValue(llaveValor)
    mer.sort(listaCanciones, cmpCancionesDuration)
    return listaCanciones 

def cmpCancionesDuration(cancion1, cancion2):
        return cancion1['duration_ms']>cancion2['duration_ms']
def cmpCancionesNombre(cancion1, cancion2):
     return cancion1['name']<cancion2['name']

#requerimiento 4
def addCancionesPaises(catalogo, cancion):
    availableMarkets=str(cancion['available_markets'])
    listaPaisesCancion=eval(availableMarkets)
    if availableMarkets != '[]':
        if type(listaPaisesCancion)==str:
            listaPaisesCancion=eval(listaPaisesCancion)
        elif type(listaPaisesCancion)==list:
            listaPaisesCancion=listaPaisesCancion
        for pais in listaPaisesCancion:
            if mp.contains(catalogo['paisCanciones'], pais ) == False:
                listaCanciones=lt.newList('ARRAY_LIST')
                lt.addLast(listaCanciones, cancion)
                mp.put(catalogo['paisCanciones'],pais,listaCanciones)
            else:
                llaveValor=mp.get(catalogo['paisCanciones'],pais)
                listaCanciones=me.getValue(llaveValor)
                lt.addLast(listaCanciones, cancion)
    else:
        llaveVacio='vacio'
        if mp.contains(catalogo['paisCanciones'],llaveVacio)==False:
            listaCanciones=lt.newList('ARRAY_LIST')
            lt.addLast(listaCanciones, cancion)
            mp.put(catalogo['paisCanciones'],llaveVacio,listaCanciones)
        else:
            llaveValor=mp.get(catalogo['generos'],llaveVacio)
            listaCanciones=me.getValue(llaveValor)
            lt.addLast(listaCanciones, cancion)
    
def listaOrdenadaPaisCanciones(catalogo, codigoPais):
    llaveValor=mp.get(catalogo['paisCanciones'], codigoPais)
    listaCanciones=me.getValue(llaveValor)
    return(listaCanciones)

def listaOrdenadaPaisAlbumes(catalogo, codigoPais):
    llaveValor=mp.get(catalogo['paisAlbumes'], codigoPais)
    listaCanciones=me.getValue(llaveValor)
    return(listaCanciones)

def cancionPopularArtistaPais(catalogo, listaCancionesPais, artista):
    listaCancionesArtista=lt.newList('ARRAY_LIST')
    llaveValor=mp.get(catalogo['artistasLlaveNombre'],artista)
    idArtista=(me.getValue(llaveValor)['id'])
    for cancion in lt.iterator(listaCancionesPais):
        if str(idArtista) in str(cancion['artists_id']):
            lt.addLast(listaCancionesArtista,cancion)
    listaCancionesArtista=mer.sort(listaCancionesArtista, cmpCancionesPopularidad)
    cancionMasPopular=lt.getElement(listaCancionesArtista,1)
    return(cancionMasPopular, listaCancionesArtista)

def cmpCancionesPopularidad(cancion1, cancion2):
    return cancion1['popularity']>cancion2['popularity']

#Requerimirnto 5:
def addArtistaAlbumes(catalogo, album):
    idArtista=str(album['artist_id'])
    if mp.contains(catalogo['artistas'],idArtista):
        llaveValorId=mp.get(catalogo['artistas'],idArtista)
        nombre=me.getValue(llaveValorId)['name']

        if mp.contains(catalogo['artistaAlbumes'],nombre)==False:
            listaAlbumes=lt.newList('ARRAY_LIST')
            lt.addLast(listaAlbumes,album)
            mp.put(catalogo['artistaAlbumes'],nombre, listaAlbumes )
        else:
            llaveValor=mp.get(catalogo['artistaAlbumes'], nombre)
            listaAlbumes=me.getValue(llaveValor)
            lt.addLast(listaAlbumes, album)
    else:
        llave='artistaNoPresente'
        if mp.contains(catalogo['artistaAlbumes'], llave)==False:
            listaAlbumes=lt.newList('ARRAY_LIST')
            lt.addLast(listaAlbumes, album)
            mp.put(catalogo['artistaAlbumes'], llave, listaAlbumes)
        else:
            llaveValor=mp.get(catalogo['artistaAlbumes'], llave)
            listaAlbumes=me.getValue(llaveValor)
            lt.addLast(listaAlbumes, album)


def listaAlbumesArtista(catalogo, nombre):
    llaveValor=mp.get(catalogo['artistaAlbumes'], nombre)
    listaAlbumesArtista=me.getValue(llaveValor)
    mer.sort(listaAlbumesArtista, cmpreleasedate)
    return listaAlbumesArtista

def cmpreleasedate(album1, album2):
    return album1['release_date'][:4]>album2['release_date'][:4]

#funciones Catacteristicas especiales
def nombreArtistaId(catalogo, artistId):
    if mp.contains(catalogo['artistas'],artistId)==True:
        llaveValor=mp.get(catalogo['artistas'], artistId)
        nombre=me.getValue(llaveValor)['name']
    else:
        nombre='UNKNOWN'
    return nombre
def nombreCancionId(catalogo, trackId):
    if mp.contains(catalogo['canciones'],trackId)==True:
        llaveValor=mp.get(catalogo['canciones'], trackId)
        nombre=me.getValue(llaveValor)['name']
    else:
        nombre='UNKNOWN'
    return nombre

def nombreAlbumId(catalogo, albumId):
    if mp.contains(catalogo['albumes'], albumId):
        llaveValor=mp.get(catalogo['albumes'], albumId)
        nombre=me.getValue(llaveValor)['name']
    else:
        nombre='UNKNOWN'
    return nombre

def nombreVariosArtistasId(catalogo, artistsId):
    lista=[]
    if type(artistsId)==str:
        artistsId=eval(artistsId)
        for artist in artistsId:
            nombre=nombreArtistaId(catalogo, artist)
            lista.append(nombre)
    else:
        for artist in artistsId:
            nombre=nombreArtistaId(catalogo, artist)
            lista.append(nombre)
    return lista

def addAlbumesPaises(catalogo, cancion):
    availableMarkets=str(cancion['available_markets'])
    listaPaisesCancion=eval(availableMarkets)
    if availableMarkets != '[]':
        if type(listaPaisesCancion)==str:
            listaPaisesCancion=eval(listaPaisesCancion)
        elif type(listaPaisesCancion)==list:
            listaPaisesCancion=listaPaisesCancion

        for pais in listaPaisesCancion:
            if mp.contains(catalogo['paisAlbumes'], pais ) == False:
                listaCanciones=lt.newList('ARRAY_LIST')
                lt.addLast(listaCanciones, cancion)
                mp.put(catalogo['paisAlbumes'],pais,listaCanciones)
            else:
                llaveValor=mp.get(catalogo['paisAlbumes'],pais)
                listaCanciones=me.getValue(llaveValor)
                lt.addLast(listaCanciones, cancion)
    else:
        llaveVacio='vacio'
        if mp.contains(catalogo['paisAlbumes'],llaveVacio)==False:
            listaCanciones=lt.newList('ARRAY_LIST')
            lt.addLast(listaCanciones, cancion)
            mp.put(catalogo['paisAlbumes'],llaveVacio,listaCanciones)
        else:
            llaveValor=mp.get(catalogo['generos'],llaveVacio)
            listaCanciones=me.getValue(llaveValor)
            lt.addLast(listaCanciones, cancion)

def listaAlbumesArtistaPais(catalogo, listaAlbumesPais, artista):
    listaAlbumesArtista=lt.newList('ARRAY_LIST')
    llaveValor=mp.get(catalogo['artistasLlaveNombre'],artista)
    idArtista=(me.getValue(llaveValor)['id'])
    for album in lt.iterator(listaAlbumesPais):
        if str(idArtista) in str(album['artist_id']):
            lt.addLast(listaAlbumesArtista,album)
    return listaAlbumesArtista
    
def tipoAlbumesArtista(listaAlbumesArtista):
    sencillo=lt.newList('ARRAY_LIST')
    recopilacion=lt.newList('ARRAY_LIST')
    album=lt.newList('ARRAY_LIST')
    for albumes in lt.iterator(listaAlbumesArtista):
        if albumes['album_type']=='single':
            lt.addLast(sencillo,albumes )
        elif albumes['album_type']=='compilation':
            lt.addLast(recopilacion, albumes)
        elif albumes['album_type']== 'album':
            lt.addLast(album,albumes)
    return sencillo, recopilacion, album

def addCancionesAlbumId(catalogo, cancion):
    albumId=cancion['album_id']
    if mp.contains(catalogo['cancionesAlbumId'], albumId)==False:
        listaCanciones=lt.newList('ARRAY_LIST')
        lt.addLast(listaCanciones, cancion)
        mp.put(catalogo['cancionesAlbumId'],albumId, listaCanciones )
    else:
        llaveValor=mp.get(catalogo['cancionesAlbumId'],albumId)
        listaCanciones=me.getValue(llaveValor)
        lt.addLast(listaCanciones, cancion)

def cancionPopularAlbum(catalogo, albumId):
    llaveValor=mp.get(catalogo['cancionesAlbumId'], albumId)
    listaCanciones=me.getValue(llaveValor)
    listaCanciones=mer.sort(listaCanciones, cmpCancionesPopularidad)
    cancion=lt.getElement(listaCanciones, 1)

    return cancion

# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamientos

#requerimiento 1
