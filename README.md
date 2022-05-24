# Project Name :: XT-O1-Dynamic

# Commands 
Create Virtualvenv
- clone project from git
> after cloning 
> use below commands
- python -m venv clock-env
- clock-env\Scripts\activate.bat 
- go to project dir (cd )
- pip install -r requirements.txt

# change DataBase in settings
tables & cloums use below commands, (adding single or more fields into the model use, "migrate command")
- after defining db details (models)
> Use Below Commands
- python manage.py makemigrations
- python manage.py migrate

# Installations
install any Third party library (1) or avialable req list use (2) below commands
- pip install packagename
- pip list
- pip install -r requirements.txt

-Installation
Before you get started with using PostgreSQL, you'll have to install it. Follow these steps to get started:

Website:
There are a couple of ways to install PostgreSQL. One of the easier ways to get started is with Postgres.app. Navigate to http://postgresapp.com/ and then click "Download":


# Settings.py
add third party librarys ,apps  and Database changes,,,,,,
>DB settings

DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': '#',
            'USER': '#',
            'PASSWORD': '#',
            'HOST': 'localhost',
            'PORT': '5432',
            'options':{
                'init_command':"SET sql_mode='STRICT_TRANS_TABLES'"
            }
        }
    }

 ![Example screenshot](imgage/db.png)

## Table of Contents
* [General Info](#general-information)
* [Technologies Used](#technologies-used)
* [Setup](#setup)
* [Run Server](#RunServer-Commands)
* [Host](#Host)


## General Information
- This is a UserManagement Application.
- This application contains diffrent roles
> What is the purpose of your project?
- working some domain and doing the work as per requirements. 



## Technologies Used
- Django -3.2.13
- djangorestframework -3.13.1
- Python 3.8.10


## Setup
What are the project requirements/dependencies? Where are they listed?
- check A requirements.txt.
- Where is it located? project or git

>Proceed to describe how to install 
clone project

- setup one's local environment 
- get started with the project.


## RunServer-Commands
How to run server  use below commands
- python manage.py runserver 
> below command you can use custom port 
> Feature it will change
- python manage.py runserver 9000



## Host
Moving to production 

- change the host name ,in settings.py file 
- ALLOWED_HOSTS = [] => add port number here ex: ALLOWED_HOSTS=[127.0.2.47.200]
- Db details chnage details , add server db details
> Uploading your code to PythonAnywhere¶



