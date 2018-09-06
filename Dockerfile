FROM python:3.7

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /agora-digital-backend
WORKDIR /agora-digital-backend
COPY requirements.txt ./
RUN pip install -r requirements.txt

ADD . /agora-digital-backend/


CMD ./manage.py runserver 0.0.0.0:8000

EXPOSE 8000
