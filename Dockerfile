# Dockefile used for development

FROM agoradigital/python3.7-pandas-psycopg2-alpine

RUN mkdir /agora-digital-backend
WORKDIR /agora-digital-backend
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY requirements_dev.txt .
RUN pip install -r requirements_dev.txt

CMD ./manage.py migrate && ./manage.py runserver 0.0.0.0:8000

EXPOSE 8000
