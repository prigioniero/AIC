import numpy as np
import pandas as pd
import similaritymeasures
from dask.distributed import Client

import matplotlib.pyplot as plt
from datetime import datetime
import argparse,os
from multiprocessing import Pool
from itertools import product

import subprocess,re
from random import randrange
from qarialib import genera_grafici_meteo, genera_file_meteo, misura_similarita_serie_storiche,controlla_files,chk_files
from config import d_stazioni,d_stazioni_lombardia,nome_colonna_data_meteo,nome_colonna_valore_meteo,sep_meteo,skip_meteo

### #Client DASK
### client = Client(n_workers=2, threads_per_worker=2, processes=False, memory_limit='2GB')


def main():
    print("main\n")
    # inizio sviluppo lavorazione file in parallelo  -- oppure con subprocess lanciare i comandi linux su README
    parser = argparse.ArgumentParser()
    parser.add_argument('--files_meteo'
                        ,type=chk_files
                        ,help="Inserire lista separata da virgola di nome_file_meteo:anno_file. Il file dei dati di tutta la regione"
                        ,required=True)
    parser.add_argument('--evento'
                        ,type=str
                        ,choices=['umidita','temperature','precipitazioni']
                        ,help="eventi meteo da produrre"
                        ,required=True)
    parser.add_argument('--genera'
                        ,type=int
                        ,choices=[0,1]
                        ,help="se devo generare il file evento da quello al parametro --files_meteo[1], se ho gia' prodotto i file[0]",required=True)
    
    
    parser.add_argument('--sep_csv'
                        ,type=str
                        ,help="inserire separatore dei file csv in input"
                        ,default=sep_meteo
                        ,required=False)
    parser.add_argument('--skip_riga'
                        ,type=int
                        ,help="Inserire 1 se il file ha intestazione"
                        ,default=skip_meteo
                        ,required=False)
    parser.add_argument('--colonna_data'
                        ,type=str
                        ,help="Inserire nome della colonna contenente la data della serie storica"
                        ,default=nome_colonna_data_meteo
                        ,required=False)
    parser.add_argument('--colonna_valore'
                        ,type=str
                        ,help="Inserire nome della colonna contenente il valore della serie storica"
                        ,default=nome_colonna_valore_meteo
                        ,required=False)
    
    args = parser.parse_args()
    l_anni = [a.split(":")[1] for a in args.files_meteo.split(',')]
    l_file_in = [a.split(":")[0] for a in args.files_meteo.split(',')]
    d_files_meteo = {a.split(":")[0]:a.split(":")[1] for a in args.files_meteo.split(',')}
    
    print("file: ",l_file_in,"\n")
    print("anni: ",l_anni,"\n")
    print("dizionario: ",d_files_meteo)
    
    d_file_evento={}
    print("preparazione file eventi atmosferici\n")
    if 1==args.genera:
        if not controlla_files(l_file_in):
            print("lista file non corretta: vanno inseriti nome file esistenti")
            exit(-1)
        else:
            print("Parametri file corretti")
        
        for f,anno in d_files_meteo.items():
            print("produco %s anno %s"%(f,anno))
            ### l_file_evento.append( genera_file_meteo(f,d_stazioni[args.evento],args.evento,anno))
            d_file_evento[anno]=genera_file_meteo(f,d_stazioni_lombardia[args.evento],args.evento,anno)
        
        ### if (file_precipi or file_temper or file_umidit):
        if all([f for f in d_file_evento.values()]):
            print("abbiamo prodotto tutti i file, bene!!")
        else:
            print("qualche errorino l'abbiamo fatto!!! Esco.\n")
            exit(-1)
        
    print("FINE: preparazione file eventi atmosferici\n")
    
    print("Generazione grafici, Media Mobile per smussare la serie\n")
    d_file_evento={'2020':'%s_meteo_2020.csv'%args.evento
                   ,'2019':'%s_meteo_2019.csv'%args.evento
                   ,'2018':'%s_meteo_2018.csv'%args.evento}
    
    genera_grafici_meteo(d_file_evento=d_file_evento,skip=0,sep=",",cdata="Data",cvalore="Valore")

    
if __name__ == '__main__':
    main();