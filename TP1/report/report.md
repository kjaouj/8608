# Exercice 1 :
```
Name : Kjaouj Aymane
Github link : https://github.com/kjaouj/8608
Execution : Tout est fait sur ma machine locale
```

N.B. : concernant le fichier requirements.txt, il contient de nombreuses dépendances, même celles qui ne sont pas nécessaires pour ce TP. Ceci est dû au fait que j'ai choisi de réutiliser un environnement conda existant qui disposait déjà de toutes les dépendances nécessaires.

![Capture API](img/Pasted%20image%2020260123140429.png)

![Capture API](img/Pasted%20image%2020260123101149.png)

![Capture API](img/Pasted%20image%2020260123105517.png)

![Capture API](img/Pasted%20image%2020260123105548.png)

![Capture API](img/Pasted%20image%2020260123105612.png)

# Exercice 2 :

![Capture API](img/Pasted%20image%2020260123105854.png)

#### **matthew-ball-2L11W39hDYo-unsplash.jpg**
**Cas simple** : image contenant un objet principal bien centré (plante en pot) sur un fond uniforme et peu chargé, avec un bon contraste global, ce qui facilite une segmentation stable et précise.
#### **andrew-resheto-v-f8tr3MJzhc-unsplash.jpg**
**Cas simple** : un seul objet clairement identifiable (plante) avec des contours relativement nets et peu d’éléments perturbateurs en arrière-plan, servant de référence pour évaluer les performances de base du modèle.
#### **chromatograph-R-xqhYJ4ZKs-unsplash.jpg**
**Cas chargé** : scène intérieure complexe contenant de nombreux objets, des textures variées et des zones partiellement occluses, ce qui permet d’évaluer la capacité du modèle à séparer plusieurs instances dans un environnement dense.
####  **jorge-franganillo-QUoMZNWcMI-unsplash.jpg**
**Cas chargé** : scène de marché avec une forte densité d’objets, des couleurs variées et un arrière-plan très structuré, rendant la délimitation des objets individuels plus difficile pour la segmentation automatique.
####  **moritz-kindler-F9O1b2i8BVo-unsplash.jpg**
**Cas difficile** : présence d’un objet transparent et réfléchissant (sphère en verre) déformant l’arrière-plan, introduisant des ambiguïtés visuelles importantes (reflets, frontières floues, mélange objet/fond).
### Cas simple : 
![Capture API](img/matthew-ball-2L11W39hDYo-unsplash.jpg)
### Cas complexe :

![Capture API](img/moritz-kindler-F9O1b2i8BVo-unsplash.jpg)

# Exercice 3 :

![Capture API](img/Pasted%20image%2020260123111554.png)

![Capture API](img/Pasted%20image%2020260123112811.png)

Le modèle de segmentation utilisé est **Segment Anything Model (SAM) – ViT-H**, avec le checkpoint **`sam_vit_h_4b8939.pth`**

```
- image : `(5472, 3648, 3)`,
- masque : `(5472, 3648)`,
- score de confiance : `0.85`.
```

Le chargement du modèle et l’inférence fonctionnent correctement sur GPU. La segmentation est valide et le score obtenu est raisonnable, indiquant une bonne correspondance entre la bounding box fournie et l’objet segmenté. En revanche, le modèle ViT-H reste relativement coûteux en calcul, ce qui peut entraîner une latence perceptible pour des images de grande résolution, soulignant l’intérêt éventuel de modèles plus légers ou d’une réduction de la taille des images.
# Exercice 4 :

![Capture API](img/Pasted%20image%2020260123122840.png)
![Capture API](img/Pasted%20image%2020260123122827.png)

| Image | Score | Area (pixels) | Perimeter (pixels) |
|------|------:|--------------:|-------------------:|
| stephanie-harvey-T0inbt7nRME-unsplash.jpg | 0.955 | 1 819 244 | 12 313.35 |
| matthew-ball-2L11W39hDYo-unsplash.jpg | 0.979 | 6 240 048 | 10 185.95 |
| jonathan-borba-af7c0GwLsGU-unsplash.jpg | 0.921 | 1 706 161 | 15 396.56 |
L'overlay est particulièrement utile pour le débogage du comportement du modèle et de la définition du prompt. Elle permet de vérifier immédiatement que le cadre de délimitation couvre correctement l'objet cible et n'inclut pas d'arrière-plan excessif. Dans les cas simples, la superposition affiche un alignement précis entre le masque et les contours de l'objet, confirmant ainsi une segmentation stable. Dans les cas plus complexes, comme pour les objets aux structures fines ou proches de l'arrière-plan, la superposition révèle des fuites de masque ou des zones manquantes qui ne sont pas visibles à partir du seul score. Ce retour visuel aide à déterminer si les erreurs proviennent d'un cadre de délimitation imprécis, des limitations du modèle ou des caractéristiques de l'image. En définitive, la superposition est un outil essentiel pour comprendre la qualité de la segmentation au-delà des simples mesures numériques.

# Exercice 5 :

![Capture API](img/Pasted%20image%2020260123124344.png)

![Capture API](img/Pasted%20image%2020260123124458.png)

![Capture API](img/Pasted%20image%2020260123124423.png)

### Image 2 : 
![Capture API](img/Pasted%20image%2020260123124951.png)

![Capture API](img/Pasted%20image%2020260123124938.png)
![Capture API](img/Pasted%20image%2020260123125007.png)

