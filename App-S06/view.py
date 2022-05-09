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
import pycountry

def newController():
    """
    Se crea una instancia del controlador
    """
    control = controller.newController()
    return control

def printMenu():
    print("Welcome")
    print("1- Load information to the catalog")
    print("2- Search albums in a year of interest")
    print("3- Find artists by popularity")
    print("4- Find tracks by popularity")
    print("5- Find the most popular track by an artist")
    print("6- Find an artist's discography")
    print("7- Sort songs by artists with the highest distribution")


def loadData():
    albums, tracks, artists = controller.loadData(control)
    return albums, tracks, artists

#==========================================
# Generic functions
#==========================================

def firstThreeElements(list):
    return controller.subList(list, 1, 3)

def lastThreeElements(list):
    return controller.subList(list, -2, 3)

def sizeList(list):
    return controller.sizeList(list)

def sizeMap(map):
    return controller.sizeMap(map)

def getArtistName(artist_id):
    return controller.getArtistName(control, artist_id)

def getTrackName(track_id):
    return controller.getTrackName(control, track_id)

def getAlbumName(album_id):
    return controller.getAlbumName(control, album_id)

#==========================================
# Printing functions
#==========================================

def printChargeAlbums(albums):
    for album in lt.iterator(albums):
        artist_name = getArtistName(album['artist_id'])
        track_name = getTrackName(album['track_id'])
        if track_name == None:
            track_name = 'UNKNOWN'
        if artist_name == None:
            artist_name = 'UNKNOWN'

        print('Name: ' + album['name'] + ' | Release date: ' + str(album['date']) + ' | Relevant track: ' + track_name + ' | Artist: ' + artist_name + ' | Total tracks: ' + str(album['total_tracks']) + ' | Album Type: ' + album['album_type'] +   ' | External URLS: ' + album['external_urls'])
        print('---------------------------------------------------------------------------------------------------')

def printChargeTracks(tracks):
    for track in lt.iterator(tracks):
        album_name = getAlbumName(track['album_id'])
        if album_name == None:
            album_name = 'UNKNOWN'

        if len(track['artists_id']) > 1:
            artists_names = []
            for artist_id in track['artists_id']:
                artist_name = getArtistName(artist_id)
                if artist_name == None:
                    artist_name = 'UNKNOWN'
                artists_names.append(artist_name)
        else:
            artists_names = getArtistName(track['artists_id'][0])
            if artists_names == None:
                artists_names = 'UNKNOWN'

        print('Name: ' + track['name'] + ' | Popularity: ' + str(track['popularity']) + ' | Album: ' + album_name + ' | Disc number: ' + track['disc_number'] + ' | Track number: ' + track['track_number'] + ' | Duration: ' + str(track['duration_ms']) + ' | Artists: ' + str(artists_names) + ' | Href: ' + track['href'])
        print('---------------------------------------------------------------------------------------------------')

def printChargeArtists(artists):
    for artist in lt.iterator(artists):
        track_name = getTrackName(artist['track_id'])
        if track_name == None:
            track_name = 'UNKNOWN'
        if artist['genres'] == '[]':
            genres = 'NO DATA'
        else:
            genres = artist['genres']
        print('Name: ' + artist['name'] + ' | Popularity: ' + str(artist['artist_popularity']) + ' | Followers: ' + artist['followers'] + ' | Relevant Track: ' + track_name + ' | Genres: ' + str(genres))
        print('---------------------------------------------------------------------------------------------------')

def printAlbumsByYear(albums):
    for album in lt.iterator(albums):
        print('Name: ' + album['name'] + ' | Release date: ' + str(album['date']) + ' | Album Type: ' + album['album_type'] + ' | Artist: ' + album['artist_id'] + ' | Total tracks: ' + str(album['total_tracks']) + ' | External URLS: ' + album['external_urls'])
        print('---------------------------------------------------------------------------------------------------')

