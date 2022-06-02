# importer une image de base
FROM python:3.8-slim
# définir le répertoire de travail actuel
WORKDIR profiling-batch
# copier le contenu dans le répertoire de travail
ADD . /profiling-batch
# exécuter pip pour installer les dépendances de l'application flask
RUN pip install -r requirements.txt
# définir la commande pour démarrer le conteneur
CMD ["python","./src/app.py"]