# Exercice 1 : 

![Capture API](tp6imgs/Pasted%20image%2020260106232023.png)

![Capture API](tp6imgs/Pasted%20image%2020260106232040.png)

![Capture API](tp6imgs/Pasted%20image%2020260106232110.png)

# Exercice 2 : 

![Capture API](tp6imgs/Pasted%20image%2020260106235325.png)

![Capture API](tp6imgs/Pasted%20image%2020260106235112.png)

Afin de faciliter les tests unitaires, la logique de décision de promotion a été extraite dans une fonction pure (`should_promote`). Cette approche permet de tester le comportement métier de manière isolée, déterministe et rapide, sans dépendre de composants externes tels que Prefect ou MLflow, ce qui améliore la fiabilité, la lisibilité et la maintenabilité des tests.

# Exercice 3 : 

![Capture API](tp6imgs/Pasted%20image%2020260107000501.png)

![Capture API](tp6imgs/Pasted%20image%2020260107000918.png)

L’introduction d’un delta permet d’éviter la promotion de modèles dont l’amélioration de performance est marginale ou due au bruit statistique. Ainsi, seule une amélioration significative des performances justifie un changement de modèle en production.
# Exercice 4 : 

![Capture API](tp6imgs/Pasted%20image%2020260107004201.png)

![Capture API](tp6imgs/Pasted%20image%2020260107004312.png)
# Exercice 5 : 

![Capture API](tp6imgs/Pasted%20image%2020260107004807.png)

L’API charge le modèle depuis MLflow au moment de son démarrage. Lorsqu’une nouvelle version du modèle est promue au stage _Production_, cette mise à jour n’est pas automatiquement reflétée dans un service déjà en cours d’exécution. Il est donc nécessaire de redémarrer l’API afin qu’elle recharge explicitement la dernière version du modèle en production et serve les prédictions avec ce modèle mis à jour.
# Exercice 6 : 

![Capture API](tp6imgs/Pasted%20image%2020260107103247.png)

Le démarrage de la stack Docker Compose dans la CI permet de valider l’intégration entre les différents services (API, base de données, feature store, MLflow) dans un environnement proche de la production. Ce test de bout en bout garantit que l’API démarre correctement et reste fonctionnelle lorsque tous les services dépendants sont actifs.
# Exercice 7 : 

## Question 7.a -
### Mesure du drift et rôle du seuil

Le drift est mesuré à l’aide d’Evidently en comparant la distribution des features entre un mois de référence et un mois courant. Pour chaque variable, un test statistique est appliqué afin de détecter un changement significatif de distribution. Le _drift_share_ correspond à la proportion de variables considérées comme driftées.  
Un seuil de déclenchement est utilisé (0.02) : si le _drift_share_ dépasse ce seuil, un réentraînement est lancé automatiquement. Ce seuil est volontairement bas afin de forcer le comportement de retraining ; en pratique industrielle, il serait plus élevé pour éviter des réentraînements trop fréquents dus à du bruit statistique.

### Comparaison des modèles et décision de promotion

Le flow `train_and_compare_flow` entraîne un modèle candidat sur les données du mois courant, calcule ses métriques de validation (notamment le `val_auc`) et évalue le modèle actuellement en Production sur exactement le même split de données. La décision de promotion repose sur la comparaison suivante : si le `val_auc` du candidat dépasse celui du modèle Production d’au moins un delta fixé, alors le modèle candidat est promu en Production via MLflow Model Registry ; sinon, la promotion est ignorée (_skipped_). Ce mécanisme évite de promouvoir des modèles dont l’amélioration est marginale ou non significative.

### Rôle de Prefect vs GitHub Actions

Prefect est utilisé pour l’orchestration des workflows MLOps : monitoring du drift, entraînement, évaluation, comparaison et promotion des modèles. Il gère la logique métier, les dépendances entre tâches et l’exécution conditionnelle.  
GitHub Actions, quant à lui, est dédié à la CI : il exécute les tests unitaires et des tests d’intégration légers via Docker Compose (healthcheck de l’API). La CI valide la qualité du code et l’intégration des services, mais ne déclenche pas de logique métier lourde comme l’entraînement.

## Question 7.b -

- **Pourquoi la CI n’entraîne pas le modèle complet**  
    L’entraînement est coûteux, long et potentiellement non déterministe (données, ressources). L’exécuter en CI rendrait les pipelines lents, instables et peu reproductibles. La CI doit rester rapide et fiable.
    
- **Tests manquants**  
    Il manque des tests d’intégration plus profonds (ex. test complet du flow Prefect, validation des features Feast...) ainsi que des tests de performance et de robustesse du modèle.
    
- **Nécessité d’une gouvernance humaine**  
    En conditions réelles, une promotion automatique pure est rarement suffisante. Une validation humaine est souvent requise pour vérifier l’impact métier, la conformité réglementaire, l’équité du modèle ou des signaux externes non capturés par les métriques (ex. incidents, changements de contexte). Des étapes d’approbation manuelle ou semi-automatique sont donc généralement intégrées aux pipelines MLOps industriels.