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

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
assert cf
from prettytable import PrettyTable, ALL
import pycountry

default_limit = 10000
sys.setrecursionlimit(default_limit * 10000)

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

def printMenu():
    print("\nBienvenido querido usuario <3:")
    print("1- Cargar información en el catálogo")
    print("2- Examinar los álbumes en un año de interés")
    print("3- Encontrar los artistas por popularidad")
    print("4- Encontrar las canciones por popularidad")
    print("5- Encontrar la canción más popular de un artista")
    print("6- Encontrar la discografía de un artista")
    print("7- Clasificar las canciones de artistas con mayor distribución")
    print("8- Pruebas memoria y tiempos variando los Loadfactors")
    print("0- Salir")

def printMapOptions():
    print('\nIngrese el numero del tipo de mapa que desee: ')
    print(' 1. SEPARATE CHAINING.')
    print(' 2. LINEAR PROBING.')

def printLoadChainingOptions():
    print('\nIngrese el numero del tipo de mapa que desee: ')
    print(' 1. 2.0')
    print(' 2. 4.0')
    print(' 3. 8.0')

def printLoadProbingOptions():
    print('\nIngrese el numero del tipo de mapa que desee: ')
    print(' 1. 0.10')
    print(' 2. 0.50')
    print(' 3. 0.90')

catalog = None

def printSimplePrettyTable(spotifyList, keys):
    table = PrettyTable()
    table.max_width = 20
    table.hrules = ALL
    table.field_names = keys
    rows = []
    for element in lt.iterator(spotifyList):
        row = []
        for key in keys:
            strElement = str(element[key])
            if len(strElement) > 20:
                strElement = strElement[:20]
            row.append(strElement)
        rows.append(row)
    table.add_rows(rows)
    print(table)

def printONEPrettyTable(spotifyList, keys):
    temporal_list = lt.newList ('ARRAY_LIST')
    for element in lt.iterator(spotifyList):
        lt.addLast(temporal_list, element)
        albumname = str(element['album_name'])
        print('Most popular track in ' + albumname)
        printSimplePrettyTable(temporal_list, keys)
        lt.removeLast(temporal_list)

def headers(req_num, messageone, messagetwo):
    print("\n============= Req No. " + str(req_num) + " Inputs =============")
    print(messageone)
    print("\n============= Req No. " + str(req_num) + " Answer =============" )
    print(messagetwo)

def calculator(control, mapType, loadFactor):
    return controller.calculator(control, mapType, loadFactor)

def loadData():
    """
    Solicita al controlador que cargue los datos en el modelo
    """
    albums, artists, tracks = controller.loadData(control)
    return albums, artists, tracks

def sortpopularityartist(control):
    return controller.sortpopularityartist(control)

# Se crea el controlador asociado a la vista
control = newController()

