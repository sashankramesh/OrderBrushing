# -*- coding: utf-8 -*-
"""
Created on Sat Jun 13 14:19:46 2020

@author: sasha
"""

import pandas as pd

#input csv file
brush= pd.read_csv('\\Kaggle\\input\\open-2-shopee-code-league-order-brushing\\order_brush_order.csv',sep=',')
brush.columns
brush['event_time'] =  pd.to_datetime(brush['event_time'])

def removeMinutes(val):
    new_val= val.replace(minute=0, second=0)
    return new_val

brush['new_datetime']= brush['event_time'].apply(lambda x: removeMinutes(x))

ordercount= brush.groupby(['shopid','new_datetime'])['orderid'].count().reset_index()
buyercount= brush.groupby(['shopid','new_datetime'])['userid'].nunique().reset_index()

new_df= pd.merge(ordercount,buyercount,how= 'inner', on=['shopid', 'new_datetime'])
new_df['concentrate rate']=new_df['orderid']/new_df['userid']
order_brush= new_df[new_df['concentrate rate']>= 3]
user_brush= pd.merge(order_brush,brush[['shopid','new_datetime','userid']] ,how= 'left', on=['shopid', 'new_datetime']).drop_duplicates()
user_brush['userid_y']=user_brush['userid_y'].astype(str)

final=(user_brush.groupby('shopid').agg({'userid_y' : ' & '.join}).reset_index().reindex(columns=user_brush.columns))
allshops=new_df[['shopid']].drop_duplicates()

allshops=pd.merge(allshops,final[['shopid','userid_y']], on='shopid',how='left')
allshops.fillna('0',inplace=True)

allshops.to_csv('\\kaggle\\working\\order_brushing.csv')









# 


