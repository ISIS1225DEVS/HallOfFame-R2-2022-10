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

default_limit = 1000000000
sys.setrecursionlimit(default_limit)

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""
#=====================Carga de datos============================ 
def printTiempo_Memoria(tiempo, memoria): 
    mensaje = "****  Tiempo [ms]: {0} | Memoria [kb]: {1}  ****".format(round(tiempo,2), round(memoria,2))
    print(mensaje)

def printCanciones(catalog):
    size_canciones = lt.size(catalog["model"]["tracks"]) 
    cancion = "" 
    pos = [0, 1, 2, size_canciones-3, size_canciones-2, size_canciones-1]

    for i in range(6):
        cancion = lt.getElement(catalog["model"]["tracks"], pos[i])
        if   i == 0:
            print('>>>   Primeras 3 canciones cargadas son...   >>>')
        elif i == 3:
            print('>>>   Últimas 3 canciones cargadas son...    >>>')
        print(
            "      Nombre: " + 
            cancion["name"] + 
            " , Duración (ms): " + 
            str(cancion["duration_ms"] ) + 
            " , Número de canciones en el álbum: " + 
            str(int(float(cancion["track_number"]))))

        

def printArtistas(catalog):
    size_artistas = lt.size(catalog["model"]["artists"]) 
    artista = ""  

    pos = [0, 1, 2, size_artistas-3, size_artistas-2, size_artistas-1] 
    
    for i in range(6):
        artista = lt.getElement(catalog["model"]["artists"], pos[i])

        if   i == 0:
            print('>>>   Primeros 3 artistas cargados son...    >>>')
        elif i == 3:
            print('>>>   Últimos 3 artistas cargados son...     >>>')

        print(
            "      Nombre: " + 
            artista["name"] + 
            " , Géneros: " + 
            printGeneros(artista) +
            " Seguidores: " + 
            str(artista["followers"] ) + 
            " , Popularidad: " +
            str(artista["artist_popularity"])
            )
        

def printAlbumes(catalog):
    size_albumes = lt.size(catalog["model"]["albums"]) 
    album = ""
    
    pos = [0, 1, 2, size_albumes-3, size_albumes-2, size_albumes-1]

    
    for i in range(6):
        album = lt.getElement(catalog["model"]["albums"], pos[i])

        if   i == 0:
            print('>>>   Primeros 3 álbumes cargados son... >>>')
        elif i == 3:
            print('>>>   Últimos 3 álbumes cargados son...  >>>')

        print(
            "      Nombre: " + 
            album["name"] + 
            ", Tipo de álbum: " +
            album['album_type'] +
            ", Mercados disponibles: " +
            album['available_markets'][1:20] + '...' +
            ", Fecha de lanzamiento: " + 
            str(album["release_date"])
            )

#==========[Funciones de impresión]====================================================

#-------------------[Req1]-------------------------------------------------------------

def printR1(rsp_albums, rsp_artists, num_albums, albumes_del_anio):

    print("=="*35)
    print('            Para el año {0}, se encontaron {1} álbumes'.format(albumes_del_anio, num_albums))
    print("=="*35)
    print('>>>>>>   Los primeros 3 álbums en {0} son...   >>>>>>'.format(albumes_del_anio))
    for i in range(6):
        album = lt.getElement(rsp_albums, i +1)
        asc_artist = lt.getElement(rsp_artists, i+1)
        
        print(
            "Nombre: " + 
            str(album["name"]) + 
            ",\n    Fecha de lanzamiento: " + 
            str(album["release_date"] ) + 
            ",\n    Tipo de álbum: " + 
            str(album["album_type"]) + 
            ",\n    Nombre del artista: " +
            str(asc_artist) + 
            ",\n    Número de canciones del álbum: " +  
            str(album['total_tracks']) + "\n"
        )
        if i +1 == 3:
            
            print('>>>>>>   Los últimos 3 álbums en {0} son...   >>>>>>'.format(albumes_del_anio))


#--------------------------[R2]-----------------------------------------------------------

