import numpy as np
import pandas as pd
import similaritymeasures
###from dask.distributed import Client

import matplotlib.pyplot as plt
from datetime import datetime
import argparse,os

from qarialib import genera_grafici_qaria, misura_similarita_serie_storiche,controlla_files,chk_files

### #Client DASK
### client = Client(n_workers=2, threads_per_worker=2, processes=False, memory_limit='2GB')

custom_date_parser = lambda x: datetime.strptime(x, "%d/%m/%Y %H:%M:%S")

colore = {0:'green',1:'red',2:'blue',3:'yellow',4:'black'}
stile = {
    0:'solid',1:'dashed', 2:'dashdot', 3:'dotted',4:'solid'
}
tracciato_qaria=['stazione_id','data','inquinante','valore']
    

def genera_grafici(d_file_evento,colonna_data,colonna_valore):
    d_grafici={}
    l_df_evento=[]
    for anno,file_evento in d_file_evento.items():
        
        evento=pd.read_csv(file_evento,parse_dates=["Data"],date_parser=custom_date_parser,header=None,names=tracciato_meteo)
        
        # lasso di tempo che comprende la quarantena
        lock_d = (evento['Data'] > '%s-02-01'%str(anno)) & (evento['Data'] < '%s-05-01'%str(anno))
        evento = evento.loc[lock_d]
        
        evento["giorno"] = evento["Data"].dt.dayofyear
        col_name_aggre = "Valore_%s"%str(anno)
        evento=evento.rename(columns={"Valore": col_name_aggre})
        del evento["idOperatore"]
        del evento["Stato"]
        del evento["Data"]
        del evento["IdSensore"]
        #raggruppo per idSensore e sostuisco il dettaglio con la mediana per Pandas
        ts_evento=evento.groupby(evento["giorno"])[col_name_aggre].mean()
        # per Dask apply(lambda x: x.quantile(0.5))
        ###ts_evento=evento.groupby(evento["giorno"])["Valore"].apply(lambda x: x.quantile(0.5))
        
        ts_evento_roll = ts_evento.rolling(window=14)
        ts_evento_roll_mean = ts_evento_roll.mean()
        
        d_grafici[file_evento]=ts_evento_roll_mean
        
        l_df_evento.append(ts_evento_roll_mean)

    all_df=pd.concat(l_df_evento,axis=1);
    all_df=all_df.dropna()
    
    #### correlazione lineare inutile
    #### forse utile, generare serie storica delle differenze e poi correlazione com coeff angolare
    #### prossimo all zero, intercetta prossimo allo zero ...
    ###print("matrice correlazione pearson\n")
    ####print(all_df.corr(method="pearson"))
    
    d=misura_similarita_serie_storiche(all_df,2020,2019)
    print("similarita 2020/2019 %s"%str(d))
    
    d=misura_similarita_serie_storiche(all_df,2020,2018)
    print("similarita 2020/2018 %s"%str(d))
    
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
                        ,choices=['PM10','PM25','NO2','CO_8h','C6H6','O3','SO2']
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
    
    args = parser.parse_args()
    l_anni = [a.split(":")[1] for a in args.files_qaria.split(',')]
    l_file_in = [a.split(":")[0] for a in args.files_qaria.split(',')]
    d_files_qaria = {a.split(":")[1]:a.split(":")[0] for a in args.files_qaria.split(',')}
    
    print("file: ",l_file_in,"\n")
    print("anni: ",l_anni,"\n")
    print("dizionario: ",d_files_qaria)
    
    print("Generazione grafici, Media Mobile per smussare la serie\n")
    genera_grafici_qaria(d_files_qaria,args.inquinante,1,args.sep_csv)

    
if __name__ == '__main__':
    main();