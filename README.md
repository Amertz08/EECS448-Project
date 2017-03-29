# EECS 448 Project

Group project for EECS 448.

## Setup
Make a virtual environment with virtualenvwrapper.

```bash
$ mkvirtualenv EECS448
(EECS448)$ pip install -r requirements.txt
(EECS448)$ mysql -u root -p
# Login to mysql
mysql> create database EECS448_dev;
mysql> create user 'EECS448'@'localhost' identified by 'pass';
mysql> grant all privileges on EECS448_dev.* to 'EECS448'@'localhost';
mysql> exit
Bye
(EECS448)$ python app/manage.py runserver
```

## Testing
All tests should be in `app/test`. Uses `pytest` module.

```bash
# Don't forget to create test db
mysql> create database EECS448_test;
mysql> grant all privileges on EECS448_test.* to 'EECS448'@'localhost';
```
To run tests do the following.
```bash
$ python app/manage.py test
```
