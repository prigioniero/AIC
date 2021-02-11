import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from pandas import DataFrame
import argparse,os
from multiprocessing import Pool


custom_date_parser = lambda x: datetime.strptime(x, "%d/%m/%Y %H:%M:%S")
l_stazioni_temperatura=[8162,5909,2001,5920,5897,5911]
l_stazioni_umidita=[6179,6597,6174,2002,6185]
l_stazioni_precipitazioni = [14121,9341,8149,5908,19373,2006]

def lettura_file(lines,l_filtro):
    res = []
    for l in lines:
        if l.split(",")[0] in l_filtro:
            res.append(l)
    return res

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
    
    ## temperature ##
    num_processi = 8
    num_linee = 5000
    
    lines = open(args.meteo).readlines()
    pool = Pool(processes=num_processi)
    
    ## lavorazione della temperatura -- va implementato per tutte le altre componenti umidita e precipitazioni
    l_meteo = pool.starmap(lettura_file, (lines[line:line+num_linee] for line in range(0,len(lines),num_linee)), l_stazioni_temperatura)
    
    with open('out_temperature.txt', 'w') as f:
        for item in l_meteo:
            f.write("%s\n" % item)
    
    
    exit(0)
    
    ## vecchia parte di elaborazione -- file già lavorati con sed awk & Co.
    temperature=pd.read_csv('meteo/2020/temperature_2020_mi.csv',parse_dates=["Data"],date_parser=custom_date_parser)
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