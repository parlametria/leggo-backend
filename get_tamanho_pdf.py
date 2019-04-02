import requests
import pandas as pd
import sys

def tamanho_pdf(url):
	try:
		print('Processando a ', url)
		response = requests.get(url, stream=True)
		return len(response.content)
	except:
		return 0

def adc_pdf(tabela_emendas_path, write_path):
	df = pd.read_csv(tabela_emendas_path) 
	df['tamanho_pdf'] = df['inteiro_teor'].apply(tamanho_pdf)
	df.to_csv(write_path + "emendas.csv")

if __name__ == "__main__":
	if (len(sys.argv) != 3):
		print("Numero de parametros incorreto")
		print("Exemplo de uso: python get_tamanho_pdf.py data/emendas.csv data/")
	else:
		adc_pdf(sys.argv[1], sys.argv[2])