def printAlbumsByArtist(albums, artist):
    for album in lt.iterator(albums):
        print('Name: ' + album['name'] + ' | Release date: ' + str(album['date']) + ' | Album Type: ' + album['album_type'] + ' | Artist: ' + artist + ' | Total tracks: ' + str(album['total_tracks']))
        print('---------------------------------------------------------------------------------------------------')
    
def printArtistsByPopularity(artists):
    for artist in lt.iterator(artists):
        if artist['genres'] == '[]':
            genres = 'NO DATA'
        else:
            genres = artist['genres']
        print('Name: ' + artist['name'] + ' | Popularity: ' + str(artist['artist_popularity']) + ' | Followers: ' + artist['followers'] + ' | Relevant Track: ' + artist['track_id'] + ' | Genres: ' + str(genres))
        print('---------------------------------------------------------------------------------------------------')

def printTracksByPopularity(tracks):
    for track in lt.iterator(tracks):
        print('Name: ' + track['name'] + ' | Album: ' + track['album_id'] + ' | Artists: ' + str(track['artists_id']) + ' | Popularity: ' + str(track['popularity']) + ' | Duration: ' + str(track['duration_ms']) + ' | URL: ' + track['preview_url'] + ' | Lyrics: ' + track['lyrics'])
        print('---------------------------------------------------------------------------------------------------')

def printBestTrack(tracks, album_type, release_date):
    for track in lt.iterator(tracks):
        print('Name: ' + track['name'] + ' | Album: ' + track['album_name'] + ' | Album Type: ' + album_type + ' | Release Date: ' + str(release_date) + ' | Artists: ' + str(track['artists_id']) + ' | Popularity: ' + str(track['popularity']) + ' | Duration: ' + str(track['duration_ms']) + ' | URL: ' + track['preview_url'] + ' | Available Markets: ' + str(track['available_markets']) + ' | Lyrics: ' + track['lyrics'])
        print('---------------------------------------------------------------------------------------------------')

def printTracksByMarket(tracks):
    for track in lt.iterator(tracks):
        print('Name: ' + track['name'] + ' | Album: ' + track['album_id'] + ' | Release Date: ' + ' | Artists: ' + str(track['artists_id']) + ' | Popularity: ' + str(track['popularity']) + ' | Duration: ' + str(track['duration_ms']) + ' | URL: ' + track['preview_url'] + ' | Available Markets: ' + str(len(track['available_markets'])) + ' | Lyrics: ' + track['lyrics'])
        print('---------------------------------------------------------------------------------------------------')
