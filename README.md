# Cookella - Social Recipe WebApp
Cookella is a social recipe website built for cooking enthusiast and foodies
A community base social recipe, that provides cooking enthusiast a platform to post and view recipes online, Blog, and keeping track of their activities.

project link at: http://cookella.herokuapp.com/

## Tables of Content
[Key Features](#key-features)
[Technologies](#Technologies)
[Setup](#Setup)
[Dependencies](#Dependencies)
[How To Contribute](#How-To-Contribute)

## Key Features
* upload recipes 
* User Authentication [Login, SignUp, Logout, Profile, Password Handling]
* Blogging 
* Search for Recipe or blog
* Delete or Update Recipe / Blog Post
* Like, Comment and Share Recipes / Blog Post

## Technologies
Project is created on
* Django
* Bootstrap
* Javascript
* jQuery on Ajax \
Allauth is used to handle authentications

## Setup
* clone the project
* create and start a virvual env
* Install project dependencies 
`
pip install -r requirements.txt
`
* you might as well setup your secret key, here we use windows env
* create your database and add to settings.py
`run 'python manage.py migrate'`
* create admin account \
`run 'python manage.py makemigrations`
`run 'python manage.py migrate'`
* to start dev server 
`run 'python manage.py runserver'`

# Dependencies
* postgresql
* allauth
* crispy form
* boto3
etc...

# How To Contribute
fork the project and follow the setup process



