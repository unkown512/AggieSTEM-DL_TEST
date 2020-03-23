# @author xuluming
# @date 3/22/20 5:26 PM

import pymysql
import os, json

with open(os.path.dirname(os.path.abspath(__file__))+"/user_info.json", 'r') as load_json:
    load_dict = json.load(load_json)
    user = load_dict['user']
    password = load_dict['password']

db = pymysql.connect("localhost", user, password, "aggiestemdl")
cursor = db.cursor()

# sql = """
# select name from dataset where id in (select dataset_id from dataset_access where user_id=? and status=?)"""

# sql = 'select name from dataset where id in (select dataset_id from dataset_access where user_id=%s and status=%s)'
# cursor.execute(sql, ('3', 'granted',))

sql = 'select name from dataset where name like %s and id in (select dataset_id from dataset_access where user_id=%s and status=%s)'
name = 'coco'
print(cursor.mogrify(sql, ('%{}%'.format(name),'3','granted',)))
cursor.execute(sql, ('%{}%'.format(name),'3','granted',))
result = cursor.fetchall()
print(result)
