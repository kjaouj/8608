# Exercice 1 :

![Capture API](imgs/Pasted%20image%2020260219131534.png)
# Exercice 2 :

![Capture API](imgs/Pasted%20image%2020260222134203.png)
![Capture API](imgs/Pasted%20image%2020260222134213.png)
```
ffmpeg -i TP3/data/call_01.wav -ac 1 -ar 16000 TP3/data/call_01_16k.wav
```

![Capture API](imgs/Pasted%20image%2020260222134508.png)
![Capture API](imgs/Pasted%20image%2020260222134532.png)
## Question 2.e -
![Capture API](imgs/Pasted%20image%2020260222134841.png)
# Exercice 3 :
![Capture API](imgs/Pasted%20image%2020260222135350.png)

```json
{

  "audio_path": "TP3/data/call_01.wav",

  "sample_rate": 16000,

  "duration_s": 34.632,

  "min_segment_s": 0.3,

  "segments": [

    {

      "start_s": 1.186,

      "end_s": 1.63

    },

    {

      "start_s": 2.082,

      "end_s": 3.902

    },

    {

      "start_s": 4.258,

      "end_s": 5.374

    },

    {

      "start_s": 5.73,

      "end_s": 6.814

    },
```
## Question 3.c -
Le ratio parole/silence est d’environ **0,72**, ce qui indique que la majorité de l’enregistrement contient de la parole avec des pauses relativement courtes. Cela semble cohérent avec une lecture fluide ou une conversation continue, où les silences correspondent probablement aux respirations et aux transitions entre phrases. Le nombre de segments (18) confirme une structure rythmée avec plusieurs pauses naturelles plutôt qu’un discours totalement continu.

## Question 3.d -
![Capture API](imgs/Pasted%20image%2020260222140039.png)
En augmentant le seuil de **0,30 s à 0,60 s**, le nombre de segments passe de **18 à 14**, et le **speech_ratio diminue d’environ 0,72 à 0,66**. Cela montre que les segments courts correspondent principalement à de brèves prises de parole ou micro-pauses, qui sont éliminées avec un filtrage plus strict.

# Exercice 4 :
![Capture API](imgs/Pasted%20image%2020260222141156.png)

![Capture API](imgs/Pasted%20image%2020260222141400.png)
```json
{
      "segment_id": 5,
      "start_s": 12.162,
      "end_s": 13.278,
      "text": "but the screen is correct."
    },
    {
      "segment_id": 6,
      "start_s": 13.89,
      "end_s": 17.022,
      "text": "I would like to refund or replacement as soon as possible."
    },
    {
      "segment_id": 7,
      "start_s": 17.506,
      "end_s": 19.55,
      "text": "The order number is AX."
    },
```

La segmentation VAD **aide globalement** la transcription, car elle coupe les silences et réduit le risque que Whisper “dérive” pendant les pauses : ici on obtient des phrases assez propres segment par segment, et un **RTF très faible (~0,05)** grâce à des entrées plus courtes. En revanche, elle peut aussi **gêner** quand une phrase est coupée au mauvais endroit : on voit par exemple “My name is Alex.” puis “and I will help you today.”, ce qui casse la ponctuation et la majuscule en début de segment. Elle fragmente aussi les informations structurées (numéros, email) en micro-segments (“One nine.” / “7-3” / “uh… example dot com”), ce qui peut nuire à la lisibilité et augmenter les erreurs. Au final, le VAD est bénéfique pour la robustesse et le coût, mais il faut souvent **une étape de post-traitement** (fusion de segments proches, reponctuation) pour reconstruire un texte fluide.

# Exercice 5 :
![Capture API](imgs/Pasted%20image%2020260222142200.png)
## Question 5.d -

