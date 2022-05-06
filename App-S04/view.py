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
import csv
from texttable import Texttable

csv.field_size_limit(214474836)
default_limit = 1000
sys.setrecursionlimit(default_limit*10)


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def newController():
    """
    Se crea una instancia del controlador
    """
    control = controller.newController()
    return control

def loadData():
    """
    Solicita al controlador que cargue los datos en el modelo
    """
    
    artists, albums, albumyear, tracks, genres, artistpopularity,  artistsname, albumartist, trackalbum, firstartists, firstalbums, firsttracks, delta_time, delta_memory = controller.loadData(control, file)
    
    return artists, albums, albumyear, tracks, genres, artistpopularity, artistsname, albumartist, trackalbum, firstartists, firstalbums, firsttracks, delta_time, delta_memory

def Tabulate(encabezados, datos):
    columnas = len(encabezados)
    table = Texttable()
    table._row_size = columnas
    table.set_cols_align = (["c"]*columnas)
    table._rows = datos
    table._header = encabezados
    print(table.draw())

def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Albumes publicados en año de interés")
    print("3- Encontrar los artistas por popularidad")
    print("4- Encontrar las canciones por popularidad")
    print("5- Encontrar la canción más popular de un artista")
    print("6- Encontrar la discografía de un artista")
    print("7- Clasificar las canciones con mayor distribución")
    print("0- Salir")

