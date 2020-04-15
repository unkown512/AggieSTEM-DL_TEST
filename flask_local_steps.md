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

## Query dataset by keyword
1. manage data source to local mysql database

schema structure:
    user has many datasets
    dataset has many granted users
    make inner table as `id, (user.id, dataset.id)`

* schema `request_data` has column `approved`, possibly use this in the future.  Currently the schema has unnecessary columns.  Use new schema to simplify implementation.

* dataset:
  * id, primary key
  * name, char
  * description, char
  * upload time, datetime,
  * update time, datetime, # for dataset update display feature

* dataset_access:
  * id, primary key
  * dataset.id, foreign key from schema `dataset.id`
  * user.id, foreign key from schema `profile.user_id`
  * status, char, 'requested', 'granted', 'expired'
  * (possibly other datetime info on the above status)

### seed dataset
* execute seed_dataset.sql



## Error handling
* On foreign key creation error 1215, check if referenced table is of engine `MyISAM`.  If so, convert to `InnoDB`.  `ALTER TABLE user ENGINE = InnoDB`;
    * from: https://stackoverflow.com/questions/18391034/cannot-resolve-table-name-close-to

* Return keywords from request.form[] is of format '""'. remove additional quote to avoid SQL query param concatenation error.

April. 4. 2020
implement feature related to request form
1. user fill in request form
    * add auto fill form script (done)
2. user display submitted request form information (done)
3. admin view request forms from each user (done)
4. admin accept/reject request form, grant/refuse user access to a certain dataset
   * add link to dataset
     * a new column 'download_link' is appended to schema request_data
   * host dataset files on server (done)
   * select file on server
5. user see admin action reflected on their page, status update on the request, and link to download the dataset


changed columns with blob type to text type in request_data schema, to make it easier to display on front-end.

host file under the /dataset folder, upload from page: localhost:8080/upload

### manage data access
* add a link to dataset access management on dashboard if user access level is admin.
* display all data requests on this page
* admin may approve or reject a data request.  reflect update on schema request_data.approved column.