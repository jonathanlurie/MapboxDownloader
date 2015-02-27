'''
MapboxDownloader
=============
Copyright (c) 2015, Jonathan LURIE, All rights reserved.
This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 3.0 of the License, or (at your option) any later version.
This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.
You should have received a copy of the GNU Lesser General Public
License along with this library.
'''
import urllib2
import os
import datetime
import sys

from SettingFileReader import *
from PIL import Image


# downloads a distant file to a local address
# using urllib2
# return True in case of success, False in other cases
def downloadFile(distantURL, localURL):
    status = False

    #print(distantURL)

    try:

        # copy the file to local
        print("\tDownloading tile ... "),
        distantFile = urllib2.urlopen(distantURL)
        localFile = open(localURL, 'wb')
        localFile.write(distantFile.read())
        localFile.close()
        print("DONE ")
        status = False

    except urllib2.HTTPError as e:

        print("FAIL! (" + str(e.code) + ")")

    except urllib2.URLError as e:
        print("FAIL!")
        print("\nError status : " + str(e) )
        print("\nNote: Mapbox Studio need to be opened for tile downloading, is it?\n")

        exit()

    return status


# removes the contant of a specified folder,
# does not remove the containing folder itself
def removeContent(folder):

    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception, e:
            print e


# return a string containg the current datetime.
# like "2015-02-12T11-06"
def getDateFilename():
    return datetime.datetime.now().strftime("%Y-%m-%dT%H-%M")


# main
if __name__ == '__main__':

    # cleaning terminal
    os.system('cls' if os.name == 'nt' else 'clear')

    print("\n------------------------ Mapbox Downloader -------------------------------------\n")


    print("Reading settings...")

    # loading a setting from the setting file
    settings = SettingFileReader()

    # get geobox boundaries
    west = settings.getSetting("geobox", "west")
    south = settings.getSetting("geobox", "south")
    east = settings.getSetting("geobox", "east")
    north = settings.getSetting("geobox", "north")

    # get other param
    resolution =  settings.getSetting("image", "resolutionFactor")
    skin = settings.getSetting("image", "skin")
    zoom = settings.getSetting("image", "zoom")


    # get files and folder
    temporaryFolder = settings.getSetting("files", "temporaryFolder")
    outputFolder = settings.getSetting("files", "outputFolder")


    # get tiling setting
    latNbTiles = float(settings.getSetting("tiling", "latNbTiles"))
    lonNbTiles = float(settings.getSetting("tiling", "lonNbTiles"))

    # flush temporary folder
    removeContent(temporaryFolder)


    # split by a 10 x 10 mozaic
    lonStep = abs(east - west) / lonNbTiles
    latStep = abs(north - south) / latNbTiles


    # downloads the tiles to the local temporary directory
    # and build the final image tile by tile on the flow
    tileCounter = 0
    outputImage = None

    # for tile positioning within the output image
    leftPosition = 0
    topPosition = 0

    # saving tile size to check integrity
    tileWidth = None
    tileHeight = None

    numberOfWarnings = 0

    for lat in range(0, int(latNbTiles) + 0):

        tempNorth = north - lat * latStep
        tempSouth = tempNorth - latStep

        for lon in range(0, int(lonNbTiles) + 0):
            tempWest = west + lon * lonStep
            tempEast = tempWest + lonStep

            tempUrl = "http://localhost:3000/static/" + str(zoom) + "/" + str(tempWest) + "," + str(tempSouth) + "," + str(tempEast) + "," + str(tempNorth) + "@" + str(resolution) + "x.png?id=tmstyle://" + skin


            # define a local name for the tile
            localTileAddress = temporaryFolder + "/" + str(tileCounter) + ".png"

            # download the distant tile to the local temporary folder
            downloadFile(tempUrl, localTileAddress)


            # load the fresh tile with Pillow
            tempTile = Image.open(localTileAddress)


            # for the first tile, construct the output image
            if(tileCounter == 0):
                # all the tiles should be the same dimension, otherwise this won't work
                totalWidth = tempTile.size[0] * int(lonNbTiles)
                totalHeight = tempTile.size[1] * int(latNbTiles)
                outputImage = Image.new("RGB", (totalWidth, totalHeight) , "#FFFFFF")

                # for integrity checking
                tileWidth = tempTile.size[0]
                tileHeight = tempTile.size[1]

            # checking tile size
            if(tempTile.size[0] != tileWidth or tempTile.size[1] != tileHeight):
                print("[WARNING] tile size is different: " + str(abs(tempTile.size[0] - tileWidth)) + "px in width and " +  str(abs(tempTile.size[1] - tileHeight)) + "px over height.")
                numberOfWarnings = numberOfWarnings + 1

            # paste the fresh tile content to the output image
            print("\tPasting tile \t ... "),
            outputImage.paste(tempTile, (leftPosition, topPosition))
            print("DONE\t"),

            leftPosition = leftPosition + tempTile.size[0]

            tileCounter = tileCounter + 1
            percentDone = 100. * float(tileCounter) / (latNbTiles * lonNbTiles)

            print(str(percentDone) + "%")



        # update tile position
        topPosition = topPosition + tempTile.size[1]
        leftPosition = 0


    # displaying some warning message
    if(numberOfWarnings):
        print("\nFinal image is done with " + str(numberOfWarnings) + " tile size warnings (over " + str(int(latNbTiles * lonNbTiles)) + " tiles)."  )
    else:
        print("\nFinal image is done.")

    # finally export the whole map in PNG format
    finalName = outputFolder + "/" + getDateFilename() + ".png"

    print("\nSaving final image ... ")
    outputImage.save(finalName, "PNG")

    print("Final image available at:\n" + finalName + "\n")
