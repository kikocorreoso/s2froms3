#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime as dt
import sys
from pathlib import Path

sys.path.append(str(Path('.', 'src')))

import pytest
from s2froms3 import download_S2 # type: ignore
from s2froms3 import utils


def test_inputs():
    start = dt.date(2000, 1, 1)
    end = dt.date(1999, 1, 1)
    with pytest.raises(ValueError):
        download_S2(10, 10, start, end, what='B01')
    
    start = dt.date(2020, 1, 1)
    end = dt.date(2020, 2, 1)
    with pytest.raises(ValueError):
        download_S2(10, 10, start, end, what='B15')
    
    start = dt.date(2020, 1, 1)
    end = dt.date(2020, 2, 1)
    with pytest.raises(TypeError):
        download_S2(10, 10, start, end, what='B01', cloud_cover_lw='10')

def test_nodata():
    # no sentinel-2 data on this period so an empty list is returned
    start = dt.date(2014, 1, 1)
    end = dt.date(2015, 1, 1)
    assert download_S2(10, 10, start, end, what='B01') == []
    
def test_iterdates():
    start = dt.date(2000, 1, 1)
    end = dt.date(2000, 12, 1)
    assert len(list(utils._iter_dates(start, end))) == 12