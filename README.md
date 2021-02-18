## 0.Preparazione ambiente

Per eseguire l’analisi abbiamo bisogno dei moduli pandas e numpy, per non creare conflitti con altre versioni di Python ed altri moduli installati verrà creata 
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
Il nostro ambiente è attivo e la linea di comando la mostra:
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
Per la decomposizione delle serie storiche (se necessaria)
``` markdown
 pip install statsmodels
```

# 0.1 Istallazione ambiente dal file requirements.qaria.txt
Nel repository è presente il file requirements.qaria.txt da cui è possibile ricreare la virtualenv, con il comando:
``` markdown
 pip install -r requirements.qaria.txt
```


# 1.Pulizia dei dati
## 1.0 Pulizia dati regionali della qualità dell'aria
Il file delle stazioni presentano il nome esteso dell'inquinante, sostituisco il nome con la sigla per comodità:
- Biossido di Azoto: NO2 (solo per i dati regionali)
- Biossido di Zolfo: SO2
- PM10 (SM2005): PM10
- Particelle sospese PM2.5: PM25
``` console
 > sed -i 's/Biossido di Azoto/NO2/g' stazioni_qaria_lombardia.csv
 > sed -i 's/Biossido di Zolfo/SO2/g' stazioni_qaria_lombardia.csv
 > sed -i 's/PM10 (SM2005)/PM10/g' stazioni_qaria_lombardia.csv
 > sed -i 's/Particelle sospese PM2.5/PM25/g' stazioni_qaria_lombardia.csv
```
Ed in fine creo il file csv delle stazioni della regione degli inquinanti che volgio elaborare con le rispettive sigle
```console
 > grep 'SO2\|NO2\|PM10\|PM25' stazioni_qaria_lombardia.csv > stazioni_qaria_lombardia_clean.csv
```
I file all'interno dello zip ```file qaria_regione_clean.zip``` sono i dati regionali degli inquinanti ().


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
Tutte le operazioni di pulizia e filtraggio dei dati che abbiamo spiegato al punto precedente le abbiamo implementate nello script, chiamando la linea di comando linux con il modulo subprocess di python e reindirizzato l'output verso file. Con l'opzione ```console --genera 1 ``` andiamo ad eseguire questo lavoro; qualora avessimo già prodotto i file per l'evento meteo in lavorazione possiamo fornire ```console --genera 0 ``` ed indicare in ```console files_meteo``` la lista dei files dell'evento. Esempio partendo dal file generale (https://www.dati.lombardia.it/Ambiente/Dati-sensori-meteo-2020/erjn-istm):
```console
python data_clean_cl.py --files_meteo "file_meteo_generale.csv:2020,..." --evento umidita --genera 1
```
quindi sto dicendo allo script di compiere l'analisi dell'evento umidita partendo dal file generale.
Se per qualche motivo abbiamo già compiuto questo passo e volgiamo ripeterlo, avremo già prodotto i file dell'evento 
`umidita_meteo_2020.csv,umidita_meteo_2019.csv,umidita_meteo_2018.csv` quindi eseguiremo con la lista dei file già prodotti e senza generare:

```console
python data_clean_cl.py --files_meteo "umidita_meteo_2020.csv:2020,umidita_meteo_2019.csv:2019..." --evento umidita --genera 0
```

Nel Repo abbiamo caricato dei file evento già prodotti (i file generali sono di circa 2GB), spacchettare **`temperature.zip e umidita.zip`** e posizionare i file nella stessa cartella dello script.
Il nome dei file da lavorare e l'anno relativo vengono forniti nel parametro ```console --files_meteo ``` e visto che abbiamo già i file evento prodotti forniamo 0 come parametro genera.

## 2.Analisi delle Qualità dell'aria
# 2.0  
# 2.1 Script python analisi_qaria.py
Questo script mette a confronto le serie storiche dei vari anni, ad esempio

```console
python analisi_qaria.py --files_qaria "qaria_regione_clean_2020.csv:2020,qaria_regione_clean_2019.csv:2019,qaria_regione_clean_2018.csv:2018" --inquinante SO2
```
Dall'help
```console
usage: analisi_qaria.py [-h] --files_qaria FILES_QARIA
                        [--inquinante {PM10,PM25,NO2,CO_8h,C6H6,O3,SO2}]

optional arguments:
  -h, --help            show this help message and exit
  --files_qaria FILES_QARIA
                        Inserire lista separata da virgola di
                        nome_file_meteo:anno_file. Il file dei dati di tutta
                        la regione
  --inquinante {PM10,PM25,NO2,CO_8h,C6H6,O3,SO2}
                        inquinanti da lavorare
```
# 2.2 Attenzione
## Appendice. RISORSE WEB
dati meteo
- https://www.dati.lombardia.it/Ambiente/Dati-sensori-meteo-2020/erjn-istm
- https://www.dati.lombardia.it/Ambiente/Dati-sensori-meteo-2019/wrhf-6ztd
- https://www.dati.lombardia.it/Ambiente/Dati-sensori-meteo-2018/sfbe-yqe8
- https://www.dati.lombardia.it/Ambiente/Dati-sensori-meteo-2017/vx6g-atiu
- Modulo similaritymeasures [https://pypi.org/project/similaritymeasures/]
- Documentazione similaritymeasures [https://jekel.me/similarity_measures/index.html]
