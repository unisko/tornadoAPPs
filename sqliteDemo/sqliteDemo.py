#!/usr/bin/env python2.7
# -*-coding: utf-8-*-

'''
Created on 2015年7月3日

@author: peng
'''

import sqlite3
import json

conn = sqlite3.connect('example.db')
cur = conn.cursor()

sqlstr = "SELECT * FROM stocks ORDER BY price"

names = ('date', 'trans', 'symbol', 'qty', 'price')

results = list()


for row in cur.execute(sqlstr):
    result = dict()
    for i  in range(5):
        result[names[i]] = row[i]
    
    results.append(result)
        
print results