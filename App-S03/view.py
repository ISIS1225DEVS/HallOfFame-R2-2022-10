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
from prettytable import PrettyTable
from prettytable import ALL
from DISClib.ADT import list as lt
assert cf

default_limit = 1000
sys.setrecursionlimit(default_limit*10)

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""
# ================================================
# Inicializacion de la comunicacion con controller
# ================================================

def newController():
    control = controller.newController()
    return control

# =================================
# Funciones para creación de tablas
# =================================

def CreateTable(fieldnames):
    table = PrettyTable()
    table.field_names = fieldnames
    table.align = 'l'
    table.junction_char
    table.hrules = ALL
    table.max_width = 21
    return table

def TableArtist(artists):
    table = CreateTable(['name', 'artist_popularity', 'followers', 'relevant_track_name', 'genres'])
    table.align['artist_popularity'] = 'r'
    table.align['followers'] = 'r'
    for artist in lt.iterator(artists):
        table.add_row([artist[0], artist[1], artist[2], printFixer(artist[3]), printLsts(artist[4])])
    return table

def TableAlbum(albums):
    table = CreateTable(['name', 'release_date', 'available_markets', 'total_tracks', 
        'album_type', 'artist_album_name', 'external_urls'])
    table.align['total_tracks'] = 'r'
    for album in lt.iterator(albums):
        table.add_row([album[0], album[1], printLsts(album[2]), album[3], album[4], 
            printFixer(album[5]), album[6]])
    return table

def TableSong(songs):
    table = CreateTable(['name', 'release_date', 'popularity', 'disc_number', 'track_number', 
        'available_markets', 'available_markets_num', 'duration_ms', 'album_name', 'album_type',
        'artist_names', 'href', 'preview_url', 'lyrics'])
    table.align['popularity'] = 'r'
    table.align['disc_number'] = 'r'
    table.align['track_number'] = 'r'
    table.align['available_markets_num'] = 'r'
    table.align['duration_ms'] = 'r'
    for song in lt.iterator(songs):
        table.add_row([song[0], printFixer(song[1]), song[2], song[3], song[4], printLsts(song[5]), song[6],
            song[7], printFixer(song[8]), printFixer(song[9]), printLsts(song[10]), song[11], song[12], printFixer(song[13])])
    return table

def TableDiscographySong(song):
    table = CreateTable(['name', 'release_date', 'popularity', 'disc_number', 'track_number', 
        'available_markets', 'available_markets_num', 'duration_ms', 'album_name', 'album_type',
        'artist_names', 'href', 'preview_url', 'lyrics'])
    table.align['popularity'] = 'r'
    table.align['disc_number'] = 'r'
    table.align['track_number'] = 'r'
    table.align['available_markets_num'] = 'r'
    table.align['duration_ms'] = 'r'
    table.add_row([song[0], printFixer(song[1]), song[2], song[3], song[4], printLsts(song[5]), song[6],
        song[7], printFixer(song[8]), printFixer(song[9]), printLsts(song[10]), song[11], song[12], printFixer(song[13])])
    return table

# ===================================
# Funciones para imprimir resultados
# ===================================

def printerAT(artists):
    if artists:
        printer = TableArtist(artists)
        print('\n' + 'Los primeros y últimos 3 artistas cargados son: ')
        print(printer)
    else:
        print('No se cargo artistas')

def printerAB(albums):
    if albums:
        printer = TableAlbum(albums)
        printer.del_column('available_markets')
        print('\n' + 'Los primeros y últimos 3 albumes cargados son: ')
        print(printer)
    else:
        print('No se cargo álbumes')

def printerSG(songs):
    if songs:
        printer = TableSong(songs)
        printer.del_column('release_date')
        printer.del_column('available_markets')
        printer.del_column('available_markets_num')
        printer.del_column('album_type')
        printer.del_column('preview_url')
        printer.del_column('lyrics')
        print('\n' + 'Las primeras y últimas 3 canciones cargados son: ')
        print(printer)
    else:
        print('No se cargo canciones')

def printABYear(albums):
    if albums:
        printer = TableAlbum(albums)
        print('\n' + 'Los primeros y últimos 3 albumes encontrados son: ')
        print(printer)
    else:
        print('No se encontraron albumes')

def printATPopularity(artists):
    if artists:
        printer = TableArtist(artists)
        print('\n' + 'Los primeros y últimos 3 artistas encontrados son: ')
        print(printer)
    else:
        print('No se cargo artistas')

