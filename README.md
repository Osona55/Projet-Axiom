# Projet Axiom

Réimplémentation *from scratch* de plusieurs modules scientifiques de la bibliothèque standard Python, avec un objectif d'apprentissage de l'algorithmique, des mathématiques et du fonctionnement interne des bibliothèques Python.

[![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)](https://www.python.org/)
[![Status](https://img.shields.io/badge/status-in%20development-orange)](https://github.com/Osona55/MyModules)

---

## Présentation

**Projet Axiom** est un projet personnel dans lequel je réimplémente progressivement certaines fonctionnalités de la bibliothèque standard Python.

L'objectif n'est pas de remplacer les bibliothèques officielles, mais de **comprendre comment elles peuvent être construites**, en travaillant directement sur les algorithmes et les méthodes mathématiques utilisées.

Le projet me permet notamment de travailler sur :

* l'algorithmique ;
* les statistiques ;
* les probabilités ;
* les méthodes numériques ;
* la génération pseudo-aléatoire ;
* l'optimisation et la robustesse du code Python.

---

## Modules

### `my_statistics`

Réimplémentation de fonctionnalités du module [`statistics`](https://docs.python.org/3/library/statistics.html) mais aussi quelques-unes du module open-source [`scipy.stats`](https://docs.scipy.org/doc/scipy-1.18.0/reference/stats.html).

Liste complète des fonctions implémentées :

* `mean()`
* `fmean()`
* `geometric_mean()`
* `harmonic_mean()`
* `trimmed_mean()`
* `winsorized_mean()`
* `trimean()`
* `midhinge()`
* `median()`
* `median_low()`
* `median_high()`
* `median_grouped()`
* `weighted_median()`
* `mode()`
* `multimode()`
* `pvariance()`
* `variance()`
* `pstdev()`
* `stdev()`
* `mean_absolute_deviation`
* `median_absolute_deviation`
* `range_()`
* `midrange()`
* `cv()`
* `z_score()`
* `skewness()`
* `kurtosis()`
* `covariance()`
* `correlation()`
* `kendall_tau()`
* `linear_regression()`
* `r_squared()`
* `quantiles`
* `kde()`

La fonction `kde()` permet notamment d'utiliser plusieurs noyaux :

* normal / gaussien
* logistique
* sigmoid
* rectangulaire
* triangulaire
* parabolique / Epanechnikov
* quartique
* sextique
* sinusoïdale

---

### `my_random`

Réimplémentation des fonctionnalités du module [`random`](https://docs.python.org/3/library/random.html).

Le générateur de base repose actuellement sur un **Linear Congruential Generator (LCG)** :

```text
Xₙ₊₁ = (B × Xₙ + C) mod M
```

avec des paramètres connues de LCG:

```python
M = 2**32
B = 1664525
C = 1013904223
```

Fonctions déjà disponibles :

* `seed()`
* `getstate()`
* `setstate()`
* `random()`
* `randrange()`
* `randint()`
* `choice()`
* `shuffle()`
* `getrandbits()`
* `randbytes()`

Le module contient également plusieurs générateurs de lois probabilistes, notamment :

* loi géométrique
* loi exponentielle
* loi triangulaire
* loi gamma
* loi bêta
* loi normale
* loi log-normale
* loi de Pareto
* et d'autres distributions en cours d'implémentation.

---

## Utilisation

Clone le dépôt :

```bash
git clone https://github.com/Osona55/MyModules.git
cd MyModules
```

Tu peux ensuite importer les modules directement :

```python
import my_statistics as statistics
import my_random as random

data = [1, 2, 3, 4, 5]

print(statistics.mean(data))
print(statistics.median(data))

random.seed(42)

for _ in range(5):
    print(random.random())
```

---

## Exemple : moyenne tronquée

```python
import my_statistics as statistics

data = [1, 2, 3, 4, 5, 6, 7, 100]

print(statistics.mean(data))
print(statistics.trimmed_mean(data, 0.1))
```

La moyenne tronquée permet de réduire l'influence des valeurs extrêmes en retirant une partie des observations aux deux extrémités après tri.

---

## Exemple : génération aléatoire

```python
import my_random as random

random.seed(42)

values = [random.random() for _ in range(1000)]

print(min(values))
print(max(values))
```

Le générateur peut ensuite être utilisé comme base pour construire différentes distributions probabilistes.

---

## 🔬 Philosophie du projet

Chaque fonction est écrite avec l'objectif de comprendre **pourquoi elle fonctionne**, et pas uniquement de reproduire son résultat.

Par exemple, le projet explore directement :

* les formules statistiques ;
* les méthodes de génération pseudo-aléatoire ;
* les transformations utilisées pour générer différentes lois ;
* les estimateurs statistiques ;
* les méthodes de calcul des densités et CDF ;
* la gestion des erreurs et des cas limites.

Ce projet est donc avant tout un **laboratoire d'expérimentation Python et mathématique**.

---

## ⚠️ Important

**Projet Axiom** est un projet **éducatif et expérimental**.

Les modules développés ici ne sont pas destinés à remplacer les implémentations officielles de Python en production. Ils servent principalement à comprendre les algorithmes, expérimenter différentes approches et progresser en programmation.

---

## 📄 Licence

Ce projet est distribué sous licence **MIT**.

**Projet Axiom** est une réimplémentation indépendante et pédagogique de certaines fonctionnalités proposées par les modules standards de Python (`random`, `statistics`, `math`) et de SciPy (`scipy.stats`).

Le projet n'est pas affilié au projet Python ni à la Python Software Foundation ni à SciPy.

Voir le fichier [`LICENSE`](LICENSE) pour consulter le texte complet de la licence.

---

## 👤 Auteur

Projet développé par **Osona55** dans le cadre d'un travail personnel autour de Python, de l'algorithmique et des mathématiques.

Si le projet t'intéresse, n'hésite pas à explorer le code, ouvrir une issue ou proposer une amélioration.

---

## 🗺️ Roadmap

```text
statistics
[####################] Fini

random
[#################...]  Bientôt fini

math
[###.................]  À venir
```

---

## 📚 Références

* [Documentation Python — statistics](https://docs.python.org/3/library/statistics.html)
* [Documentation Python — random](https://docs.python.org/3/library/random.html)
* [Documentation Python — math](https://docs.python.org/3/library/math.html)
* [Documentation SciPy — stats](https://docs.scipy.org/doc/scipy-1.18.0/reference/stats.html).
* [Dépôt GitHub](https://github.com/Osona55/MyModules)
