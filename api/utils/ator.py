def get_nome_partido_uf(bancada, nome, partido, uf):

    if(uf == 'nan'):
        uf = '-'

    if(partido == 'nan'):
        partido = '-'
    
    if (bancada == 'governo'):
        return (nome + ' (' + partido + '/' + uf + ')')
    else:
        return ('* ' + nome + ' (' + partido + '/' + uf + ')')
