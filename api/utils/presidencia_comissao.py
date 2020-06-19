import json
import requests

from api.utils.csv_servers import post_req

URL_PRESIDENCIA_COMISSAO = "https://perfil.parlametria.org/api/busca-parlamentar"


def get_comissao_parlamentar():
    try:
        r = requests.get(url=URL_PRESIDENCIA_COMISSAO)
        data = json.loads(r.text)
        obj_arr = []
        for obj in data:
            for a in obj['parlamentarComissoes']:
                    if( a['cargo'] == "Presidente"):
                        obj_arr.append({
                            'idComissaoPresidencia': a['idComissaoVoz']
                        })
        return obj_arr 
        
    except Exception as e: 
        print(e)
        return []