"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Select an option to continue: \n')
    if int(inputs[0]) == 1:
        
        control = newController()
        print("Loading data from files ....")
        albums, tracks, artists = loadData()
        print('---------------------------------------------------------------------------------------------------')
        print('Loaded albums: ' + str(sizeMap(control['albums_ids'])))
        print('Loaded tracks: ' + str(sizeMap(control['tracks_ids'])))
        print('Loaded artists: ' + str(sizeMap(control['artists_ids'])))
        print('--------------------------------------------------------------------------------------------------- \n')

        print('The first 3 albums are: \n')
        first_three_albums = firstThreeElements(albums)
        printChargeAlbums(first_three_albums)
        print('\n')
        print('The last 3 albums are: \n')
        last_three_albums = lastThreeElements(albums)
        printChargeAlbums(last_three_albums)

        print('\n')

        print('The first 3 tracks are: \n')
        first_three_tracks = firstThreeElements(tracks)
        printChargeTracks(first_three_tracks)
        print('\n')
        print('The last 3 tracks are: \n')
        last_three_tracks = lastThreeElements(tracks)
        printChargeTracks(last_three_tracks)

        print('\n')

        print('The first 3 artists are: \n')
        first_three_artists = firstThreeElements(artists)
        printChargeArtists(first_three_artists)
        print('\n')
        print('The last 3 artists are: \n')
        last_three_artists = lastThreeElements(artists)
        printChargeArtists(last_three_artists)
        
    elif int(inputs[0]) == 2:
        year = int(input("Searching albums released on?: \n"))
        print('\n')

        albums_by_year = controller.getAlbumsYear(control, year)
        if albums_by_year == None:
            print(f'No albums available at year: {year}')
        else:
            list_size = sizeList(albums_by_year)
            print(f'There are {list_size} albums released in {year}\n')
            if list_size < 6:
                printAlbumsByYear(albums_by_year)
            else:
                print(f'The first 3 albums in {year} are: \n')
                first_three_elements = firstThreeElements(albums_by_year)
                printAlbumsByYear(first_three_elements)
                print('\n')
                print(f'The last 3 albums in {year} are: \n')
                last_three_elements = lastThreeElements(albums_by_year)
                printAlbumsByYear(last_three_elements)
    
    elif int(inputs[0]) == 3:
        popularity = float(input("Searching artists with popularity?: "))
        print('\n')

        top_artists = controller.getArtistsByPopularity(control, popularity)
        if top_artists == None:
            print(f'No artists available with popularity: {popularity}')
        else:
            list_size = sizeList(top_artists)
            print(f'There are {list_size} with popularity {popularity} \n')
            if list_size < 6:
                printArtistsByPopularity(top_artists)
            else:
                print(f'The first 3 artists with popularity {popularity} are: \n')
                first_three_elements = firstThreeElements(top_artists)
                printArtistsByPopularity(first_three_elements)
                print('\n')
                print(f'The last 3 artists with popularity {popularity} are: \n')
                last_three_elements = lastThreeElements(top_artists)
                printArtistsByPopularity(last_three_elements)

    elif int(inputs[0]) == 4:
        popularity = float(input("Searching tracks with popularity?: "))
        print('\n')

        top_tracks = controller.getTracksByPopularity(control, popularity)
        if top_tracks == None:
            print(f'No tracks available with popularity: {popularity}')
        else:
            list_size = sizeList(top_tracks)
            print(f'There are {list_size} with popularity {popularity} \n')
            if list_size < 6:
                printTracksByPopularity(top_tracks)
            else:
                print(f'The first 3 tracks with popularity {popularity} are: \n')
                first_three_elements = firstThreeElements(top_tracks)
                printTracksByPopularity(first_three_elements)
                print('\n')
                print(f'The last 3 tracks with popularity {popularity} are: \n')
                last_three_elements = lastThreeElements(top_tracks)
                printTracksByPopularity(last_three_elements)

    elif int(inputs[0]) == 5:
        artist_name = input('Enter artist name: ')
        country_name = input('Enter country name: ')
        print('\n')
        country = pycountry.countries.search_fuzzy(country_name)
        country_code = country[0].alpha_2

        artist_tracks = controller.getTracksByArtist(control, artist_name, country_code)
        artist_albums = controller.getAlbumsByArtist(control, artist_name)
        available_albums = controller.getAlbumsAvailable(artist_albums[0], country_code)
        if artist_tracks == None:
            print(f'No tracks available for: {artist_name}')
        else:
            print(f'Discography of {artist_name} in {country_name} ({country_code})')
            print(f'Available tracks: {sizeList(artist_tracks)}')
            print(f'Available albums: {sizeList(available_albums)}')
            print('\n')
            best_track = lt.subList(artist_tracks, 1, 1)
            for track in lt.iterator(best_track):
                album = controller.getAlbumById(control, track['album_id'])
                album_type = album['album_type']
                release_date = album['release_date']
            printBestTrack(best_track, album_type, release_date)
        
    elif int(inputs[0]) == 6:
        artist_name = input('Enter artist name: ')
        print('\n')

        albums_by_artist = controller.getAlbumsByArtist(control, artist_name)
        if albums_by_artist[0] == None:
            print(f'No albums availables for: {artist_name}')
        else:
            list_size = sizeList(albums_by_artist[0])
            print(f'Number of albums: {albums_by_artist[1]}')
            print(f'Number of compilations: {albums_by_artist[2]}')
            print(f'Number of sigles: {albums_by_artist[3]}')
            print(f'Total albums in Discography: {list_size}')
            print('\n')
            if list_size < 6:
                printAlbumsByArtist(albums_by_artist[0], artist_name)
                print('\n')
                for album in lt.iterator(albums_by_artist[0]):
                    track_list = controller.getTracksByAlbum(control, album['id'])
                    album_name = album['name']
                    print(f'Mos popular track in {album_name}')
                    print('\n')
                    if sizeList(track_list) == 1:
                        printTracksByPopularity(track_list)
                    else:
                        sorted_tracks = controller.sortTracksByAlbum(track_list)
                        best_track = lt.subList(sorted_tracks, 1, 1)
                        printTracksByPopularity(best_track)
                    print('-------------------------------------------------')
            else:
                print(f'The first 3 albums of {artist_name} are: \n')
                first_three_elements = firstThreeElements(albums_by_artist[0])
                printAlbumsByArtist(first_three_elements, artist_name)
                print('\n')
                print(f'The last 3 albums of {artist_name} are: \n')
                last_three_elements = lastThreeElements(albums_by_artist[0])
                printAlbumsByArtist(last_three_elements, artist_name)
                #============================================================#
                print('\n')
                for album in lt.iterator(first_three_elements):
                    track_list = controller.getTracksByAlbum(control, album['id'])
                    album_name = album['name']
                    print(f'Mos popular track in {album_name}')
                    print('\n')
                    if sizeList(track_list) == 1:
                        printTracksByPopularity(track_list)
                    else:
                        sorted_tracks = controller.sortTracksByAlbum(track_list)
                        best_track = lt.subList(sorted_tracks, 1, 1)
                        printTracksByPopularity(best_track)
                    print('\n')
                print('\n')
                for album in lt.iterator(last_three_elements):
                    track_list = controller.getTracksByAlbum(control, album['id'])
                    album_name = album['name']
                    print(f'Mos popular track in {album_name}')
                    print('\n')
                    if sizeList(track_list) == 1:
                        printTracksByPopularity(track_list)
                    else:
                        sorted_tracks = controller.sortTracksByAlbum(track_list)
                        best_track = lt.subList(sorted_tracks, 1, 1)
                        printTracksByPopularity(best_track)
                    print('\n')
        print('\n')
    
    elif int(inputs[0]) == 7:
        artist_name = input('Enter artist name: ')
        country_name = input('Enter country name: ')
        top = int(input('Searching top tracks?: '))
        print('\n')
        country = pycountry.countries.search_fuzzy(country_name)
        country_code = country[0].alpha_2

        artist_tracks = controller.getTracksByArtist(control, artist_name, country_code)
        if artist_tracks == None:
            print(f'No tracks available for: {artist_name}')
        else:
            list_size = sizeList(artist_tracks)
            if list_size >= top:
                top_artist_tracks = lt.subList(artist_tracks, 1, top)
                for track in lt.iterator(top_artist_tracks):
                    release_date = controller.getAlbumById(control, track['album_id'])['release_date']
                    album_type = controller.getAlbumById(control, track['album_id'])['album_type']
                if top < 6:
                    print(f'The top {top} tracks for {artist_name} in {country_name} are: \n')
                    printBestTrack(top_artist_tracks, album_type, release_date)
                else:
                    print(f'The first 3 tracks of {artist_name} in {country_name} are: \n')
                    first_three_elements = firstThreeElements(top_artist_tracks)
                    printBestTrack(first_three_elements, album_type, release_date)
                    print('\n')
                    print(f'The last 3 tracks of {artist_name} in {country_name} are: \n')
                    last_three_elements = lastThreeElements(top_artist_tracks)
                    printBestTrack(last_three_elements, album_type, release_date)
            else:
                print(f'The artist have less than {top} tracks')
                print('\n')
                for track in lt.iterator(artist_tracks):
                    release_date = controller.getAlbumById(control, track['album_id'])['release_date']
                    album_type = controller.getAlbumById(control, track['album_id'])['album_type']
                print(f'The top {top} tracks for {artist_name} in {country_name} are: \n')
                printBestTrack(artist_tracks, album_type, release_date)
            print('\n')
        
    else:
        sys.exit(0)
sys.exit(0)
