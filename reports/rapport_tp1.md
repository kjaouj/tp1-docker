# Exercice 1 : Installation de Docker et vérification de l’environnement

## Question 1.a - Installation de Docker

Sur ma machine, j’utilise **Docker dans WSL2**.

![[Screenshot 2025-12-05 102910.png]]
---

## Question 1.b - Vérification de l’installation avec `docker run hello-world`

![[Screenshot 2025-12-05 102918.png]]
## Question 1.c - Liste des conteneurs avec `docker ps -a`
![[Screenshot 2025-12-05 103014.png]]

La commande `docker ps -a` affiche :
- les conteneurs **en cours d'exécution**,
- les conteneurs **arrêtés mais toujours existants**,
- leur **ID**, **image utilisée**, **statut**, **heure de création**, et **nom**.
# Exercice 2 :

## Question 2.a - 

- **Une image Docker** est un modèle figé, un *template* contenant un environnement préconfiguré (fichiers, librairies, dépendances).  
  Elle est immuable et sert de base pour créer des conteneurs.

- **Un conteneur Docker** est une instance *vivante* d’une image.  
  C’est l'exécution réelle de cette image : il possède son propre système de fichiers, son état, ses processus.
## Question 2.b -

![[Screenshot 2025-12-05 103228copy.png]]
### Explication de ce qui se passe
- Docker télécharge l’image `alpine` si elle n’est pas déjà présente.
- Il crée un conteneur temporaire basé sur cette image.
- Il exécute immédiatement la commande :
```bash
echo "Bonjour depuis un conteneur Alpine"
```
- Une fois la commande terminée, le conteneur s’arrête automatiquement.

## Question 2.c - 

![[Screenshot 2025-12-05 103228ffs.png]]

On voit un conteneur basé sur l’image **alpine** avec le statut "Exited".
Parce que la commande demandée (`echo ...`) s’est exécutée **puis s’est terminée immédiatement**
Docker ferme automatiquement le conteneur lorsque le processus principal se termine.

## Question 2.d -
![[Screenshot 2025-12-05 103228.png]]
### Observations
- `ls` affiche un système de fichiers très minimaliste propre à Alpine.  
    On voit généralement : `/bin`, `/etc`, `/lib`, `/usr`, `/tmp`, etc.
- `uname -a` montre que l’environnement utilise un noyau Linux fourni par Docker/WSL (et non un vrai noyau Alpine), car les conteneurs partagent le noyau hôte.    
- La commande `exit` ferme le shell et arrête le conteneur, ce qui provoque un statut `Exited`.

# Exercice 3 :

## Question 3.a -

![[Pasted image 20251205115525.png]]
## Question 3.b -

![[Screenshot 2025-12-05 104715.png]]

## Question 3.c -

![[Screenshot 2025-12-05 104635.png]]

# Exercice 4 :

## Question 4.a -

![[Screenshot 2025-12-05 105411.png]]
L’option `-p` réalise un **mapping de port** :
- le premier `8000` = port de la **machine hôte** (Windows/WSL)
- le second `8000` = port du **conteneur** (là où Uvicorn écoute)
## Question 4.b - 4.c - 
![[Screenshot 2025-12-05 105219.png]]

Dans la ligne correspondante, on observe :
- **Nom du conteneur :** nifty_turning
- **Image utilisée :** `simple-api`
- **Port mappé :** `0.0.0.0:8000 -> 8000/tcp`
## Question 4.d -
Différence entre `docker ps` et `docker ps -a`
- `docker ps` affiche uniquement les **conteneurs actifs**
- `docker ps -a` affiche **tous** les conteneurs : actifs + arrêtés

# Exercice 5 :
## Question 5.a -
![[Screenshot 2025-12-05 105839.png]]
## Question 5.b -
![[Screenshot 2025-12-05 110122.png]]

## Question 5.c -
![[Screenshot 2025-12-05 110251.png]]

![[Screenshot 2025-12-05 110259.png]]

![[Screenshot 2025-12-05 110330.png]]

## Question 5.d - 5.e - 
![[Screenshot 2025-12-05 110503.png]]

- **`docker stop`** = arrêter un seul conteneur sans nettoyage.
- **`docker compose down`** = arrêter _toute_ l’application et supprimer tous les conteneurs/ressources liées.

# Exercice 6 :
## Question 6.a -
![[Screenshot 2025-12-05 110803.png]]

![[Screenshot 2025-12-05 110813.png]]

