# -*- coding: utf-8 -*-

import json
import datetime as dt
from typing import Union, Iterable
from pathlib import Path


import mgrs
import s3fs

from .utils import _iter_dates
from .products import Properties


def download_S2(
    lon: float, 
    lat: float, 
    start_date: Union[dt.date, dt.datetime], 
    end_date: Union[dt.date, dt.datetime], 
    what: Union[str, Iterable[str]],
    cloud_cover_le: float = 50,
    folder: Union[str, Path] = Path.home()
):
    '''Download Sentinel 2 COG (Cloud Optimized GeoTiff) images from Amazon S3. 
    
    The dataset on AWS contains all of the scenes in the original Sentinel-2 
    Public Dataset and will grow as that does. L2A data are available from 
    April 2017 over wider Europe region and globally since December  2018. Read 
    more at the url https://registry.opendata.aws/sentinel-2-l2a-cogs/
    
    Parameters
    ----------
    lon: float
        Float value defining the longitude of interest.
    lat: float
        Float value defining the latitude of interest.
    start_date: datetime.date or datetime.datetime
        Date to start looking for images to download.
    end_date: datetime.date or datetime.datetime
        Date to end looking for images to download.
    what: str or array_like
        Here you have to define what you want to download as a string or as an
        array_like of strings. Valid values are:
            'TCI', 'B01', 'B02', 'B03', 'B04', 'B05', 'B06', 'B07', 'B08',
            'B8A', 'B09', 'B11', 'B12', 'AOT', 'WVP', 'SCL'
    cloud_cover_le: float
        FLoat indicating the maximum cloud cover allowed. If the value is 10
        it indicates the allowed cloud cover on the image must be lower or
        equal to 10%. Default value is 50 (%).
    folder: str or Path
        Where to download the data. The folder must exist. Default value is 
        the home directory of the user.
    
    Returns
    -------
    list
        A list with the paths of the downloaded files.
    '''
    if start_date > end_date:
        raise ValueError(
            '`start_date` has to be lower or equal than `end_date`'
        )
    if isinstance(what, str):
        what = [what]
    for w in what:
        if w.upper() not in [item.value for item in Properties]:
            raise ValueError(f'{w} is not a valid product')
    fs = s3fs.S3FileSystem(anon=True, use_ssl=False)
    m = mgrs.MGRS()
    coord = m.toMGRS(lat, lon, MGRSPrecision=0)
    number, a, b = coord[:-3], coord[-3:-2], coord[-2:]
    start_date = dt.date(start_date. year, start_date.month, start_date.day)
    end_date = dt.date(end_date. year, end_date.month, end_date.day)
    contents = []
    for y, m in _iter_dates(start_date, end_date):
        path = f'sentinel-cogs/sentinel-s2-l2a-cogs/{number}/{a}/{b}/{y}/{m}'
        _contents = fs.ls(path)
        for _c in _contents:
            name = _c.split('/')[-1]
            info = _c + '/' + name + '.json'
            with fs.open(info, 'r') as f:
                info = json.load(f)
            date_str = name.split('_')[2]
            cc = info['properties']['eo:cloud_cover']
            date = dt.datetime.strptime(date_str, '%Y%m%d').date()
            if cloud_cover_le >= cc and start_date <= date <= end_date:
                for w in what:
                    path = _c + f'/{w}.tif'
                    contents.append(path)
                    with fs.open(path, 'rb') as f:
                        data = f.read()
                    path = Path(folder) / f'{name}_{w}.tif'
                    with open(path, 'wb') as f:
                        f.write(data)
    return sorted(contents)