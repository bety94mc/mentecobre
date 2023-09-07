FROM python:3
RUN apt-get update
RUN apt-get install -y locales locales-all
ENV LC_ALL es_ES.UTF-8
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/