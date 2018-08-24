FROM python:3.7

COPY . /app
WORKDIR /app

ENV PYTHONUNBUFFERED 1
ENV FLASK_APP=caboabanana
ENV FLASK_ENV=development

RUN mkdir /agora-digital-backend
WORKDIR /agora-digital-backend
ADD . /agora-digital-backend/

RUN pip install -r requirements.txt

EXPOSE 8000
