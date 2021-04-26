#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 14 20:02:14 2021

@author: LiShuang
"""

import requests
import math
import re
from urllib.parse import urlencode

HOST_URL = 'https://www.yelp.com/search?'

def get_response(find_desc, find_loc, start):
    '''
    get requests.Response object

    Parameters
    ----------
    find_desc : str
        the business to search
    find_loc : str
        the location to search
    start : int
        which page to start

    Returns
    -------
    response : requests.Response
        a requests.Response object
    '''
    params = {
                'find_desc': find_desc,
                'find_loc': find_loc,
                'ns': 1,
                'start': str(start*10)
            }
    response = requests.get(HOST_URL, params)
    return response

def get_max_pages_num(find_desc, find_loc):
    '''
    get the maximum number of pages on yelp.com

    Parameters
    ----------
    find_desc : str
        the business to search
    find_loc : str
        the location to search

    Returns
    -------
    max_page : int
        the maximum number of pages on yelp.com
    '''
    r = get_response(find_desc, find_loc, start=0)
    pattern = '<div class=" border-color--default__09f24__1eOdn text-align--center__09f24__1P1jK"><span class=" css-e81eai">(.*?)</span></div>'
    max_page = re.findall(pattern, r.text)[0].split(' ')[-1]
    max_page = int(max_page)
    return max_page

def get_all_business_ids(find_desc, find_loc, amounts):
    '''
    get all business unique ids on yelp.com

    Parameters
    ----------
    find_desc : str
        the business to search
    find_loc : str
        the location to search
    amounts : int
        the amount to search

    Returns
    -------
    business_ids : list
        a list of all business ids
    '''
    max_pages = get_max_pages_num(find_desc, find_loc)
    if math.ceil(amounts/10) > max_pages:
        print('The required number exceeds the maximum numbers available! ')
    else:
        max_pages = math.ceil(amounts/10)
    business_ids = []
    for page in range(max_pages):
        r = get_response(find_desc, find_loc, start=page)
        pattern = r'"bizId":"(.*?)",'
        tmp_ids = re.findall(pattern, r.text)
        business_ids.extend(tmp_ids)
    return business_ids
