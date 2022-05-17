"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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
import sys
import controller
from DISClib.ADT import list as lt
assert cf
from DISClib.ADT import map as mp
import sys
from DISClib.DataStructures import mapentry as me
default_limit = 100000
sys.setrecursionlimit(default_limit*10)

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("\nBienvenido")
    print("0- Cargar información en el catálogo")
    print("1- Examinar los álbumes en un año de interés")
    print('2- Encontrar los artistas por popularidad')
    print('3- Encontrar las canciones por popularidad')
    print('4- Encontrar la canción más popular de un artista en un pais')
    print('5- Encontrar la discografía de un artista')


def printResultsAlbums(lista, sample):
    print('\n----------------------------------------------------------------------------')
    print('Los primeros 3 ALBUMES cargados son: ')
    i=1
    while i<=sample:
        album=lt.getElement(lista,i)
        print('\nNombre: '+album['name']+ '\nTipo Album'+album['album_type']
        +'\nMercados disponibles: '+album['available_markets']+'\nFecha de Lanzamiento: '+album['release_date'])
        i+=1
    print('\n----------------------------------------------------------------------------')
    print('los ultimos 3 ALBUMES cargados son')
    i=lt.size(lista)-(sample-1)
    while i<=lt.size(lista):
        album=lt.getElement(lista,i)
        print('\nNombre: '+album['name']+ '\nTipo Album'+album['album_type']
        +'\nMercados disponibles: '+album['available_markets']+'\nFecha de Lanzamiento: '+album['release_date'])
        i+=1
    print('\n----------------------------------------------------------------------------')

def printResultsartistas(lista, sample):
    print('\n----------------------------------------------------------------------------')
    print('Los primeros 3 ARTISTAS cargados son: ')
    i=1
    while i<=sample:
        artista=lt.getElement(lista,i)
        print('\nNombre: '+artista['name']+ '\nGeneros'+artista['genres']
        +'\nPopularidad: '+artista['artist_popularity']+'\nNumero de seguidores: '+artista['followers'])
        i+=1
    print('\n----------------------------------------------------------------------------')
    print('los ultimos 3 ARTISTAS cargados son')
    i=lt.size(lista)-(sample-1)
    while i<=lt.size(lista):
        artista=lt.getElement(lista,i)
        print('\nNombre: '+artista['name']+ '\nGeneros'+artista['genres']
        +'\nPopularidad'+artista['artist_popularity']+'\nNumero de seguidores: '+artista['followers'])
        i+=1
    print('\n----------------------------------------------------------------------------')

def printResultsCanciones(lista, sample, catalogo):
    print('\n----------------------------------------------------------------------------')
    print('Las primeros 3 CANCIONES cargadas son: ')
    i=1
    while i<=sample:
        cancion=lt.getElement(lista,i)
        numCancionesAlbum=controller.numeroCancionesAlbum(catalogo, cancion['album_id'])
        print('\nNombre: '+cancion['name']+ '\nDuracion [ms]: '+cancion['duration_ms']
        +'\nNumero Canciones en el Album: '+numCancionesAlbum)
        i+=1
    print('\n----------------------------------------------------------------------------')
    print('las ultimos 3 CANCIONES cargadas son')
    i=lt.size(lista)-(sample-1)
    while i<=lt.size(lista):
        cancion=lt.getElement(lista,i)
        numCancionesAlbum=controller.numeroCancionesAlbum(catalogo, cancion['album_id'])
        print('\nNombre: '+cancion['name']+ '\nDuracion [ms]: '+cancion['duration_ms']
        +'\nNumero Canciones en el Album: '+numCancionesAlbum)
        i+=1
    print('\n----------------------------------------------------------------------------')

