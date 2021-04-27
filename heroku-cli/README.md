## Heroku-cli Parlametria

<br>

Este é o módulo responsável por capturar o dump do banco de dados remoto hospedado no heroku para a aplicação do backend do Parlametria.

Para que este módulo funcione é necessário que o serviço heroku-cli definido no `docker-compose.override.yml` na raiz desse repositório tenha sido iniciado. Recomenda-se iniciar este serviço usando o repositório orquestrador [leggo-geral](https://github.com/parlametria/leggo-geral).

#### **Configuração de volumes**
Se ao levantar os serviços usando o leggo-geral o seguinte erro for encontrado:
```sh
ERROR: Volume backup_data declared as external, but could not be found. Please create the volume manually using `docker volume create --name=backup_data` and try again.
```
Então execute em um terminal local: `docker volume create --name=backup_data`

## Configuração das variáveis de ambiente

1. Crie um arquivo .env no mesmo diretório deste README.
2. Copia o conteúdo do .env.sample para este novo arquivo .env
3. Preencha HEROKU_APP_NAME com o nome do app no heroku ao qual o banco de dados está associado. Entre em contato em caso de dúvidas.
4. Preencha HEROKU_API_KEY com a sua chave da API para acesso ao heroku via linha de comando. Mais informações sobre como obter essa chave abaixo.

### Como obter HEROKU_API_KEY

Existem duas formas de obter sua HEROKU_API_KEY:

**Via Dashboard do Heroku**
1. Visite e faça o login em https://dashboard.heroku.com
2. Acessa sua conta em https://dashboard.heroku.com/account
3. Na seção API KEY obtenha sua chave de acesso a API. Essa é a chave que deve ser preenchida na variável HEROKU_API_KEY do .env.

**Via heroku-cli**
1. Ceritifique-se que os serviços do leggo-backend foram iniciados. Seja via docker-compose na raiz desse repositório ou usando o leggo-geral (ex: através do comando python3.x compose/run painel up).
2. Da raiz desse repositório execute:
```
make get-heroku-api-key
```
3. Preencha com seu login e senha no heroku. É importante que você tenha acesso/permissão ao app no Heroku. Caso você não tenha entre em contato.
4. Copie o código mostrado e preencha a a variável HEROKU_API_KEY no .env com ele.
5. Pare e reinicie os serviços do leggo-backend, conforme feito no passo 1, para que a mudança no .env seja aplicada.

Após configurar a variável HEROKU_API_KEY não será preciso repetir esse processo novamente. A menos que a KEY tenha expirado (após 1 ano da sua criação). Nunca faça commit da sua chave particular no repositório!

## Download do dump do banco de dados remoto no heroku

Certifique-se que as variáveis de ambiente foram configuradas corretamente seguindo as seções anteriores. Para isto execute o comando (na raiz desse repositório):

```
make download_remote_db_heroku
```

## Sincronizar BD local com base no dump do BD no heroku

Certifique-se que as variáveis de ambiente foram configuradas corretamente seguindo as seções anteriores. Para isto execute o comando (na raiz desse repositório):

Certifique-se que 

```
make sync-db-with-heroku
```
