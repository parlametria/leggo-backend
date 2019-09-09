FROM node:10

WORKDIR /

COPY package* ./
COPY . .

RUN npm install

EXPOSE 8080

CMD npm start