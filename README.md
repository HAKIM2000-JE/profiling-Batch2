
1-installer la version 3.8 du python sur https://www.python.org/downloads/release/python-380/

2- dans le répertoire du projet lancer la commande  
####pip install -r requirements.txt   
cela permet d’importer les librairies du projet  
3- dans le répertoire src lancer la commande :               
####python addRegion.py    
cela crée une collection region avec 18 documents sur la base de données 

4- sur le fichier environnement.py il y a une valeur BATCH_HOUR qui permet de préciser  l’heure du batch quotidien sous la forme string 

5- dans le répertoire src lancer la commande :  
####python app.py  
le batch se lance dans l’heure demandée 
