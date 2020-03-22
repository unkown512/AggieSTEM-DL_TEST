## Ignore error on pip3 install -r requirements.txt
https://stackoverflow.com/questions/22250483/stop-pip-from-failing-on-single-package-when-installing-with-requirements-txt

`cat requirements.txt | xargs -n 1 pip install` 

## modifications

flaskapp.wsgi moved to folder with __init__.py
change username and password in database_setup.py to local user.

## database setup

1. install mysql

2. configure user based on `https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-18-04` 

3. create table aggiestemdl

4. new a json file `AggieSTEM-DL-PRODUCTION/html/FlaskApp/FlaskApp/database/user_info.json` which contains your mysql username and password:

```
{
	"user": your username,
	"password": your password
}

```

5. run database_setup.py to initialize schema

## run flask app locally

1.copy snippet from `run_server.py` in AggieSTEM_DL_TEST repo

2. change ip to localhost
3. manually visit route other than localhost:8080/, such as localhost:8080/signup