def printResultsReq1(lista, sample, catalogo,time, memory):
    size=lt.size(lista)
    numAlbumes=lt.size(lista)
    print('\nNumero de Albumes en el anio: '+str(numAlbumes)+'\n')
    if size <= sample*2:
        print('Los albumes del anio odenados ALFABETICAMENTE son:')
        for album in lt.iterator(lista):
            artistId=album['artist_id']
            nombreArtista=controller.nombreArtistaId(catalogo, artistId)
            print( 'Nombre: '+ str(album['name']) + '\nFecha publicacion: '+ str(album['release_date']) 
            + "\nTipo de album: " + str(album['album_type'])+'\nArtista asociado: '+ str(nombreArtista) +'\nNumero Canciones: '
            +str(album['total_tracks']))
    else:
        print('--------------------------------------------------------------------------------------------------------------------------------------------------------')
        print('Los primeros 3 ALBUMES ordenados ALFABETICAMENTE son: ')
        i=1
        while i<= sample:
            album= lt.getElement(lista, i )
            artistId=album['artist_id']
            nombreArtista=controller.nombreArtistaId(catalogo, artistId)
            print( '\nNombre: '+ str(album['name']) + '\nFecha publicacion: '+ str(album['release_date'] )
            + "\nTipo de album: " + str(album['album_type'])+'\nArtista asociado: '+ str(nombreArtista) +'\nNumero Canciones: '
            +str(album['total_tracks']))
            i+=1
        print('\n--------------------------------------------------------------------------------------------------------------------------------------------------------')
        print('Los ultimos 3 ALBUMES ordenados ALFABETICAMENTE son: ')
        i=size-(sample-1)
        while i<=size:
            album=lt.getElement(lista,i)
            artistId=album['artist_id']
            nombreArtista=controller.nombreArtistaId(catalogo, artistId)
            print( '\nNombre: '+ str(album['name']) + '\nFecha publicacion: '+ str(album['release_date'])
            + "\nTipo de album: " + str(album['album_type'])+'\nArtista asociado: '+ str(nombreArtista) +'\nNumero Canciones: '
            +str(album['total_tracks'] ))
            i+=1
        print('\n--------------------------------------------------------------------------------------------------------------------------------------------------------')
    print("Tiempo Req1[ms]: ", f"{time:.3f}",
              "\nMemoria Req1[kB]: ", f"{memory:.3f}")
    print('---------------------------------------------------------------------------------------------------\n')

def printResultsReq2(lista, sample, catalogo,time, memory):
    size=lt.size(lista)
    numArtistas=lt.size(lista)
    print('\nNumero artsistas con esta popularidad: '+str(numArtistas)+'\n')
    if size <= sample*2:
        print('Los primeros 3 ARTISTAS con esta popularidad ordenados por sus SEGUIDORES son:')
        for artista in lt.iterator(lista):
            idCancion=artista['track_id']
            nombreCancion=controller.nombreCancionId(catalogo, idCancion)
            print( '\nNombre: '+ str(artista['name']) + '\nPopularidad: '+ str(artista['artist_popularity'])
            + "\nSeguidores: " + str(artista['followers'])+'\nGeneros asociados: '+ str(artista['genres']) +'\nCancion referente: '
            +str(nombreCancion))
    else:
        print('---------------------------------------------------------------------------------------------------')
        print('Los primeros 3 ARTISTAS con esta popularidad ordenados por sus SEGUIDORES son:')
        i=1
        while i<= sample:
            artista=lt.getElement(lista, i)
            idCancion=artista['track_id']
            nombreCancion=controller.nombreCancionId(catalogo, idCancion)
            print( '\nNombre: '+ str(artista['name']) + '\nPopularidad: '+ str(artista['artist_popularity'])
            + "\nSeguidores: " + str(artista['followers'])+'\nGeneros asociados: '+ str(artista['genres']) +'\nCancion referente: '
            +str(nombreCancion))
            i+=1
        print('\n--------------------------------------------------------------------------------------------------')
        print('Los ultimos 3 ARTISTAS con esta popularidad ordenados por sus SEGUIDORES son:')
        i=size-(sample-1)
        while i<=size:
            artista=lt.getElement(lista, i)
            idCancion=artista['track_id']
            nombreCancion=controller.nombreCancionId(catalogo, idCancion)
            print( '\nNombre: '+ str(artista['name']) + '\nPopularidad: '+ str(artista['artist_popularity'])
            + "\nSeguidores: " + str(artista['followers'])+'\nGeneros asociados: '+ str(artista['genres']) +'\nCancion referente: '
            +str(nombreCancion))
            i+=1
        print('\n--------------------------------------------------------------------------------------------------')
        print("Tiempo carga Req2[ms]: ", f"{time:.3f}",
              "\nMemoria carga Req2[kB]: ", f"{memory:.3f}")
    print('---------------------------------------------------------------------------------------------------\n')

