#!/usr/bin/python2.7
#coding=utf-8
'''
Created on 2015年6月22日

@author: peng
'''

import web
import xml.etree.ElementTree as ET

tree = ET.parse('./user_data.xml')
root = tree.getroot()

urls = ('/users', 'list_users',
        '/users/(.*)', 'get_user')

app = web.application(urls, globals())

class list_users:
    def GET(self):
        output = 'users:['
        for child in root:
            output += str(child.attrib) + ','
        output += ']'
        return output

class get_user:
    def GET(self, user):
        for child in root:
            if child.attrib['id'] == user:
                return str(child.attrib)
            
if __name__ == '__main__':
    app.run()
