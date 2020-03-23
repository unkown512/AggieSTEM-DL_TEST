# @author xuluming
# @date 3/22/20 7:13 AM

import pymysql
import os, json

with open(os.path.dirname(os.path.abspath(__file__)) + "/user_info.json", 'r') as load_json:
    load_dict = json.load(load_json)
    user = load_dict['user']
    password = load_dict['password']

db = pymysql.connect("localhost", user, password, "aggiestemdl")
cursor = db.cursor()

with open(os.path.dirname(os.path.abspath(__file__)) + '/dataset_schema.sql', 'r') as f:
    sql_querys = f.read().split('\n\n')
    for query in sql_querys:
        cursor.execute(query)

with open(os.path.dirname(os.path.abspath(__file__)) + '/seed_dataset.sql', 'r') as f:
    sql_querys = f.read().split('\n\n')
    for query in sql_querys:
        cursor.execute(query)

db.commit()
db.close()

print('dataset seed complete.')
