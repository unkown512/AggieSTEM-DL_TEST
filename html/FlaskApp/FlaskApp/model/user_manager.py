"""
  User manage model to manage the following functions:
    # db is the database object
    # user_id is the recno from user table
    # data is information in a dict to be used
    # answers are a list from [0,1,2] |-> [Q1,Q2,Q3]

    1) get_access_level(db, user_id)
    2) get_user_id(db, user_id)
    3) validate_user(db, email)
    4) check_password_hash(db, pw)
    5) check_security_answers(db, user_id, answers)
    6) add_user(db, data)
    7) get_all_users(db)
    8) update_user(db, user_id, new_user_data)
    9) delete_user(db, user_id)
    10) get_last_login(db, user_id)
    11) update_user_profile(db, user_id, data)

"""

from werkzeug.security import generate_password_hash, check_password_hash
from uuid import uuid4

import datetime
import random
import pymysql


def add_user(db, data):
    """
      Add a user to the database.
      user_data: [username, password, email, position, phone_number, pa, ca]
        pa: privacy agreement
        ca: contact agreement
    """
    username, password, email, position, phone_number, privacy_agreement, contact_agreement = data[:7]

    access_level_map = {'D': 3, 'S': 2}
    access_level_map = access_level_map.get(position, 0)

    password_hash = generate_password_hash(password)

    cursor = db.cursor()

    # user table insert
    sql = """ INSERT INTO `user`(username, position, email, phone_number,
            privacy_agreement, contact_agreement) 
            VALUES ('%s', '%s', '%s', '%s', '%s', '%s')
        """
    insert_tuple = (username, access_level_map, email, phone_number, str(privacy_agreement), str(contact_agreement))
    try:
        cursor.execute(sql % insert_tuple)
        db.commit()
    except pymysql.Error as e:
        print('Got error {!r}, errno is {}. Rollback'.format(e, e.args[0]))
        db.rollback()

    # security table insert. Q1-3 is empty for now
    user_id = str(get_user_id(db, username))
    sql = """ INSERT INTO `security`(user_id, password, question1, question2,
            question3, code) 
            VALUES ('%s', '%s', '%s', '%s', '%s', '%s')
        """
    insert_tuple = (user_id, password_hash, "", "", "", "")
    try:
        cursor.execute(sql % insert_tuple)
        db.commit()
    except pymysql.Error as e:
        print('Got error {!r}, errno is {}. Rollback'.format(e, e.args[0]))
        db.rollback()

    # profile table insert.
    sql = """ INSERT INTO `profile`(user_id, ref_name, external_link) 
            VALUES ('%s', '%s', '%s')
        """
    insert_tuple = (user_id, "", "")
    try:
        cursor.execute(sql % insert_tuple)
        db.commit()
    except pymysql.Error as e:
        print('Got error {!r}, errno is {}. Rollback'.format(e, e.args[0]))
        db.rollback()


def update_user_password(db, pw, user_id):
    cursor = db.cursor()
    sql = """ UPDATE `security` set password = '%s' where user_id='%s' """
    try:
        cursor.execute(sql % (generate_password_hash(pw), str(user_id)))
    except pymysql.Error as e:
        print('Got error {!r}, errno is {}. Rollback'.format(e, e.args[0]))
        db.rollback()
        return False
    return True


def validate_user(db, user_email, pw):
    cursor = db.cursor()
    # get user_id from user table.
    sql = """ SELECT recno from `user` where email = '%s' 
        """
    insert_tuple = (str(user_email))
    print(insert_tuple)
    try:
        print(sql % insert_tuple)
        cursor.execute(sql % insert_tuple)
        user_id = str(cursor.fetchone()[0])
        print(user_id)
    except pymysql.Error as e:
        print('Got error {!r}, errno is {}. Rollback'.format(e, e.args[0]))
        db.rollback()
        return False

    # get hash pw from security table
    sql = """ SELECT password from `security` where user_id = '%s' 
        """
    insert_tuple = (user_id)
    try:
        cursor.execute(sql % insert_tuple)
        hash_pw = str(cursor.fetchone()[0])
    except pymysql.Error as e:
        print('Got error {!r}, errno is {}. Rollback'.format(e, e.args[0]))
        db.rollback()
        return False

    if (check_password_hash(hash_pw, pw)):
        if (update_last_login(db, user_id)):
            return True

    return False


def update_last_login(db, user_id):
    cursor = db.cursor()
    sql = """ UPDATE user set last_login = NOW() where recno = '%s' limit 1"""
    insert_tuple = (user_id)
    try:
        cursor.execute(sql % insert_tuple)
        db.commit()
    except pymysql.Error as e:
        print('Got error {!r}, errno is {}. Rollback'.format(e, e.args[0]))
        db.rollback()
        return False
    return True


def get_id_from_email(db, email):
    cursor = db.cursor()
    # Get user_id from email
    try:
        cursor.execute("select recno from `user` where email = '%s'" % email)
    except pymysql.Error as e:
        print('Got error {!r}, errno is {}. Rollback'.format(e, e.args[0]))
        db.rollback()
        return False
    result = cursor.fetchone()
    if (result == None):
        return False
    return result[0]