def printResultsReq3(lista, sample, catalogo, time, memory):
    size=lt.size(lista)
    numArtistas=lt.size(lista)
    print('\nNumero CANCIONES con esta popularidad: '+str(numArtistas)+'\n')
    if size <= sample*2:
        print('--------------------------------------------------------------------------------------------------')
        print('Las CANCIONES con esta popularidad ordenadas por DURACION son:')
        for cancion in lt.iterator(lista):
            if cancion['lyrics']=='-99':
                lyrics='UNKNOWN'
            else:
                lyrics=cancion['lyrics']
            idAlbum=cancion['album_id']
            idArtists=cancion['artists_id']
            nombreAlbum=controller.nombreAlbumId(catalogo, idAlbum)
            nombreArtistas=controller.nombreVariosArtistasId(catalogo,idArtists)
            print( '\nNombre: '+ str(cancion['name']) + '\nAlbum: '+ str(nombreAlbum)
            + "\nArtistas Involucrados: " + str(nombreArtistas)+'\nPopularidad: '+ str(cancion['popularity']) +'\nDuracion[ms]: '
            +str(cancion['duration_ms']+'\nEnlace externo: '+cancion['href']+'\nLetra: '+'\nLyrics: ')+str(lyrics))
    else:
        print('---------------------------------------------------------------------------------------------------')
        print('Las primeras 3 CANCIONES con esta popularidad ordenadas por DURACION son: ')
        i=1
        while i<= sample:
            cancion=lt.getElement(lista, i)
            if cancion['lyrics']=='-99':
                lyrics='UNKNOWN'
            else:
                lyrics=cancion['lyrics']
            idAlbum=cancion['album_id']
            idArtists=cancion['artists_id']
            nombreAlbum=controller.nombreAlbumId(catalogo, idAlbum)
            nombreArtistas=controller.nombreVariosArtistasId(catalogo,idArtists)
            print( '\nNombre: '+ str(cancion['name']) + '\nAlbum: '+ str(nombreAlbum)
            + "\nArtistas Involucrados: " + str(nombreArtistas)+'\nPopularidad: '+ str(cancion['popularity']) +'\nDuracion[ms]: '
            +str(cancion['duration_ms']+'\nEnlace externo: '+cancion['href']+'\nLetra: '+'\nLyrics: ')+str(lyrics))
            i+=1
        print('\n--------------------------------------------------------------------------------------------------')
        print('Las ultimas 3 CANCIONES con esta popularidad ordenadas por DURACION son: ')
        i=size-(sample-1)
        while i<=size:
            cancion=lt.getElement(lista, i)
            if cancion['lyrics']=='-99':
                lyrics='UNKNOWN'
            else:
                lyrics=cancion['lyrics']
            idAlbum=cancion['album_id']
            idArtists=cancion['artists_id']
            nombreAlbum=controller.nombreAlbumId(catalogo, idAlbum)
            nombreArtistas=controller.nombreVariosArtistasId(catalogo,idArtists)
            print( '\nNombre: '+ str(cancion['name']) + '\nAlbum: '+ str(nombreAlbum)
            + "\nArtistas Involucrados: " + str(nombreArtistas)+'\nPopularidad: '+ str(cancion['popularity']) +'\nDuracion[ms]: '
            +str(cancion['duration_ms']+'\nEnlace externo: '+cancion['href']+'\nLetra: '+'\nLyrics: ')+str(lyrics))
            i+=1
        print('\n--------------------------------------------------------------------------------------------------')
    print("Tiempo carga REQ3[ms]: ", f"{time:.3f}",
              "\nMemoria carga REQ3[kB]: ", f"{memory:.3f}")
    print('---------------------------------------------------------------------------------------------------\n')

def printReq4(catalogo, cancion, listaAlbumesArtistaPais, lista, time, memory):
    numAlbumes=lt.size(listaAlbumesArtistaPais)
    numCanciones=lt.size(lista)
    idAlbum=cancion['album_id']
    idArtists=cancion['artists_id']
    nombreAlbum=controller.nombreAlbumId(catalogo, idAlbum)
    nombreArtistas=controller.nombreVariosArtistasId(catalogo,idArtists)
    print('---------------------------------------------------------------------------------------------------')
    print('Albumes de este artista en el pais: '+str(numAlbumes))
    print('Canciones de este artista en el pais: '+str(numCanciones))
    print('---------------------------------------------------------------------------------------------------\n')
    print('Nombre Cancion: '+str(cancion['name']))
    print('Nombre Album: '+str(nombreAlbum))
    #print('Fecha Publicacion: '+str(cancion['release_date']))
    #no esta la llave release date en las canciones de este reto
    print('Artistas involucrados: '+str(nombreArtistas))
    print('Popularidad: '+str(cancion['popularity']))
    print('Enlace URL: '+str(cancion['href']))
    print('lyrics: '+cancion['lyrics'])
    print('---------------------------------------------------------------------------------------------------')
    print("Tiempo carga REQ4[ms]: ", f"{time:.3f}",
              "\nMemoria carga REQ5[kB]: ", f"{memory:.3f}")
    print('---------------------------------------------------------------------------------------------------\n')

