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

import time
import config as cf
from pycountry import pycountry
from datetime import datetime
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import mergesort as merge
assert cf

class Model:
    class Catalog:
        artists = None
        albums = None
        tracks = None
        artistsId = None
        albumsId = None
        tracksId = None
        artistsName = None
        albumsByYear = None
        artistsInPop = None
        tracksByPop = None
        artistsIdMarket = None
        artistsIdAlbums = None
        albumTracks = None


    class Lists:
        def __init__(self, list_type):
            self.list = lt.newList(list_type)

        def cmp(self, el1, el2):
            return el1.name <= el2.name

        def addLast(self, element):
            lt.addLast(self.list, element)

        def getSize(self):
            return lt.size(self.list)

        def print(self):
            if self.getSize() >=6:
                f3 = lt.subList(self.list, 1, 3)
                l3 = lt.subList(self.list, self.getSize()-2, 3)
                for el in lt.iterator(l3):
                    lt.addLast(f3, el)
                return lt.iterator(f3)
            else:
                return lt.iterator(self.list)

        def firstElement(self):
            return lt.iterator(lt.subList(self.list, 1, 1))

        def mergeSort(self):
            self.list = merge.sort(self.list, self.cmp)


    class TracksWithPop(Lists):
        def cmp(self, track1, track2):
            if track1.duration_ms == track2.duration_ms:
                return track1.name <= track2.name
            else:
                return track1.duration_ms > track2.duration_ms

    class ArtistWithPop(Lists):
        def cmp(self, artist1, artist2):
            if float(artist1.followers) == float(artist2.followers):
                return artist1.name <= artist2.name
            else:
                return float(artist1.followers) > float(artist2.followers)

    class TracksByPop(Lists):
        def cmp(self, track1, track2):
            if track1.popularity == track2.popularity:
                if track1.duration_ms == track2.duration_ms:
                    return track1.name <= track2.name
                else:
                    return track1.duration_ms > track2.duration_ms
            else:
                return track1.popularity > track2.popularity

    class Maps:
        def __init__(self, map_type, load_factor, num = 10) -> None:
            self.mapa = mp.newMap(numelements=num, maptype=map_type,
                                loadfactor=load_factor)

        def addElement(self, key, value):
            mp.put(self.mapa, key, value)

        def getSize(self):
            return mp.size(self.mapa)


    class AlbumsYear(Maps):
        def addAlbumYear(self, album):
            key = album.year
            if not mp.contains(self.mapa, key):
                value = {'list': Model.Lists("ARRAY_LIST"),
                        'jan_count': 0}
            else:
                value = mp.get(self.mapa, key)
                value = me.getValue(value)

            if album.getMonth() == '01':
                value['jan_count'] += 1

            value['list'].addLast(album)
            super().addElement(key, value)


    class ArtistPop(Maps):
        def addArtistInPop(self, artist):
            key = artist.artist_popularity
            if not mp.contains(self.mapa, key):
                value = Model.ArtistWithPop("ARRAY_LIST")
            else:
                value = mp.get(self.mapa, key)
                value = me.getValue(value)

            value.addLast(artist)
            super().addElement(key, value)

    class TracksPop(Maps):
        def addTrackPop(self, track):
            key = track.popularity
            if not mp.contains(self.mapa, key):
                value = Model.TracksWithPop("ARRAY_LIST")
            else:
                value = mp.get(self.mapa, key)
                value = me.getValue(value)

            value.addLast(track)
            super().addElement(key, value)

    class MarketMap(Maps):
        def addAlbumByMarket(self, album):
            for country in album.available_markets:
                key = country
                if not mp.contains(self.mapa, key):
                    value = {
                        'albums': Model.Lists("ARRAY_LIST"),
                        'tracks': Model.TracksByPop("ARRAY_LIST")
                    }
                else:
                    value = mp.get(self.mapa, key)
                    value = me.getValue(value)
                value['albums'].addLast(album)
                super().addElement(key, value)

        def addTrackByMarket(self, track):
            for country in track.available_markets:
                key = country
                if not mp.contains(self.mapa, key):
                    value = {
                        'albums': Model.Lists("ARRAY_LIST"),
                        'tracks': Model.TracksByPop("ARRAY_LIST")
                    }
                else:
                    value = mp.get(self.mapa, key)
                    value = me.getValue(value)
                value['tracks'].addLast(track)
                super().addElement(key, value)

    class ArtistIdMarket(Maps):
        def addArtistId(self, artist):
            key = artist.id
            value = Model.MarketMap('PROBING', 0.5)
            super().addElement(key, value)

        def getArtistsMap(self, ids):
            mapsToAdd = []
            for id in ids:
                if mp.contains(self.mapa, id):
                    value = mp.get(self.mapa, id)
                    value = me.getValue(value)
                    mapsToAdd.append(value)
            return mapsToAdd

    class TypeMap(Maps):
        def addAlbumByType(self, album):
            key = album.album_type
            if not mp.contains(self.mapa, key):
                value = {
                    'albumsId': Model.Maps('PROBING', 0.5),
                    'albums_list': Model.Lists("ARRAY_LIST")
                }
            else:
                value = mp.get(self.mapa, key)
                value = me.getValue(value)
            value['albums_list'].addLast(album)
            value['albumsId'].addElement(album.id, album)
            super().addElement(key, value)



    class ArtistIdAlbums(Maps):
        def addArtistId(self, artist):
            key = artist.id
            value = {
                'albums_list' : Model.Lists("ARRAY_LIST"),
                'albumsType' : Model.TypeMap('PROBING', 0.5, 7)
            }
            super().addElement(key, value)

        def getArtistsMap(self, ids):
            mapsToAdd = []
            for id in ids:
                if mp.contains(self.mapa, id):
                    value = mp.get(self.mapa, id)
                    value = me.getValue(value)
                    mapsToAdd.append(value)
            return mapsToAdd

    class AlbumTracks(Maps):
        def addTrack(self, track):
            key = track.album_id
            if not mp.contains(self.mapa, key):
                value = Model.TracksByPop("ARRAY_LIST")
            else:
                value = mp.get(self.mapa, key)
                value = me.getValue(value)
            value.addLast(track)
            super().addElement(key, value)
    class Artist:
        revelant_track_name = "Unknown"

        def __init__(self, name, id, track_id, artist_popularity, followers,
                    genres) -> None:
            self.name = name
            self.id = id
            self.track_id = track_id
            self.artist_popularity = artist_popularity
            self.followers = followers
            self.genres = eval(genres)

        def trackName(self, tracksId):
            if mp.contains(tracksId, self.track_id):
                track = mp.get(tracksId, self.track_id)
                track = me.getValue(track)
                name = track.name
                self.revelant_track_name = name

        def toDic(self):
            val = {
                'name': self.name,
                'id': self.id,
                'revelant_track_name': self.revelant_track_name,
                'artist_popularity': self.artist_popularity,
                'followers': self.followers,
                'genres': self.genres,
            }
            return val


    class Album:
        revelant_track_name = "Unknown"
        artist_album_name = "Unknown"
        def __init__(self, name, id, track_id, total_tracks, external_urls, album_type,
                    available_markets, artist_id, release_date, relase_date_precision) -> None:
            self.name = name
            self.id = id
            self.track_id = track_id
            self.total_tracks = total_tracks
            self.external_urls = eval(external_urls)
            self.album_type = album_type
            self.available_markets = eval(available_markets)
            self.artist_id = artist_id
            self.release_date_precision = relase_date_precision
            self.release_date = release_date
            self.year = self.getYear()

        def getYear(self):
            presicion = self.release_date_precision
            if presicion == "day":
                date = datetime.strptime(self.release_date, "%Y-%m-%d")
                year = datetime.strftime(date, "%Y")

            elif presicion == "month":
                date = datetime.strptime(self.release_date, "%b-%y")
                year = datetime.strftime(date, "%Y")
            else:
                year = self.release_date

            return year

        def getMonth(self):
            presicion = self.release_date_precision
            if presicion == "day":
                date = datetime.strptime(self.release_date, "%Y-%m-%d")
                month = datetime.strftime(date, "%m")

            elif presicion == "month":
                date = datetime.strptime(self.release_date, "%b-%y")
                month = datetime.strftime(date, "%m")
            else:
                month = -1

            return month

        def artistName(self, artistsId):
            if mp.contains(artistsId, self.artist_id):
                artista = mp.get(artistsId, self.artist_id)
                artista = me.getValue(artista)
                name = artista.name
                self.artist_album_name = name

        def trackName(self, tracksId):
            if mp.contains(tracksId, self.track_id):
                track = mp.get(tracksId, self.track_id)
                track = me.getValue(track)
                name = track.name
                self.revelant_track_name = name

        def toDic(self):
            val = {
                'name': self.name,
                'id': self.id,
                'revelant_track_name': self.revelant_track_name,
                'artist_album_name': self.artist_album_name,
                'total_tracks': self.total_tracks,
                'external_urls': self.external_urls,
                'album_type': self.album_type,
                # 'available_markets': self.available_markets,
                'release_date': self.release_date,
            }
            return val


    class Track:
        album_name = "Unknown"
        release_date = "Unknown"
        album_type = "Unkonwn"
        available_markets = "Unknown"

        def __init__(self, name, id, album_id, popularity, artists_id,
                    duration_ms, href, lyrics, available_markets, track_number) -> None:
            self.name = name
            self.id = id
            self.album_id = album_id
            self.popularity = popularity[:-2]
            self.artists_id = eval(artists_id)
            self.artists_names = []
            self.duration_ms = float(duration_ms)
            self.href = href
            self.lyrics = lyrics
            self.available_markets = eval(available_markets[1:-1])
            self.track_number = track_number

        def artistsName(self, artistsId):
            for artist_id in self.artists_id:
                if mp.contains(artistsId, artist_id):
                    artista = mp.get(artistsId, artist_id)
                    artista = me.getValue(artista)
                    name = artista.name
                    self.artists_names.append(name)

        def albumInfo(self, albumsId):
            if mp.contains(albumsId, self.album_id):
                album = mp.get(albumsId, self.album_id)
                album = me.getValue(album)
                name = album.name
                release = album.release_date
                album_type = album.album_type
                markets = album.available_markets
                self.album_name = name
                self.release_date = release
                self.album_type = album_type
                self.available_markets = markets

        def toDic(self):
            val = {
                'name': self.name,
                'id': self.id,
                'album_name': self.album_name,
                'popularity': self.popularity,
                'artists_names': self.artists_names,
                'duration_ms': str(self.duration_ms),
                'release_date': self.release_date,
                'album_type': self.album_type,
                'href': self.href,
                'lyrics': self.lyrics,
                'available_markets': self.available_markets,
            }
            return val

        def format(self):
            val = {
                'name': self.name,
                'id': self.id,
                'album_name': self.album_name,
                'popularity': self.popularity,
                'artists_names': self.artists_names,
                'duration_ms': str(self.duration_ms),
                'track_number': self.track_number,
                'href': self.href,
                'lyrics': self.lyrics,
            }
            return val

    def createAlbum(album):
        album  = Model.Album(album["name"], album["id"], album["track_id"], album["total_tracks"],
                    album["external_urls"], album["album_type"], album["available_markets"],
                    album["artist_id"], album["release_date"], album["release_date_precision"])

        return album


    def createArtist(artist):
        artist  = Model.Artist(artist["name"], artist["id"], artist["track_id"], artist["artist_popularity"],
                    artist["followers"], artist["genres"])
        return artist

    def createTrack(track):
        track  = Model.Track(track["name"], track["id"], track["album_id"], track["popularity"],
                    track["artists_id"], track["duration_ms"], track["href"], track["lyrics"], track['available_markets'], track['track_number'])
        return track

    def two(catalog, year):
        albumsInYear_count = mp.get(catalog.mapa, year)
        albumsInYear = me.getValue(albumsInYear_count)['list']
        albumsInYear.mergeSort()
        jan_count = me.getValue(albumsInYear_count)['jan_count']
        return albumsInYear, jan_count

    def three(catalog, pop):
        artistsInPop = mp.get(catalog.mapa, (pop + ".0"))
        artistsInPop = me.getValue(artistsInPop)
        artistsInPop.mergeSort()
        return artistsInPop

    def four(catalog, pop):
        tracksByPop = mp.get(catalog.mapa, pop)
        tracksByPop = me.getValue(tracksByPop)
        tracksByPop.mergeSort()
        return tracksByPop

    def five(self, catalog, artist_name, market, artistsName):
        artist_id = mp.get(artistsName.mapa, artist_name)
        artist_id = me.getValue(artist_id).id
        market = self.formatMarket(market)
        marketsByArtist = mp.get(catalog.mapa, artist_id)
        marketsByArtist = me.getValue(marketsByArtist)
        artistMarket = mp.get(marketsByArtist.mapa, market)
        artistMarket = me.getValue(artistMarket)
        albumsArtistMarket = artistMarket['albums']
        tracksArtistMarket = artistMarket['tracks']

        tracksArtistMarket.mergeSort()

        return albumsArtistMarket, tracksArtistMarket

    def six(self, catalog, artist_name, artistsName, albumTracks):
        artist_id = mp.get(artistsName.mapa, artist_name)
        artist_id = me.getValue(artist_id).id
        artistAlbums = mp.get(catalog.mapa, artist_id)
        artistAlbums = me.getValue(artistAlbums)
        albumsArtistList = artistAlbums['albums_list']
        albumsArtistType= artistAlbums['albumsType']
        tracks = []
        for album in albumsArtistList.print():
            key = album.id
            if mp.contains(albumTracks.mapa, key):
                albumWithTracks = mp.get(albumTracks.mapa, key)
                albumWithTracks = me.getValue(albumWithTracks)
                if albumWithTracks.getSize() > 0:
                    albumWithTracks.mergeSort()
                    tracks.append(albumWithTracks.firstElement())

        albumsArtistTypeInfo= {'compilation': 0, 'single': 0, 'album': 0}
        for k in albumsArtistTypeInfo.keys():
            # print(mp.keySet(albumsArtistType.mapa))
            if mp.contains(albumsArtistType.mapa, k):
                size = mp.get(albumsArtistType.mapa, k)
                size = me.getValue(size)
                size = size['albums_list'].getSize()
                albumsArtistTypeInfo[k] = size

        return albumsArtistList, albumsArtistTypeInfo, tracks
    def formatMarket(market_name):
        market_id = pycountry.countries.search_fuzzy(market_name)
        market_id = market_id[0].alpha_2
        return market_id

