# Exercice 1 :
## Question 1.a -
![Capture API](tp2imgs/Screenshot%202025-12-11%20151156.png)
## Question 1.b -
![Capture API](tp2imgs/Screenshot%202025-12-11%20151139.png)

Side note: Ici j'ai fait une faute de frappe et écrit « init » avec deux « n ». Je me suis rendu compte de cette erreur plus tard et je l'ai corrigée.
## Question 1.c -

![Capture API](tp2imgs/Pasted%20image%2020251211165958.png)
# Exercice 2 :
## Question 2.a -
![Capture API](tp2imgs/Pasted%20image%2020251211152755.png)

![Capture API](tp2imgs/Pasted%20image%2020251211152729.png)

## Question 2.b -
![Capture API](tp2imgs/Pasted%20image%2020251211153004.png)

Le fichier _.env_ dans un projet Docker sert à centraliser les variables d’environnement (ports, mots de passe, chemins, configurations…) afin de faciliter la configuration, éviter de modifier directement le _docker-compose.yml_ et simplifier la gestion des paramètres sensibles.

## Question 2.c -
![Capture API](tp2imgs/Pasted%20image%2020251211153620.png)

![Capture API](tp2imgs/Pasted%20image%2020251211153644.png)
## Question 2.d -
![Capture API](tp2imgs/Pasted%20image%2020251211154600.png)

![Capture API](tp2imgs/Pasted%20image%2020251211162005.png)
### **Commentaires sur les tables**

- **labels** : contient les étiquettes / catégories liées aux utilisateurs (par exemple churn / non-churn ou classification utilisée dans l’analyse).
- **payments_agg_90d** : regroupe les données de paiement **agrégées sur les 90 derniers jours** pour chaque utilisateur (montants, fréquence, etc.).
- **subscriptions** : stocke les informations détaillées sur les abonnements des utilisateurs (type d’abonnement, dates de début/fin, statut…).
- **support_agg_90d** : contient les données **agrégées sur 90 jours** concernant les interactions avec le support client (tickets, demandes, réclamations).
- **usage_agg_30d** : rassemble les indicateurs d’utilisation de la plateforme **sur les 30 derniers jours** (fréquence d’usage, volume, activité…).
- **users** : table principale contenant le profil des utilisateurs (identifiants, informations générales, métadonnées associées).

# Exercice 3 :
## Question 3.a -
![Capture API](tp2imgs/Pasted%20image%2020251211163356.png)
![Capture API](tp2imgs/Pasted%20image%2020251211163406.png)

- Le conteneur _prefect_ sert d’orchestrateur du pipeline d’ingestion : il planifie, exécute et supervise les différentes étapes de traitement des données afin d’assurer un flux fiable, automatisé et reproductible entre les services du projet.
## Question 3.b -

La fonction **`upsert_csv`** charge un fichier CSV dans PostgreSQL en appliquant une stratégie d’**upsert** (insert + update). Elle commence par lire le CSV dans un DataFrame Pandas, effectue quelques conversions de types (dates, booléens), puis crée une **table temporaire** dans la base. Les données du CSV sont insérées dans cette table temporaire, avant d’être fusionnées avec la table cible via une requête SQL :  
`INSERT ... ON CONFLICT (...) DO UPDATE`.

En cas de conflit sur la clé primaire, la fonction met simplement à jour les colonnes existantes avec les nouvelles valeurs. Enfin, la table temporaire est supprimée et la fonction retourne le nombre de lignes traitées.
## Question 3.c -
![Capture API](tp2imgs/Pasted%20image%2020251211170709.png)
![Capture API](tp2imgs/Pasted%20image%2020251211170729.png)

# Exercice 4 :
## Question 4.a -

La fonction **`validate_with_ge`** joue le rôle de garde-fou qualité dans le pipeline d’ingestion. Après le chargement des données, elle récupère un extrait de la table depuis PostgreSQL et applique plusieurs **expectations Great Expectations** pour vérifier la structure et la cohérence des données (présence des colonnes attendues, valeurs non nulles, bornes minimales, etc.).

Si une expectation échoue, la fonction déclenche une exception, ce qui **interrompt immédiatement le flow Prefect** pour éviter que des données incorrectes ou corrompues ne soient utilisées dans les étapes suivantes.
## Question 4.b -
![Capture API](tp2imgs/Pasted%20image%2020251211172728.png)
## Question 4.c -
![Capture API](tp2imgs/Pasted%20image%2020251211173026.png)

Les bornes choisies (`>= 0` sur _watch_hours_30d_, _avg_session_mins_7d_, _unique_devices_30d_, _skips_7d_) garantissent que les agrégats d’usage restent cohérents avec la réalité : des heures visionnées, des appareils utilisés ou des sauts de contenu ne peuvent jamais être négatifs.

Ces règles permettent de détecter immédiatement des fichiers corrompus, des erreurs d’ingestion ou des transformations incorrectes avant qu’elles n’atteignent le modèle. Elles protègent donc la qualité des futures features et évitent d’entraîner un modèle sur des données impossibles ou incohérentes, ce qui améliore la fiabilité globale du pipeline.
# Exercice 5 :
## Question 5.a -
`snapshot_month(as_of)` crée une photographie immuable des tables au mois donné : il enregistre l’état exact des données à la date _as_of_, ce qui permet de garder une version stable et reproductible pour l’entraînement et l’évaluation futurs du modèle.
## Question 5.b -
![Capture API](tp2imgs/Pasted%20image%2020251211174151.png)

![Capture API](tp2imgs/Pasted%20image%2020251211174206.png)

- Les snapshots du 31/01/2024 et du 29/02/2024 n’ont pas le même nombre de lignes. Le premier snapshot contient 0 lignes car la table `subscriptions` ne contenait aucune donnée lors de l’ingestion du mois _month_000_. Le second snapshot contient 7043 lignes car les données du mois _month_001_ étaient présentes au moment de l’ingestion.
## Question 5.c -
### Diagramme du pipeline d’ingestion
```
     +---------------------+
     |   CSV Seeds (mois)  |
     +----------+----------+
                |
                v
    +------------------------+
    |   upsert_csv (6 tables)|
    +-----------+------------+
                |
                v
   +-------------------------+
   | Great Expectations (GE) |
   | validate_with_ge        |
   +-----------+-------------+
                |
                v
   +-------------------------+
   |   snapshot_month(as_of) |
   +-----------+-------------+
                |
                v
   +-------------------------+
   |  *_snapshots tables     |
   |  (figées par mois)      |
   +-------------------------+
```

### Pourquoi ne pas entraîner un modèle directement sur les tables live ?
On n’utilise pas les tables live car elles changent en continu : les valeurs peuvent être mises à jour, corrigées ou modifiées d’un jour à l’autre. Entraîner un modèle dessus introduirait une forte instabilité et rendrait les résultats impossibles à reproduire.  
De plus, certaines colonnes live contiennent des informations futures (postérieures au mois d’étude), ce qui introduirait du **data leakage**.

### Pourquoi les snapshots sont essentiels pour éviter le data leakage et garantir la reproductibilité ?
Les snapshots permettent de figer l’état exact des données **au moment où l’on souhaite entraîner un modèle**, en ajoutant un champ `as_of` qui représente la date d’observation.  
Cela garantit :

- qu’aucune information future n’est utilisée (pas de data leakage) ;
- que l’on peut reconstruire exactement les mêmes features plus tard ;
- que les performances du modèle sont comparables dans le temps car les données d’origine ne changent plus.
Les snapshots forment donc une base d’apprentissage stable, cohérente et reproductible.
