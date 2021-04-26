#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  9 20:26:07 2021

@author: LiShuang
"""
import sys
import urllib
import os
sys.path.append('..')
from my_api_key import API_KEY
import argparse
import json
import pprint
import requests
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.parse import urlencode

# MY API_KEY
API_KEY = API_KEY

# API_HOST
API_HOST = 'https://api.yelp.com'
BUSINESS_PATH = '/v3/businesses/'

def request(host, path, api_key, url_params=None):
    '''
    Given your API_KEY, send a GET request to the API.

    Parameters
    ----------
    host : str
        The domain host of the API.
    path : str
        The path of the API after the domain.
    api_key : str
        Your API Key.
    url_params : dict, optional
        An optional set of query parameters in the request. The default is None.

    Returns
    -------
    dict
        The JSON response from the request.
    '''

    url_params = url_params or {}
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    headers = {
        'Authorization': 'Bearer %s' % api_key,
    }

    # print(u'Querying {0} ...'.format(url))

    response = requests.request('GET', url, headers=headers, params=url_params)

    return response.json()


def get_business(api_key, business_id):
    '''
    Query the Business API by a business ID.

    Parameters
    ----------
    api_key : str
        Your api key
    business_id : str
        The ID of the business to query.

    Returns
    -------
    dict
        The JSON response from the request.
    '''
    business_path = BUSINESS_PATH + business_id
    return request(API_HOST, business_path, api_key)

def get_business_reviews(api_key, business_id):
    '''
    Query the Business Reviews API by a business ID.

    Parameters
    ----------
    api_key : str
        Your api key
    business_id : str
        The ID of the business to query.

    Returns
    -------
    dict
        The JSON response from the request.
    '''
    business_review_path = BUSINESS_PATH + business_id + '/reviews'
    return request(API_HOST, business_review_path, api_key)