def printResultsReq5(listaAlbumes, sample, catalogo, sencillo, recopilacion , tipoalbum, time, memory):
    size=lt.size(listaAlbumes)
    numAlbumes=lt.size(listaAlbumes)
    albumesOrden=lt.newList('ARRAY_LIST')
    listaCancionesPopulares=lt.newList('ARRAY_LIST')
    print('\nNumero ALBUMES total de este artista: '+str(numAlbumes)+'\n')
    print('Numero ALBUMES tipo SENCILLO de este artista: '+str(lt.size(sencillo))+'\n')
    print('Numero ALBUMES tipo RECOPILACION de este artista: '+str(lt.size(recopilacion))+'\n')
    print('Numero ALBUMES tipo ALBUM de este artista: '+str(lt.size(tipoalbum)))
    if size <= sample*2:
        print('--------------------------------------------------------------------------------------------------')
        print('Los ALBUMES de este Artista son:')
        for album in lt.iterator(listaAlbumes):
            idArtista=album['artist_id']
            albumId=album['id']
            nombreArtista=controller.nombreArtistaId(catalogo, idArtista)
            cancionPopularAlbum=controller.cancionPopularAlbum(catalogo, albumId)
            lt.addLast(albumesOrden, album['name'])
            lt.addLast(listaCancionesPopulares, cancionPopularAlbum)
            print( '\nNombre: '+ str(album['name']) + '\nFecha Publiocacion: '+ str(album['release_date'])
            + "\nNumero de canciones: " + str(album['total_tracks'])+'\nTipo de album: '+ str(album['album_type']) +'\nArtista principal: '
            +str(nombreArtista))
    else:
        print('---------------------------------------------------------------------------------------------------')
        print('Los primeros 3 ALBUMES de este artsista son: ')
        i=1
        while i<= sample:
            album=lt.getElement(listaAlbumes,i)
            idArtista=album['artist_id']
            albumId=album['id']
            nombreArtista=controller.nombreArtistaId(catalogo, idArtista)
            cancionPopularAlbum=controller.cancionPopularAlbum(catalogo, albumId)
            lt.addLast(albumesOrden, album['name'])
            lt.addLast(listaCancionesPopulares, cancionPopularAlbum)
            print( '\nNombre: '+ str(album['name']) + '\nFecha Publiocacion: '+ str(album['release_date'])
            + "\nNumero de canciones: " + str(album['total_tracks'])+'\nTipo de album: '+ str(album['album_type']) +'\nArtista principal: '
            +str(nombreArtista))
            i+=1
        print('\n--------------------------------------------------------------------------------------------------')
        print('Las ultimos 3 ALBUMES de este artista son: ')
        i=size-(sample-1)
        while i<=size:
            album=lt.getElement(listaAlbumes,i)
            idArtista=album['artist_id']
            albumId=album['id']
            nombreArtista=controller.nombreArtistaId(catalogo, idArtista)
            cancionPopularAlbum=controller.cancionPopularAlbum(catalogo, albumId)
            lt.addLast(albumesOrden, album['name'])
            lt.addLast(listaCancionesPopulares, cancionPopularAlbum)
            print( '\nNombre: '+ str(album['name']) + '\nFecha Publiocacion: '+ str(album['release_date'])
            + "\nNumero de canciones: " + str(album['total_tracks'])+'\nTipo de album: '+ str(album['album_type']) +'\nArtista principal: '
            +str(nombreArtista))
            i+=1
        print('\n--------------------------------------------------------------------------------------------------')
        i=1
        while i<=lt.size(listaCancionesPopulares):
            cancion=lt.getElement(listaCancionesPopulares,i)
            idArtists=cancion['artists_id']
            nombreArtistas=controller.nombreVariosArtistasId(catalogo,idArtists)
            print('\n--------------------------------------------------------------------------------------------------')
            print('La cancion mas Popular del album '+str(lt.getElement(albumesOrden,i))+': ')
            print('\nNombre: '+str(cancion['name'])+'\nNombre Artistas Involucrados: '+ str(nombreArtistas) +'\nDuracion: '+str(cancion['duration_ms'])+
            '\nPopularidad: '+cancion['popularity'] +"\nEnlace de la Cancion: "+cancion['preview_url']+'\nLyrics: '+str(cancion['lyrics']))
            i+=1
            print('\n--------------------------------------------------------------------------------------------------')
    print("Tiempo carga REQ5[ms]: ", f"{time:.3f}",
              "\nMemoria carga REQ4[kB]: ", f"{memory:.3f}")
    print('---------------------------------------------------------------------------------------------------\n')


