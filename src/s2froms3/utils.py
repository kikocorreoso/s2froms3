#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
This module contains some utils used mainly by the library itself.
'''

from typing import Union
import datetime as dt

def _iter_dates(
    start_date: Union[dt.date, dt.datetime], 
    end_date: Union[dt.date, dt.datetime]
):
    '''Helper function to create a (year, month) iterator from start_date to
    end_date.'''
    # REF: https://stackoverflow.com/a/5734564
    ym_start= 12*start_date.year + start_date.month - 1
    ym_end= 12*end_date.year + end_date.month - 1
    for ym in range( ym_start, ym_end + 1):
        y, m = divmod(ym, 12)
        yield y, m+1