def update_recover_code(db, email, code):
    cursor = db.cursor()
    # Get user_id from email
    try:
        cursor.execute("select recno from `user` where email = '%s'" % email)
    except pymysql.Error as e:
        print('Got error {!r}, errno is {}. Rollback'.format(e, e.args[0]))
        db.rollback()
        return False
    user_id = cursor.fetchone()[0]

    sql = """ UPDATE `security` set code = '%s', request_new_pw='1' where user_id = '%s' limit 1"""
    insert_tuple = (code, str(user_id))
    try:
        cursor.execute(sql % insert_tuple)
        db.commit()
    except pymysql.Error as e:
        print('Got error {!r}, errno is {}. Rollback'.format(e, e.args[0]))
        db.rollback()
        return False
    return True


def check_recover_code(db, email, code):
    cursor = db.cursor()
    # Get user_id from email
    try:
        cursor.execute("select recno from `user` where email = '%s'" % email)
    except pymysql.Error as e:
        print('Got error {!r}, errno is {}. Rollback'.format(e, e.args[0]))
        db.rollback()
        return False
    user_id = cursor.fetchone()[0]

    sql = """ select recno from `security` where user_id = '%s' and code = '%s' limit 1"""
    insert_tuple = (str(user_id), code)
    try:
        cursor.execute(sql % insert_tuple)
        db.commit()
    except pymysql.Error as e:
        print('Got error {!r}, errno is {}. Rollback'.format(e, e.args[0]))
        db.rollback()
        return False
    result = cursor.fetchone()
    if (result != None):
        return True
    else:
        return False


def get_user_id(db, username):
    cursor = db.cursor()
    sql = """
        SELECT recno from `user` where username = '%s' limit 1
        """
    try:
        cursor.execute(sql % username)
    except pymysql.Error as e:
        print('Got error {!r}, errno is {}. Rollback'.format(e, e.args[0]))
        db.rollback()
        return False
    return cursor.fetchone()[0]


def check_login(db, userid):
    cursor = db.cursor()
    sql = """
        SELECT recno, username, is_logged_in from `user` where recno = '%s' limit 1
        """
    try:
        cursor.execute(sql % userid)
        db.commit()
    except pymysql.Error as e:
        print('Got error {!r}, errno is {}. Rollback'.format(e, e.args[0]))
        db.rollback()
        return False
    result = cursor.fetchone()
    if result is None or result[2] == 0:
        return False
    return result


def user_login_status(db, userid, status):
    cursor = db.cursor()
    sql = """
        UPDATE `user` set is_logged_in = '%s' where recno = '%s' limit 1
        """
    try:
        cursor.execute(sql % (status, userid))
    except pymysql.Error as e:
        print('Got error {!r}, errno is {}. Rollback'.format(e, e.args[0]))
        db.rollback()
        return False
    return True


def get_username(db, email):
    cursor = db.cursor()
    sql = """
        SELECT username from `user` where email = '%s' limit 1
        """
    try:
        cursor.execute(sql % email)
    except pymysql.Error as e:
        print('Got error {!r}, errno is {}. Rollback'.format(e, e.args[0]))
        db.rollback()
        return False
    result = cursor.fetchone()
    if (result == None):
        return False
    return result[0]


def authenticate_user_id(db, user_id):
    cursor = db.cursor()
    sql = """
        SELECT username from `user` where recno = '%s' limit 1
        """
    try:
        cursor.execute(sql % user_id)
    except pymysql.Error as e:
        print('Got error {!r}, errno is {}. Rollback'.format(e, e.args[0]))
        db.rollback()
        return False

    result = cursor.fetchall()
    if (result == 1):
        return cursor.fetchone()[0]
    return False


def get_access_level(db, user_id):
    cursor = db.cursor()
    sql = """
        SELECT access_level from `security` where user_id = '%s' limit 1
        """
    try:
        cursor.execute(sql % user_id)
    except pymysql.Error as e:
        print('Got error {!r}, errno is {}. Rollback'.format(e, e.args[0]))
        db.rollback()
        return False
    return cursor.fetchone()[0]


def get_hashpw(db, user_id):
    cursor = db.cursor()
    sql = """
        SELECT passwword from `security` where user_id = '%s' limit 1
        """
    try:
        cursor.execute(sql % user_id)
    except pymysql.Error as e:
        print('Got error {!r}, errno is {}. Rollback'.format(e, e.args[0]))
        db.rollback()
        return False
    return cursor.fetchone()[0]


def get_profile_ahref_links(db, user_id):
    cursor = db.cursor()
    linkdata = {"ext": "", "csv": ""}
    sql = """
        SELECT external_link, ref_name from `profile` 
        where user_id = '%s' limit 1
        """
    try:
        cursor.execute(sql % user_id)
    except pymysql.Error as e:
        print('Got error {!r}, errno is {}. Rollback'.format(e, e.args[0]))
        db.rollback()
        return linkdata
    results = cursor.fetchone()
    if (results):
        linkdata['ext'] = results[0]
        linkdata['csv'] = results[1]
    return linkdata


