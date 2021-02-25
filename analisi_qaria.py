import numpy as np
import pandas as pd
import similaritymeasures
###from dask.distributed import Client

import matplotlib.pyplot as plt
from datetime import datetime
import argparse,os

## import funzioni da qarialib
from qarialib import genera_grafici_qaria,misura_similarita_serie_storiche,controlla_files,chk_files
from qarialib import custom_date_parser

# importo dizionari e liste da config.py
from config import colore,stile,tracciato_qaria
from config import nome_colonna_data,nome_colonna_valore
### #Client DASK
### client = Client(n_workers=2, threads_per_worker=2, processes=False, memory_limit='2GB')    


def main():
    print("main\n")
    # inizio sviluppo lavorazione file in parallelo  -- oppure con subprocess lanciare i comandi linux su README
    parser = argparse.ArgumentParser()
    parser.add_argument('--files_qaria'
                        ,type=chk_files
                        ,help="Inserire lista separata da virgola di nome_file_meteo:anno_file. Il file dei dati di tutta la regione"
                        ,required=True)
    parser.add_argument('--inquinante'
                        ,type=str
                        ,choices=['PM10','PM25','NO2','SO2']
                        ,help="inquinanti da lavorare"
                        ,default="PM10"
                        ,required=False)
    parser.add_argument('--sep_csv'
                        ,type=str
                        ,help="inserire separatore dei file csv in input"
                        ,default=","
                        ,required=False)
    parser.add_argument('--skip_riga'
                        ,type=int
                        ,help="Inserire 1 se il file ha intestazione"
                        ,default=1
                        ,required=False)
    #tracciato_qaria=['stazione_id','data','inquinante','valore']
    ###parser.add_argument('--tracciato_qaria'
    ###                    ,type=str
    ###                    ,help="Inserire tracciato record file qaria separato da virgola"
    ###                    ,default='stazione_id,data,inquinante,valore'
    ###                    ,required=False)
    
    parser.add_argument('--colonna_data'
                        ,type=str
                        ,help="Inserire nome della colonna contenente la data della serie storica"
                        ,default=nome_colonna_data
                        ,required=False)
    parser.add_argument('--colonna_valore'
                        ,type=str
                        ,help="Inserire nome della colonna contenente il valore della serie storica"
                        ,default=nome_colonna_valore
                        ,required=False)
    
    args = parser.parse_args()
    l_anni = [a.split(":")[1] for a in args.files_qaria.split(',')]
    l_file_in = [a.split(":")[0] for a in args.files_qaria.split(',')]
    d_files_qaria = {a.split(":")[1]:a.split(":")[0] for a in args.files_qaria.split(',')}
    
    c_data = args.colonna_data
    c_valore = args.colonna_valore
    
    ###tracciato_qaria=[x for x in args.tracciato_qaria.split(",")]
    
    print("file: ",l_file_in,"\n")
    print("anni: ",l_anni,"\n")
    print("dizionario: ",d_files_qaria)
    
    print("Generazione grafici, applico Media Mobile per smussare la serie\n")
    genera_grafici_qaria(d_files_qaria,args.inquinante,1,args.sep_csv,c_data,c_valore)

    
if __name__ == '__main__':
    main();