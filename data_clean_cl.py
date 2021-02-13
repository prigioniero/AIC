import numpy as np
import pandas as pd
##from pandas import DataFrame
##import dask.dataframe as pd
from dask.distributed import Client

import matplotlib.pyplot as plt
from datetime import datetime
import argparse,os
from multiprocessing import Pool
from itertools import product

import subprocess,re
from random import randrange

### Client DASK
client = Client(n_workers=2, threads_per_worker=2, processes=False, memory_limit='2GB')

custom_date_parser = lambda x: datetime.strptime(x, "%d/%m/%Y %H:%M:%S")
d_stazioni = {
    'temperature': [8162,5909,2001,5920,5897,5911],
    'umidita': [6179,6597,6174,2002,6185],
    'precipitazioni': [14121,9341,8149,5908,19373,2006]
}

colore = {0:'green',1:'red',2:'blue',3:'yellow',4:'black'}
stile = {
    0:'solid',1:'dashed', 2:'dashdot', 3:'dotted',4:'solid'
}
tracciato_meteo=['IdSensore','Data','Valore','Stato','idOperatore']

def genera_grafici(d_file_evento):
    d_grafici={}
    for anno,file_evento in d_file_evento.items():
        
        evento=pd.read_csv(file_evento,parse_dates=["Data"],date_parser=custom_date_parser,header=None,names=tracciato_meteo)
        
        # lasso di tempo che comprende la quarantena
        lock_d = (evento['Data'] > '%s-02-01'%str(anno)) & (evento['Data'] < '%s-05-01'%str(anno))
        evento = evento.loc[lock_d]
        
        evento["giorno"] = evento["Data"].dt.dayofyear
        del evento["idOperatore"]
        del evento["Stato"]
        del evento["Data"]
        del evento["IdSensore"]
        #raggruppo per idSensore e sostuisco il dettaglio con la mediana per Pandas
        ts_evento=evento.groupby(evento["giorno"])["Valore"].mean()
        # per Dask apply(lambda x: x.quantile(0.5))
        ###ts_evento=evento.groupby(evento["giorno"])["Valore"].apply(lambda x: x.quantile(0.5))
        
        ts_evento_roll = ts_evento.rolling(window=14)
        ts_evento_roll_mean = ts_evento_roll.mean()
        
        d_grafici[file_evento]=ts_evento_roll_mean
        ### ts_evento.plot()
        ### ts_evento_roll_mean.plot(color=colore[n],label=file_evento)
    l_plot=[]
    n=0
    for f,g in d_grafici.items():
        ###n=randrange(5)
        ###g=g.compute()
        appo_plot=g.plot(color=colore[n],label=f,linestyle=stile[n])
        l_plot.append(appo_plot)
        n+=1
    plt.legend()
    plt.show()
    

def genera_file_meteo(file_meteo,lista_id_sensori,evento,anno):
    try:
        appo_cmd = r'\|'.join(list(map(str,lista_id_sensori)))
        cmd_evento = "cat %s | sed -n '/^\(%s\)/p'"%(file_meteo,appo_cmd)
        file_name='%s_%s'%(evento,file_meteo)
        with open(file_name, "w") as outfile:
            subprocess.run(cmd_evento, stdout=outfile,shell=True)
        return file_name
    except:
        return ''

def prepara_dati(file_sorgente,anno):
    return 0

def controlla_files(l_file):
    for f in l_file:
        if not os.path.isfile(f):
            return False
        else:
            return True

def chk_files_meteo(arg,pat=re.compile(r"^(.+\.csv\:20[0-9]{2}\,{0,1})+$")):
    if not pat.match(arg):
        raise argparse.ArgumentTypeError("inserisci formattazione corretta: nome_file.csv;anno_file[,nome_file:anno_file]")
    return arg

def main():
    print("main\n")
    # inizio sviluppo lavorazione file in parallelo  -- oppure con subprocess lanciare i comandi linux su README
    parser = argparse.ArgumentParser()
    parser.add_argument('--files_meteo', type=chk_files_meteo,help="inserire lista separata da virgola di nome_file_meteo:anno_file",required=True)
    parser.add_argument('--evento', type=str,choices=['umidita','temperature','precipitazioni'],help="controlla valori ammessi",required=True)
    
    args = parser.parse_args()
    l_anni = [a.split(":")[1] for a in args.files_meteo.split(',')]
    l_file_in = [a.split(":")[0] for a in args.files_meteo.split(',')]
    d_files_meteo = {a.split(":")[0]:a.split(":")[1] for a in args.files_meteo.split(',')}
    
    print("file: ",l_file_in,"\n")
    print("anni: ",l_anni,"\n")
    print("dizionario: ",d_files_meteo)
    
    d_file_evento={}
    print("preparazione file eventi atmosferici\n")
    if 1==1:
        if not controlla_files(l_file_in):
            print("lista file non corretta: vanno inseriti nome file esistenti")
            exit(-1)
        else:
            print("Parametri file corretti")
        
        for f,anno in d_files_meteo.items():
            print("produco %s anno %s"%(f,anno))
            ### l_file_evento.append( genera_file_meteo(f,d_stazioni[args.evento],args.evento,anno))
            d_file_evento[anno]=genera_file_meteo(f,d_stazioni[args.evento],args.evento,anno)
        
        ### if (file_precipi or file_temper or file_umidit):
        if all([f for f in d_file_evento.values()]):
            print("abbiamo prodotto tutti i file, bene!!")
        else:
            print("qualche errorino l'abbiamo fatto!!! Esco.\n")
            exit(-1)
        
    print("FINE: preparazione file eventi atmosferici\n")
    
    print("Generazione grafici, Media Mobile per smussare la \n")
    genera_grafici(d_file_evento)

    
if __name__ == '__main__':
    main();