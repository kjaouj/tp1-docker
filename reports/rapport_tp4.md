# Exercice 1 : 
![Capture API](tp4imgs/Pasted%20image%2020251217104138.png)

![Capture API](tp4imgs/Pasted%20image%2020251217104941.png)

![Capture API](tp4imgs/Pasted%20image%2020251217105213.png)

La stack Docker fait tourner **PostgreSQL** pour le stockage des données et labels, **Feast** pour la gestion des features online et historiques, **MLflow** pour la traçabilité des entraînements et la gestion des modèles, et une **API FastAPI** pour exposer des endpoints de vérification et de prédiction.  
Ensemble, ces composants permettent un pipeline MLOps reproductible allant des données jusqu’au serving du modèle.

# Exercice 2 : 

![Capture API](tp4imgs/Pasted%20image%2020251217110808.png)
## Question 2.c -
L’entraînement a été réalisé avec la valeur **AS_OF = 2024-01-31**.  
Le dataset d’entraînement, après jointure entre les features Feast et les labels, contient **7043 lignes**.  
La seule colonne catégorielle détectée automatiquement est **`net_service`**.  
Les métriques obtenues sur le jeu de validation sont les suivantes : **AUC = 0.8227**, **F1-score = 0.5159** et **Accuracy = 0.7836**.  
Le temps d’entraînement du modèle RandomForest est journalisé dans MLflow via la métrique `train_time_sec`.

## Question 2.d -

Fixer la valeur de **AS_OF** permet de garantir la reproductibilité temporelle du pipeline d’entraînement. En effet, les features et les labels sont dépendants du temps : sans une date de référence fixe, le dataset d’entraînement évoluerait à chaque exécution en fonction des nouvelles données disponibles, rendant les résultats non comparables.  
De même, fixer le **random_state** permet de rendre déterministes les opérations stochastiques du pipeline, notamment la séparation train/validation et l’apprentissage du modèle RandomForest. Sans cela, deux exécutions sur les mêmes données pourraient produire des métriques différentes.  
Ensemble, `AS_OF` et `random_state` garantissent que l’entraînement est entièrement reproductible, condition indispensable pour comparer des modèles, analyser leur performance dans le temps et assurer une traçabilité fiable en production.

# Exercice 3 : 

![Capture API](tp4imgs/Pasted%20image%2020251217112056.png)

![Capture API](tp4imgs/Pasted%20image%2020251217112319.png)

![Capture API](tp4imgs/Pasted%20image%2020251217111738.png)

![Capture API](tp4imgs/Pasted%20image%2020251217112920.png)

![Capture API](tp4imgs/Pasted%20image%2020251217113001.png)
## Question 3.g -

La promotion d’un modèle via le **Model Registry** et ses stages (None, Staging, Production) permet de dissocier l’entraînement du déploiement. Le changement de stage ne nécessite ni modification de code ni redéploiement manuel, ce qui réduit fortement les risques d’erreur.  
Cette approche garantit qu’un **unique modèle de référence** est utilisé en production, identifié de manière explicite et traçable. Elle permet également de conserver l’historique des versions, de comparer les performances et de revenir facilement à une version précédente en cas de problème.  
À l’inverse, un déploiement basé sur des fichiers locaux ou des chemins d’artefacts rend la traçabilité fragile et complique la gestion des versions dans un contexte MLOps.

# Exercice 4 :
![Capture API](tp4imgs/Pasted%20image%2020251217114033.png)

![Capture API](tp4imgs/Pasted%20image%2020251217114018.png)

![Capture API](tp4imgs/Pasted%20image%2020251217114001.png)

![Capture API](tp4imgs/Pasted%20image%2020251217114109.png)

![Capture API](tp4imgs/Pasted%20image%2020251217114534.png)
![Capture API](tp4imgs/Pasted%20image%2020251217114614.png)

