# Ágora Digital backend
[![Build Status](https://travis-ci.com/analytics-ufcg/agora-digital-backend.svg?branch=master)](https://travis-ci.com/analytics-ufcg/agora-digital-backend)

API para consulta de propostas de leis no senado e na câmara

## Setup

O código atual assume que este repositório está em uma pasta lado a lado com o repositório R. Isso é importante para que este código consiga acessar os CSVs gerados pelo R.

### Docker
Rodando com docker, o serviço estará disponível em http://0.0.0.0:8000/

#### Docker-compose
Para rodar com docker-compose, é preciso clonar o repositório:
```
git clone https://github.com/analytics-ufcg/agora-digital-backend/
```

Após isso basta:
```
docker-compose up 
```

E depois para carregar os dados:
```
docker exec -it "agorapi" sh -c './manage.py flush --no-input; ./manage.py import_data'
```

#### Dockhub

**Essa seção precisa ser atualizada ou removida, uma vez que não dá para rodar mais sem o BD que o docker-compose fornece.**

Com dockhub você não precisar clonar o repositório, basta apenas baixar a imagem docker:

```
docker pull agoradigital/agorapi
```

E depois rodar um container expondo a porta 8000:

```
docker run -p 8000:8000 agoradigital/agorapi
```

Se você está desenvolvendo, é preferível que use o *docker-compose* pois garante que você está pegando a versão de desenvolvimento mais atualizada da api.

## Uso

Alguns comando básicos para manipulação de seus containers dockers.

### Reconstruir a imagem do zero com docker-compose up
Caso você esteja querendo reegerar a imagem, forçando-a a pegar as atualizações novas, use:

```
docker-compose up --build
```

### Visualizar containers rodando

```
docker ps
```

### Matar um container
Rode docker ps, copie o *container-id* e use:

```
docker kill <id>
```
 
#### Sem docker
```
virtualenv env
. env/bin/activate
pip install -r requirements.txt
./manage.py runserver
```

### Docker Produção

> Atenção:
> Estamos usando um `.dockerignore` bastante rígido (que ignora tudo menos alguns arquivos). Isso evita copiar para a imagem docker de produção arquivos desnecessários ou secretos.
> Porém, é preciso lembrar disso e possivelmente adicionar uma nova regra nesse arquivo caso precise adicionar novos arquivos na imagem.

Criar um arquivo `deploy/env` com:
```
SECRET_KEY=umasenhasecreta
DEBUG=False
```
E rodar:
```
docker-compose -f docker-compose.yml -f deploy/prod.yml up
```
(substituir `up` por `build` caso seja necessário gerar a imagem)

Acessar em http://localhost:9002/

## Comandos úteis

Gerar migrações e migrar base:
```
./manage.py makemigrations && ./manage.py migrate
```

Limpar base de dados:
```
./manage.py flush --no-input
```

Importar dados do CSV para o BD:
```
./manage.py import_data
```

Testes com cobertura de código:
```
coverage run --source=agorapi,api --omit='*/migrations/*' ./manage.py test
coverage report
```
