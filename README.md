# MotorQuotationLab
A basic Motor Insurance Quotation App with Django

Here is the result of the first sprint.
I tried to apply best practices with Django and Python

Some of the features asked are not exactly what i wanted them to be (see you at next sprint ?)

## Installation
- Download or clone this repository
- open a shell with python installed
- go to the project's root (where this REAME.md file is)
- set your virtual env if needed
- run "pip insall -r requirement.txt" or equivallent on your system
- if the provided database is working, no need to do thoses steps :
  - create a superuser : python manage.py createsuperuser
  - initialise the models : python manage.py makemigrations
  - apply the models to the database : python manage.py migrate
- start the local server : python manage.py runserver

## Accounts
I've created several users : 
 - admin/admin : general admin account. It can add or modify coverages description and price in http://127.0.0.0:8080/admin
 - agent/agent : user you are supposed to use for the batch mode on http://127.0.0.1:8000/quotations-admin/
 - user1/azer1234 : first user
 - user2/azer1234 : second user

## Usage
 - go to http://127.0.0.1:8000/, login or create a new account
 - Have fun !

## Features and bonuses
 - visit [Motor Quotation App project board](https://github.com/GuillaumeGSO/MotorQuotationLab/projects/1) to view my progress
 - visit [Issues and tasks project board](https://github.com/GuillaumeGSO/MotorQuotationLab/projects/2) to add tasks, issues, new features requests
