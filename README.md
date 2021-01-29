# Nonogram #
Submission for CS50-2019 Final Project
https://en.wikipedia.org/wiki/Nonogram

![Game](https://i.imgur.com/Q6AwRJI.png)


The main focus of the project is the game, which i coded in js.
Its possible to change the size of the Grid, so a level system could also be implemented
When a Users plays a Game his Wins get tracked and all Users are displayed on the Leaderboard

### Setup Project in Editor ###
-- Setup Process may vary according --
1. Install venv 
`python3 -m pip install virtualenv`
2. Setup venv
`python3 -m virtualenv venv`
3. Activate venv
`/ProjectDir/venv/Scripts/activate.bat`
4. Install Required Packages
`pip install -r requirements.txt`

### Running the Website ##
1. Set Flask Application
`set FLASK_APP=application.py`
2. Run
`flask run`

## Features ##
* Login System
    * With a SQLite Database
* Randomly generated Game Grid
* Leaderboard & Profile Tracking

## Technologies ##
* Backend:
    * Flask
    * SQLite3
* Frontend:
    * JQuery
    * Sass
 