- `exec` : exécuter une commande à l'intérieur d'un conteneur en cours d'exécution.
- `db` : Il s'agit du nom du service dans notre fichier docker-compose.yml.
- `-U` : Cet indicateur indique à PostgreSQL avec quel utilisateur de base de données se connecter.
- `-d` : Ce paramètre indique à PostgreSQL quelle base de données ouvrir.
## Question 6.b -
![[Screenshot 2025-12-05 110850.png]] 

## Question 6.c -
Lorsqu’on utilise **Docker Compose**, tous les services d’un même fichier `docker-compose.yml` partagent **le même réseau interne**, ce qui permet de les connecter simplement à PostgreSQL.
Pour qu’un service se connecte à la base PostgreSQL, il suffit d’utiliser les informations suivantes:
- Hostname : **le nom du service PostgreSQL** dans `docker-compose.yml` (dans ce cas db). Docker crée automatiquement un DNS interne, donc l'API peut se connecter en appelant `db` (pas besoin d'adresse IP).
- Port : 5432 (Le mapping de port vers l’extérieur – `5432:5432` – ne concerne pas les autres services Docker, uniquement l’hôte.)
- Utilisateur et mot de passe : proviennent des variables d’environnement définies dans le service PostgreSQL (test_user, test).
- Nom de la base : testDB (comme defini dans le yml)

## Question 6.d -
![[Screenshot 2025-12-05 111134.png]]

L’option **`-v`** dans `docker compose down -v` supprime **tous les volumes associés aux services** du fichier `docker-compose.yml`.  
Et doncm, **toutes les données persistantes (ex. base de données, fichiers stockés)** sont définitivement effacées.

# Exercice 7 :
## Question 7.a -
![[Screenshot 2025-12-05 111438.png]]
## Question 7.b - 7.c - 
![[Screenshot 2025-12-05 111827.png]]

en lançant `ls` et `python --version`, j’observe :
- un système de fichiers minimal propre au conteneur,
- la présence du fichier `app.py` et des dépendances installées,
- la version de Python correspondant à celle de l’image utilisée (Python 3.11.14).

Un redémarrage est utile lorsque :
- un service plante ou devient instable,
- une mise à jour de configuration a été faite,
- une variable d’environnement a changé,
- le service doit être relancé sans arrêter toute l’application.
Cela permet de relancer uniquement le service concerné sans interrompre les autres.
## Question 7.d -
![[Screenshot 2025-12-05 111940.png]]

![[Screenshot 2025-12-05 112045.png]]

![[Screenshot 2025-12-05 112109.png]]

## Question 7.e -
![[Screenshot 2025-12-05 112300.png]]

Il est utile de nettoyer régulièrement Docker car :
- **les conteneurs arrêtés** et **les images inutilisées** occupent rapidement beaucoup d’espace disque.
- cela évite l’accumulation de ressources obsolètes qui peuvent rendre l’environnement plus lent ou difficile à gérer.
# Exercice 8 :
## Question 8.a -
Un notebook Jupyter n’est généralement **pas adapté** au déploiement d’un modèle de Machine Learning en production pour plusieurs raisons :

1. **Manque de reproductibilité**  
   Le code d’un notebook dépend de l’ordre d’exécution des cellules. Cela peut conduire à des incohérences et rendre difficile la reproduction exacte d’un traitement ou d’un modèle.

2. **Pas d’environnement contrôlé**  
   Les notebooks ne garantissent pas un environnement stable : versions de bibliothèques, packages installés, dépendances… Rien n’est figé.  
   En production, on doit au contraire pouvoir recréer l’environnement **à l’identique**.

3. **Difficulté d’automatisation**  
   Les notebooks ne sont pas pensés pour être exécutés automatiquement dans un pipeline CI/CD ou un service exposé via API.  
   Un code de production doit être scripté, testé et intégré facilement dans une architecture automatisée.
## Question 8.b -

Docker Compose est essentiel lorsqu’on manipule plusieurs services (API, base de données, front-end…) car il permet :

1. **La gestion centralisée de plusieurs conteneurs**  
   Avec un seul fichier `docker-compose.yml`, on peut lancer, arrêter et configurer plusieurs services de manière cohérente.

2. **La création automatique d’un réseau partagé**  
   Les services peuvent communiquer entre eux via des hostnames simples (ex : `db`), sans configuration réseau complexe.

3. **La reproductibilité de l’environnement complet**  
   Docker Compose permet de recréer exactement le même environnement sur n’importe quelle machine : utile pour le travail en groupe, le déploiement ou les TP.

Pendant ce TP, l’avantage le plus visible est la facilité de faire communiquer **l’API FastAPI** avec **la base PostgreSQL** sans aucune configuration réseau manuelle.