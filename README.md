# [Python Sirius - Social Network]

This is a full-stack web application (a social network) created with the python framework [Flask](https://flask.palletsprojects.com/en/3.0.x/).

## Table of Contents

- [Introduction](#introduction)
- [Screenshot](#screenshot)
- [Live Demo](#live-demo)
- [Features](#features)
- [Technologies](#technologies)
- [Getting Started](#getting-started)
- [Author](#author)

## Introduction

This is a social network in which users can create post and submit images with them.

## Screenshot

![screenshot](https://github.com/Robertron624/python-sirius/assets/72587880/f9fe7b66-c121-427b-b44e-b0d4b230876f)

## Live Demo

- In Progress

## Features

- New users can register a new account
- Users can login into their accounts
- Users can see a feed of submitted post by other users
- Users can click a post and it will redirect to the individual post page
- In the individual post page users can read and post comments about the page
- Users can edit and delete the comments that he/she has made
- Users can create a new post with an image and a text to go by
- Users can delete and edit the post they have submitted
- Users can edit the personal info that they submitted in the Sign up process
- Users can change their passwords
- Users can log out when clicking a link in the header's navigation bar
- Users can ask for help to the admins by writing a message to them

## Technologies

- Flask: web framework
- SQLite: local database
- JavaScript: for interactivity, without relying just in Flask
- Jinja: template engine, HTML
- CSS: for styling
- flask_wtf: for handling forms
- werkzeug: for security and handling passwords
- markupsafe: for preventing Cross site attacks

## Getting Started

- Install python if you don't have it
- Clone this repository
- Go to the proyect's root folder
- Start a python virtual environment
- Install the project's dependencies by running the following command

```
  pip install -r requirements.txt
```

- Run the proyect by running the `àpp.py` file:

On windows
  ```
    python app.py
  ```

On MacOS
  ```
    python3 app.py
  ```

Or, if you have the Python VS Code extension, just open the `app.py` file and click the play button to start running the app

- It will start a server on `http://127.1.0:8080`

## Author

- [LinkedIn](www.linkedin.com/in/roberto-ramirez-aguilar)
- [Github](https://github.com/Robertron624)
- [Webpage](https://robert-ramirez.co/)
