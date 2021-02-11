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


## Appendice. RISORSE WEB
dati meteo
- https://www.dati.lombardia.it/Ambiente/Dati-sensori-meteo-2020/erjn-istm
- https://www.dati.lombardia.it/Ambiente/Dati-sensori-meteo-2019/wrhf-6ztd
- https://www.dati.lombardia.it/Ambiente/Dati-sensori-meteo-2018/sfbe-yqe8
- https://www.dati.lombardia.it/Ambiente/Dati-sensori-meteo-2017/vx6g-atiu
