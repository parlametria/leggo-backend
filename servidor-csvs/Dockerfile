FROM node:10

WORKDIR /

COPY package* ./

RUN npm install

COPY . .

EXPOSE 8080

CMD npm start