# 3250-3-ia-i-tp4

Rendu de TP4 pour le cours d'intelligence artificielle I, par Maëlys Bühler et Nima Dekhli

Ce TP a été réalisé en Python 3.11.
La version finale utilise plusieurs stratégie pour évaluer un état du jeu.

- La mobilité: Un coup qui offre le moins de possibilité a un meilleur score.
- Les coins: Un coup qui offre le plus de coin a un meilleur score.
- Les cases adjacentes au coin: Un coup qui ne prend pas une case adjacente a un coin a un meilleur score.
- Les cases définitive: Un coup qui permet le posséder le plus de cases définitive a un meilleur score. C'est la stratégie qui est la plus importante pour notre algorithme, elle est donc la plus pondérée.
- Le score: Le score temporaire du jeu a aussi un poids dans notre algorithme, mais il est moins important que les cases définitives.
