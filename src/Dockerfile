# pull official base image
FROM python:3.11

# set work directory
RUN mkdir /code
WORKDIR /code

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

#update apt
RUN apt-get update

#install locale
RUN apt-get install -y locales locales-all
ENV LC_ALL es_ES.UTF-8

# install dependencies
RUN pip install --upgrade pip
COPY requirements.txt /code/
RUN pip install -r requirements.txt

# copy project
COPY .. /code/
