# Contexte 
# Mise en place de Feast 

![Capture API](tp3imgs/Pasted%20image%2020251212091128.png)

![Capture API](tp3imgs/Pasted%20image%2020251212092718.png)
```
docker compose up -d --build
```
Cette commande permet de construire les images Docker si nécessaire (`--build`) et de démarrer l’ensemble des services (Postgres, Prefect et Feast) en arrière-plan (`-d`).

### Rôle du conteneur `feast`

Le conteneur `feast` héberge le **Feature Store Feast**, qui centralise la définition, le stockage et la gestion des features utilisées par les modèles de machine learning.  
La configuration du Feature Store (fichiers `feature_store.yaml`, définitions des entities, feature views, etc.) se trouve dans le dossier monté `/repo`, provenant de `./services/feast_repo/repo` sur la machine hôte.

Feast sera utilisé en exécutant des commandes directement dans le conteneur, par exemple :
```
docker compose exec feast feast apply
docker compose exec feast feast materialize-incremental $(date +%Y-%m-%d)
```
Ces commandes permettent respectivement d’appliquer la configuration du Feature Store et de matérialiser les features dans la base de données Postgres.
# Définition du Feature Store 
## Question 3.a -
![Capture API](tp3imgs/Pasted%20image%2020251212101642.png)

Une Entity dans Feast représente un objet métier central auquel les features sont associées. Elle permet de définir une clé de jointure commune entre différentes sources de données afin de garantir la cohérence des features lors de l’entraînement et de l’inférence des modèles.

Dans notre cas, l’entité _user_ représente un utilisateur de StreamFlow. Le champ `user_id` constitue une clé de jointure pertinente car il identifie de manière unique chaque utilisateur et est présent dans l’ensemble des jeux de données décrivant son comportement (historique d’activité, consommation, interactions). Cela permet d’agréger et de récupérer les features utilisateur de façon fiable et cohérente.
## Question 3.b -

Les données utilisées par le Feature Store proviennent de tables de snapshots mensuels stockées dans PostgreSQL. Par exemple, la table `usage_agg_30d_snapshots` contient des agrégations d’usage utilisateur sur une fenêtre glissante de 30 jours.

Elle inclut notamment les colonnes `watch_hours_30d`, `sessions_count_30d` et `active_days_30d`, qui décrivent l’intensité et la régularité d’utilisation de la plateforme par chaque utilisateur. Ces données sont historisées via la colonne `as_of`, utilisée par Feast comme référence temporelle pour garantir la cohérence entre entraînement et inférence.

## Question 3.c -
![Capture API](tp3imgs/Pasted%20image%2020251212104602.png)

* La commande `feast apply` permet de valider et d’enregistrer la définition du Feature Store (entités, sources de données et FeatureViews) dans le registre Feast. Elle synchronise la configuration déclarative avec l’infrastructure sous-jacente afin de rendre les features disponibles de manière cohérente pour l’entraînement et l’inférence des modèles.
# Récupération offline & online 
![Capture API](tp3imgs/Pasted%20image%2020251212111332.png)
![Capture API](tp3imgs/Pasted%20image%2020251212111458.png)
## Question 4.d - 
Feast garantit la _point-in-time correctness_ en utilisant le champ `timestamp_field="as_of"` défini dans les DataSources comme référence temporelle des features. Lors de la récupération offline, les features sont jointes à l’`entity_df` en respectant la date `event_timestamp` associée à chaque `user_id`, ce qui assure que seules les valeurs disponibles à cette date sont utilisées et évite toute fuite de données futures.

## Question 4.e - 

![Capture API](tp3imgs/Pasted%20image%2020251212112510.png)
## Question 4.f - 

![Capture API](tp3imgs/Pasted%20image%2020251212120613.png)
## Question 4.g - 

```python
{
  'user_id': ['3413-BMNZE'],
  'monthly_fee': [45.25],
  'paperless_billing': [False],
  'months_active': [1]
}
```

Lorsqu’un `user_id` ne possède pas de features matérialisées (par exemple s’il n’existe pas ou s’il est en dehors de la fenêtre de matérialisation), Feast retourne des valeurs nulles ou absentes pour les features demandées. Cela permet d’éviter toute fuite de données et garantit que seules les informations effectivement disponibles dans l’Online Store sont utilisées lors de l’inférence.

## Question 4.h - 
![Capture API](tp3imgs/Pasted%20image%2020251212121436.png)
## Question 4.i - 4.j -
![Capture API](tp3imgs/Pasted%20image%2020251212122927.png)
# Réflexion

L’endpoint `/features/{user_id}` permet de servir en production exactement les mêmes features que celles utilisées lors de l’entraînement des modèles, car elles sont définies et gérées de manière centralisée dans Feast. Cette unification entre offline et online garantit la cohérence des calculs de features et évite les divergences de logique ou de données entre entraînement et inférence. Ainsi, le _training-serving skew_ est réduit, ce qui améliore la fiabilité et la stabilité des prédictions en production.
