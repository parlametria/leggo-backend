import json
import requests

from api.utils.csv_servers import post_req


URL_PRESIDENCIA_COMISSAO = "https://perfil.parlametria.org/api/busca-parlamentar"

def get_comissao_parlamentar(lista_ids):
    try:
        r = requests.get(url=URL_PRESIDENCIA_COMISSAO)
        data = json.loads(r.text)
             
        teste = []

        for obj in data:
            for a in obj['parlamentarComissoes']:
                    if( a['cargo'] == "Presidente"):
                        quant += 1
                        teste.append({
                            'idComissaoPresidencia': a['idComissaoVoz']
                        })
        return teste 
    except Exception as e: 
        print(e)
        return []