### Image 3 : 
![Capture API](img/Pasted%20image%2020260123124828.png)

## Question 5.c -
![Capture API](img/Pasted%20image%2020260123130028.png)

## Question 5.d -
![Capture API](img/Pasted%20image%2020260123131311.png)
![Capture API](img/Pasted%20image%2020260123131258.png)

![Capture API](img/Pasted%20image%2020260123131500.png)
![Capture API](img/Pasted%20image%2020260123131429.png)

![Capture API](img/Pasted%20image%2020260123131637.png)![Capture API](img/Pasted%20image%2020260123131646.png)

| Image (case)                       | Score | Area (px) | Perimeter (px) | Time (ms) | bbox(x1, y1, x2, y2)   |
| ---------------------------------- | ----- | --------- | -------------- | --------- | ---------------------- |
| lye-clicks-9jXJluGUhew-unsplash    | 1.004 | 8,523,577 | 11,709.37      | 1,460.5   | (4797, 94, 7546, 3920) |
| raul-angel-QLhbqCx_YdM-unsplash    | 0.991 | 2,102,132 | 6,400.81       | 151.4     | (421, 991, 2294, 2994) |
| chromatograph-R-xqhYU4ZKs-unsplash | 0.621 | 1,557,105 | 33,521.77      | 1,880.3   | (0, 417, 4200, 2354)   |
Lorsque le bounding box  est trop petite, SAM risque de ne segmenter qu'une partie de l'objet ou d'omettre des zones importantes, ce qui entraîne des masques incomplets et des scores instables. En agrandissant la boîte englobante, le modèle dispose de plus de contexte et produit généralement des segmentations plus complètes, mais peut également inclure des zones d'arrière-plan, notamment dans les scènes complexes. Des boîtes très grandes ont tendance à accroître l'ambiguïté et peuvent provoquer des débordements de masque sur les objets voisins. L'aperçu en direct de la boîte englobante permet de détecter ces problèmes avant la segmentation. Ajuster la taille de la boîte englobante est donc un outil de débogage essentiel pour trouver le bon équilibre entre exhaustivité et précision de la segmentation.

# Exercice 6 :

### **BBox only** : 

![Capture API](img/Pasted%20image%2020260123135620.png)
![Capture API](img/Pasted%20image%2020260123135607.png)
### **BBox + 1 FG point** : 

![Capture API](img/Pasted%20image%2020260123135535.png)
![Capture API](img/Pasted%20image%2020260123135523.png)
![Capture API](img/Pasted%20image%2020260123135459.png)

### **BBox + FG + 1 BG point** : 

![Capture API](img/Pasted%20image%2020260123135857.png)

![Capture API](img/Pasted%20image%2020260123135912.png)
![Capture API](img/Pasted%20image%2020260123135920.png)

Sur les images complexes où la boîte englobante contient plusieurs objets ou un arrière-plan complexe, l'utilisation d'une simple boîte englobante conduit souvent à des masques ambigus ou incorrects. L'ajout d'un point de premier plan (FG) guide efficacement SAM vers l'objet ciblé et améliore considérablement la qualité de la segmentation. En cas de fuite d'arrière-plan persistante, l'ajout d'un point d'arrière-plan (BG) permet au modèle d'exclure explicitement les zones indésirables. La sortie multimasque facilite également le choix en proposant des candidats alternatifs, permettant ainsi à l'utilisateur de sélectionner le masque le plus cohérent. En définitive, le guidage par points accroît considérablement la robustesse et la précision du contrôle dans les scènes complexes.
# Exercice 7 :

## Question 7.a -
>Lors de mes essais, la segmentation échoue principalement dans trois cas.  
>Premièrement, lorsque la bounding box contient plusieurs objets ou un fond très complexe, SAM produit un masque plausible mais ambigu, qui ne correspond pas toujours à l’objet ciblé. Une action efficace consiste à ajouter des points de guidage foreground (FG) et background (BG) afin de contraindre explicitement la sélection.  
>Deuxièmement, les objets fins, transparents ou partiellement occultés (verre, reflets, câbles) sont souvent mal segmentés, car leurs contours sont peu contrastés. Cela peut être amélioré par un raffinement interactif via plusieurs points FG et par un post-traitement morphologique des masques.  
>Enfin, des bounding boxes trop larges ou mal positionnées augmentent l’ambiguïté. L’ajout de contraintes UI (alerte bbox trop grande/petite, prévisualisation) et, à plus long terme, l’utilisation d’un dataset métier dédié permettraient de renforcer la robustesse globale du pipeline.

---
## Question 7.b -

> Pour industrialiser cette brique de segmentation, plusieurs signaux clés doivent être loggés et monitorés.  
> En priorité, le **score de confiance des masques** permet de détecter des prédictions anormalement faibles ou instables. Le **temps d’inférence** est essentiel pour identifier des régressions de performance ou des problèmes de charge GPU.  
> La **surface du masque** et son **ratio par rapport à la bbox** permettent de détecter des dérives (masques trop grands ou trop petits). Le **nombre de points FG/BG utilisés** renseigne sur la difficulté des images et l’effort utilisateur.  
> Enfin, le **taux de sélection du premier masque multimask** est un bon indicateur de qualité intrinsèque du modèle. Ensemble, ces métriques permettent d’anticiper le drift des données, les régressions modèles et les problèmes d’ergonomie UI.

---