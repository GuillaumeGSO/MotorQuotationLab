# MotorQuotationLab
A basic Motor Insurance Quotation App with Django

Here is the result of the second sprint.
I tried to apply best practices with Django and Python

Some of the features asked are not exactly what i wanted them to be (see you at next sprint ?)

## Installation
- Download or clone this repository
- open a shell with python installed
- go to the project's root (where this REAME.md file is)
- set your virtual env if needed
- run "pip install -r requirement.txt" or equivallent on your system
- the database is already initialized
- start the local server : python manage.py runserver

## Accounts
I've created several users : 
 - admin/admin : general admin account. It can add or modify coverages description and price in http://127.0.0.0:8080/admin
 
## Usage
 - go to http://127.0.0.1:8000/
 - Each new email entered create a new account with a common password

## Features and bonuses
 - visite http://127.0.0.1:8000/quotations-admin/ to review all the quotation like an agent
 - an admin action allow to send email in "batch mode"
 - a bonus admin action allow to recalculate the final quotation if coverage price evolved
 - visit [Motor Quotation App project board](https://github.com/GuillaumeGSO/MotorQuotationLab/projects/1) to view my progress
 - visit [Issues and tasks project board](https://github.com/GuillaumeGSO/MotorQuotationLab/projects/2) to add tasks, issues, new features requests
