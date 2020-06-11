import json


from api.utils.csv_servers import post_req


URL_PESO_POLITICO = "https://perfil.parlametria.org/api/perfil/"


def get_peso_politico_lista(lista_ids):
    try:
      payload = {"parlamentares": lista_ids}

      r = post_req(URL_PESO_POLITICO + "lista", payload)
      processed_data = [
         dict(id_autor=e["idParlamentarVoz"], peso_politico=e["pesoPolitico"])
         for e in json.loads(r)
      ]
      return processed_data

    except Exception as e:
      return []
