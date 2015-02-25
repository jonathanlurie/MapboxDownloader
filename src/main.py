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
from TileMerger import *

from SettingFileReader import *


def downloadFile(distantURL, localURL):
    try:

        # copy the file to local
        print("\tFile is downloading ... "),
        distantFile = urllib2.urlopen(distantURL)
        localFile = open(localURL, 'wb')
        localFile.write(distantFile.read())
        localFile.close()
        print("DONE "),

    except urllib2.HTTPError as e:

        print("FAIL! (" + str(e.code) + ")")


def removeContent(folder):

    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception, e:
            print e

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



    print("Fetchings tiles...")

    tileCounter = 0

    for lat in range(0, int(latNbTiles) + 0):

        #tempSouth = south + lat * latStep
        #tempNorth = tempSouth + latStep

        tempNorth = north - lat * latStep
        tempSouth = tempNorth - latStep

        for lon in range(0, int(lonNbTiles) + 0):
            tempWest = west + lon * lonStep
            tempEast = tempWest + lonStep

            tempUrl = "http://localhost:3000/static/" + str(zoom) + "/" + str(tempWest) + "," + str(tempSouth) + "," + str(tempEast) + "," + str(tempNorth) + "@" + str(resolution) + "x.png?id=tmstyle://" + skin

            downloadFile(tempUrl, temporaryFolder + "/" + str(tileCounter) + ".png")
            tileCounter = tileCounter + 1
            percentDone = 100. * float(tileCounter) / (latNbTiles * lonNbTiles)

            print("\t" + str(percentDone) + "%")



    print("\nMerging tiles...")
    # merge files

    merger = TileMerger()
    merger.setNbXtiles(int(lonNbTiles))
    merger.setNbYtiles(int(latNbTiles))
    merger.setMarginColor("#FFFFFF")
    merger.setMarginSize(0)
    merger.setTileExtention(".png")
    merger.setTileDirectory(temporaryFolder)
    merger.setOutputDirectory(outputFolder)
    merger.setTitle(getDateFilename())
    merger.mergeTilesAndExport()

    print("\nDone!\n")
