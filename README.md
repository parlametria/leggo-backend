# Ágora Digital backend
API para consulta de propostas de leis no senado e na câmara

## Uso

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

#### Dockhub
Com dockhub você não precisar clonar o repositório, basta apenas baixar a imagem docker:

```
docker pull agoradigital/agorapi
```

E depois rodar um container expondo a porta 8000:

```
docker run -p 8000:8000 agoradigital/agorapi
```

Se você está desenvolvendo, é preferível que use o *docker-compose* pois garante que você está pegando a versão de desenvolvimento mais atualizada da api.

#### Sem docker
```
virtualenv env
. env/bin/activate
pip install -r requirements.txt
./manage.py runserver
```

## Endpoints

Veja em http://0.0.0.0:8000/

## Comandos úteis

Limpar base de dados:
```
./manage.py flush --no-input
```

Importar dados do CSV para o BD:
```
./manage.py import_data
```
