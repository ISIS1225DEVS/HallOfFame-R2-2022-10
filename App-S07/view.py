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

from tabulate import tabulate
import textwrap
import config as cf
import sys
assert cf

from controller import Controller
default_limit = 1000
sys.setrecursionlimit(default_limit*100)

ctrl = Controller()
catalog = ctrl.catalog

class View():
    """
    La vista se encarga de la interacción con el usuario
    Presenta el menu de opciones y por cada seleccion
    se hace la solicitud al controlador para ejecutar la
    operación solicitada
    """
    size_load = "0%"
    inputs = -1

    def data(self):
        m = False
        if self.size_load == '0%':
            m = "+++ Por favor cargue los datos +++\n"
        return m
    def menu(self):
        print("Bienvenido")
        d = self.data()
        if d:
            print(d)
        else:
            print(f'Datos cargados actualmente: {self.size_load}')
        print("1- Cargar información en el catálogo")
        print("2- Listar los albumes en un año")
        print("3- Encontrar los artistas con una popularidad específica")
        print("4- Encontrar las canciones con una popularidad específica")
        print("5- Encontrar la canción más popular de un artista")
        print("6- Encontrar la discografia de un artista")
        # print("7- Clasificar las canciones con mayor distribución")
        print("0- Salir")

    def load(self):
        file_size = input("Ingrese tamaño del archivo: ")
        try:
            print("Cargando información de los archivos ....")
            bench = ctrl.loadData(file_size)
            self.size_load = file_size

            print(f'En total tardó {round(bench.elapsed,2)}ms y ocupó {round(bench.memo,2)}kB.')

            print('-'*38)
            print('artists ID count: '+ str(ctrl.catalog.artists.getSize()))
            # print('artistsMarket ID count: '+ str(ctrl.catalog.artistsIdMarket.getSize()))
            print('albums ID count: '+ str(ctrl.catalog.albums.getSize()))
            print('tracks ID count: '+ str(ctrl.catalog.tracks.getSize()))
            # print('years count: '+ str(ctrl.catalog.albumsByYear.getSize()))
            print('-'*38)

            list_albums = ctrl.catalog.albums.print()
            list_artists = ctrl.catalog.artists.print()
            list_tracks = ctrl.catalog.tracks.print()

            print('The first 3 and last 3 artists in the range are...')
            print(self.tabu(list_artists))
            print('The first 3 and last 3 albums in the range are...')
            print(self.tabu(list_albums))
            print('The first 3 and last 3 tracks in the range are...')
            print(self.tabu(list_tracks, True)[0])
        except Exception as e:
            print("No se encontró el archivo a cargar...")
            print("Más información:")
            print(e)
            print()
            self.size_load = '0%'

    def two(self):
        print("Por favor ingrese el año de los albumes a buscar...")
        year = input("Año: ")

        try:
            bench, (albumnsInYear, jan_count) = ctrl.two(year)
            print(f'En total tardó {round(bench.elapsed,2)}ms y ocupó {round(bench.memo,2)}kB.')

            print(f'There are {albumnsInYear.getSize()} albums released in {year}.')
            print(f'There are {jan_count} albums released in january-{year}.')

            lt = albumnsInYear.print()

            print(self.tabu(lt))
        except Exception as e:
            d = self.data()
            if d:
                print(d)
            else:
                print(f'No se encontró el año {year}.')
                print("Más información:")
                print(e)
                print()

    def three(self):
        print("Por favor ingrese el número de popularidad de los artistas a buscar...")
        popularity = input("Popularidad: ")
        try:
            bench, artistsInPop = ctrl.three(popularity)
            print(f'En total tardó {round(bench.elapsed,2)}ms y ocupó {round(bench.memo,2)}kB.')

            print(f'There are {artistsInPop.getSize()} artists with {popularity} of popularity.')
            lt = artistsInPop.print()
            print(self.tabu(lt))
        except Exception as e:
            d = self.data()
            if d:
                print(d)
            else:
                print(f'No se encontraron canciones con {popularity} de popularidad.')
                print("Más información:")
                print(e)
                print()

    def four(self):
        print("Por favor ingrese la popularidad de las canciones a buscar...")
        pop = input("Popularidad: ")
        try:
            bench, tracksByPop = ctrl.four(pop)
            print(f'En total tardó {round(bench.elapsed,2)}ms y ocupó {round(bench.memo,2)}kB.')

            print(f'There are {tracksByPop.getSize()} tracks with {pop} of popularity.')
            print(f'The first 3 and last 3 tracks with popularity of {pop} are...')
            lt = tracksByPop.print()
            print(self.tabu(lt, True)[0])
        except Exception as e:
            d = self.data()
            if d:
                print(d)
            else:
                print(f'No se encontraron canciones con {pop} de popularidad.')
                print("Más información:")
                print(e)
                print()

    def five(self):
        try:
            artist_name = input("Por favor ingrese el nombre del artista: ")
            market = input("Por favor ingrese el mercado: ")
            bench, albumsByArtistMarket, tracksByArtistMarket = ctrl.five(artist_name, market)
            print(f'En total tardó {round(bench.elapsed,2)}ms y ocupó {round(bench.memo,2)}kB.')

            print(f'There are {albumsByArtistMarket.getSize()} albums.')
            print(f'There are {tracksByArtistMarket.getSize()} tracks.')
            print(f'The most popular track are...')
            lt = tracksByArtistMarket.firstElement()
            print(self.tabu(lt))
        except Exception as e:
            d = self.data()
            if d:
                print(d)
            else:
                print(f'No se encontraron canciones con del artista {artist_name} en {market}.')
                print("Más información:")
                print(e)
                print()

    def six(self):
        artist_name = input("Por favor ingrese el nombre del artista: ")
        try:
            bench, albumsByArtist, albumsByArtistType ,tracks = ctrl.six(artist_name)

            print(f'En total tardó {round(bench.elapsed,2)}ms y ocupó {round(bench.memo,2)}kB.')

            # print(albumsByArtistType)
            for k,v in albumsByArtistType.items():
                if v > 0:
                    print(f'Number of "{k}": {v}')

            print(f'Total albums in discography: {albumsByArtist.getSize()}')

            lt = albumsByArtist.print()
            print('+++ Albums details +++')
            print('The first 3 and last 3 albums in the range are...')
            print(self.tabu(lt))

            print('+++ Tracks details +++')
            for track in tracks:
                print_track, name = self.tabu(track, True)
                print(f'Most popular track in "{name}"')
                print(print_track)
        except Exception as e:
            d = self.data()
            if d:
                print(d)
            else:
                print(f'No se encontró el artista {artist_name}.')
                print("Más información:")
                print(e)
                print()

    def tabu(self, lista, track=False):
        l = []
        dict_print = {}
        if not track:
            for element in lista:
                l.append(element.toDic())
        else:
            for element in lista:
                l.append(element.format())
        for k in l[0].keys():
            dict_print[k]= []

        for el in l:
            for k,v in el.items():
                if type(v) == list:
                    if len(v) <= 0:
                        v_str = "Unknown"
                    else:
                        v_str = ', '.join(v)
                elif type(v) == dict:
                    v_str = v['spotify']
                else:
                    v_str = v.strip()
                    if k == 'lyrics':
                        if v_str == '-99':
                            v_str = "Letra de la canción NO disponible"
                        else:
                            v_str = textwrap.shorten(v, width=96, placeholder='...')
                    if track and k == 'album_name':
                        name = v

                if k == 'available_markets':
                    v_str = textwrap.wrap(v_str, 32)
                else:
                    v_str = textwrap.wrap(v_str, 16)
                v_str = '\n'.join(v_str)
                dict_print[k].append(v_str)

        if not track:
            return tabulate(dict_print, headers="keys", tablefmt='grid')
        else:
            return tabulate(dict_print, headers="keys", tablefmt='grid'), name

    def run(self):
        while True:
            self.menu()
            inp = self.inputs
            try:
                if inp < 0:
                    inp = input("Seleccione una opción para continuar...\n")

                if int(inp) == 1:
                    ctrl.conf()
                    self.load()

                elif int(inp) == 2:
                    self.two()

                elif int(inp) == 3:
                    self.three()

                elif int(inp) == 4:
                    self.four()

                elif int(inp) == 5:
                    self.five()

                elif int(inp) == 6:
                    self.six()

                # exit program
                elif int(inp) == 0:
                    sys.exit(0)

                # other option selected
                else:
                    print("Opción invalida, por favor seleccione una opción valida...")
            except Exception as e:
                print("Opción invalida, por favor seleccione una opción valida...")


if __name__ == "__main__":
    # creating the View() object and running it
    main = View()
    main.run()
