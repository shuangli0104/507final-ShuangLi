#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 19 11:05:10 2021

@author: LiShuang
"""


import sqlite3

def execute_sql(statement, db='yelp_fusion_cache.db'):
    '''
    execute sql statement

    Parameters
    ----------
    statement : str
        the sql statement
    db : str, optional
        the name of database. The default is 'yelp_fusion_cache.db'.

    Returns
    -------
    data : list
        the select result.
    '''
    db = sqlite3.connect(db)
    c = db.cursor()
    c.execute(statement)
    if statement.startswith('SELECT'):
        data = c.fetchall()
        db.commit()
        db.close()
        return data
    else:
        db.commit()
        db.close()
    
def select_statement(table_name, business_id):
    '''
    create a select statement

    Parameters
    ----------
    table_name : str
        the name of table which to select
    business_id : str
        the business id to select

    Returns
    -------
    statement : str
        the sql select statement
    '''
    statement = "SELECT * FROM {} WHERE Business_id='{}'".format(table_name, business_id)
    return statement

def insert_statement(table_name, values):
    '''
    create a insert statement

    Parameters
    ----------
    table_name : str
        the name of table which to insert
    values : list
        a list data to insert

    Returns
    -------
    statement : str
        the sql insert statement
    '''
    statement = 'INSERT INTO %s ' % table_name + 'VALUES (' + ','.join(repr(value) for value in values) + ')'
    return statement