control = newController()

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("1- small")
        print("2- 5pct")
        print("3- 10pct")
        print("4- 20pct")
        print("5- 30pct")
        print("6- 50pct")
        print("7- 80pct")
        print("8- large")
        number = input("Ingrese el tamaño del archivo a cargar: ")
        if int(number) == 1:
            file = "small"
        elif int(number) == 2:
            file = "5pct"
        elif int(number) == 3:
            file = "10pct"
        elif int(number) == 4:
            file = "20pct"
        elif int(number) == 5:
            file = "30pct"
        elif int(number) == 6:
            file = "50pct"
        elif int(number) == 7:
            file = "80pct"
        elif int(number) == 8:
            file = "large"
        catalog = control["model"]
        print("Cargando información de los archivos ....")
        answer = loadData()
        artists, albums, albumyear, tracks, genres, artistpopularity, artistsname, albumartist, trackalbum, firstartists, firstalbums, firsttracks, delta_time, delta_memory = loadData()
        print('Artistas cargados: ' + str(artists))
        print('Albumes cargados: ' + str(albums))
        print('Canciones cargadas: ' + str(tracks))
        print("Generos cargados: " + str(genres))
        print("Tiempo [ms]: " + str(delta_time) + ", "
              "Memoria [kB]: " + str(delta_memory))
        print("Los primeros 3 y los últimos 3 artistas cargados son: ")
        encabezado = ["Name", "Artist_Popularity", "Followers", "Relevant_Track", "Genres"]
        datos = firstartists
        Tabulate(encabezado, datos)
        print("Los primeros 3 y los últimos 3 albumes cargados son: ")
        encabezado = ["Name", "Release_Date", "Relevant_Track", "Artist", "Total_Tracks", "Album_Type"]
        datos = firstalbums
        Tabulate(encabezado, datos)
        print("Las primeras 3 y las últimas 3 canciones cargados son: ")
        encabezado = ["Name", "Popularity", "Album", "Disc_Number", "Track_Number", "Duration_ms"]
        datos =  firsttracks
        Tabulate(encabezado, datos)

    elif int(inputs[0]) == 2:
        year = int(input("Ingrese el año deseado: "))
        catalog = control["model"]
        primero, segundo, tercero, antepenultimo, penultimo, ultimo, size, delta_time, delta_memory = controller.AlbumsinCertainYear(year, catalog)
        print("El número de albumes publicados en " + str(year) + " es de " + str(size))
        encabezado = ["Album", "Release_Date", "Album_Type", "Artist", "Total_Tracks"]
        datos = [primero, segundo, tercero, antepenultimo, penultimo, ultimo]
        Tabulate(encabezado, datos)
        print("Tiempo [ms]: " + str(delta_time) + ", "
              "Memoria [kB]: " + str(delta_memory))


    elif int(inputs[0]) == 3:
        popularity = float(input("Ingrese la popularidad deseada: "))
        catalog = control["model"]
        primero, segundo, tercero, antepenultimo, penultimo, ultimo, size, delta_time, delta_memory = controller.ArtistswithCertainPopularity(popularity, catalog)
        print("Hay " + str(size) + " artistas con popularidad de " + str(popularity))
        encabezado = ["Artist", "Popularity", "Followers", "Genres", "Relevant_Track"]
        datos = [primero, segundo, tercero, antepenultimo, penultimo, ultimo]
        Tabulate(encabezado, datos)
        print("Tiempo [ms]: " + str(delta_time) + ", "
              "Memoria [kB]: " + str(delta_memory))

    elif int(inputs[0]) == 4:
        popularity = float(input("Ingrese la popularidad deseada: "))
        catalog = control["model"]
        Totaldict = controller.TrackByPopularity(popularity, catalog)
        info = Totaldict["resultado"]
        if info != None:
            print("Hay {} canciones con {} en popularidad \n".format(info[0], int(popularity)))
            titulo = ["track name", "album name", "artists name", "popularity", "duration (m)", "href", "lyrics"]
            datos = list(info[1: len(info)+1])
            Tabulate(titulo, datos)
            delta_time = Totaldict["tiempo"]
            delta_memory = Totaldict["memoria"]
            print("Tiempo [ms]: " + str(delta_time) + ", "
              "Memoria [kB]: " + str(delta_memory))
        else: 
            print("El indice de popularidad no se encuentra disponible en las canciones cargadas inicialmente")


    elif int(inputs[0]) == 5:
        name = input("Ingrese el nombre del artista: ")
        country = input("Ingrese el nombre del país: ")
        catalog = control["model"]
        Totaldict = controller.MostPopularArtistSong(name, country, catalog)
        info = Totaldict["resultado"]
        if info != None:
            print("\n{} tiene disponible el siguiente repertorio en {} ({}): \n".format(name, country, info[0]))
            print("Albumes disponibles: {}".format(info[2]))
            print("Canciones disponibles: {} \n".format(info[1]))
            titulo = ["track name", "album name", "release date", "artists name", "duration (ms)", "popularity", "preview url", "lyrics"]
            datos = list(info[3: len(info)+1])
            Tabulate(titulo, datos)
            delta_time = Totaldict["tiempo"]
            delta_memory = Totaldict["memoria"]
            print("Tiempo [ms]: " + str(delta_time) + ", "
              "Memoria [kB]: " + str(delta_memory))
            
        else: 
            print("No se encontro el cantante solicitado")


    elif int(inputs[0]) == 6:
        name = input("Ingrese el nombre del artista: ")
        catalog = control["model"]
        single_albums, compilation_albums, album_albums, total_albums, primero, segundo, tercero, antepenultimo, penultimo, ultimo, popular_songs, delta_time, delta_memory = controller.ArtistDiscography(name, catalog)
        print("El número de sencillos es: " + str(single_albums))
        print("El número de compilaciones es: " + str(compilation_albums))
        print("El número de albumes es: " + str(album_albums))
        print("El número total de albumes cargados es: " + str(total_albums))
        encabezado = ["Release_Date", "Album", "Total_Tracks", "Album_Type", "Artist_Album_Name"]
        datos = [primero, segundo, tercero, antepenultimo, penultimo, ultimo]
        Tabulate(encabezado, datos)
        encabezado2 = ["Track", "Artists", "Duration_ms", "Popularity", "Preview_Url", "Lyrics"]
        print("La canción más popular de " + str(primero[1]))
        datos2 = popular_songs[0]
        Tabulate(encabezado2, [datos2])
        print("La canción más popular de " + str(segundo[1]))
        datos3 = popular_songs[1]
        Tabulate(encabezado2, [datos3])
        print("La canción más popular de " + str(tercero[1]))
        datos4 = popular_songs[2]
        Tabulate(encabezado2, [datos4])
        print("La canción más popular de " + str(antepenultimo[1]))
        datos5 = popular_songs[3]
        Tabulate(encabezado2, [datos5])
        print("La canción más popular de " + str(penultimo[1]))
        datos6 = popular_songs[4]
        Tabulate(encabezado2, [datos6])
        print("La canción más popular de " + str(ultimo[1]))
        datos7 = popular_songs[5]
        Tabulate(encabezado2, [datos7])
        print("Tiempo [ms]: " + str(delta_time) + ", "
              "Memoria [kB]: " + str(delta_memory))
        

    elif int(inputs[0]) == 7:
        name = input("Ingrese el nombre del artista: ")
        country = input("Ingrese el nombre del país: ")
        top = int(input("Ingrese el TOP de popularidad deseada: "))
        Totaldict= controller.Bonus(name, country, top, catalog)
        info = Totaldict["resultado"]
        if info != None:
            print("\n Hay {} canciones con mayor distribuccion del artista: {} \n". format(info[0], name))
            titulo = ["track name", "album name", "release date", "artists name", "available markets num", "popularity", "duration (m)", "lyrics" ]
            datos = list(info[1:len(info)+1])
            Tabulate(titulo, datos)
            delta_time = Totaldict["tiempo"]
            delta_memory = Totaldict["memoria"]
            print("Tiempo [ms]: " + str(delta_time) + ", "
              "Memoria [kB]: " + str(delta_memory))
            
        else: 
            print("El indice de popularidad no se encuentra disponible en las canciones cargadas inicialmente")


    else:
        sys.exit(0)
sys.exit(0)