"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 0:
        print("Cargando información de los archivos ....")
        tamanioarchivo=input('\nSeleccione el Tamanio de archivo: \n1-small\n2-5pct\n3-10pct\n4-20pct\n5-30pct\n6-50pct\n7-80pct\n8-large\n')
        if int(tamanioarchivo)==1:
            tamanioarchivo='small'
        elif int(tamanioarchivo)==2:
            tamanioarchivo="5pct"
        elif int(tamanioarchivo)==3:
            tamanioarchivo="10pct"
        elif int(tamanioarchivo)==4:
            tamanioarchivo="20pct"
        elif int(tamanioarchivo)==5:
            tamanioarchivo="30pct"
        elif int(tamanioarchivo)==6:
            tamanioarchivo="50pct"
        elif int(tamanioarchivo)==7:
            tamanioarchivo="80pct"
        elif int(tamanioarchivo)==8:
            tamanioarchivo='large'
        catalogo=controller.inicializarCatalogo()
        delta_time, deltamemory, listaArtistas, listaAlbumes, listaCanciones=controller.loadData(catalogo, str(tamanioarchivo))
        print('Numero Artistas: '+str(controller.artistasSize(catalogo)))
        print('Numero canciones: '+str(controller.cancionesSize(catalogo)))
        print('Numero Albumes: '+str(controller.albumesSize(catalogo)))
        print("Tiempo carga datos[ms]: ", f"{delta_time:.3f}", "||",
              "Memoria carga datos[kB]: ", f"{deltamemory:.3f}")
        print(lt.size(listaArtistas))
        printResultsartistas(listaArtistas,3)
        printResultsAlbums(listaAlbumes, 3,)
        printResultsCanciones(listaCanciones, 3, catalogo)
        
    elif int(inputs[0]) == 1:
        anio=input('Anio de interes: ')
        listaAlbumesAnio, time, memory=controller.listaOrdenadaAlbumesAnio(catalogo, anio)
        printResultsReq1(listaAlbumesAnio, 3, catalogo,time,memory)

    elif int(inputs[0]) == 2:
        popularidad=int(input('Ingrese la Popularidad (sin decimal): '))
        listaArtistasPopularidad, time, memory=controller.listaOrdenadaArtistasPopularidad(catalogo,popularidad)
        printResultsReq2(listaArtistasPopularidad, 3, catalogo, time, memory)
        
    elif int(inputs[0])==3:
        popularidadCanciones = int(input("Ingrese la popularidad de la canción (sin decimal): "))
        listaCancionesPopularidad, time, memory=controller.listaOrdenadaCancionesPopularidad(catalogo, popularidadCanciones)
        printResultsReq3(listaCancionesPopularidad, 3, catalogo, time, memory)

    elif int(inputs[0])==4:
        codigoPais=input('Ingrese el codigo del pais: ')
        nombreArtista=input('Ingrese nombre Artistas: ')
        listaPaisCanciones, time, memory=controller.listaOrdenadaPaisCanciones(catalogo, codigoPais)
        listaPaisAlbumes=controller.listaOrdenadaPaisAlbumes(catalogo,codigoPais )
        listaAlbumesArtistaPais=controller.listaAlbumesArtistaPais(catalogo, listaPaisAlbumes, nombreArtista)
        cancion, listaCancionesArtista=(controller.cancionPopularArtistaPais(catalogo, listaPaisCanciones, nombreArtista))
        printReq4(catalogo, cancion, listaAlbumesArtistaPais, listaCancionesArtista, time, memory)
        
    elif int(inputs[0])==5:
        nombreArtista=input('Ingrese el nombre del artista: ')
        listaAlbumesArtista,time, memory=controller.listaAlbumesArtista(catalogo, nombreArtista)
        sencillo, recopilacion, album=controller.tipoAlbumesArtista(listaAlbumesArtista)
        printResultsReq5(listaAlbumesArtista, 3, catalogo, sencillo, recopilacion, album, time, memory)

    else:
        sys.exit(0)