def printSGPopularity(songs):
    if songs:
        printer = TableSong(songs)
        printer.del_column('release_date')
        printer.del_column('disc_number')
        printer.del_column('track_number')
        printer.del_column('available_markets')
        printer.del_column('available_markets_num')
        printer.del_column('album_type')
        printer.del_column('preview_url')
        print('\n' + 'Las primeras y últimas 3 canciones encontradas son: ')
        print(printer)
    else:
        print('No se encontraron canciones')

def printSGByArtistCountry(songs):
    if songs:
        printer = TableSong(songs)
        printer.del_column('disc_number')
        printer.del_column('track_number')
        printer.del_column('available_markets')
        printer.del_column('available_markets_num')
        printer.del_column('album_type')
        printer.del_column('href')
        print('\n' + 'La canción popular del artista es: ')
        print(printer)
    else:
        print('No se encontró canción')

def printDiscography(albums, songs):
    if albums and songs:
        printABDiscography(albums)
        print('\n' + '-----Detalles de canciones-----')
        for i in range(1, lt.size(albums)+1):
            song = lt.getElement(songs, i)
            if song:
                album = lt.getElement(albums, i)
                print('\n' + 'Canción popular del album: ' + album[0])
                printSGDiscography(song)
            else:
                print('No se encontró canciones del album: ' + album[0]) 
    elif albums:
        printABDiscography(albums)
        print('No se encontró canciones de los albumes')
    else:
        print('No se encontraron albumes')  

def printABDiscography(albums):
    printer = TableAlbum(albums)
    printer.del_column('available_markets')
    print('\n' + 'Los primeros y últimos 3 albumes encontrados son: ')
    print(printer)

def printSGDiscography(song):
    printer = TableDiscographySong(song)
    printer.del_column('release_date')
    printer.del_column('disc_number')
    printer.del_column('track_number')
    printer.del_column('available_markets')
    printer.del_column('available_markets_num')
    printer.del_column('album_name')
    printer.del_column('album_type')
    printer.del_column('href')
    print(printer)

def printSGByArtistCountryTOP(songs):
    if songs:
        printer = TableSong(songs)
        printer.del_column('disc_number')
        printer.del_column('track_number')
        printer.del_column('preview_url')
        printer.del_column('available_markets')
        print('\n' + 'Las primeras y últimas 3 canciones encontradas son: ')
        print(printer)
    else:
        print('No se encontró canción')

# ====================
# Funciones de arreglo
# ====================

def printFixer(string):
    if string == None:
        return 'Desconocido'
    return string

def printLsts(Lsts):
    if Lsts == None:
        return 'Desconocido'
    elif lt.isEmpty(Lsts):
        return 'Desconocido'
    String = ""
    for Element in lt.iterator(Lsts):
        String = String + str(Element) + ', '
    return String[:-2]

def printLine(length):
    string = ''
    i = 0
    while i < length:
        string = string + '='
        i += 1
    print(string)

# ================
# Menu de opciones
# ================
def printMenu():
    print()
    printLine(70)
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Consultar álbumes de un año")
    print("3- Consultar los artistas con X popularidad")
    print("4- Consultar las canciones con X popularidad")
    print("5- Consultar la canción más popular de un artista en un país")
    print("6- Consultar la discografía de un artista")
    print("7- Consultar el TOP X de canciones más populares en un país")
    print("8- Prueba de rendimiento")
    print("0- Salir")
    printLine(70)

def printTestMenu():
    print()
    printLine(44)
    print("Bienvenido al menú de Pruebas de Rendimiento")
    print("1- Prueba mapa género")
    print("2- Prueba de programa con tiempos")
    print("3- Retornar al menú principal")
    print("0- Salir")
    printLine(44)

def testMapGenre():
    type_input = input('Ingrese C para Separate Chaining y P para Linear Probing:\n')        
    fc = input('Ingrese el factor a usar:\n')
    if type_input[0] == 'C':
        typeM = 'CHAINING'
    elif type_input[0] == 'P':
            typeM = 'PROBING'
    print('Cargando la información según la petición ....')
    answer = controller.loadMapGenre(cntrl, typeM, float(fc))
    print('Tamaño del mapa: ', answer[0])
    print("Tiempo [ms]: ", f"{answer[1]:.3f}", "||",
        "Memoria [kB]: ", f"{answer[2]:.3f}")

# ==============
# Menu Principal
# ==============

