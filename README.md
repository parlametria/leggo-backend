# agora-digital-backend

## Instalar e rodar

O código atual assume que este repositório está em uma pasta lado a lado com o repositório R. Isso é importante para que este código consiga acessar os CSVs gerados pelo R.

Clone este repositório, entre na pasta e rode:

    virtualenv env
    . env/bin/activate
    pip install -r requirements.txt
    cd agorapi
    ./manage.py runserver

Abrir no navegador [http://127.0.0.1:8000/proposicoes/](http://127.0.0.1:8000/proposicoes/).