"""
Menu principal
"""
while True:
    try:
        printMenu()
        inputs = input('Seleccione una opción para continuar: ')
        if int(inputs[0]) == 1:
            print("\nCargando información de los archivos ....")
            albums, artists, tracks = loadData()
            print('\n' + 'Albums cargados: ' + str(albums))
            lastNumAlbums = controller.answerLst(control['model']['albums'])
            printSimplePrettyTable(lastNumAlbums, ['name','release_date','inicial_track_name','artist_name','total_tracks','album_type','external_urls'])
            print('\n' + 'Artistas cargados: ' + str(artists))
            lastNumArtists = controller.answerLst(control['model']['artists'])
            printSimplePrettyTable(lastNumArtists, ['name','artist_popularity','followers','relevant_track_name','genres'])
            print('\n' + 'Tracks cargados: ' + str(tracks))
            lastNumTracks = controller.answerLst(control['model']['tracks'])
            printSimplePrettyTable(lastNumTracks, ['name','popularity','disc_number','track_number','duration_ms','artists_names','href'])

        elif int(inputs[0]) == 2:
            year = int(input('Ingrese el año que desee consultar: ').strip())
            albumsByYear, howMany, time, memory = controller.albumsByReleaseYear(control['model'], year)
            if lt.size(albumsByYear) != 0:
                firstMessage = 'Albums released in ' + str(year)
                secondMessage = 'There are ' + str(howMany) + ' albums released in year ' + str(year)
                headers(1, firstMessage, secondMessage)
                print('\n The first 3 and last 3 albums in ' + str(year) + ' are: ')
                printSimplePrettyTable(albumsByYear, ['name','release_date','total_tracks','album_type','artist_name','external_urls'])
                print('Time used: ' + str(time))
                print('Memory used: ' + str(memory))
            else:
                input('No se encontraron albums. Oprima ENTER para continuar...1')

        elif int(inputs[0]) == 3:
            popularity = int(input('Ingrese la popularidad de los artistas que desee consultar: ').strip())
            artistByPopularity, howMany, time, memory = controller.artistByPopularity(control['model'], popularity)
            if lt.size(artistByPopularity) != 0:
                firstMessage = 'The artists with popularity rating of: ' + str(popularity)
                secondMessage = 'There are ' + str(howMany) + ' artists with ' + str(popularity) + ' popularity.'
                headers(2, firstMessage, secondMessage)
                print('\n The first 3 and last 3 albums with ' + str(howMany) + ' in popularity are: ... ')
                printSimplePrettyTable(artistByPopularity, ['artist_popularity', 'followers', 'name', 'relevant_track_name', 'genres'])
                print('Time used: ' + str(time))
                print('Memory used: ' + str(memory))
            else:
                input('No se encontraron albums. Oprima ENTER para continuar...')

        elif int(inputs[0]) == 4:
            popularity = int(input('Ingrese el nivel de popularidad de canciones que desee consultar: ').strip())
            tracksByPopularity, howMany, time, memory = controller.tracksByPopularity(control['model'], popularity)
            if lt.size(tracksByPopularity) != 0:
                firstMessage = 'The tracks with popularity ranking of' + str(popularity)
                secondMessage = 'There are ' + str(howMany) + ' tracks with ranking of ' + str(popularity)
                headers(3, firstMessage, secondMessage)
                print('\n The first 3 and last 3 tracks with ' + str(popularity) + ' in popularity are: ')
                printSimplePrettyTable(tracksByPopularity, ['popularity','duration_ms','name','disc_number','track_number','album_name','artists_names','href','lyrics'])
                print('Time used: ' + str(time))
                print('Memory used: ' + str(memory))
            else:
                input('No se encontraron canciones. Oprima ENTER para continuar...')

        elif int(inputs[0]) == 5:
            artistName = input('Ingrese el nombre del artista que desea consultar: ').strip()
            namesakeCount, artistlt = controller.UEXNamesake(control['model'], artistName)
            print('El artistas ' + str(artistName) + ' tiene '+ str(namesakeCount)+ ' homonimos.')
            if namesakeCount > 0:
                i = 0
                for artist in lt.iterator(artistlt):
                    i = i + 1
                    print(str(i) + '. ' + str(artist))
                namesake = int(input('Ingrese el homonimo que desea: ').strip())
                artistName = lt.getElement(artistlt, namesake)
            countryCode = input('Ingrese el nombre del pais a consultar (en Ingles): ').strip()
            countryname = pycountry.countries.search_fuzzy(countryCode)
            countryname = countryname[0].alpha_2
            popularTrackByArtist, howMany, time, memory, albumsSize, songSize = controller.popularTrackByArtist(control['model'], artistName, countryname)

            if lt.size(popularTrackByArtist) != 0:
                message1 = str(artistName) + ' Discography metrics in ' + countryCode + ' Code: ' + str(countryname)
                message2 = str(artistName) + ' avilable discography in ' + countryCode + ' Code: ' + str(countryname)
                headers(4, message1, message2)
                print('Unique Available Albums: ' + str(albumsSize))
                print('Unique Available Tracks: ' + str(songSize))
                print('\n The first 3 and last 3 albums in the range are ...')
                printSimplePrettyTable(popularTrackByArtist, ['name', 'album_name', 'artists_names', 'duration_ms', 'popularity', 'preview_url','href','lyrics'])
                print('Tiempo de ejecucion: ', time)
                print('Memory used: ' + str(memory))

            else:
                input('No se encontraron canciones. Oprima ENTER para continuar...')

        elif int(inputs[0]) == 6:
            artistName = input('Ingrese el nombre del artista que desee consultar: ').strip()
            namesakeCount, artistlt = controller.UEXNamesake(control['model'], artistName)
            print('El artistas ' + str(artistName) + ' tiene '+ str(namesakeCount)+ ' homonimos.')
            if namesakeCount > 0:
                i = 0
                for artist in lt.iterator(artistlt):
                    i = i + 1
                    print(str(i) + '. ' + str(artist))
                namesake = int(input('Ingrese el homonimo que desea: ').strip())
                artistName = lt.getElement(artistlt, namesake)
            sizeAlbumsArtist, countByType, albumssorted, trackArray, time, memory = controller.albumInfo(control['model'], artistName)
            if lt.size(albumssorted) != 0:
                firstMessage = 'Discography metrics from ' + str(artistName)
                secondMessage = 'Number of "singles": ' + str(countByType[0]) + '\nNumber of "compilations": ' + str(countByType[1]) + '\nNumber of "album": ' + str(countByType[2])  + '\nTotal Albums in Discorgraphy: ' + str(sizeAlbumsArtist)
                headers(5, firstMessage, secondMessage)
                print("\n +++ Albums Details +++ \nThe first and last 3 tracks in the range are ...")
                printSimplePrettyTable(albumssorted,['release_date', 'name' ,'total_tracks','album_type','artist_name', 'external_urls'])
                if lt.size(trackArray) != 0:
                    printONEPrettyTable(trackArray,['popularity','duration_ms','name','disc_number',"track_number",'artists_names','preview_url', 'href','lyrics'])
                    print('Time used: ' + str(time))
                    print('Memory used: ' + str(memory))
                else:
                    input('No se encuentran las canciones de los albums. Oprima ENTER para continuar...')
            else:
                input('No se encontraron albums. Oprima ENTER para continuar...')


        elif int(inputs[0]) == 7:
            countryName = input('Ingrese el nombre del pais a consultar (en Ingles): ').strip()
            countryCode = pycountry.countries.search_fuzzy(countryName)
            countryCode= countryCode[0].alpha_2
            artistName = input('Ingrese el nombre del artista que desea consultar: ').strip()
            namesakeCount, artistlt = controller.UEXNamesake(control['model'], artistName)
            print('El artistas ' + str(artistName) + ' tiene '+ str(namesakeCount)+ ' homonimos.')
            if namesakeCount > 0:
                i = 0
                for artist in lt.iterator(artistlt):
                    i = i + 1
                    print(str(i) + '. ' + str(artist))
                namesake = int(input('Ingrese el homonimo que desea: ').strip())
                artistName = lt.getElement(artistlt, namesake)
            topNum = int(input('\nIngrese el numero del top de canciones a identificar: ').strip())
            topTracks, tracksSize, time, memory = controller.tracksByDistributionOfArtist(control['model'], countryCode, artistName, topNum)
            if lt.size(topTracks) != 0:
                firstMessage = 'TOP ' + str(topNum) + ' tracks of ' + str(artistName) + ' in ' + str(countryName) + ' CODE: ' +str(countryCode)
                secondMessage = 'There are ' + str(tracksSize) + ' tracks released by ' + str(artistName) + ' in ' + str(countryName) + ' CODE: ' +str(countryCode)
                headers("6 (BONUS)", firstMessage, secondMessage)
                print('\nthe TOP' + str(topNum) + 'most popular tracks of this artist in Spotify are: ')
                printSimplePrettyTable(topTracks, ['release_date', 'available_markets', 'distribution', 'popularity', 'name', 'duration_ms','album_name', 'album_type', 'artists_names', 'href','lyrics'])
                print('Time used: ' + str(time))
                print('Memory used: ' + str(memory))



        elif int(inputs[0]) == 8:
            mapSelection = False
            while mapSelection == False:
                printMapOptions()
                mapTypeSelection = input('Opción seleccionada: ')
                if int(mapTypeSelection[0]) == 1:
                    mapType = 'CHAINING'
                    print('\nSeleciono SEPARATE_CHAINING')
                    input('Seleccion exitosa! Oprima ENTER para continuar...')
                    mapSelection = True
                elif int(mapTypeSelection[0]) == 2:
                    mapType = 'PROBING'
                    print('\nSeleciono LINEAR_PROBING')
                    input('Seleccion exitosa! Oprima ENTER para continuar...')
                    mapSelection = True
                else:
                    input('\nSeleccion Erronea! Oprima ENTER para continuar...')

            loadSelection = False
            while loadSelection == False:
                if int(mapTypeSelection) == 1:
                    printLoadChainingOptions()
                    loadChainingSelection = input('Opción seleccionada: ')
                    if int(loadChainingSelection[0]) == 1:
                        loadFactor = 2.0
                        print('\nSeleciono 2.0')
                        input('Seleccion exitosa! Oprima ENTER para continuar...')
                        loadSelection = True
                    elif int(loadChainingSelection[0]) == 2:
                        loadFactor = 4.0
                        print('\nSeleciono 4.0')
                        input('Seleccion exitosa! Oprima ENTER para continuar...')
                        loadSelection = True
                    elif int(loadChainingSelection[0]) == 3:
                        loadFactor = 8.0
                        print('\nSeleciono 8.0')
                        input('Seleccion exitosa! Oprima ENTER para continuar...')
                        loadSelection = True
                    else:
                        input('\nSeleccion Erronea! Oprima ENTER para continuar...')
                elif int(mapTypeSelection) == 2:
                    printLoadProbingOptions()
                    loadProbingSelection = input('Opción seleccionada: ')
                    if int(loadProbingSelection[0]) == 1:
                        loadFactor = 0.1
                        print('\nSeleciono 0.1')
                        input('Seleccion exitosa! Oprima ENTER para continuar...')
                        loadSelection = True
                    elif int(loadProbingSelection[0]) == 2:
                        loadFactor = 0.5
                        print('\nSeleciono 0.5')
                        input('Seleccion exitosa! Oprima ENTER para continuar...')
                        loadSelection = True
                    elif int(loadProbingSelection[0]) == 3:
                        loadFactor = 0.9
                        print('\nSeleciono 0.9')
                        input('Seleccion exitosa! Oprima ENTER para continuar...')
                        loadSelection = True
                    else:
                        input('\nSeleccion Erronea! Oprima ENTER para continuar...')
                else:
                    input('\nSeleccion Erronea :/ ! Oprima ENTER para continuar...')

            resultT, resultM = controller.calculator(control['model'], mapType, loadFactor)
            print('Para un mapa ', mapType, ' y un factor de carga ', loadFactor, ' los resultados son: ')
            print('Tiempo promedio: ', resultT, 'ms')
            print('Memoria promedio: ', resultM, 'kB')

        elif int(inputs[0]) == 0:
            break
        else:

            continue
    except:
        print("Ingreso una opción invalida, inténtelo de nuevo ...")
        continue

sys.exit(0)
