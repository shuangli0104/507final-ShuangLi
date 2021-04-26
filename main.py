#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 18 19:35:44 2021

@author: LiShuang
"""

import sqlite3
import sys
sys.path.append('tools/')
sys.path.append('visualization/')
from tools.scraping_ids import get_all_business_ids
from tools.yelp_fusion import get_business
from tools.yelp_fusion import get_business_reviews
from tools.my_api_key  import API_KEY
from tools.sql_tools import *
from tools.parse_tools import *
import pandas as pd
import numpy as np
from visualization.charts import *
import os
os.system('python create_cache.py')

#%%
def main():
    global data
    global review_data
    while True:
        # The user interaction
        search_item = input('The restaurant you want to search(e.g. burgers, etc or exit): \n>>> ')
        if search_item == 'exit':
            break
        search_place = input('The place you want to search(e.g. Hong Kong, etc or exit): \n>>> ')
        if search_place == 'exit':
            break
        search_num = input('The number you want to search(P.S. Ten times, we suggest input less than 50 or exit): \n>>> ')
        if search_num == 'exit':
            break
        
        # get all business ids from yelp.com
        ids = get_all_business_ids(search_item, search_place, int(search_num))

        # initial the business detail data
        data = []
        
        # loop the ids and filter the business which doesn't have any information
        # step1: select from database by business id and return a list
        # Step2: if the list is null, then fetching, otherwise using cache
        for ID in ids:
            statement = select_statement('Details', ID)
            select_result = execute_sql(statement)
            if select_result == []:
                print('Fetching...')
                tmp_data = get_business(API_KEY, ID)
                tmp_data = parse_business_details(tmp_data)
            
                if tmp_data == '':
                    ids.remove(ID)
                    continue
                else:
                    statement = insert_statement('Details', tmp_data)
                    execute_sql(statement)
                    data.append(tmp_data)
            else:
                print('Using Cache...')
                data.append(select_result[0])
        
        # create a dataframe of all business details
        data = pd.DataFrame(data, columns=['Business_id', 'Name', 'is_closed',\
                                           'url', 'phone', 'display_phoone',\
                                           'review_count', 'category', 'rating',\
                                           'location', 'latitude', 'longitude',\
                                           'photos', 'price', 'start', 'end',\
                                           'transactions'], index=np.arange(1, len(data)+1))
        # show the business name list
        print('We found the following results...')
        print('-'*60)
        print(data['Name'])
        print('-'*60)
        
        # user interactive to show the specified business detail
        while True:
            business_NO = input('Please input the number of business you want to know(or exit): \n>>> ')
            print('\n')
            try:
                business_NO = int(business_NO)
                if business_NO > len(data):
                    print('The input exceed the maximum number, please try again!')
                    continue
                else:
                    print(data.loc[business_NO, ])
            except:
                if business_NO == 'exit':
                    break
                else:
                    print('Invalid number, please try again!')
                    continue
        
        # user interactive to show the specifed business review information
        # Step1: select from database by business id and return a list
        # Step2: if the list is null, then fetching, otherwise using cache
        while True:
            review_NO = input('Please input the number and we will show the reviews(or exit): \n>>> ')
            print('\n')
            try:
                review_NO = int(review_NO)
                if review_NO > len(data):
                    print('The input exceed the maximum number, please try again!')
                    continue
                else:
                    ID = data.loc[review_NO, 'Business_id']
                    statement = select_statement('Reviews', ID)
                    select_result = execute_sql(statement)
                    review_data = []
                    if select_result == []:
                        print('Fetching...')
                        tmp_data = get_business_reviews(API_KEY, ID)
                        for review in tmp_data['reviews']:
                            TMP = parse_business_reviews(review, ID)
                            statement = insert_statement('Reviews', TMP)
                            execute_sql(statement)
                            review_data.append(TMP)
                    else:
                        print('Using Cache...')
                        review_data.append(select_result[0])
            except:
                if review_NO == 'exit':
                    break
                else:
                    print('Invalid number, please try again!')
                    continue
            
            # create a dataframe of business review information
            review_data = pd.DataFrame(review_data, columns=['Business_id', 'Review_id', 'Text',\
                                                             'Rating', 'Time_created', 'UserId',\
                                                             'Username'], index=np.arange(1, len(review_data)+1))
                
            for index, user_review in enumerate(review_data['Text']):
                print(index+1, ' ', user_review)

        print('I can provide the following plots for you to know the data...')
        print('1.The rating distribution of the searched results(Histogram)')
        print('2.The price distribution of the searched results(Histogram)')
        print('3.The number of reviews distribution of the searched results(Histogram)')
        print('4.The pie chart of the business categories')
        print('5.The comparison(rating, price and reviews count) of any business you select(Barplot, better input less than 5)')
              
        while True:
            plot_no = input('Please choose a plot you want(or exit): \n>>> ')
            if plot_no == 'exit':
                break
            elif plot_no == '1':
                histogram(data['rating'], 'rating')
            elif plot_no == '2':
                histogram(data['price'].apply(lambda x: x.count('$')), 'price')
            elif plot_no == '3':
                histogram(data['review_count'], 'review counts')
            elif plot_no == '4':
                pie(data, 'category')
            elif plot_no == '5':
                business_no = input('Please input the business you want to know(split by ",", e.g. 1,3): \n>>> ')
                business_no = business_no.split(',')
                business_no = list(map(lambda x: int(x), business_no))
                barchart(data.loc[business_no, :])
            else:
                print('Invalid input, please try again!')
                continue
            
if __name__ == '__main__':
    main()