## Question 4.g -
Charger le modèle via `models:/streamflow_churn/Production` permet à l’API de toujours utiliser la version officiellement validée pour la production, sans dépendre d’un chemin local ou d’un artefact spécifique à un run.  
Cette approche découple complètement l’entraînement du serving : une nouvelle version du modèle peut être promue ou rétrogradée via le Model Registry sans modifier le code de l’API ni redéployer le service.  
Elle garantit également la traçabilité, la gestion des versions et la possibilité de rollback, ce qui serait difficile voire impossible avec un chargement manuel basé sur des fichiers locaux.

# Exercice 5 :

## Question 5.a -
```
curl -X 'POST' \
  'http://localhost:8000/predict' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "user_id": "3413-BMNZE"
}'
```

```
{
  "user_id": "3413-BMNZE",
  "prediction": 0,
  "features_used": {
    "paperless_billing": false,
    "monthly_fee": 45.25,
    "plan_stream_movies": false,
    "plan_stream_tv": false,
    "months_active": 1,
    "net_service": "DSL",
    "avg_session_mins_7d": 29.14104461669922,
    "watch_hours_30d": 32.09199142456055,
    "rebuffer_events_7d": 3,
    "unique_devices_30d": 3,
    "skips_7d": 6,
    "failed_payments_90d": 0,
    "ticket_avg_resolution_hrs_90d": 5.800000190734863,
    "support_tickets_90d": 0
  }
}
```
## Question 5.b -
![Capture API](tp4imgs/Pasted%20image%2020251217115112.png)

## Question 5.c -
En phase de serving, de nombreuses erreurs proviennent non pas du modèle lui-même mais des **features utilisées pour la prédiction**. Un premier cas d’échec fréquent est l’**absence de l’entité demandée** : si le `user_id` n’existe pas dans l’online store Feast, les features retournées sont nulles ou incomplètes, rendant la prédiction impossible. Un second cas courant est un **online store incomplet ou obsolète**, par exemple lorsque la matérialisation des features n’a pas été exécutée ou n’est plus à jour, ce qui se traduit également par des valeurs manquantes côté API. Ces problèmes peuvent être détectés tôt grâce à des **sanity checks simples au niveau de l’API**, comme la vérification de la présence de valeurs nulles et le retour d’erreurs explicites (`missing_features`), permettant d’éviter des prédictions silencieusement incorrectes en production.

# Exercice 6 :

## Question 6.a -

MLflow garantit la **traçabilité des entraînements** en enregistrant pour chaque run les paramètres, les métriques, les artefacts et la version du code associée, ce qui permet de comprendre précisément comment un modèle a été produit.  
Il assure également une **identification claire des modèles servis** grâce au Model Registry, où chaque version de modèle est nommée, versionnée et associée à un stage explicite. Cela permet de relier sans ambiguïté une prédiction en production à un entraînement donné et à ses résultats.
## Question 6.b -

Le stage **Production** désigne la version du modèle considérée comme valide pour être utilisée en environnement opérationnel. Au démarrage, l’API charge automatiquement le modèle pointant vers `models:/streamflow_churn/Production`, indépendamment de son numéro de version.  
Cela permet de changer le modèle servi simplement en modifiant son stage dans MLflow, sans toucher au code de l’API ni redéployer le service. En contrepartie, seules les versions explicitement promues en Production peuvent être utilisées, ce qui empêche le serving accidentel de modèles non validés.
## Question 6.c -

Malgré l’utilisation de MLflow, la reproductibilité peut encore être compromise à plusieurs niveaux. 
Premièrement, les **données** peuvent évoluer : une modification des tables sources, des labels ou une matérialisation Feast différente peut produire un dataset distinct même avec le même code.  
Deuxièmement, la **configuration et l’environnement** peuvent varier, par exemple une version différente de Python, de scikit-learn ou des dépendances système, entraînant des résultats légèrement différents.  
Enfin, la reproductibilité peut casser si certains éléments du pipeline ne sont pas figés, comme des paramètres aléatoires non contrôlés, des variables d’environnement implicites ou des chemins de configuration externes non versionnés.