import requests
import json
import os
from lxml import html
import subprocess


def post_req(req_url, data_dict):
    '''
    Faz uma requisição HTTP POST para uma url.

    Parameters
    ----------
    req_url : str
            A URL para onde a requisição será direcionada
    data_dict : dict
            Dicionário com dados a serem passados na requisição
    '''
    resp = requests.post(url=req_url, data=data_dict)
    return resp.text


def get_req(req_url, req_headers, req_params):
    '''
    Faz uma requisição HTTP GET para uma url.

    Parameters
    ----------
    req_url : str
            A URL para onde a requisição será direcionada
    req_headers : dict
            Dicionário com headers a serem passados na requisição
    data_dict : dict
            Dicionário com dados a serem passados na requisição
    '''
    resp = requests.get(url=req_url, headers=req_headers, params=req_params)
    return resp


def get_binary(req_url, req_headers, req_params, file_path):
    '''
    Faz uma requisição HTTP GET para obter um dado binário (arquivo) a partir de uma url.

    Parameters
    ----------
    req_url : str
            A URL para onde a requisição será direcionada
    req_headers : dict
            Dicionário com headers a serem passados na requisição
    req_params : dict
            Dicionário com parâmetros a serem passados na requisição
    file_path : str
            Caminho do arquivo onde será salvo o dado baixado
    '''
    file_resp = requests.get(url=req_url, headers=req_headers, params=req_params,
                             allow_redirects=True)
    open(file_path, 'wb').write(file_resp.content)
    subprocess.call(['chmod', '0666', file_path])


def get_token(base_url, leggo_user, leggo_pwd):
    '''
    Obtém o token do servidor de CSVs do Leggo.

    Parameters
    ----------
    base_url : str
            A URL base para onde a requisição será direcionada
    leggo_user : str
            Usuário do Servidor de CSVs do Leggo
    leggo_pwd : str
            Senha do Servidor de CSVs do Leggo
    '''
    token_creds = {
        "user": leggo_user,
        "pwd": leggo_pwd
    }

    token_resp = json.loads(post_req(base_url + "/login", token_creds))

    return token_resp["token"]


def get_csvs_from_page(page):
    '''
    Função auxiliar que lê o conteúdo de uma página html contendo links para csvs
    e retorna uma lista com os arquivos csvs que há na página.

    Parameters
    ----------
    page : requests.models.Response
           Objeto representando a página HTML contendo links para csvs
    '''
    webpage = html.fromstring(page.content)
    files_urls = webpage.xpath('//a/@href')

    files = [u.split('/')[-1] for u in files_urls if '.csv' in u]

    return files


def get_leggo_files(base_url, token, output_folderpath):
    '''
    Função que faz o download dos arquivos do Leggo (csvs) do servidor de CSVs do Leggo.

    Parameters
    ----------
    base_url : str
            A URL base do Servidor de CSVs do Leggo
    token : str
            O Token obtido para acessar o servidor
    output_folderpath: str
            O caminho da pasta onde serão salvos os CSVs.

    '''
    token_header = {"x-access-token": token}
    req_page = get_req(base_url + "/csvs/", token_header, None)

    leggo_base_files = get_csvs_from_page(req_page)

    for leggo_file in leggo_base_files:
        get_binary(base_url + "/csvs/" + leggo_file, token_header, None,
                   output_folderpath + os.sep + leggo_file)

    pop_req_page = get_req(base_url + "/csvs/pops/", token_header, None)
    pop_files = get_csvs_from_page(pop_req_page)

    for pop_file in pop_files:
        get_binary(base_url + "/csvs/pops/" + pop_file, token_header, None,
                   output_folderpath + os.sep + "pops" + os.sep + pop_file)
