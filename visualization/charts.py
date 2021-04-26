#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 20 12:42:16 2021

@author: LiShuang
"""

import matplotlib.pyplot as plt
plt.rcParams['axes.unicode_minus'] = False
from matplotlib.offsetbox import TextArea
from matplotlib.offsetbox import AnnotationBbox
import seaborn as sns
import numpy as np
import pandas as pd

#%%
def pie(df, name):
    '''
    A histogram oof the specifed variable

    Parameters
    ----------
    df : pd.DataFrame
        Business details dataframe
    name : str
        A specified field of business details

    Returns
    -------
    None.
    '''
    df = df['category'].str.split('|').apply(lambda x: x[0])
    df = df.value_counts()
    plt.pie(df, labels=df.index.tolist())
    plt.title('The {} distribution of the searched results'.format(name))
    plt.show()
    
def histogram(df, name):
    '''
    a histogram of the specified variable

    Parameters
    ----------
    df : pd.DataFrame
        Business details dataframe
    name : str
        A specified field of business details

    Returns
    -------
    None.
    '''
    df = df.apply(float)
    plt.hist(df)
    plt.title("The {} distribution of the searched results".format(name))
    plt.show()

def barchart(df):
    '''
    a multi variable barplot

    Parameters
    ----------
    df : pd.DataFrame
        business details dataframe of chosen businesses

    Returns
    -------
    None.
    '''
    df['Name'] = [df['Name'].iloc[i]+'('+str(df.index[i])+')' for i in range(len(df))]
    df['rating'] = df['rating'].apply(float)
    df['price'] = df['price'].apply(lambda x: x.count('$'))
    df['review_count'] = df['review_count'].apply(int)
    df = df.loc[:, ['Name', 'rating', 'price', 'review_count']]
    df = df.set_index('Name')
    x = np.arange(len(df))

    y1 = df['rating']
    y2 = df['price']
    y3 = df['review_count']
    bar_width = 0.3
    tick_label = df.index.tolist()

    plt.bar(x,y1,bar_width,color='salmon',label='rating')
    plt.bar(x+bar_width,y2,bar_width,color='orchid',label='price')
    plt.bar(x+bar_width*2, y3, bar_width, color='orange', label='review_count')

    plt.legend()
    plt.xticks(x+bar_width/2, tick_label, rotation=45)
    plt.show()
    

def funnelchart(df):
    
    N = len(df)
    width = 0.55
    x1 = df.values
    x2= np.array((x1.max()-x1)/2)
    #x1+x2
    x3=[]
    for i,j in zip(x1,x2):
        x3.append(i+j)
    x3 = np.array(x3)
    
    y = -np.sort(-np.arange(N))
    labels = df.index.tolist()
    
    #figure
    fig = plt.figure(figsize=(12,8))
    ax = fig.add_subplot(111)
    
    #plot
    ax.barh(y,x3,width,tick_label=labels,color='r',alpha=0.85)
    ax.plot(x3,y,'red',alpha=0.7)
    ax.barh(y,x2,width,color='w',alpha =1)
    ax.plot(x2,y,'red',alpha=0.7)
    
    #setting
    transform = []       
    for i in range(0,len(x1)):
        if i < len(x1)-1:
            transform.append('%.2f%%'%((x1[i+1]/x1[i])*100))
    l = [(500,3),(500,2),(500, 1),(500, 0)]
    for a,b in zip(transform,l):
        offsetbox = TextArea(a, minimumdescent=False)
        ab = AnnotationBbox(offsetbox, b,
                            xybox=(0, 40),
                            boxcoords="offset points",
                            arrowprops=dict(arrowstyle="->"))
        ax.add_artist(ab)
    ax.set_xticks([0,1000])
    ax.set_yticks(y)
    
    plt.show()
    
