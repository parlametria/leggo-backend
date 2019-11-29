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
