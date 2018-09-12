FROM agoradigital/python3.7-pandas-psycopg2-alpine

RUN mkdir /agora-digital-backend
WORKDIR /agora-digital-backend
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY requirements_prod.txt .
RUN pip install -r requirements_prod.txt

COPY . /agora-digital-backend/

CMD ./manage.py collectstatic --noinput && uwsgi --ini /agora-digital-backend/deploy/uwsgi.ini
