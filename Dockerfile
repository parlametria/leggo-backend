# Dockefile used for development

FROM agoradigital/python3.7-pandas-psycopg2-alpine

# needed to install Python packages from Github
RUN apk add git
RUN apk add --update --no-cache libc-dev gcc libxslt-dev libxml2-dev python-dev

RUN mkdir /agora-digital-backend
WORKDIR /agora-digital-backend
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY requirements_dev.txt .
RUN pip install -r requirements_dev.txt

CMD ./manage.py migrate && ./manage.py runserver 0.0.0.0:8000

EXPOSE 8000
