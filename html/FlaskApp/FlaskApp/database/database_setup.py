#!/usr/bin/python3

import pymysql 
from database_table_schemas import db_table_schemas

# Open database connection
user = "xuluming"
password = "xuluming"
# db = pymysql.connect("localhost","aggie","Awsedrft22$","aggiestemdl")
db = pymysql.connect("localhost",user,password,"aggiestemdl")

# Initlaize cursor object to execute queries
cursor = db.cursor()

(table_list, table_attributes) = db_table_schemas()

#Create tables if they do not exists
for table in table_list:
  # create table query
  if(table in table_attributes):
    sql = "CREATE TABLE IF NOT EXISTS %s (" % table
    for columns in table_attributes[table]:
      sql += """ %s %s %s comment '%s' , """ % (columns[0], columns[1], columns[2], columns[3])
    sql += """ PRIMARY KEY(recno)) ENGINE=MyISAM DEFAULT CHARSET=latin1;"""
    print("CREATING TABLE %s \n %s" % (table, sql))
    cursor.execute(sql)

db.close()

