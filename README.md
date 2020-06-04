[![pipeline status](https://gitlab.com/analytics-ufcg/agora-digital-backend/badges/master/pipeline.svg)](https://gitlab.com/analytics-ufcg/agora-digital-backend/commits/master)
[![coverage report](https://gitlab.com/analytics-ufcg/agora-digital-backend/badges/master/coverage.svg)](https://gitlab.com/analytics-ufcg/agora-digital-backend/commits/master)

# Leggo backend

Este é o repositório com a API do [Leg.go](https://leggo.parlametria.org). 

Leg.go é uma plataforma de inteligência para o acompanhamento das atividades no Congresso Nacional. Coletamos dados da Câmara e do Senado para encontrar quais proposições estão quentes, o que está tramitando com mais energia, como o conteúdo dos projetos é alterado e quem são os atores importantes nesse processo. Acesse o [Leg.go](https://leggo.parlametria.org).

## Setup

Recomendamos que você instale o [docker](https://docs.docker.com/install/linux/docker-ce/ubuntu/#install-docker-ce) e o [docker-compose](https://docs.docker.com/compose/install/) para configuração do ambiente de desenvolvimento.

Este repositório é responsável apenas pelo código do backend do Leg.go. Recomendamos que caso você esteja interessado em configurar o ambiente de desenvolvimento por completo, acesse nosso [orquestrador de repositórios](https://github.com/parlametria/leggo-geral/tree/master/compose): o leggo-geral. Lá você irá encontrar instruções para configurar todo o ambiente incluindo: **banco de dados, backend e frontend**.

Pelo leggo-geral você conseguirá executar todos os serviços incluindo este aqui: o leggo-backend.

Antes de ir lá pro leggo-geral, outra etapa de configuração importante é a criação do arquivo de variáveis de ambiente usado pelo leggo-backend. 

Para isto faça uma cópia do arquivo .ENV.sample e a reinomeie para .ENV. Entre em [contato](https://github.com/parlametria/leggo-backend/issues) com a equipe de desenvolvimento para obter as chaves de acesso ao servidor de dados processados e atualizados diariamente.

Com o arquivo .ENV criado e preenchido agora é possível seguir os passos do [leggo-geral](https://github.com/parlametria/leggo-geral/tree/master/compose) para levantar os serviços e configurar o ambiente de desenvolvimento.

A API estará disponível em localhost:8000.
O nome do container que está servindo a api é **agorapi**.

## Make	
O make deste repositório ajuda a executar alguns comandos docker comuns durante o processo de desenvolvimento.

 Comando | Descrição	
------- | -----------
**make update** | Realiza as migrações e importa os dados.
**make update-data-remote** | Atualiza o banco de acordo com os dados do servidor remoto. Muio útil para quando não se quer processar os dados localmente usando os repositórios de tratamento de dados. Os csvs são recuperados já processados e são importados para o banco de dados pelo leggo-backend.
**make shell** | Abre terminal psql para o banco de dados presente no container dbapi.
**make run** | Build e create dos containers. (não usa o leggo-geral)	
**make start** | Começa containers já existentes. (não usa o leggo-geral)		
**make import** | Importa dados da pasta `data/` e escreve no banco de dados.
**make update-agorapi** | Realiza as migrações do banco.	
**make help** | Para visualizar os demais comandos.

## Executando sem ajuda do leggo-geral

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

