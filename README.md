# CIS421StoreApp
## Set up
You must download and install python 3.8 to use this application, to do so go to the link below. \
https://www.python.org/downloads/release/python-382/ \
\
You must also install the LTS version of Node: \
https://nodejs.org/en/
<br>
## Installation
Navigate into the project \
`cd CIS421StoreApp/` \

Optional: its normally best practice to enter the virtual environment and develop from there \
`virtualenv venv && venv/Scripts/activate` 

Install the requirements \
`pip install -r requirements.txt` 

Install the frontend requirements \
`npm install` 

Migrate the database \
`python manage.py migrate`


## Run
`python manage.py runserver`
