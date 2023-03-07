# Challenge-Securite-SISE

Projet de Visualisation de données de sécurité durant le master SISE

## Objectif de ce repository

Ce repository présente comment utiliser l'image Docker pour accéder à l'application Streamlit

## Comment utiliser ce repository :

Vous avez deux moyens d'utiliser ce repository :

## 1. Obtenir l'image par Docker Hub

Pour récupérer les images par le Docker Hub voici les étapes

### Requis

* Avoir Docker Desktop et un compte Docker Hub

Lancer un terminal et faire les commandes insérées ci-dessous : 

```
$ # Le username est le mot de passe concerne celui de votre compte Docker Hub
$ docker login --username=your_username --password=your_password
$ docker pull htitouan/chall-secu
$ docker run -p 8501:8501 htitouan/chall-secu
```

Après avoir lancé ces commandes vous pouvez ouvrir l'application sur : localhost:8501

## 2. Construire l'image à partir du Git

Pour construire l'image Docker à partir des fichiers voici les étapes : 

### Requis 

* Avoir téléchargé le git et au minima avoir le dossier Streamlit dans son ordinateur
* Télécharger le dossier data dans le drive et l'insérer dans le dossier "streamlit"

Lancer un terminal et faire les commandes insérées ci-dessous : 

```
$ cd 'path/to/your/repository/folder/streamlit'
$ docker build -t "nom_image_de_votre_choix" .
$ docker run -p 8501:8501 "nom_image_de_votre_choix"
```
Après avoir lancé ces commandes vous pouvez ouvrir l'application sur : localhost:8501
