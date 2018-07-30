[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![Build Status](https://travis-ci.org/muhumuzab/MyDiary-API.svg?branch=develop)](https://travis-ci.org/muhumuzab/MyDiary-API) [![Coverage Status](https://coveralls.io/repos/github/muhumuzab/MyDiary-API/badge.svg?branch=develop)](https://coveralls.io/github/muhumuzab/MyDiary-API?branch=develop) <a href="https://codeclimate.com/github/codeclimate/codeclimate/maintainability"><img src="https://api.codeclimate.com/v1/badges/a99a88d28ad37a79dbf6/maintainability" /></a>

# Introduction

* **My Diary** is an online journal where users can pen down their thoughts and feelings.  

# Features

* Users can create an account and log in. 
* Users can view all entries to their diary. 
* Users can view the contents of a diary entry. 
* Users can add or modify an entry. 
  
# API Endpoints

|  Endpoints | Description  | Public Access |
| --- | :--- | ---: |
| POST  `/api/v1/entries/signup`  | Sign up.| TRUE
| POST  `/api/v1/entries/login`  | Log in.| TRUE
| POST  `/api/v1/entries/`  | Add a diary entry.| FALSE
| GET  `/api/v1/entries/`   | gets all diary entries.| FALSE
| GET  `/api/v1/entries/<entry_id>`  | Get diary entry by id. | FALSE
| PUT  `/api/v1/entries/<entry_id>`  | Update diary entry by id. | FALSE




# Installation
To run this project, you'll need a working installation of python 3 and pip3. You also may need virtualenv.

## To install the app:
1. Clone this repository - git clone https://github.com/muhumuzab/MyDiary-API-v2/
2. Make a virtual environment for the project - virtualenv /path/to/my-project-venv
3. Activate the virtual environment - source /path/to/my-project-venv/bin/activate
4. Install requirements - pip3 install requirements.txt
6. Navigate to the project root and run the app.py file - type 'python run.py'



# Testing