def get_user_profile(db, user_id):
    cursor = db.cursor()
    sql = """
        SELECT phone_number, email, position, username from `user` where recno = '%s' limit 1
        """
    try:
        cursor.execute(sql % user_id)
    except pymysql.Error as e:
        print('Got error {!r}, errno is {}. Rollback'.format(e, e.args[0]))
        db.rollback()
        return False
    results = cursor.fetchone()
    userdata = {"phone": results[0], "email": results[1], "position": results[2], "username": results[3]}
    return userdata


def get_all_users(db):
    cursor = db.cursor()
    sql = """
        SELECT phone_number, email, position, username, recno, last_login, deleted from `user`
        """
    try:
        cursor.execute(sql)
    except pymysql.Error as e:
        print('Got error {!r}, errno is {}. Rollback'.format(e, e.args[0]))
        db.rollback()
        return False
    results = cursor.fetchall()
    return results


def delete_user(db, user_id):
    if (get_user_profile(db, user_id)):
        cursor = db.cursor()
        sql = """
          UPDATE `user` set deleted='1' where recno = '%s' limit 1
          """
        insert_tuple = (user_id)
        try:
            cursor.execute(sql % insert_tuple)
        except pymysql.Error as e:
            print('Got error {!r}, errno is {}. Rollback'.format(e, e.args[0]))
            db.rollback()
            return False
    return True


def update_user(db, user_id, new_user_data):
    if (get_user_profile(db, user_id)):
        cursor = db.cursor()
        insert_tuple = (user_id)
        valid_user_fields = ["position", "deleted"]
        valid_security_fields = ["access_level"]
        for col in new_user_data:
            if (col in valid_user_fields):
                sql = """ UPDATE `user` set """
                sql += col + "='"
                sql += str(new_user_data[col]) + "'"
                sql += " where recno='%s'"
                try:
                    cursor.execute(sql % insert_tuple)
                except pymysql.Error as e:
                    print('Got error {!r}, errno is {}. Rollback'.format(e, e.args[0]))
                    db.rollback()
                    return False
            elif (col in valid_security_fields):
                sql = """ UPDATE `security` set """
                sql += col + "='"
                sql += str(new_user_data[col]) + "'"
                sql += " where user_id='%s'"
                try:
                    cursor.execute(sql % insert_tuple)
                except pymysql.Error as e:
                    print('Got error {!r}, errno is {}. Rollback'.format(e, e.args[0]))
                    db.rollback()
                    return False
            else:
                return False
    else:
        return False
    return True


def check_email(db, email):
    cursor = db.cursor()
    sql = """
        SELECT email from `user` where email = '%s' limit 1
        """
    insert_tuple = (email)
    try:
        cursor.execute(sql % insert_tuple)
    except pymysql.Error as e:
        print('Got error {!r}, errno is {}. Rollback'.format(e, e.args[0]))
        db.rollback()
        return False
    results = cursor.fetchone()
    if (results != None):
        return True
    return False


def check_phone_number(db, phone_number):
    cursor = db.cursor()
    sql = """
        SELECT phone_number from `user` where phone_number = '%s' limit 1
        """
    insert_tuple = (phone_number)
    try:
        cursor.execute(sql % insert_tuple)
    except pymysql.Error as e:
        print('Got error {!r}, errno is {}. Rollback'.format(e, e.args[0]))
        db.rollback()
        return False
    results = cursor.fetchone()
    if (results != None):
        return True
    return False


def add_request_form(db, data):
    cursor = db.cursor()

    columns = "("
    values = "("
    for col in data:
        columns += str(col) + ","
        values += "'" + str(data[col]) + "'" + ","
    columns = columns[:-1] + ")"
    values = values[:-1] + ")"

    # user table insert
    sql = """ INSERT INTO `request_data` %s 
            VALUES %s
        """
    insert_tuple = (columns, values)
    try:
        cursor.execute(sql % insert_tuple)
        db.commit()
    except pymysql.Error as e:
        print('Got error {!r}, errno is {}. Rollback'.format(e, e.args[0]))
        db.rollback()


# TEST CASES FUNCTIONS
def DB_client():
    f = open("/home/aggie/.mysql/credentials", "rt")
    data = f.read().split("\n")
    host = data[0].split("=")[1].lstrip()
    user = data[1].split("=")[1].lstrip()
    pw = data[2].split("=")[1].lstrip()
    database = data[3].split("=")[1].lstrip()
    return pymysql.connect(host, user, pw, database)
# add_user(DB, ["test", "pw12345678", "djb@tamu.edu", "D", "8322740571", 1, 1])
# print(validate_user(DB, "djb@tamu.edu", "pw12345678"))
# print(get_username(DB, "djb@tamu.edu"))
# print(get_access_level(DB, "djb@tamu.edu"))
# print(get_user_profile(DB, "1"))
# print(get_user_profile(DB, "2"))
# print(get_all_users(DB))
# get_profile_ahref_links(DB, "1")
