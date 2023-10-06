# Django usercustomisation api
## Description

cette application permet la gestion de l'utilisateur base sur le module utilisateur fourni par django. Et l'ajout de champs supplementaires telque une image et bien d'autre si besoin. Nous avons creer une classe abstraite AbstractUser qui herite de AbstractBaseUser fourni par django.contrib.auth.models.

## Fonctionnalités
Avec ce projet, il est possible de :
- Se connecter
- Se déconnecter
- Vérifier si un e-mail existe
- Vérifier si un numéro de téléphone existe
- Vérifier le code envoyé à l'utilisateur
- Envoyer un code à l'utilisateur pour vérifier son e-mail/numéro de téléphone (pas encore implémenté)
- Solliciter un nouveau code de vérification
- Enregistrer un nouvel utilisateur
- Lister tous les utilisateurs enregistrés
- Afficher les informations d'un utilisateur
- Modifier les informations d'un utilisateur
- Supprimer un utilisateur (pas encore implémenté)

## Environnement de developpement
- python 3.8
- Ubuntu 20.04
- MySQL Database
- VS Code

## Requirement
- altgraph==0.17.3
- asgiref==3.6.0
- auto-py-to-exe==2.32.0
- backports.zoneinfo==0.2.1
- bottle==0.12.25
- bottle-websocket==0.2.9
- certifi==2023.5.7
- cffi==1.15.1
- charset-normalizer==3.1.0
- coreapi==2.3.3
- coreschema==0.0.4
- cryptography==39.0.2
- Django==4.2.3
- django-cors-headers==4.1.0
- django-rest-knox==4.2.0
- django-rest-swagger==2.2.0
- Django-Verify-Email==2.0.3
- djangorestframework==3.14.0
- djangorestframework-simplejwt==5.2.2
- drf-yasg==1.21.6
- Eel==0.14.0
- exceptiongroup==1.1.2
- future==0.18.3
- gevent==22.10.2
- gevent-websocket==0.10.1
- greenlet==2.0.2
- idna==3.4
- inflection==0.5.1
- iniconfig==2.0.0
- install==1.3.5
- itypes==1.2.0
- Jinja2==3.1.2
- MarkupSafe==2.1.3
- mysqlclient==2.2.0
- openapi-codec==1.3.2
- packaging==23.1
- Pillow==9.4.0
- pluggy==1.2.0
- pycparser==2.21
- pyinstaller==5.8.0
- pyinstaller-hooks-contrib==2023.0
- PyJWT==2.6.0
- pyparsing==3.0.9
- pytest==7.4.0
- pytz==2022.7.1
- PyYAML==6.0
- requests==2.31.0
- simplejson==3.19.1
- sqlparse==0.4.3
- tomli==2.0.1
- uritemplate==4.1.1
- urllib3==2.0.3
- whichcraft==0.6.1
- zope.event==4.6
- zope.interface==5.5.2

## Executer le projet

Pour executer le projet il faudra:
- Crer un environnement virtuel via la commande :
```shell
python -m venv my_virtuasl_env
```
- Activer l'environnement virtuel via la commande :
```shell
source my_virtuasl_env/bin/activate
```
- Installer les package qui sont dans les requirements
```shell
pip install -r < requirements
```
- Demarrer le serveur django depuis la racine du projet
```shell
python manage.py runserver
```
## Contribution 
Nous accueillons les contributions de la communauté. Si vous souhaitez contribuer à ce projet, veuillez suivre les directives de la contribution dans le fichier CONTRIBUTING.md

## Licence
C projet est distribué sous la licence
