Para rodar o servidor usando docker primeiro você deve dar o build na imagem realizando o seguinte comando:
docker build -t <your image> .
Depois para rodar utilizar o comando:
docker run -p 8080:8080 csv-server
Então o seu servidor estará rodando na porta 8080, para ter acesso aos csvs entre na url:
http://localhost:8080/csvs/