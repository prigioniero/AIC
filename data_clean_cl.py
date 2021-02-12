import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from pandas import DataFrame
import argparse,os
from multiprocessing import Pool
from itertools import product

import subprocess


custom_date_parser = lambda x: datetime.strptime(x, "%d/%m/%Y %H:%M:%S")
l_stazioni_temperatura=[8162,5909,2001,5920,5897,5911]
l_stazioni_umidita=[6179,6597,6174,2002,6185]
l_stazioni_precipitazioni = [14121,9341,8149,5908,19373,2006]

tracciato_meteo=['IdSensore','Data','Valore','Stato','idOperatore']

def genera_file_meteo(file_meteo,lista_id_sensori,evento,anno):
    try:
        appo_cmd = r'\|'.join(list(map(str,lista_id_sensori)))
        cmd_evento = "cat %s | sed -n '/^\(%s\)/p'"%(file_meteo,appo_cmd)
        file_name='%s_%s.csv'%(evento,str(anno))
        with open(file_name, "w") as outfile:
            subprocess.run(cmd_evento, stdout=outfile,shell=True)
        return file_name
    except:
        return ''

def prepara_dati(file_sorgente,anno):
    return 0

def controlla_file(file_path):
    if os.path.isfile(file_path):
        return True
    else:
        return False

def main():
    print("main")
    # inizio sviluppo lavorazione file in parallelo  -- oppure con subprocess lanciare i comandi linux su README
    parser = argparse.ArgumentParser()
    parser.add_argument('--meteo', type=str,required=True)
    parser.add_argument('--anno', type=int,required=True)
    
    args = parser.parse_args()
    
    if not controlla_file(args.meteo):
        print("Parametri file non corretti")
        exit(-1)
    else:
        print("Parametri file corretti")
    
    ### ## genero file meteo
    ### appo_cmd_precipitazioni = r'\|'.join(list(map(str,l_stazioni_precipitazioni)))
    ### cmd_precipitazioni = "cat %s | sed -n '/^\(%s\)/p'"%(args.meteo,appo_cmd_precipitazioni);
    ### with open('myfile_out_prep.csv', "w") as outfile:
    ###     subprocess.run(cmd_precipitazioni, stdout=outfile,shell=True)
    
    file_precipi = genera_file_meteo(args.meteo,l_stazioni_precipitazioni,"precipitazioni",2020)
    file_temper = genera_file_meteo(args.meteo,l_stazioni_temperatura,"temperature",2020)
    file_umidit = genera_file_meteo(args.meteo,l_stazioni_umidita,"umidita",2020)
    
    if (file_precipi or file_temper or file_umidit):
        print("abbiamo prodotto tutti i file, bene!!")
    else:
        print("qualche errorino l'abbiamo fatto!!! Esco.\n")
        print("prep: %s, temp: %s, umidit: %s"%(file_precipi,file_temper,file_umidit))
        exit(-1)

    ## vecchia parte di elaborazione -- file già lavorati con sed awk & Co.
    
    #print("abbiamo prodotto tutti i file, bene!!")#
    temperature=pd.read_csv(file_temper,parse_dates=["Data"],date_parser=custom_date_parser,header=None,names=tracciato_meteo)
    # aggiungo il mese
    print(temperature.info())
    lock_d = (temperature['Data'] > '2020-02-01') & (temperature['Data'] < '2020-05-01')

    temperature = temperature.loc[lock_d]
    
    temperature["giorno"] = temperature["Data"].dt.dayofyear
    del temperature["idOperatore"]
    del temperature["Stato"]
    del temperature["Data"]
    del temperature["IdSensore"]
    #raggruppo per idSensore e sostuisco il dettaglio con la media.
    ts_temp=temperature.groupby(temperature["giorno"])["Valore"].median()
    
    ts_temp.plot()
    
    plt.show()

    
if __name__ == '__main__':
    main();