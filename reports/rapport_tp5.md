# Exercice 1 : 

![Capture API](tp5imgs/Pasted%20image%2020251218082502.png)

![Capture API](tp5imgs/Pasted%20image%2020251218083628.png)

![Capture API](tp5imgs/Pasted%20image%2020251218083640.png)

![Capture API](tp5imgs/Pasted%20image%2020251218083834.png)

![Capture API](tp5imgs/Pasted%20image%2020251218083848.png)

## Question 1.e -
Prometheus utilise `api:8000` car Docker Compose fournit une résolution DNS interne basée sur les noms de services, alors que `localhost` fait référence uniquement au conteneur courant.

# Exercice 2 :
![Capture API](tp5imgs/Pasted%20image%2020251218085519.png)

![Capture API](tp5imgs/Pasted%20image%2020251218085542.png)

![Capture API](tp5imgs/Pasted%20image%2020251218091955.png)

![Capture API](tp5imgs/Pasted%20image%2020251218092053.png)
## Question 2.c -
Un histogramme permet d’observer la distribution complète des latences (percentiles, variations, requêtes lentes), alors qu’une moyenne masque les pics et les cas extrêmes.  
Il est donc plus pertinent pour analyser la qualité de service réelle et détecter des dégradations ponctuelles.
# Exercice 3 :
## Question 3.a -
![Capture API](tp5imgs/Pasted%20image%2020251218092413.png)
![Capture API](tp5imgs/Pasted%20image%2020251218092703.png)

![Capture API](tp5imgs/Pasted%20image%2020251218092832.png)
## Question 3.c -
Cette requête représente la **latence moyenne des requêtes API sur les 5 dernières minutes**, calculée à partir de l’histogramme Prometheus comme le rapport entre la somme des latences observées et le nombre total de requêtes sur la période.

# Exercice 4 :

![Capture API](tp5imgs/Pasted%20image%2020251218093654.png)

![Capture API](tp5imgs/Pasted%20image%2020251218093840.png)

![Capture API](tp5imgs/Pasted%20image%2020251218094758.png)
![Capture API](tp5imgs/Pasted%20image%2020251218094850.png)

![Capture API](tp5imgs/Pasted%20image%2020251218095136.png)
## Question 4.e -
Les métriques affichées permettent de surveiller le volume de requêtes traitées par l’API (RPS) ainsi que la latence moyenne de réponse, ce qui donne une vision du comportement et de la charge du service.  
Elles permettent de détecter des pics de trafic, des ralentissements ou des problèmes de performance côté infrastructure ou application.  
En revanche, ces métriques ne fournissent aucune information sur la qualité fonctionnelle des réponses, comme la pertinence ou l’exactitude des prédictions du modèle.  
Elles ne permettent pas non plus d’identifier la cause métier d’une latence élevée (données d’entrée, modèle, logique interne), mais uniquement son impact global sur le temps de réponse.
# Exercice 5 :
![Capture API](tp5imgs/Pasted%20image%2020251218100120.png)

![Capture API](tp5imgs/Pasted%20image%2020251218100148.png)

## Question 5.c -
Le covariate drift correspond à un changement dans la distribution des variables d’entrée entre la période de référence et la période courante.  
Le target drift correspond à une évolution de la distribution de la variable cible (`churn_label`), indiquant un changement du comportement à prédire.

Décision finale :
NO_ACTION drift_share=0.06 < 0.30 (target_drift=0.0)