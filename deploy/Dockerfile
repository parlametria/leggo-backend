FROM agoradigital/python3.7-pandas-psycopg2-alpine

# needed to install Python packages from Github
RUN apk add git

RUN mkdir /agora-digital-backend
WORKDIR /agora-digital-backend
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY requirements_prod.txt .
RUN pip install -r requirements_prod.txt

COPY . /agora-digital-backend/

CMD deploy/run.sh
