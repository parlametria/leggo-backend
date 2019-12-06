def get_nome_partido_uf(casa, bancada, nome, partido, uf):
    marcador_bancada = ''

    if (uf == 'nan'):
        uf = '-'

    if (partido == 'nan'):
        partido = '-'

    if (bancada == 'oposição'):
        marcador_bancada = '* '

    descricao_parlamentar = marcador_bancada + \
        nome + ' (' + partido + '/' + uf + ')'

    return(descricao_parlamentar)

def get_sigla_formatada(casa, sigla_local):
    '''Formata a sigla local para ter a casa'''
    if casa == 'camara':
        casa = 'Câmara'
    else:
        casa = 'Senado'

    if sigla_local == 'PLEN':
        sigla_local = 'Plenário'

    return sigla_local + ' - ' + casa
