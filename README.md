# Mapbox Dowloader
## What is it?
A tool to (easily) download big maps using a Mapbox Studio skins, mainly for printing purposes.

## Why Mapbox Downloader?
When you want to print a hi-res map using Mapbox Studio and your favorite Mapbox skin project, you usually have to deal with **downloading** and then **merging** under Photoshop. That might be tricky an take some time.  
You may have tried to download a big area with hi-res and hi-zoom level directly from Mapbox Studio, but as far as you fill the buffer (or usually even before), the image to image to be downloaded is so huge that it won't work.

## How does it work?
You specify a geographic box (eventualy pretty large), a zoom level and a resolution factor, and then, Mapbox Downloader will automatically:

- Split the area in a mosaic
- Download tiles
- Merge them
- Export to a big map image in PNG format



## How to use it?
First, you have to edit the `setting.ini` file. Inside, you must mainly specify :

- The **geobox** , *west*, *south*, *east* and *north* are the WGS84 (means GPS) coordinates
- The **zoom** level in the **[image]** section, between 1 (super far) and 22 (super close)
- The **resolutionFactor** in the **[image]** section, from 1 (poor resolution) to 10 (high resolution)
- The **skin** address, is the local path to your `*.tm2` Mapbox Studio skin project

Then, you can specify the **latNbTiles** and **latNbTiles** values in the **[tiling]** section from 2 to 10 (or more).  
Lets say:

- High zoom level + High resolution + big area = high tiling (closer to 10)
- little surface + low res + far zoom level = little tiling (closer to 2)
- If you don't know, leave 5


## Compatibilities
Mapbox Downloader was coded and tested on Mac OSX Yosemite but should work as well on any Unix platform.

Windows users should just replace the *launcher.sh* file by the *.bat* equivalent.

## Dependencies
The image processing library [Pillow](https://github.com/python-pillow/Pillow) must be installed on your computer.

## TODO
Automatically (smartly) guess in how many tiles the area should be splited.