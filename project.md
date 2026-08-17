## Dataset
https://www.kaggle.com/mylesoneill/world-university-rankings

## Quesito / problema
prevedere se un’università è top-tier o no usando le metriche disponibili nei ranking.

### Target consigliato
Top-tier = 1 se world_rank <= 100.
Top-tier = 0 altrimenti.
È una label chiara, difendibile e facile da spiegare nel report.

### Perché funziona
Il contesto è forte: ranking universitari, qualità, ricerca, internazionalizzazione, spesa educativa.
Hai abbastanza feature per fare preprocessing e selezione variabili senza forzature.
Il report può seguire bene la struttura tipica del corso: exploration, preprocessing, models, evaluation.

## Research Questions
- RQ1: Quali metriche distinguono davvero le università top-tier dalle altre?
- RQ2: Quanto sono predittive le variabili di ranking rispetto alla classe top-tier (Top-tier = 1 se world_rank ≤ 100, 0 altrimenti)?
- RQ3: I modelli lineari e non lineari ottengono risultati diversi su questo task di classificazione top-tier/non-top-tier?

## Workflow KNIME iniziale
- Caricamento delle tabelle principali dei ranking (timesData, shanghaiData, cwurData) e della tabella school_and_country_table.
- Pulizia dei dati e armonizzazione di nomi università e paesi.
- Creazione del target binario Top-tier a partire da world_rank.
- Gestione dei valori mancanti (rimozione/imputazione).
- Encoding delle variabili categoriche (es. country).
- Eventuale aggiunta di feature di contesto dalla spesa educativa per paese.
- Train/test split con stratificazione sulla classe Top-tier.
- Addestramento dei modelli di classificazione (logistic regression, alberi, ensemble).
- Valutazione con metriche adatte alla classification (accuracy, precision, recall, F1, ROC-AUC).

## Note
