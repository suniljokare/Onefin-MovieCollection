# Onefin-MovieCollection



# Movie Collection App

Movie Collection App is a Django-based web application that allows users to manage their movie collections. Users can register, log in, view a list of movies, create collections, add movies to their collections, and manage multiple collections.

## Features

- User registration and authentication.
- Movie list with details.
- Create, edit, and delete collections.
- Add and remove movies from collections.
- User-friendly API for interacting with the application.

## Installation

### Prerequisites

- Python 3.7+
- PostgreSQL database server
- [pip](https://pip.pypa.io/en/stable/) for Python package management

### Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/suniljokare/Onefin-MovieCollection.git
   cd movie-collection-app

### steps:
   
1) Install project dependencies:
      
    pip install -r requirements.txt

2) Create a PostgreSQL database for the application and configure your database settings in settings.py

3) Apply database migrations:
    
    python manage.py makemigrations
    python manage.py migrate

4) python manage.py runserver

5) Access the application in your web browser at http://localhost:8000/.


### Usage
    Register a new user account or log in with an existing account.
    Browse the list of movies and click on a movie to view its details.
    Create collections to organize your movies.
    Add or remove movies from your collections.
    Manage multiple collections.


## API Collection

You can find the Thunder Client API collection for this project [here](./path/to//home/Desktop/thunder-collection_MOVIE COLLECTIONS.json).