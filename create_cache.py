#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 18 19:39:22 2021

@author: LiShuang
"""

from tools.sql_tools import execute_sql
import os

#%%
statement1 = '''
                CREATE TABLE Details
                (
                Business_id varchar(255) NOT NULL PRIMARY KEY,
                Name varchar(255),
                Is_closed varchar(255),
                Url varchar(255),
                Phone varchar(255),
                Display_phone varchar(255),
                Review_count varchar(255),
                Category varchar(255),
                Rating varchar(255),
                Location varchar(255),
                Latitude varchar(255),
                Longitude varchar(255),
                Photos varchar(255),
                Price varchar(255),
                Start varchar(255),
                End varchar(255),
                Transactions varchar(255)
                )
            '''

statement2 = '''
                CREATE TABLE Reviews
                (
                Business_id varchar(255) NOT NULL,
                Review_id varchar(255) NOT NULL,
                Text varchar(255),
                Rating varchar(255),
                Time_created varchar(255),
                Userid varchar(255),
                Username varchar(255),
                FOREIGN KEY (Business_id) REFERENCES Details(Business_id)
                )
                '''

#%%
if not os.path.exists('yelp_fusion_cache.db'):
    execute_sql(statement1)
    execute_sql(statement2)
    
    print('Database created Succesfully!')
else:
    print('Database already exists!')