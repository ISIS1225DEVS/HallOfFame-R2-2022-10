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
 """

import config as cf
import csv
import time
import tracemalloc

csv.field_size_limit(2147483647)

from model import Model

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""
class Controller():
    catalog = Model.Catalog()

    def conf(self):
        self.catalog.artists = Model.Lists("ARRAY_LIST")
        self.catalog.albums = Model.Lists("ARRAY_LIST")
        self.catalog.tracks = Model.Lists("ARRAY_LIST")
        self.catalog.artistsId = Model.Maps("PROBING", 0.5)
        self.catalog.albumsId = Model.Maps("PROBING", 0.5)
        self.catalog.tracksId = Model.Maps("PROBING", 0.5)
        self.catalog.artistsName = Model.Maps("PROBING", 0.5)
        self.catalog.albumsByYear = Model.AlbumsYear("PROBING", 0.5, 47)
        self.catalog.artistsInPop = Model.ArtistPop("PROBING", 0.5, 96)
        self.catalog.tracksByPop = Model.TracksPop("PROBING", 0.5)
        self.catalog.artistsIdMarket = Model.ArtistIdMarket("PROBING", 0.5)
        self.catalog.artistsIdAlbums = Model.ArtistIdAlbums("PROBING", 0.5)
        self.catalog.albumTracks = Model.AlbumTracks("PROBING", 0.5)

    def loadData(self, file_size):
        __benchmark = Controller.Benchmark()
        __benchmark.start()
        self.conf()
        self.loadTracksId(file_size)
        self.loadArtists(file_size)
        self.loadAlbums(file_size)
        self.loadTracks(file_size)
        __benchmark.stop()
        return __benchmark

    def loadArtists(self, file_size):
        artistsfile = cf.data_dir + f'Spotify/spotify-artists-utf8-{file_size}.csv'
        input_file = csv.DictReader(open(artistsfile, encoding='utf-8'))
        for artist in input_file:
            ar = Model.createArtist(artist)
            ar.trackName(self.catalog.tracksId.mapa)
            self.catalog.artistsId.addElement(ar.id, ar)
            self.catalog.artistsName.addElement(ar.name, ar)
            self.catalog.artists.addLast(ar)
            self.catalog.artistsInPop.addArtistInPop(ar)
            self.catalog.artistsIdMarket.addArtistId(ar)
            self.catalog.artistsIdAlbums.addArtistId(ar)

    def loadAlbums(self, file_size):
        albumsfile = cf.data_dir + f'Spotify/spotify-albums-utf8-{file_size}.csv'
        input_file = csv.DictReader(open(albumsfile, encoding='utf-8'))
        for album in input_file:
            al = Model.createAlbum(album)
            al.artistName(self.catalog.artistsId.mapa)
            al.trackName(self.catalog.tracksId.mapa)
            self.catalog.albumsByYear.addAlbumYear(al)
            self.catalog.albumsId.addElement(al.id, al)
            self.catalog.albums.addLast(al)
            mapsToAdd = self.catalog.artistsIdMarket.getArtistsMap([al.artist_id])
            for artist in mapsToAdd:
                artist.addAlbumByMarket(al)

            mapsToAdd = self.catalog.artistsIdAlbums.getArtistsMap([al.artist_id])
            for artist in mapsToAdd:
                artist['albumsType'].addAlbumByType(al)
                artist['albums_list'].addLast(al)

    def loadTracks(self, file_size):
        tracksfile = cf.data_dir + f'Spotify/spotify-tracks-utf8-{file_size}.csv'
        input_file = csv.DictReader(open(tracksfile, encoding='utf-8'))
        for track in input_file:
            tr = Model.createTrack(track)
            tr.albumInfo(self.catalog.albumsId.mapa)
            tr.artistsName(self.catalog.artistsId.mapa)
            self.catalog.tracksByPop.addTrackPop(tr)
            self.catalog.tracks.addLast(tr)
            mapsToAdd = self.catalog.artistsIdMarket.getArtistsMap(tr.artists_id)
            for artist in mapsToAdd:
                artist.addTrackByMarket(tr)

            self.catalog.albumTracks.addTrack(tr)

            # mapsToAdd = self.catalog.artistsIdAlbums.getArtistsMap(tr.artists_id)

    def loadTracksId(self, file_size):
        tracksfile = cf.data_dir + f'Spotify/spotify-tracks-utf8-{file_size}.csv'
        input_file = csv.DictReader(open(tracksfile, encoding='utf-8'))
        for track in input_file:
            tr = Model.createTrack(track)
            self.catalog.tracksId.addElement(tr.id, tr)

    def two(self, year):
        __benchmark = Controller.Benchmark()
        __benchmark.start()
        albumsInYear = Model.two(self.catalog.albumsByYear, year)
        __benchmark.stop()
        return __benchmark, albumsInYear

    def three(self, pop):
        __benchmark = Controller.Benchmark()
        __benchmark.start()
        artistsInPop = Model.three(self.catalog.artistsInPop, pop)
        __benchmark.stop()
        return __benchmark, artistsInPop

    def four(self, pop):
        __benchmark = Controller.Benchmark()
        __benchmark.start()
        tracksByPop = Model.four(self.catalog.tracksByPop, pop)
        __benchmark.stop()
        return __benchmark, tracksByPop

    def five(self, artist_name, market):
        __benchmark = Controller.Benchmark()
        __benchmark.start()
        albumsByArtistMarket, tracksByArtistMarket = Model.five(Model, self.catalog.artistsIdMarket, artist_name, market, self.catalog.artistsName)
        __benchmark.stop()
        return __benchmark, albumsByArtistMarket, tracksByArtistMarket

    def six(self, artist_name):
        __benchmark = Controller.Benchmark()
        __benchmark.start()
        albumsByArtist, albumsByArtistType, tracks = Model.six(Model, self.catalog.artistsIdAlbums, artist_name, self.catalog.artistsName, self.catalog.albumTracks)
        __benchmark.stop()
        return __benchmark, albumsByArtist, albumsByArtistType, tracks


    class Benchmark:
        elapse = 0
        memo = 0

        def start(self):
            tracemalloc.start()
            self.start_time = self.getTime()
            self.start_memory = self.getMemory()

        def stop(self):
            self.stop_time = self.getTime()
            self.stop_memory = self.getMemory()
            self.elapsed = self.deltaTime(self.stop_time, self.start_time)
            self.memo = self.deltaMemory(self.stop_memory, self.start_memory)
            tracemalloc.stop()

        def getTime(self):
            """
            devuelve el instante tiempo de procesamiento en milisegundos
            """
            return float(time.perf_counter()*1000)

        def deltaTime(self, end, start):
            """
            devuelve la diferencia entre tiempos de procesamiento muestreados
            """
            elapsed = float(end - start)
            return elapsed

        # Funciones para medir la memoria utilizada

        def getMemory(self):
            """
            toma una muestra de la memoria alocada en instante de tiempo
            """
            return tracemalloc.take_snapshot()

        def deltaMemory(self, stop_memory, start_memory):
            """
            calcula la diferencia en memoria alocada del programa entre dos
            instantes de tiempo y devuelve el resultado en bytes (ej.: 2100.0 B)
            """
            memory_diff = stop_memory.compare_to(start_memory, "filename")
            delta_memory = 0.0

            # suma de las diferencias en uso de memoria
            for stat in memory_diff:
                delta_memory = delta_memory + stat.size_diff
            # de Byte -> kByte
            delta_memory = delta_memory/1024.0
            return delta_memory
