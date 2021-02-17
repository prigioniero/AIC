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
from qarialib import genera_grafici_meteo, misura_similarita_serie_storiche,controlla_files,chk_files

### #Client DASK
### client = Client(n_workers=2, threads_per_worker=2, processes=False, memory_limit='2GB')



d_trans_inqui = {'Biossido di Azoto':'NO2'
                 ,'Biossido di Zolfo': 'SO2'
                 ,'PM10 (SM2005)':'PM10'
                 ,'Particelle sospese PM2.5':'PM25'}
l_inquinanti = ['NO2','SO2','PM10','PM25']
def main():
    print("main\n")
    # inizio sviluppo lavorazione file in parallelo  -- oppure con subprocess lanciare i comandi linux su README
    parser = argparse.ArgumentParser()
    parser.add_argument('--file_stazioni'
                        ,type=str
                        ,help="Inserire file anagrafica stazioni della Regione"
                        ,required=True)
    parser.add_argument('--files_qaria'
                        ,type=chk_files
                        ,help="Inserire lista separata da virgola di nome_file_qaria:anno_file. Il file dei dati di tutta la regione"
                        ,required=True)
    ### parser.add_argument('--inquinante'
    ###                     ,type=str
    ###                     ,choices=['PM10','PM25','NO2','CO_8h','C6H6','O3']
    ###                     ,help="inquinanti da lavorare"
    ###                     ,default="PM10"
    ###                     ,required=False)
    
    args = parser.parse_args()
    d_files_qaria = {a.split(":")[1]:a.split(":")[0] for a in args.files_qaria.split(',')}
    d_df_qaria={}
    print(args.file_stazioni)
    stazioni=pd.read_csv(args.file_stazioni)
    print(stazioni.info)
    stazioni=stazioni[stazioni['NomeTipoSensore'].isin(l_inquinanti)]
    stazioni_ =stazioni[["IdSensore","NomeTipoSensore"]]
    stazioni_=stazioni_.rename(columns={"NomeTipoSensore": "inquinante"})
    
    ###stazioni_["inquinante"]=[d_trans_inqui.get(x) if x in d_trans_inqui.keys() else None for x in stazioni_["NomeTipoSensore"]]
    
    for anno,f in d_files_qaria.items():
        df_appo=pd.read_csv(f,parse_dates=["Data"])
        df_appo = df_appo[df_appo['Stato'].notna()]
        del df_appo["Stato"]
        del df_appo["idOperatore"]
        res=pd.merge(df_appo,stazioni_,how='left',on=['IdSensore'])
        res = res[res['inquinante'].notna()]
        ## stazione_id;data;inquinante;valore
        res=res.rename(columns={"Valore": "valore", "IdSensore":"stazione_id","Data":"data"})
        res = res[["stazione_id","data","inquinante","valore"]]
        res.to_csv('qaria_regione_clean_%s.csv'%str(anno),index=False)

    
if __name__ == '__main__':
    main();