# Mentecobre 1.0.0

## Introduction
This projects build a django web app designed to organize the Coppermind translation
to Spanish. It offers the administration panel from Django to deal with SQL database,
some public views offered to general public and some private views offered only to
Spanish translator team to help with the site translation.
The database have a list of all pages from es.coppermind.net and whether they are translated
or not. It also have a table with glossary terms.

## Build
The repository has the necessary files to build this project in Docker:
- Dockerfile
- requirments.txt 
- dev.yml

To do this, execute the following commands in order:

```
docker-compose -f dev.yml build
docker-compose -f dev.yml up
```

This will build the images in docker and run a container with a PostgresSQL database
and a Django web app.


For security purposes, no SECRET_KEY should be included in the code. So, a .env file is needed to be created 
and secret_key included there such as:
```
DJANGO_SECRET_KEY = 'askdjlk123hbasdbhjasd1@#aso123€¬'
```
The key is literally anything, it has no relevance to the development environment.

## APP

The app uses Django with PostgreSQL. It also uses html and css to build the template part.
