FROM python:3.7-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk --no-cache add musl-dev linux-headers g++ postgresql-dev python3-dev

RUN mkdir /agora-digital-backend
WORKDIR /agora-digital-backend
COPY requirements.txt ./
RUN pip install -r requirements.txt

ADD . /agora-digital-backend/


CMD ./manage.py runserver 0.0.0.0:8000

EXPOSE 8000