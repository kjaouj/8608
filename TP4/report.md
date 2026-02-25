# Exercice 1 :
![Capture API](imgs/Pasted%20image%2020260222235859.png)

![Capture API](imgs/Pasted%20image%2020260223000941.png)

# Exercice 2 :
## Question 2.g - 
On sépare les métriques car **chaque masque correspond à un usage différent**.  
Sur `train_mask`, on mesure si le modèle **apprend effectivement** (et on détecte vite un bug ou une sous-capacité).  
Sur `val_mask`, on estime la performance sur des données **non vues pendant l’optimisation**, et on s’en sert pour **choisir les hyperparamètres / stopper** sans “tricher”.  
Sur `test_mask`, on fait une **évaluation finale** uniquement à la fin : c’est la mesure la plus “objective” de la généralisation.  
Comparer train vs val/test permet aussi de diagnostiquer **overfitting** (train haut, val/test bas) ou **underfitting** (tout bas).

## Question 2.h - 

![Capture API](imgs/Pasted%20image%2020260223001913.png)Le modèle atteint 100% sur train mais ~57% sur test → forte généralisation limitée (overfitting), ce qui confirme que l’info de graphe manque dans la baseline MLP.

# Exercice 3 :
![Capture API](imgs/Pasted%20image%2020260223003107.png)

| Modèle | test_acc   | test_f1    | total_train_time_s |
| ------ | ---------- | ---------- | ------------------ |
| MLP    | **0.5740** | **0.5619** | **0.7497 s**       |
| GCN    | **0.8100** | **0.8026** | **0.8661 s**       |
## Question 3.f - 
Sur Cora, le MLP utilise uniquement les features des nœuds, donc il ignore complètement la structure de citations entre articles.  
Le GCN, lui, exploite `edge_index` pour agréger l’information des voisins : chaque nœud incorpore un **contexte local** issu du graphe.  
Comme Cora présente une **forte homophilie** (les articles liés appartiennent souvent au même domaine), cette propagation fournit un signal très informatif pour la classification.  
On observe donc une meilleure généralisation : le MLP atteint 100% sur train mais reste autour de 57% sur test, alors que le GCN monte à ~81%, preuve que le graphe apporte une information supplémentaire.  
Le coût computationnel est légèrement plus élevé car chaque couche fait une opération de message passing, mais reste faible sur un graphe de taille Cora.  
Le gain pourrait être moindre si les features étaient déjà parfaitement discriminantes ou si le graphe était bruité ou hétérophile.

# Note
>À partir de l’Exercice 4, l’entraînement avec **NeighborLoader** nécessitait les dépendances PyG natives (`pyg-lib` / `torch-sparse`).  
Malgré plusieurs tentatives d’installation, des incompatibilités de versions entre **PyTorch, CUDA et PyG** ont provoqué des erreurs d’import et de compilation (notamment `NeighborSampler requires pyg-lib or torch-sparse` et erreurs de symboles).

>Afin de garantir la reproductibilité et de poursuivre l’expérimentation sans bloquer le TP, l’exécution a été basculée en **mode CPU** avec un environnement PyTorch compatible.

>Ce changement n’affecte pas la validité de la comparaison entre modèles (les métriques de qualité restent identiques), mais peut influencer :
- les temps d’entraînement
- la latence d’inférence
>Les résultats doivent donc être interprétés comme des **mesures CPU**, cohérentes entre modèles mais non directement comparables à un benchmark GPU.
# Exercice 4 :
```
- **batch_size** : 250
- **num_neighbors** : [10, 10]
```

![Capture API](imgs/Pasted%20image%2020260225131323.png)

| Modèle                   | Test Accuracy | Test F1   | Temps entraînement total (s) | Type entraînement            |
| ------------------------ | ------------- | --------- | ---------------------------- | ---------------------------- |
| **MLP**                  | **0.574**     | **0.562** | **0.750**                    | Full-batch (sans graphe)     |
| **GCN**                  | **0.810**     | **0.803** | **0.866**                    | Full-batch graphe            |
| **GraphSAGE (sampling)** | **0.800**     | **0.790** | **0.482**                    | Mini-batch neighbor sampling |
## Question 4.f - 

Le _neighbor sampling_ accélère l’entraînement des GNN en limitant le nombre de voisins explorés à chaque couche (fanout). Au lieu de propager l’information sur tout le graphe, le modèle travaille sur des sous-graphes locaux, ce qui réduit fortement la mémoire GPU et le temps de calcul, surtout sur les grands graphes. Cette approche permet donc un apprentissage en mini-batch, impossible en full-batch pour des graphes massifs.

Cependant, ce gain de vitesse introduit une approximation du gradient, car tous les voisins ne sont pas pris en compte. Cela augmente la variance du gradient et peut légèrement dégrader la performance finale, comme on l’observe souvent avec une accuracy un peu inférieure à celle d’un GCN full-batch. Les nœuds à fort degré (hubs) sont particulièrement sensibles : un fanout trop faible peut perdre de l’information importante.

Enfin, le sampling lui-même a un coût CPU non négligeable (construction des sous-graphes), ce qui crée un compromis global : plus le fanout est élevé, plus la performance se rapproche du full-batch, mais plus le coût mémoire et temps augmente.

