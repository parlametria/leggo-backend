def queryAutoriasAgregadas(data_inicio, interesse, tema, destaque):
  q_tema = ""
  q_destaque = ""

  if tema:
    destaque = None

    temaArg = tema.center(len(tema) + 4, '%') if tema else '%%'
    q_tema = (
    f" AND interesse.tema_slug LIKE '{temaArg}'"
  )
  
  if destaque == "'true'":
    q_destaque = (
      f" AND interesse.id_leggo IN (SELECT DISTINCT(id_leggo) \
        FROM api_destaques \
        WHERE (casa_req_urgencia_aprovado = 'true' \
        OR criterio_req_urgencia_apresentado = 'true' \
        OR criterio_aprovada_em_uma_casa = 'true')"
    )

  q = (
    f"SELECT \
    1 as id, \
    autoria.id_autor_parlametria AS id_autor_parlamentar, \
    autoria.tipo_acao AS tipo_acao, \
    COUNT(autoria.tipo_acao) AS num_documentos, \
    SUM(autoria.peso_autor_documento) AS peso_total, \
    ROW_NUMBER() OVER ( \
    PARTITION BY tipo_acao \
    ORDER BY COUNT(tipo_acao) DESC) \
    AS ranking_documentos \
    FROM ( \
      SELECT \
        DISTINCT(id_documento), \
        id_autor_parlametria, \
        tipo_acao, \
        peso_autor_documento \
      FROM api_autoria \
      WHERE data >= '{data_inicio}' AND id_leggo IN ( \
        SELECT interesse.id_leggo \
        FROM api_interesse as interesse \
        WHERE interesse.interesse = '{interesse}' \
        {q_tema} {q_destaque}) \
      GROUP BY id_autor_parlametria, id_documento, tipo_acao, peso_autor_documento \
    ) AS autoria  \
    GROUP BY id_autor_parlametria, tipo_acao \
    ORDER BY ranking_documentos ASC, tipo_acao ASC;" \
  )

  return q

def queryAutoriasAgregadasByAutor(data_inicio, interesse, tema, destaque, id_autor_parlametria, tipo_acao = 'Proposição'):
  query_lista_agregada = queryAutoriasAgregadas(data_inicio, interesse, tema, destaque)
  # q = (
  #   f"SELECT \
  #     1 as id, \
  #     autoria.id_autor_parlametria,
  #     autoria.num_documentos, \
  #     autoria.
      
    
    
  #   ")


  return True