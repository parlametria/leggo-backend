import json
import requests


URL_PESO_POLITICO = "https://perfil.parlametria.org/api/perfil/"


def get_peso_politico_lista(lista_ids):
    try:
        r = requests.get(url=URL_PESO_POLITICO + "lista")
        data = json.loads(r.text)

        lista_ids_str = list(map(str, lista_ids))

        filtered_parlamentares = [
            obj for obj in data if obj["idParlamentarVoz"] in lista_ids_str
        ]

        for obj in filtered_parlamentares:
            obj["id_autor_parlametria"] = int(obj["idParlamentarVoz"])
            obj["peso_politico"] = obj["pesoPolitico"]

        return filtered_parlamentares

    except Exception:
        return []


def get_peso_politico_parlamentar(id):
    try:
        r = requests.get(url=URL_PESO_POLITICO + str(id))
        data = json.loads(r.text)

        obj_arr = []

        data["id_autor_parlametria"] = int(data["idParlamentarVoz"])
        data["peso_politico"] = data["pesoPolitico"]

        obj_arr.append(data)

        return obj_arr

    except Exception:
        return []
