def queryPressaoOitoDias(interesse):

    p = f"SELECT DISTINCT ON (p.id_leggo) \
            1 AS id, \
            aux_top.id_leggo, \
            popularity, \
            aux_top.pressao_oito_dias AS pressao_oito_dias \
            FROM  api_pressao p \
            INNER JOIN \
            (SELECT DISTINCT(id_leggo) \
            FROM api_interesse \
            WHERE interesse = '{interesse}') AS interesse_aux \
            ON p.id_leggo = interesse_aux.id_leggo \
            LEFT JOIN \
            (WITH summary AS ( \
                SELECT p.id_leggo,  \
                    p.popularity AS pressao_oito_dias,  \
                    ROW_NUMBER() OVER(PARTITION BY p.id_leggo  \
                                            ORDER BY p.date DESC) AS rk \
                FROM api_pressao p \
                WHERE p.interesse = '{interesse}') \
            SELECT s.* \
            FROM summary s \
            WHERE s.rk = 2) AS aux_top  ON \
            aux_top.id_leggo = p.id_leggo \
            ORDER  BY p.id_leggo, p.date DESC;"

    return p


def queryTemperaturaQuinzeDias(interesse):

    q = f"SELECT DISTINCT ON (t.id_leggo) \
            1 AS id, \
            aux_top.id_leggo, \
            temperatura_recente, \
            temp_quinze_dias \
            FROM  api_temperaturahistorico t \
            INNER JOIN \
            (SELECT DISTINCT(id_leggo) \
            FROM api_interesse \
            WHERE interesse = '{interesse}') AS interesse_aux \
            ON t.id_leggo = interesse_aux.id_leggo \
            LEFT JOIN \
            (WITH summary AS ( \
                SELECT t.id_leggo,  \
                    t.temperatura_recente AS temp_quinze_dias,  \
                    ROW_NUMBER() OVER(PARTITION BY t.proposicao_id  \
                                            ORDER BY t.periodo DESC) AS rk \
                FROM api_temperaturahistorico t) \
            SELECT s.* \
            FROM summary s \
            WHERE s.rk = 3) AS aux_top  ON \
            aux_top.id_leggo = t.id_leggo \
            ORDER  BY t.id_leggo, t.periodo DESC;"

    return q