![Capture API](imgs/Pasted%20image%2020260222142818.png)
![Capture API](imgs/Pasted%20image%2020260222142830.png)
## Question 5.e -
Avant post-traitement, l’intention prédite est **general_support** (scores: general_support=5, delivery_issue=4), et **aucune PII n’est détectée** (emails=0, phones=0). Les termes dominants contiennent notamment **“one”** (lié aux chiffres épelés) et l’email/numéro restent sous une forme difficile à détecter.

Après post-traitement, l’intention bascule vers **delivery_issue** (scores: delivery_issue=5, general_support=5) et on détecte un nouvel identifiant **orders=1** avec masquage **[REDACTED_ORDER]**. Les top terms deviennent plus cohérents (“order” apparaît 2 fois) car le texte est normalisé, ce qui aide l’heuristique d’intention. En revanche, la **redaction email/téléphone reste imparfaite** (emails=0, phones=0) car la transcription contient encore des formes “parlées” ou dégradées.

## Question 5.f -
Les erreurs de transcription qui impactent le plus mes analytics sont celles qui touchent les **PII** et les **mots-clés d’intention**. Par exemple, l’email “parlé” est transcrit comme **“jonder.smith.com … example dot com”** (ou **“example.com”**), ce qui ne correspond pas au pattern `user@domain.tld`, donc **emails=0** et l’adresse n’est pas masquée. De même, le téléphone est fragmenté (**“555. Oh, one.”** puis **“555.0, 1.”**), ce qui empêche la regex téléphone de matcher correctement → **phones=0**. Côté intention, une phrase mal reconnue comme **“botanowder”** (au lieu du produit réel) ou des petites erreurs de formulation peuvent réduire le score de “refund_or_replacement”, tandis que la normalisation (“order”) augmente artificiellement “delivery_issue”. Au final, la qualité des analytics dépend fortement d’un post-traitement robuste qui **recolle** les chiffres épelés et convertit les PII “parlées” en formats détectables.
# Exercice 6 :
![Capture API](imgs/Pasted%20image%2020260222143744.png)
![Capture API](imgs/Pasted%20image%2020260222143814.png)
## Question 6.d -
La sortie TTS est globalement **intelligible** : le message est compréhensible et les mots clés (“damaged”, “replacement”, “refund”) ressortent correctement. La **prosodie** reste assez neutre/monotone, avec une intonation parfois un peu “robotique” typique des modèles TTS légers, mais sans coupures majeures. On peut percevoir de légers **artefacts** (timbre un peu métallique / transitions moins naturelles entre phrases) selon l’écoute, surtout sur les enchaînements. Côté latence, le **RTF ≈ 0,086** indique une génération bien plus rapide que le temps réel (≈ 11–12×), donc la réponse est perçue comme quasi immédiate.

## Question 6.e -
![Capture API](imgs/Pasted%20image%2020260222144342.png)

# Exercice 7 :
![Capture API](imgs/Pasted%20image%2020260222145106.png)

![Capture API](imgs/Pasted%20image%2020260222145210.png)
## Question 7.d -
Le principal goulet d’étranglement temporel de la pipeline est l’étape **ASR**, qui reste la plus coûteuse malgré un RTF faible (~0,05) : elle domine le temps total car elle traite l’audio complet, alors que le VAD et l’analytics sont quasi instantanés et le TTS reste court (~0,94 s pour ~8,8 s audio). L’étape la plus fragile en qualité est clairement **l’ASR**, car les erreurs de transcription (mots mal reconnus, PII non détectées) se propagent ensuite vers l’analytics, ce qui explique par exemple l’absence de détection d’email/téléphone malgré leur présence implicite.

Pour industrialiser sans changer de modèle, deux améliorations concrètes seraient :  
- Ajouter un **post-traitement plus robuste** (normalisation des nombres épelés, reconstruction d’emails/numéros, reponctuation) afin d’améliorer la détection PII et l’intention ;  
-  Implémenter un **batching / streaming par segments VAD** avec parallélisation pour réduire encore la latence perçue et stabiliser le débit en production.