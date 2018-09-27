#!/usr/bin/env Rscript
library(magrittr)
library(dplyr)

args = commandArgs(trailingOnly = TRUE)

MIN_NUM_ARGS = 2

if (length(args) < MIN_NUM_ARGS) {
    stop(paste("Wrong number of arguments!",
               "Usage: Rscript fetch_updated_bills_data.R <pls_ids_filepath> <tmp_csvs_folderpath>",sep="\n"))
}


pls_ids_filepath = args[1]
tmp_csvs_folderpath = args[2]

devtools::install_github('analytics-ufcg/agora-digital', force=TRUE)

all_pls <- readr::read_csv(pls_ids_filepath)

process_pl <- function(id, casa, tema, apelido) {
  print(paste("Processando id",id,"da casa",casa))
  prop <- agoradigital::fetch_proposicao(id, casa, apelido, tema, TRUE)
  tram <- agoradigital::fetch_tramitacao(id,casa,TRUE)
  proc_tram <- agoradigital::process_proposicao(prop,tram,casa)%>%
    dplyr::mutate(data_hora = as.POSIXct(data_hora))
  status <- agoradigital::extract_status_tramitacao(tram)
  historico_energia <- agoradigital::get_historico_energia_recente(proc_tram) %>%
    dplyr::mutate(id_ext = prop$prop_id,
                  casa = prop$casa) %>%
    dplyr::select(id_ext, casa, periodo, energia_periodo, energia_recente)
  energia_value <- historico_energia[nrow(historico_energia),]$energia_recente
  
  extended_prop <- merge(prop,status,by="prop_id") %>%
    dplyr::mutate(energia = energia_value)
  
  pl_data <- list(proposicao = extended_prop, 
                  fases_eventos = proc_tram,
                  hist_energia = historico_energia)
}

res <- purrr::pmap(list(all_pls$id, all_pls$casa, all_pls$apelido, all_pls$tema), function(x, y, z, w) process_pl(x, y, z, w))
proposicoes <- purrr::map_df(res, ~ .$proposicao)
tramitacoes <- purrr::map_df(res, ~ .$fases_eventos)
hists_energia <- purrr::map_df(res, ~ .$hist_energia)
proposicoes <- proposicoes %>%
  select(-ano)

names(proposicoes) <- c("id_ext", "casa", "sigla_tipo", "numero", "data_apresentacao", "ementa", "palavras_chave",
            "casa_origem", "autor_nome", "tema", "apelido", "regime_tramitacao", "forma_apreciacao", 
            "em_pauta", "energia")

names(tramitacoes) <- c("id_ext","casa","data","sequencia","texto_tramitacao","sigla_local",
  "id_situacao","descricao_situacao","fase","situacao_descricao_situacao",
  "evento","data_audiencia","local","global")

readr::write_csv(proposicoes,paste0(tmp_csvs_folderpath,'/proposicoes.csv'))
readr::write_csv(tramitacoes,paste0(tmp_csvs_folderpath,'/trams.csv'))
readr::write_csv(hists_energia,paste0(tmp_csvs_folderpath,'/hists_energia.csv'))

