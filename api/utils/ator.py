def get_nome_partido_uf(nome, partido, uf):

    if(uf == 'nan'):
        uf = '-'

    if(partido == 'nan'):
        partido = '-'
    return (nome + ' (' + partido + '/' + uf + ')')
