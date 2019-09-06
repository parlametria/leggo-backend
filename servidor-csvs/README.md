# Servidor csvs

#### Criando arquivos .env
Crie o arqivo .env e o .env.example na pasta do servidor com as seguintes variáveis:
```
SECRET= 
USUARIO=
SENHA=
```
Exemplo:
```
SECRET='Rapadura e doce mas nao e mole';
USUARIO=jair
SENHA=123
```

#### Build do docker
Para rodar o servidor usando docker primeiro você deve dar o build na imagem realizando o seguinte comando:
```
docker build -t <your image> .
```

#### Rodar o docker
Para rodar utilizar o comando:
```
docker run -p 8080:8080 <your image>
```

Então o seu servidor estará rodando na porta 8080, para ter acesso aos csvs entre na url:
http://localhost:8080/csvs/
