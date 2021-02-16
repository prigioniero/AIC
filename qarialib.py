import numpy as np
import pandas as pd
import similaritymeasures
###from dask.distributed import Client

import matplotlib.pyplot as plt
from datetime import datetime
import argparse,os,re,subprocess


custom_date_parser = lambda x: datetime.strptime(x, "%d/%m/%Y %H:%M:%S")
custom_date_parser_qaria = lambda x: datetime.strptime(x, "%Y/%m/%d")
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
tracciato_qaria=['stazione_id','data','inquinante','valore']


##########################
def chk_files(arg,pat=re.compile(r"^(.+\.csv\:20[0-9]{2}\,{0,1})+$")):
    if not pat.match(arg):
        raise argparse.ArgumentTypeError("inserisci formattazione corretta: nome_file.csv;anno_file[,nome_file:anno_file]")
    return arg
###########################

########################
def controlla_files(l_file):
    for f in l_file:
        if not os.path.isfile(f):
            return False
        else:
            return True

#######################

###################################
def genera_grafici_meteo(d_file_evento):
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
        ### ts_evento.plot()
        ### ts_evento_roll_mean.plot(color=colore[n],label=file_evento)
    all_df=pd.concat(l_df_evento,axis=1);
    all_df=all_df.dropna()
    
    #print("matrice correlazione pearson\n")
    #print(all_df.corr(method="pearson"))

    d=misura_similarita_serie_storiche(all_df,2020,2019)
    print("similarita 2020/2019 %s"%str(d))
    
    d=misura_similarita_serie_storiche(all_df,2020,2018)
    print("similarita 2020/2018 %s"%str(d))
    
    l_plot=[]
    ##print(all_df.corr(method='kendall'))
    n=0
    for f,g in d_grafici.items():
        ###n=randrange(5)
        ###g=g.compute()
        appo_plot=g.plot(color=colore[n],label=f,linestyle=stile[n])
        l_plot.append(appo_plot)
        n+=1
    plt.legend()
    plt.show()

###################################

###################################
def genera_grafici_qaria(d_files_qaria,inquinante):
    d_grafici={}
    l_df_qaria=[]
    for anno,file_qaria in d_files_qaria.items():
        ##################### ,date_parser=custom_date_parser_qaria
        qaria=pd.read_csv(file_qaria,parse_dates=["data"],header=None,names=tracciato_qaria,sep=';',skiprows=1)
        qaria.resample("data",freq=1).fillna(0)
        qaria = qaria.loc[qaria['inquinante'] == inquinante]
        
        # lasso di tempo che comprende la quarantena
        lock_d = (qaria['data'] > '%s/02/01'%str(anno)) & (qaria['data'] < '%s/05/01'%str(anno))
        qaria = qaria.loc[lock_d]
        
        qaria["giorno"] = qaria["data"].dt.dayofyear
        col_name_aggre = "Valore_%s"%str(anno)
        qaria=qaria.rename(columns={"valore": col_name_aggre})
        del qaria["stazione_id"]
        #raggruppo per idSensore e sostuisco il dettaglio con la mediana per Pandas
        ts_qaria=qaria.groupby(qaria["giorno"])[col_name_aggre].median()
        # per Dask apply(lambda x: x.quantile(0.5))
        ###ts_evento=evento.groupby(evento["giorno"])["Valore"].apply(lambda x: x.quantile(0.5))
        print("anno",anno,"\n",ts_qaria)
        
        ts_qaria_roll = ts_qaria.rolling(window=5)
        ts_qaria_roll_mean = ts_qaria_roll.mean()
        
        d_grafici[file_qaria]=ts_qaria_roll_mean
        l_df_qaria.append(ts_qaria_roll_mean)
        
        ###d_grafici[file_qaria]=ts_qaria
        ###l_df_qaria.append(ts_qaria)
        ### ts_evento.plot()
        ### ts_evento_roll_mean.plot(color=colore[n],label=file_evento)
    all_df=pd.concat(l_df_qaria,axis=1);
    
    ##all_df=all_df.dropna()
    #print("matrice correlazione pearson\n")
    #print(all_df.corr(method="pearson"))

    d=misura_similarita_serie_storiche(all_df,2020,2019)
    print("similarita 2020/2019 %s"%str(d))
    
    d=misura_similarita_serie_storiche(all_df,2020,2018)
    print("similarita 2020/2018 %s"%str(d))
    
    l_plot=[]
    ##print(all_df.corr(method='kendall'))
    n=0
    for f,g in d_grafici.items():
        ###n=randrange(5)
        ###g=g.compute()
        appo_plot=g.plot(color=colore[n],label=f,linestyle=stile[n])
        l_plot.append(appo_plot)
        n+=1
    plt.legend()
    plt.show()

###################################

####################################
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


def misura_similarita_serie_storiche(all_df,base,compara_con):
    try:
        res={}
        indici=all_df.index
        num_righe = len(indici)
        arr_base = np.zeros((num_righe, 2))
        arr_compara_con=np.zeros((num_righe, 2))
        
        arr_base[:,0] = all_df.index
        arr_base[:,1] = all_df['Valore_%s'%str(base)].to_numpy()
        
        arr_compara_con[:,0] = all_df.index
        arr_compara_con[:,1] = all_df['Valore_%s'%str(compara_con)].to_numpy()
        
        return {'pcm':similaritymeasures.pcm(arr_base, arr_compara_con)
                ,'area_between_two_curves':similaritymeasures.area_between_two_curves(arr_base, arr_compara_con)
                ,'frechet_dist':similaritymeasures.frechet_dist(arr_base, arr_compara_con)
        }
    except:
        return None

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