while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    print()
    if int(inputs[0]) == 1:
        print('Cargando información de los archivos ....')
        cntrl = newController()
        printAB, printSG, printAT = controller.loadData(cntrl)
        printLine(25)
        print('Albumes cargados: ' + str(printAB[0]))
        print('Canciones cargadas: ' + str(printSG[0]))
        print('Artistas cargados: ' + str(printAT[0]))
        printLine(25)
        printerAT(printAT[1])  
        printerAB(printAB[1])
        printerSG(printSG[1])
        print('\n')

    elif int(inputs[0]) == 2:
        print('El formato a utilizar es AAAA. Ejemplo: 2016')
        year = input('Año a buscar: ')
        Verifier = False
        try:
            year = int(year)
            Verifier = True
        except ValueError:
            pass
        if Verifier == True:
            printYearAlbum = controller.getAlbumsYear(cntrl, year)
            printLine(30)
            print('El número total de álbumes encontrados es: ' + str(printYearAlbum[0]))
            printLine(30)
            printABYear(printYearAlbum[1])
            print('\n')
        else:
            print('Año inválido.')

    elif int(inputs[0]) == 3:
        number = input('Valor popularidad artista: ')
        Verifier = False
        try:
            number = int(number)
            Verifier = True
        except ValueError:
            pass
        if Verifier == True:
            printPopularityArtist = controller.getArtistPopurality(cntrl, number)
            printLine(30)
            print('El número total de artistas encontrados es: ' + str(printPopularityArtist[0]))
            printLine(30)
            printATPopularity(printPopularityArtist[1])
            print('\n')
        else:
            print('Número inválido, por favor verifique.')

    elif int(inputs[0]) == 4:
        number = input('Valor popularidad canción: ')
        Verifier = False
        try:
            number = int(number)
            Verifier = True
        except ValueError:
            pass
        if Verifier == True:
            printPopularitySong = controller.getSongPopurality(cntrl, number)
            printLine(30)
            print('El número total de canciones encontradas es: ' + str(printPopularitySong[0]))
            printLine(30)
            printSGPopularity(printPopularitySong[1])
            print('\n')
        else:
            print('Número inválido, por favor verifique.')

    elif int(inputs[0]) == 5:
        name = input('Nombre del artista: ')
        country = input('Código del país a buscar: ')
        printSGArtistCountry = controller.getSGByArtistCountry(cntrl, name, country[:2])
        printLine(40)
        print('Información para ' + name + ' en ' + country[:2])
        print('El número total de álbumes encontradas es: ' + str(printSGArtistCountry[0]))
        print('El número total de canciones encontradas es: ' + str(printSGArtistCountry[1]))
        printLine(40)
        printSGByArtistCountry(printSGArtistCountry[2])
        print('\n')

    elif int(inputs[0]) == 6:
        name = input('Nombre del artista: ')
        printArtistDiscography = controller.getDiscography(cntrl, name)
        printLine(20)
        print('Total sencillos: ' + str(printArtistDiscography[0]))
        print('Total recopilaciones: ' + str(printArtistDiscography[1]))
        print('Total álbumes: ' + str(printArtistDiscography[2]))
        printLine(20)
        printDiscography(printArtistDiscography[3], printArtistDiscography[4])

    elif int(inputs[0]) == 7:
        name = input('Nombre del artista: ')
        country = input('Código del país a buscar: ')
        number = input('TOP de canciones a encontrar: ')
        Verifier = False
        try:
            number = int(number)
            Verifier = True
        except ValueError:
            pass
        if Verifier == True:
            printSGArtistCountryTOP = controller.getSGArtistCountryTOP(cntrl, name, country[:2], number)
            printLine(40)
            print('TOP ' + str(number) + ' para ' + name + ' en ' + country[:2])
            print('El número total de canciones encontradas: ' + str(printSGArtistCountryTOP[0]))
            printLine(40)
            printSGByArtistCountryTOP(printSGArtistCountryTOP[1])
            print('\n')
        else:
            print('Número inválido, por favor verifique.')

    elif int(inputs[0]) == 8:
        guard = True
        while guard:
            printTestMenu()
            inputTest = input('Seleccione una opción para continuar\n')
            if int(inputTest[0]) == 1:
                testMapGenre()
                guard = False
            elif int(inputTest[0]) == 2:
                import testcontroller as controller
                guard = False
            elif int(inputTest[0]) == 3:
                guard = False
            elif int(inputTest[0]) == 0:
                sys.exit(0)
            else:
                continue

    elif int(inputs[0]) == 0:
        sys.exit(0)

    else:
        continue
sys.exit(0)