def printR2(rsp_artists, rsp_tracks, num_artists, inp_popularity):

    print("=="*35)
    print('            Para la popularidad {0}, se encontaron {1} artistas'.format(inp_popularity, num_artists))
    print("=="*35)
    print('>>>>>>   Los primeros 3 artistas con popularidad {0} son...   >>>>>>'.format(inp_popularity))
    for i in range(6):
        artist = lt.getElement(rsp_artists, i +1)
        asc_track = lt.getElement(rsp_tracks, i+1)
        
        print(
            "Nombre: " + 
            str(artist["name"]) + 
            ",\n    Popularidad: " + 
            str(artist["artist_popularity"] ) + 
            ",\n    Seguidores: " + 
            str(artist["followers"]) + 
            ",\n    Géneros: " +
            printGeneros(artist) + 
            "\n    Canción referente: " +  
            str(asc_track) + "\n"
        )
        if i +1 == 3:
            
            print('>>>>>>   Los últimos 3 artistas con popularidad {0} son...   >>>>>>'.format(inp_popularity))

def printGeneros(artist):
    generos = artist["genres"].strip("[]").replace("'","").split(",")
    cadena_print = ''
    for genero in generos:
        if genero:
            cadena_print += genero +","
    
    return cadena_print

#--------------------------[R3]-----------------------------------------------------------

def printR3(tam_list, list_resp_R3, names_albums, inp_track_popularity, names_artists):

    print("=="*35)
    print("\nEl número de canciones con popularidad {0} es: {1}".format(inp_track_popularity, str(tam_list)))
    print('>>>>>>   Las primeras 3 canciones con popularidad {0} son...   >>>>>>'.format(inp_track_popularity))
    for i in range(6):
        track = lt.getElement(list_resp_R3, i +1)
        name_album = lt.getElement(names_albums, i+1)
        list_names_artists = lt.getElement(names_artists, i+1) 

        letra ="Letra de la canción no está disponible."
        if track["lyrics"] != "-99":
            letra = track["lyrics"][:100] + "..."

        artists_names = ""
        for name in lt.iterator(list_names_artists):
            artists_names += name +", "

        
        print(
            "Nombre: " + 
            str(track["name"]) + 
            ",\n      Nombre del álbum: " + 
            str(name_album) + 
            ",\n      Artistas asociados: " + 
            str(artists_names[:-2]) + 
            ",\n      Popularidad: " +
            str(track["popularity"]) + 
            ",\n      Duración: " +  
            str(track["duration_ms"]) + 
            ",\n      Enlace externo: " +  
            str(track["href"]) + 
            ",\n      Letra: " +  
            "\n    "+ letra + 
            "\n"
        )
        if i +1 == 3:
            
            print('>>>>>>    Las últimas 3 canciones con popularidad {0} son...   >>>>>>'.format(inp_track_popularity))

#---------------------------[R4]-------------------------------------------------------------------------

def printR4(popular_track, num_tracks, num_albums, inp_artist_name, inp_country):

    print("=="*35)
    print("             '{0}' con canciones en {1}: ".format(inp_artist_name, inp_country))
    print("               Número de álbumes únicos:   {0}".format(num_albums))
    print("               Número de canciones únicas: {0}".format(num_tracks))
    print("=="*35)
    print('\n>>>>> La canción más popular (con los criterios de ord. de R4) es... >>>>>')


    if popular_track["lyrics"] == "-99":
        letra = "Letra de la cancion: No disponible"

    else:
        letra = str(popular_track["lyrics"]).replace("\n", " ")[:50] +'..."'
   
    print(
        "Nombre: " + 
        str(popular_track["name"]) + 
        ",\n    Nombre del álbum: " + 
        str(popular_track['album_name']) + 
        ",\n    Fecha de publicación: " + 
        str(popular_track['release_date']) + 
        ",\n    Nombres de artistas involucrados: " + 
        str(popular_track['artists_name'])[:-2] + 
        ",\n    Duración: " +  
        str(int(float(popular_track["duration_ms"]))) +
        ",\n    Popularidad: " +
        str(int(float(popular_track["popularity"]))) + 
        ",\n    Enlace a audio de muestra: " +  
        str(popular_track["preview_url"]) + 
        ',\n    Letra:  ' +  
        str(letra) + 
        "\n"
    )

#=================================[R5]======================================

