[![pipeline status](https://gitlab.com/analytics-ufcg/agora-digital-backend/badges/master/pipeline.svg)](https://gitlab.com/analytics-ufcg/agora-digital-backend/commits/master)
[![coverage report](https://gitlab.com/analytics-ufcg/agora-digital-backend/badges/master/coverage.svg)](https://gitlab.com/analytics-ufcg/agora-digital-backend/commits/master)

# Leggo backend

API para consulta de propostas de leis no senado e na câmara

## Setup

O código atual assume que este repositório está em uma pasta lado a lado com o repositório R. Isso é importante para que este código consiga acessar os CSVs gerados pelo R.

## Make	
Usando o make ele já ajuda a rodar os comandos do docker-compose de maneira simples:	

 Comando | Descrição	
------- | -----------	
**make run** | Build e create dos containers.	
**make start** |Começa containers já existentes.	
**make import** | Importa dados da pasta `data/` e escreve no banco de dados.	
**make update** | Realiza as migrações e importa os dados	
**make update-agorapi** | Realiza as migrações do banco.	
**make update-data-remote** | Atualiza o banco de acordo com os dados do servidor remoto.
**make help** | Para visualizar os demais comandos.

### Docker
Rodando com docker, o serviço estará disponível em http://0.0.0.0:8000/

#### Docker-compose
Para rodar com docker-compose, é preciso clonar o repositório:
```
git clone https://github.com/analytics-ufcg/leggo-backend/
```

Após isso basta:
```
docker-compose up 
```

E depois para carregar os dados:
```
docker exec -it "agorapi" sh -c './manage.py flush --no-input; ./manage.py import_data'
```

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

Gera migrações, migra, limpa dados e importa de novo ao mesmo tempo:
```
./manage.py update_db
```

Testes com cobertura de código:
```
./manage.py test_all
```
No Docker
```
docker exec -it agorapi sh -c './manage.py test_all'
```

### Gerar diagrama do BD

É possivel gerar um diagrama que mostre as classes/tabelas do banco, atributos/colunas de dados e as relações entre elas.

Primeiro é necessário rodar isso dentro do container do código, para instalar as dependências:

```
pip install pydot django_extensions
apk add ttf-dejavu
apk add graphviz
```

Depois o diagrama pode ser gerado dessa forma:

```
docker exec -it "agorapi" sh -c './manage.py graph_models --pydot -g -o diagram.pdf api'
```

Mais informações na [doc](https://django-extensions.readthedocs.io/en/latest/graph_models.html) e aqui um [exemplo de diagrama](https://medium.com/@yathomasi1/1-using-django-extensions-to-visualize-the-database-diagram-in-django-application-c5fa7e710e16) gerado.

