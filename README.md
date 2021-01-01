Juntagrico for Gartenberg
===========

This repository sets up a project to be used with juntagrico.science as hosting.

# Setting up locally to test setup

Install Python 3, and add it to your path (tested with python 3.9.1)

## Linux

### Set your environment variables


### Installing requirements

In order to compile python-psycopg2, you need to install the postgresql libraries. Otherwise the following error will appear: Error: pg_config executable not found Under Archlinux the following command can be used: `sudo pacman -S postgresql-libs-13.1-3`

    sudo easy_install pip
    sudo pip install virtualenv
    virtualenv venv
    source ./venv/bin/activate
    pip install --upgrade -r requirements.txt

### Setup DB

    chmod +x manage.py
    ./manage.py migrate
    
### Setup Admin User

    ./manage.py createsuperuser
    ./manage.py create_member_for_superusers
    
### Create Tesdata (not required)

Simple

    ./manage.py generate_testdata

More complex

    ./manage.py generate_testdata_advanced
    
### Run the server

    ./manage.py runserver

## Windows

### Set your environment variables

This should do it for your local setup:


### Installing requirements

    pip install virtualenv
    virtualenv --distribute venv
    venv\Scripts\activate.bat
    pip install --upgrade -r requirements.txt

### Setup DB

    python -m manage migrate
    
### Setup Admin User

    python -m manage createsuperuser
    python -m manage create_member_for_superusers
    
### Create Tesdata (not required)

Simple

    python -m manage generate_testdata

More complex

    python -m manage generate_testdata_advanced
    
### Run the server

    python -m manage runserver
    
# Heroku

you have to login to a heroku bash and setup the db and create the admin user as desbribed in the UNIX section
