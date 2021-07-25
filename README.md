# s2froms3

[THIS REPOSITORY HAS BEEN MIGRATED TO [CODEBERG](https://codeberg.org/kikocorreoso/s2froms3)].

Get Sentinel-2 Cloud Optimized Geotiffs (COG) files from AWS S3.

## Installation

`pip install s2froms3`

## Dependencies

`mgrs`, `s3fs`

## Tutorial

The library is small and limited. It could be used to download Cloud Optimized
Geotiff files from AWS S3.

First of all we should import the library:

`import s2froms3`

To know what you can download from S3 you can use:

```python
for item in s2froms3.products.Properties:
    print(item.value)
    description = item.describe()
    for k, v in description.items():
        print(f'    {k}: {v}')
    print()
```

The previous code will print the available options to download COGs:

```
TCI
    resolution: 10
    title: True color image
    center wavelength: None

B01
    resolution: 60
    title: Band 1 (coastal)
    center wavelength: 0.4439

B02
    resolution: 10
    title: Band 2 (blue)
    center wavelength: 0.4966

B03
    resolution: 10
    title: Band 3 (green)
    center wavelength: 0.56

B04
    resolution: 10
    title: Band 4 (red)
    center wavelength: 0.6645

B05
    resolution: 20
    title: Band 5
    center wavelength: 0.7039

B06
    resolution: 20
    title: Band 6
    center wavelength: 0.7402

B07
    resolution: 20
    title: Band 7
    center wavelength: 0.7825

B08
    resolution: 10
    title: Band 8 (nir)
    center wavelength: 0.8351

B8A
    resolution: 20
    title: Band 8A
    center wavelength: 0.8648

B09
    resolution: 60
    title: Band 9
    center wavelength: 0.945

B11
    resolution: 20
    title: Band 11 (swir16)
    center wavelength: 1.6137

B12
    resolution: 20
    title: Band 12 (swir22)
    center wavelength: 2.22024

AOT
    resolution: 60
    title: Aerosol Optical Thickness (AOT)
    center wavelength: None

WVP
    resolution: 10
    title: Water Vapour (WVP)
    center wavelength: None

SCL
    resolution: 20
    title: Scene Classification Map (SCL)
    center wavelength: None
```

Once you know the different possibilities you can start to download COGs using
the following:

```python
import datetime as dt
from pathlib import Path

lon = 10 # Longitude of interest
lat = 10 # Latitude of interest
start_date = dt.date(2020, 8, 1) # Start date to search images
end_date = dt.date(2020, 8, 15) # End date to search images
what = ['B02', 'B03', 'B04'] # What we want to download
cc = 25 # Minimum cloud cover on each image, 25 is 25%
folder = Path('.') # Where the files will be downloaded

downloaded = s2froms3.download_S2(
    lon=lon,
    lat=lat,
    start_date=start_date,
    end_date=end_date,
    what=what,
    cloud_cover_le=cc,
    folder=folder
)
```

After a while, you will find several COG files in the same folder where you
were running the code. The function above will return the S3 file paths of
the downloaded files:

```python
print(downloaded)
```

The previous code will show:

```
['sentinel-cogs/sentinel-s2-l2a-cogs/32/P/PS/2020/8/S2A_32PPS_20200804_0_L2A/B02.tif',
 'sentinel-cogs/sentinel-s2-l2a-cogs/32/P/PS/2020/8/S2A_32PPS_20200804_0_L2A/B03.tif',
 'sentinel-cogs/sentinel-s2-l2a-cogs/32/P/PS/2020/8/S2A_32PPS_20200804_0_L2A/B04.tif',
 'sentinel-cogs/sentinel-s2-l2a-cogs/32/P/PS/2020/8/S2B_32PPS_20200809_0_L2A/B02.tif',
 'sentinel-cogs/sentinel-s2-l2a-cogs/32/P/PS/2020/8/S2B_32PPS_20200809_0_L2A/B03.tif',
 'sentinel-cogs/sentinel-s2-l2a-cogs/32/P/PS/2020/8/S2B_32PPS_20200809_0_L2A/B04.tif',
 'sentinel-cogs/sentinel-s2-l2a-cogs/32/P/PS/2020/8/S2B_32PPS_20200812_0_L2A/B02.tif',
 'sentinel-cogs/sentinel-s2-l2a-cogs/32/P/PS/2020/8/S2B_32PPS_20200812_0_L2A/B03.tif',
 'sentinel-cogs/sentinel-s2-l2a-cogs/32/P/PS/2020/8/S2B_32PPS_20200812_0_L2A/B04.tif']
```

Sometimes the location you have in mind is in a border of a tile (COG) and
the scene you want to analyze is not complete. You can check if the location
is close to a border/corner using the following function:

```python
from s2froms3 import point_in_tile

print(s2froms3.point_in_tile(2.98279, 39.73887))
```

The previous code will show

```

+ + + + + + + + + + + 
+                 O + 
+                   + 
+                   + 
+                   + 
+                   + 
+                   + 
+                   + 
+                   + 
+                   + 
+ + + + + + + + + + + 

```

This way you can better understand if, in this case, you will need to 
download also the COGs in the East, the Northeast and/or the North.

if you want to download also COG files adjacent to the target location
you could use the `also` option. For instance, in the previous case you
maybe also want to download the COGs located to the East (E), to the North
(N) and to the Northeast (NE). You could do so with the following code:

```python
lon, lat = 2.98279, 39.73887

downloaded = s2froms3.download_S2(
    lon=lon,
    lat=lat,
    start_date=start_date,
    end_date=end_date,
    what=what,
    cloud_cover_le=cc,
    folder=folder,
    also=['N', 'NE', 'E']
)
```

Now, you will get several COGs but also the COGs located to the N, NE and E.

You can see a practical example in the notebooks folder of this repo (in spanish and english).

## TO-DO

* ~~Use threading to download the files~~ (done :heavy_check_mark:).
* Add entry point / cli command (I'm thinking about it. Let's see).

## Issues / Feature requests

File an issue [here](https://github.com/kikocorreoso/s2froms3/issues) or start
a discussion [here](https://github.com/kikocorreoso/s2froms3/discussions).

## Code of conduct

Any interaction you have with me or others must be guided by the highest 
standards of politeness and respect.

## Releases

version 0.2.0

* Added function `point_in_tile` to check where is located the requested location within the COG tile.
* Added `ssl_option` keyword in `download_S2` function.
* Use threading to download COG files.
* Added `also` and `download` keywords in `download_S2` function.

version 0.1.0

* Initial version with basic machinery to download Sentinel-2 COGs from S3.
