## 0.Preparazione ambiente

per eseguire l’analisi abbiamo bisogno dei moduli pandas e numpy, per non creare conflitti con altre versioni di Python ed altri moduli installati installo 
una virtualenv per isolare il nostro ambiente; se virtualenv non è presente installarla prima:
``` markdown
 sudo apt install python3-virtualenv
```
procedere con la creazione dell’ambiente:
``` markdown
 python3 -m venv qaria
```
nella cartella dove abbiamo creato la venv ora abbiamo una sottocartella che conterrà tutto l’ambiente che andremo a creare e lo script di attivazione della stessa; 
attiviamola:
``` markdown
 . qaria/bin/activate
 ```
il nostro ambiente è attivo e la linea di comando la mostra:
(qaria) silvio@LAPTOP-1E60R3SA:/mnt/home/py$

da questo momento in poi tutto quello che installiamo sarà all’interno di questo ambiente.
Procediamo con l’installazione di pandas
``` markdown
 pip install pandas
```
questa si porterà con se l’installazione anche di numpy.
Per i grafici
``` markdown
 pip install matplotlib
 ```
Per la decomposizione delle serie storiche
``` markdown
 pip install statsmodels
```

# 0.1 Istallazione ambiente dal file requirements.qaria.txt
Nel repository è presente il file requirements.qaria.txt da cui è possibile ricreare la virtualenv, con il comando:
``` markdown
 pip install -r requirements.qaria.txt
```


## 1.Pulizia dei dati

# 1.1 dati meteo
I dati relativi alle temperature, all’unidità ed alle precipitazioni sono scaricabili sotto forma di opendata  dal sito della regione lombardia, 
quindi è necessario filtrarli per individuare quelli di Milano.
Partendo dall’anagrafica delle stazioni (https://www.dati.lombardia.it/Ambiente/Stazioni-Meteorologiche/nf78-nj6b) 
procediamo a filtrare i record di interesse (ad es. i dati del 2020 sono in https://www.dati.lombardia.it/Ambiente/Dati-sensori-meteo-2020/erjn-istm). 
I file sono di grandi dimensioni quindi per il momento eviteremo caricamento su database (200Mb zippati, circa 2Gb scompattati)
o lavorazione tramite strumenti con interfaccia grafica. 
Saranni lavorati con gli strumenti presenti in un terminale Linux.
i) anagrafica stazioni di rilevamento
``` markdown
 awk '/Umidit/ || /Temperatura/ || /Precipitazione/' Stazioni_Meteorologiche.csv | awk '/,Milano/' > stazioni_meteo_MI_2020.csv
```
oppure singolarmente
``` markdown
 cat Stazioni_Meteorologiche.csv | sed -n '/,Precipitazione,mm/p' | sed -n '/,Milano/p' > stazioni_precipitazioni_MI.csv
 ```
 
ii) filtrare i dati delle stazioni di rilevamento sulla base degli idSensore filtrati per Milano.
Gli idSensore di Milano sono:
* temperature: 8162,5909,2001,5920,5897,5911
* umidità: 6179,6597,6174,2002,6185
* precipitazioni: 	14121,9341,8149,5908,19373,2006
	
Con gli identificativi delle stazioni di Milano andiamo a filtrare i dati relativi al 2020
``` markdown
 cat meteo_2020.csv | sed -n '/^\(8162\|5909\|2001\|5920\|5897\|5911\)/p' > meteo/2020/temperature_2020_mi.csv
 cat meteo_2020.csv | sed -n '/^\(6179\|6597\|6174\|2002\|6185\)/p' > meteo/2020/umidita_2020_mi.csv
 cat meteo_2020.csv | sed -n '/^\(14121\|9341\|8149\|5908\|19373\|2006\)/p' > meteo/2020/precipitazioni_2020_mi.csv
 ```
Questa operazione andrà ripetuta per i dati del 2019 e 2018.

# 1.2 Script data_clean_cl.py
Lo script si esegue nell'ambiente virtuale (qaria) di cui abbiamo il file di requirement nel repository; questo accetta come parametri di ingresso
``` console
usage: data_clean_cl.py [-h] --files_meteo FILES_METEO --evento
                        {umidita,temperature,precipitazioni} --genera {0,1}

optional arguments:
  -h, --help            show this help message and exit
  --files_meteo FILES_METEO
                        Inserire lista separata da virgola di
                        nome_file_meteo:anno_file. Il file dei dati di tutta
                        la regione
  --evento {umidita,temperature,precipitazioni}
                        eventi meteo da produrre
  --genera {0,1}        se devo generare il file evento da quello al parametro
                        --files_meteo[1], se ho gia' prodotto i file[0]
```
Tutte le operazioni di pulizia e filtraggio dei dati che abbiamo spiegato al punto precedente le abbiamo implementate nello script, chiamando la linea di comando linux con il modulo subprocess di python e reindirizzato l'output verso file. Con l'opzione ```console --genera 1 ``` andiamo ad eseguire questo lavoro; qualora avessimo già prodotto i file per l'evento meteo in lavorazione possiamo fornire ```console --genera 1 ```.
Nel Repo abbiamo caricato dei file evento già prodotti, spacchettare **`temperature.zip e umidita.zip`** e posizionare i file nella stessa cartella dello script.
Il nome dei file da filtrare e l'anno relativo vengono forniti nel parametro ```console --files_meteo ``` e se ho chiesto allo script di generare avrò come risultato [umidita|temperature|precipitazioni]_nome_file_da_filtrare

## Appendice. RISORSE WEB
dati meteo
- https://www.dati.lombardia.it/Ambiente/Dati-sensori-meteo-2020/erjn-istm
- https://www.dati.lombardia.it/Ambiente/Dati-sensori-meteo-2019/wrhf-6ztd
- https://www.dati.lombardia.it/Ambiente/Dati-sensori-meteo-2018/sfbe-yqe8
- https://www.dati.lombardia.it/Ambiente/Dati-sensori-meteo-2017/vx6g-atiu
- Modulo similaritymeasures [https://pypi.org/project/similaritymeasures/]
- Documentazione similaritymeasures [https://jekel.me/similarity_measures/index.html]
