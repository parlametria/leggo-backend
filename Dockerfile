FROM python:3.7

ENV PYTHONUNBUFFERED 1

RUN mkdir /agora-digital-backend
WORKDIR /agora-digital-backend
ADD . /agora-digital-backend/

RUN pip install -r requirements.txt

CMD ./agorapi/manage.py runserver

EXPOSE 8000