def printR5(album_types, resp_albums, resp_tracks, names_artists, artist_name):
    singles, compilations, albums, total = album_types
    print("=="*35)
    print("         {0} tiene: {1} Sencillos, {2} Compilaciones y {3} Albumes.".format(artist_name, singles, compilations, albums))
    print("         Constituyendo un total de {0} proyectos.".format(total))
    
    print("\n>>>>>>    Los 3 primeros albumes en la discografia de {0} son: ".format(artist_name))

    for i in range(6):
        album = lt.getElement(resp_albums, i +1)
        
        print(
            "Fecha de publicacion: " + 
            str(album["release_date"]) + 
            ",\n      Nombre del álbum: " + 
            str(album["name"]) + 
            ",\n      Canciones en el album: " + 
            str(album["total_tracks"]) + 
            ",\n      Tipo de album: " +
            str(album["album_type"]) + 
            ",\n      Nombre del artista: " +  
            str(artist_name) + 
            "\n"
        )
        if i +1 == 3:
            
            print(">>>>>>    Los 3 últimos albumes en la discografia de {0} son: ".format(artist_name))

    print("\n>>>>>>    Las canciones más populares de los primeros 3 albumes en la discografia de {0} son: ".format(artist_name))
    for i in range(6):
        album_name = lt.getElement(resp_albums, i+1)["name"]
        asociated_artists_list = lt.getElement(names_artists, i+1)
        track = lt.getElement(resp_tracks, i +1)

        artists_names = ""
        for name in lt.iterator(asociated_artists_list):
            artists_names += name +", "
        artists_names = artists_names[:-2]
        
        letra ="Letra de la canción no está disponible."
        if track["lyrics"] != "-99":
            letra = track["lyrics"][:100] + "..."

        print(
            "Nombre del album: " + 
            str(album_name) + 
            ",\n      Nombre de la canción: " + 
            str(track["name"]) + 
            ",\n      Artistas involucrados: " + 
            str(artists_names) + 
            ",\n      Tiempo de duración: " +
            str(track["duration_ms"]) + 
            ",\n      Popularidad: " +  
            str(track["popularity"]) + 
            ",\n      Enlace de muestra: " +  
            str(track["preview_url"]) +           
            ",\n      Letra: " +  
            str(letra) + 
            "\n"
        )
        
        if i +1 == 3:
            
            print(">>>>>>    Las canciones más populares de los ultimos 3 albumes en la discografia de {0} son: ".format(artist_name))




#-------------------------[R6]--------------------------------------------------

def printR6(answer_list, num_tracks, inp_artist_name, inp_country, inp_n):
    print("=="*35)
    print("         '{0}' con canciones en {1}, se ha escogido el TOP {2}".format(inp_artist_name, inp_country, inp_n))
    print("                    Número de canciones: {0}".format(num_tracks))
    print("=="*35)
    print('>>>>>>   Las primeras 3 canciones del TOP {0} son...   >>>>>>'.format(inp_n))

    if num_tracks < 6:
        a = num_tracks -1
    else:
        a = 5
    a_list = range(a)
    for i in a_list:
        track = lt.getElement(answer_list, i +1)

        if track["lyrics"] == "-99":
            letra = "Letra de la cancion: No disponible"

        else:
            letra = str(track["lyrics"]).replace("\n", " ")[:50] +'..."'

        print(
            "Nombre: " + 
            str(track["name"]) + 
            ",\n    Nombre del álbum: " + 
            str(track['album_name']) + 
            ",\n    Fecha de publicación: " + 
            str(track['release_date']) + 
            ",\n    Nombres de artistas involucrados: " + 
            str(track['artists_name'])[:-2] + 
            ",\n    Número de países de distribución: " + 
            str(track['distribution']) +
            ",\n    Popularidad: " +
            str(int(float(track["popularity"]))) +
            ",\n    Duración: " +  
            str(int(float(track["duration_ms"]))) +
            ',\n    Letra:  ' +  
            letra + 
            '"\n'
        )
        if i +1 == 3:
            
            print('>>>>>>    Las últimas 3 canciones del top {0} son...   >>>>>>'.format(inp_n))
