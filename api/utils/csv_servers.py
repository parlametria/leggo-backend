import requests
import json
import os
from lxml import html

def post_req(req_url,data_dict):
    resp = requests.post(url = req_url, data = data_dict)
    return resp.text

def get_req(req_url, req_headers, req_params):
    resp = requests.get(url = req_url, headers = req_headers, params = req_params)
    return resp

def get_binary(req_url, req_headers, req_params, file_path):
    file_resp = requests.get(url = req_url, headers = req_headers, params = req_params, allow_redirects = True)
    open(file_path, 'wb').write(file_resp.content)
   
def get_token(base_url, leggo_user, leggo_pwd):
    token_creds = {
        "user": leggo_user,
        "pwd": leggo_pwd
    }

    token_resp = json.loads(post_req(base_url + "/login", token_creds))
    
    return token_resp["token"] 

def get_csvs_from_page(page):
    webpage = html.fromstring(page.content)
    files_urls = webpage.xpath('//a/@href')

    files = [u.split('/')[-1] for u in files_urls if '.csv' in u]
    
    return files

def get_leggo_files(base_url, token, output_folderpath):
    token_header = { "x-access-token": token }
    req_page = get_req(base_url + "/csvs/", token_header, None)

    leggo_base_files = get_csvs_from_page(req_page)

    for leggo_file in leggo_base_files:
        get_binary(base_url + "/csvs/" + leggo_file, token_header, None, output_folderpath + os.sep + leggo_file)

    pop_req_page = get_req(base_url + "/csvs/pops/", token_header, None)
    pop_files = get_csvs_from_page(pop_req_page)

    for pop_file in pop_files:
        get_binary(base_url + "/csvs/pops/" + pop_file, token_header, None, output_folderpath + os.sep + "pops" + os.sep + pop_file)