# Exercice 5 :
## Question 5.d - 
**-> MLP**
```
model: mlp
device: cpu
avg_forward_ms: 0.8737
num_nodes: 2708
ms_per_node_approx: 0.00032262
```
**-> GCN** 
```
model: gcn
device: cpu
avg_forward_ms: 2.6765
num_nodes: 2708
ms_per_node_approx: 0.00098837
```
**-> GraphSage**
```
model: sage
device: cpu
avg_forward_ms: 11.8351
num_nodes: 2708
ms_per_node_approx: 0.00437042
```

| Modèle                   | test_acc | test_f1 (macro) | total_train_time_s | avg_forward_ms (CPU) |
| ------------------------ | -------: | --------------: | -----------------: | -------------------: |
| **MLP**                  |   0.5740 |          0.5619 |             0.7497 |               0.8737 |
| **GCN**                  |   0.8100 |          0.8026 |             0.8661 |               2.6765 |
| **GraphSAGE (sampling)** |   0.8000 |          0.7895 |             0.4820 |              11.8351 |
## Question 5.e - 
On fait un **warmup** parce que les premières itérations ne représentent pas le régime “stable” : elles déclenchent souvent des surcoûts (allocation mémoire, initialisation de kernels, mise en cache, compilation/optimisations internes). Sans warmup, la moyenne serait biaisée vers le haut et peu reproductible.  
Sur GPU, l’exécution est **asynchrone** : quand tu lances un forward, Python peut reprendre la main avant que le GPU ait réellement fini le calcul. Du coup, si tu mesures juste avec un timer CPU, tu risques de chronométrer seulement l’“envoi” de la tâche au GPU, pas le calcul.  
C’est pour ça qu’on appelle `torch.cuda.synchronize()` **avant** (pour être sûr qu’il n’y a pas de travail en attente) et **après** (pour être sûr que le forward est terminé) la section chronométrée. Ça garantit que le temps mesuré correspond bien au calcul forward.  
Même sur CPU (comme tes résultats), le warmup reste utile car il stabilise caches et allocations, et rend les mesures plus comparables entre modèles.

# Exercice 6 :
## Question 6.a -
| Modèle        | test_acc | test_macro_f1 | total_train_time_s | train_loop_time | avg_forward_ms |
| ------------- | -------: | ------------: | -----------------: | --------------: | -------------: |
| **MLP**       |   0.5740 |        0.5619 |             0.7497 |          2.1177 |         0.8737 |
| **GCN**       |   0.8100 |        0.8026 |             0.8661 |          2.3780 |         2.6765 |
| **GraphSAGE** |   0.8000 |        0.7895 |             0.4820 |          1.1026 |        11.8351 |


Les résultats montrent un compromis clair entre **qualité prédictive** et **coût computationnel**.  
Le **MLP** est le plus rapide en inférence mais ses performances sont nettement inférieures car il n’exploite pas la structure du graphe.  
Le **GCN** obtient la meilleure qualité (accuracy et F1) au prix d’un coût d’inférence plus élevé que le MLP, mais reste raisonnable.  
Le **GraphSAGE** atteint une qualité proche du GCN tout en étant plus rapide à entraîner grâce au sampling, mais son inference full-batch est la plus lente sur CPU.  
Globalement, les modèles graphes apportent un gain significatif de qualité, justifiant leur coût supplémentaire.
## Question 6.c -
Au vu des mesures, le choix du modèle dépend principalement de la contrainte opérationnelle.  
Si la priorité est la **qualité prédictive**, le **GCN** est le meilleur choix avec une accuracy d’environ **0.81** et un macro-F1 de **0.80**, tout en conservant un temps d’entraînement raisonnable (~0.87 s).  
Si la contrainte principale est la **latence d’inférence**, par exemple pour un service temps réel, le **MLP** est le plus adapté avec seulement **0.87 ms** par forward, mais au prix d’une baisse importante de performance (~0.57 accuracy).  
Le **GraphSAGE** constitue un bon compromis dans des scénarios à **grands graphes** ou en production distribuée : son entraînement mini-batch est le plus rapide (~0.48 s) et sa qualité reste proche du GCN (~0.80 accuracy).  
Ainsi, pour un système offline ou analytique je recommanderais le GCN, tandis que pour un système à forte contrainte de latence le MLP serait préférable.  
Pour des graphes très volumineux où la scalabilité prime, GraphSAGE devient le choix le plus pertinent.
## Question 6.d -
Un risque majeur dans ce TP est la **non-comparabilité des conditions expérimentales**.  
Par exemple, mesurer la latence sur CPU alors que certains modèles sont optimisés pour GPU peut biaiser les conclusions.  
De même, l’absence de contrôle strict de la **seed** peut introduire de la variance dans les métriques de qualité, rendant la comparaison instable.  
Un autre risque est le **data leakage** si les masques train/val/test étaient modifiés ou mal utilisés.  
Enfin, les mesures de temps peuvent être faussées sans warmup ou synchronisation, surtout sur GPU.  
Dans un vrai projet, on éviterait ces biais en fixant les seeds, en exécutant plusieurs runs avec moyenne et écart-type, et en mesurant tous les modèles dans exactement le même environnement matériel.
## Question 6.e -
Le dépôt contient uniquement le code source, les fichiers de configuration et le rapport. Aucun fichier volumineux (datasets, checkpoints ou logs) n’a été versionné afin de respecter les bonnes pratiques de gestion de dépôt.