def printMenu():
    
    print("====="*15)
    print("          >>               Bienvenido                    <<     ")
    print("  [R0]   q- Cargar información en el catálogo.")
    print("  [R1]   1- Examinar los álbumes en un año de interés.")
    print("  [R2]   2- Encontrar los artistas por popularidad.")
    print("  [R3]   3- Encontrar las canciones por popularidad.")
    print("  [R4]   4- Encontrar la canción más popular de un artista.")
    print("  [R5]   5- Encontrar la discografía de un artista.")
    print("  [R6]   6- Clasificar las canciones de artistas con mayor distribución.")
    print("         0- Salir")
    print("====="*15)

catalog = controller.newController()

"""
Menú principal
"""
while True:
    printMenu()
    inputs = input('>> Seleccione una opción para continuar: ')
    if inputs == "q":
        print("Cargando información de los archivos ....")
        tam_tracks, tam_albums, tam_artists, tiempo, memoria = controller.loadData(catalog)
        print("=="*40)
        print("      Número de artistas: {0}".format(tam_artists))
        print("      Número de álbumes: {0}".format(tam_albums))
        print("      Número de tracks: {0}".format(tam_tracks))


        print("=="*70)
        printArtistas(catalog)
        print("=="*70)
        printAlbumes(catalog)
        print("=="*70)
        printCanciones(catalog)

        printTiempo_Memoria(tiempo, memoria)

    elif int(inputs) == 1:
        albumes_del_anio = input("> Ingrese el año que desea examinar: ")
        rsp_albums, rsp_artists, num_albums, d_time, d_memory = controller.call_answer_r1(catalog, albumes_del_anio)

        if d_time == None:
            print('     No se halló este año')
        else:
            printR1(rsp_albums, rsp_artists, num_albums, albumes_del_anio)
            printTiempo_Memoria(d_time, d_memory)


    elif int(inputs) == 2:
        inp_popularity = input('> Ingrese la popularidad del artista: ')
        rsp_artists, rsp_tracks, num_artistas, d_time, d_memory = controller.call_answer_r2(catalog, inp_popularity)

        if d_time == None:
            print('     No se encontraron artistas con la popularidad dada')
        else:
            printR2(rsp_artists, rsp_tracks, num_artistas, inp_popularity)
            printTiempo_Memoria(d_time, d_memory)
   
    elif int(inputs) == 3:
        inp_track_popularity = input("> Ingrese la popularidad de la canción: ")
        
    
        time, memory, tam_list, list_resp_R3, names_albums, names_artists = controller.call_answer_R3(catalog, inp_track_popularity)
        
        if time == None:
            print("     No se halló esa popularidad")
        else:
            printR3(tam_list, list_resp_R3, names_albums, inp_track_popularity, names_artists)
            printTiempo_Memoria(time, memory)

    elif int(inputs) == 4:
        inp_artist_name = input('> Ingrese el nombre del artista: ')
        inp_country = input('> Ingrese las siglas del país:   ')

        popular_track, num_tracks, num_albums, time, memory = controller.call_answer_r4(catalog, inp_artist_name, inp_country)

        if time == None:
            print("     No se encontraron canciones dados los parámetros")
        else:
            printR4(popular_track, num_tracks, num_albums, inp_artist_name, inp_country)
            printTiempo_Memoria(time, memory)


    elif int(inputs) == 5:
        artist_name = input("Ingrese el nombre del artista que desea buscar: ")
        time, memory, album_types, resp_albums, resp_tracks, names_artists = controller.call_answer_R5(catalog, artist_name)
        
        if time == None:
            print("     No se encontró la discrografía de ese artista")
        else:
            printR5(album_types, resp_albums, resp_tracks, names_artists, artist_name)
            printTiempo_Memoria(time, memory)

    elif int(inputs) == 6:
        inp_artist_name = input('> Ingrese el nombre del artista: ')
        inp_country = input('> Ingrese las siglas del país:   ')
        inp_n = int(input('> Ingrese el TOP n:              '))

        answer_tracks, num_tracks, time, memory = controller.call_answer_r6(catalog, inp_artist_name, inp_country, inp_n)
        
        if time == None:
            print("     No se encontraron canciones dados los parámetros")
        else:
            printR6(answer_tracks, num_tracks, inp_artist_name, inp_country, inp_n)
            printTiempo_Memoria(time, memory)


    elif int(inputs) == 0:
        sys.exit(0)





