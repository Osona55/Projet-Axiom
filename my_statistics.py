# -*- coding: utf-8 -*-
# @author : Osona
# Copyright (c) 2026 Osona
# Licensed under the MIT License.

#=== Importation des modules ===
from math import pi, exp, log, sqrt, cos, sin, cosh, sinh, erf, atan
from typing import Iterable, List, Union, Tuple, Any

#=== Error ===

class StatisticsError(Exception):
    """Erreur spécifique aux fonctions de ce module"""
    pass

#=== Moyennes ===

def mean(data: Iterable[float]) -> float:
    """Renvoie la moyenne arithmétique de *data* sous la forme d'un float.

    Args:
        data (Iterable[float]): Échantillon de nombres réels dont on veut la moyenne arithmétique.

    Raises:
        StatisticsError: Lorsque *data* est vide.

    Returns:
        float: Moyenne arithmétique de *data*.
    """
    data = list(data) if not isinstance(data, list) else data
    n = len(data)
    if n == 0:
        raise StatisticsError("Attention entrée vide")
    return sum(data) / n

def fmean(data: Iterable[float], weights: Union[Iterable[float], None] = None) -> float:
    """Renvoie la moyenne arithmétique de *data* pondérée par *weights* sous la forme d'un float.

    Args:
        data (Iterable[float]): Échantillon de nombres réels dont on veut la moyenne arithmétique pondérée.
        weights (Iterable[float], optional): Poids de la moyenne. Defaults to None.

    Raises:
        StatisticsError: Lorsque *data* est vide.
        StatisticsError: Lorsque *data* et *weights* n'ont pas la même dimension.
        StatisticsError: Lorsqu'un des poids est négatif.
        StatisticsError: Lorsque tous les poids sont nuls.

    Returns:
        float: Moyenne arithmétique de *data* pondérée par *weights*.
    """
    data = list(data) if not isinstance(data, list) else data
    n = len(data)
    if n == 0:
        raise StatisticsError("Attention entrée vide")
    if weights is None:
        return sum(data) / n
    weights = list(weights) if not isinstance(weights, list) else weights
    if n != len(weights):
        raise StatisticsError("Attention entrées avec des dimensions différentes")
    somme = 0.0
    for i in range(n):
        if weights[i] < 0.0:
            raise StatisticsError("Attention aux poids négatifs")
        somme += data[i] * weights[i]
    somme_w = sum(weights)
    if somme_w == 0.0:
        raise StatisticsError("Attention tous les poids sont nuls")
    return somme / somme_w

def geometric_mean(data: Iterable[float]) -> float:
    """Renvoie la moyenne géométrique de *data* sous la forme d'un float.

    Args:
        data (Iterable[float]): Échantillon de nombres réels dont on veut la moyenne géométrique.

    Raises:
        StatisticsError: Lorsque *data* est vide.
        StatisticsError: Lorsqu'une valeur de *data* est nulle ou négative.

    Returns:
        float: Moyenne géométrique de *data*.
    """
    data = list(data) if not isinstance(data, list) else data
    n = len(data)
    if n == 0:
        raise StatisticsError("Attention entrée vide")
    p = 0.0
    for x in data:
        if x <= 0:
            raise StatisticsError("Attention valeur négative ou nulle en entrée")
        p += log(x)
    return exp(p / n)

def harmonic_mean(data: Iterable[float], weights: Union[Iterable[float], None] = None) -> float:
    """Renvoie la moyenne harmonique de *data* pondérée par *weights* sous la forme d'un float.

    Args:
        data (Iterable[float]): Échantillon de nombres réels dont on veut la moyenne harmonique pondérée.
        weights (Iterable[float], optional): Poids de la moyenne. Defaults to None.

    Raises:
        StatisticsError: Lorsque *data* est vide.
        StatisticsError: Lorsque *data* et *weights* n'ont pas la même dimension.
        StatisticsError: Lorsqu'un poids est négatif.
        StatisticsError: Lorsqu'une des valeurs est négative.

    Returns:
        float: Moyenne harmonique de *data* pondérée par *weights*.
    """
    data = list(data) if not isinstance(data, list) else data
    n = len(data)
    if n == 0:
        raise StatisticsError("Attention entrée vide")
    if weights is None:
        somme = 0
        for x in data:
            if x < 0:
                raise StatisticsError("Attention valeur négative")
            if x == 0:
                return 0.0
            somme += 1 / x
        return n / somme
    weights = list(weights) if not isinstance(weights, list) else weights
    m = len(weights)
    if n != m:
        raise StatisticsError("Attention entrées avec des dimensions différentes")
    somme = 0.0
    s_weights = 0.0
    for i in range(n):
        x = data[i]
        w = weights[i]
        if x == 0 and w == 0:
            continue
        elif x == 0 :   #and w != 0
            return 0.0
        elif w < 0:
            raise StatisticsError("Attention poids négatif")
        elif x < 0:
            raise StatisticsError("Attention valeur négative")
        somme += (1 / x) * w
        s_weights += w
    if s_weights == 0.0:
        raise StatisticsError("Attention tous les poids sont nuls")
    if somme == 0.0:
        raise StatisticsError("Attention la somme harmonique est nulle")
    return s_weights / somme

def trimmed_mean(data: Iterable[float], h: float) -> float:
    """Renvoie la moyenne tronquée de *data* sous la forme d'un float.

    Args:
        data (Iterable[float]): Échantillon de nombres réels dont on veut la moyenne tronquée.
        h (float): Taux de troncature.

    Raises:
        StatisticsError: Lorsque *data* est vide.
        StatisticsError: Lorsque *h* est négatif.
        StatisticsError: Lorsque *h* est trop grand.

    Returns:
        float: Moyenne tronquée de *data*.
    """
    data = list(data) if not isinstance(data, list) else data
    n = len(data)
    if n == 0:
        raise StatisticsError("Attention entrée vide")
    if h < 0:
        raise StatisticsError("Attention h doit être positif")
    if h == 0.0 :
        return mean(data)
    k = int(h * n)
    if 2 * k >= n:
        raise StatisticsError("Attention le taux de troncature h est trop grand.")
    data_sorted = sorted(data)
    somme = sum(data_sorted[i] for i in range(k, n - k))
    return somme / (n - 2 * k)

def winsorized_mean(data: Iterable[float], h: float) -> float:
    """Renvoie la moyenne winsorisée de *data* sous la forme d'un float.

    Args:
        data (Iterable[float]): Échantillon de nombres réels dont on veut la moyenne winsorisée.
        h (float): Taux de winsorisation.

    Raises:
        StatisticsError: Lorsque *data* est vide.
        StatisticsError: Lorsque *h* est négatif.
        StatisticsError: Lorsque *h* est trop grand.

    Returns:
        float: Moyenne winsorisée de *data*.
    """
    data = list(data) if not isinstance(data, list) else data
    n = len(data)
    if n == 0:
        raise StatisticsError("Attention entrée vide")
    if h < 0.0:
        raise StatisticsError("Attention h doit être positif")
    if h == 0.0:
        return mean(data)
    k = int(h * n)
    if 2 * k >= n:
        raise StatisticsError("Attention le taux de winsorisation h est trop grand")
    x = sorted(data)
    low = x[k]
    high = x[n - k - 1]
    winsorized = [low] * k + x[k : n - k] + [high] * k
    return mean(winsorized)

def trimean(data: Iterable[float]) -> float:
    """Renvoie la trimoyenne de Tukey de *data*.

    Args:
        data (Iterable[float]): Échantillon de nombres réels.

    Raises:
        StatisticsError: Lorsque la taille de l'échantillon *data* n'est pas assez grande.

    Returns:
        float: Trimoyenne de *data*.
    """
    data = list(data) if not isinstance(data, list) else data
    q = quantiles(data, n=4)
    return (q[0] + 2 * q[1] + q[2]) / 4

def midhinge(data: Iterable[float]) -> float:
    """Renvoie la midhinge (moyenne du premier et du troisième quartile) de *data*.

    Args:
        data (Iterable[float]): Échantillon de nombres réels.

    Raises:
        StatisticsError: Lorsque la taille de l'échantillon *data* n'est pas assez grande.

    Returns:
        float: Midhinge de *data*.
    """
    data = list(data) if not isinstance(data, list) else data
    q = quantiles(data, n = 4)
    return (q[0] + q[2]) / 2

#=== Médianes ===

def median(data: Iterable[float]) -> Union[float, int]:
    """Renvoie la médiane de *data*.

    Args:
        data (Iterable[float]): Échantillon de nombres réels dont on veut la médiane.

    Raises:
        StatisticsError: Lorsque *data* est vide.

    Returns:
        Union[float, int]: Médiane de *data* (nombre réel).
    """
    data = list(data) if not isinstance(data, list) else data
    n = len(data)
    if n == 0:
        raise StatisticsError("Attention entrée vide")
    L = sorted(data)
    mid = n // 2
    if n % 2 == 0:
        return (L[mid - 1] + L[mid]) / 2
    return L[mid]

def median_low(data: Iterable[float]) -> Union[float, int]:
    """Renvoie la médiane basse de *data*, fonctionne même si les données ne sont pas numériques mais peuvent être triées.

    Args:
        data (Iterable[float]): Échantillon de nombres réels dont on veut la médiane basse.

    Raises:
        StatisticsError: Lorsque *data* est vide.

    Returns:
        Union[float, int]: Médiane basse de *data* (nombre réel).
    """
    data = list(data) if not isinstance(data, list) else data
    n = len(data)
    if n == 0:
        raise StatisticsError("Attention entrée vide")
    L = sorted(data)
    mid = n // 2
    if n % 2 == 0:
        return L[mid - 1]
    return L[mid]

def median_high(data: Iterable[float]) -> Union[float, int]:
    """Renvoie la médiane haute de *data*, fonctionne même si les données ne sont pas numériques mais peuvent être triées.

    Args:
        data (Iterable[float]): Échantillon de nombres réels dont on veut la médiane haute.

    Raises:
        StatisticsError: Lorsque *data* est vide.

    Returns:
        Union[float, int]: Médiane haute de *data* (nombre réel).
    """
    data = list(data) if not isinstance(data, list) else data
    n = len(data)
    if n == 0:
        raise StatisticsError("Attention entrée vide")
    L = sorted(data)
    mid = n // 2
    return L[mid]

def median_grouped(data: Iterable[float], interval: float = 1.0) -> float:
    """Renvoie la médiane groupée d'un ensemble de données *data*.

    Args:
        data (Iterable[float]): Ensemble des observations numériques. Les données ne doivent pas être vides.
        interval (float, optional): Largeur supposée des classes. Doit être strictement positif. Defaults to 1.0.

    Raises:
        StatisticsError: Lorsque *data* est vide.
        StatisticsError: Lorsque *interval* n'est pas strictement positif.

    Returns:
        float: Médiane estimée.
    """
    data = list(data) if not isinstance(data, list) else data
    n = len(data)
    if n == 0:
        raise StatisticsError("Attention entrée vide")
    if interval <= 0.0:
        raise StatisticsError("Attention l'intervalle doit être strictement positif")
    DATA = sorted(data)
    m = DATA[n // 2]
    L = m - interval / 2
    f_m = DATA.count(m)
    if f_m == 0:
        raise StatisticsError("Attention erreur lors du calcul de la fréquence de la médiane")
    CF = sum(1 for v in DATA if v < m)
    return L + ((n / 2 - CF) / f_m) * interval

def weighted_median(data: Iterable[float], weights: Iterable[float]) -> float:
    """Renvoie la médiane pondérée de *data* selon les poids *weights*.

    Args:
        data (Iterable[float]): Échantillon de nombres réels.
        weights (Iterable[float]): Poids associés à chaque valeur de *data*.

    Raises:
        StatisticsError: Lorsque *data* est vide.
        StatisticsError: Lorsque *data* et *weights* n'ont pas la même dimension.
        StatisticsError: Lorsqu'un poids est négatif.
        StatisticsError: Lorsque la somme des poids est nulle.

    Returns:
        float: Médiane pondérée de *data*.
    """
    data = list(data) if not isinstance(data, list) else data
    weights = list(weights) if not isinstance(weights, list) else weights
    n = len(data)
    if n == 0:
        raise StatisticsError("Attention entrée vide")
    if n != len(weights):
        raise StatisticsError("Attention entrées avec des dimensions différentes")
    if any(w < 0 for w in weights):
        raise StatisticsError("Attention poids négatif")
    total = sum(weights)
    if total == 0:
        raise StatisticsError("Attention somme des poids nulle")
    pairs = sorted(((x, w) for x, w in zip(data, weights) if w != 0), key=lambda p: p[0])
    cumul = 0.0
    half = total / 2
    for i, (x, w) in enumerate(pairs):
        cumul += w
        if cumul == half and i + 1 < len(pairs):
            return (pairs[i][0] + pairs[i + 1][0]) / 2
        if cumul > half:
            return x
    return pairs[-1][0]

#=== Mode ===

def mode(data: Iterable[Any]) -> Any:
    """Renvoie la valeur la plus représentée (la première apparue s'il y en a plusieurs) dans l'échantillon *data*.

    Args:
        data (Iterable[Any]): Échantillon dont on veut le mode.

    Raises:
        StatisticsError: Lorsque *data* est vide.

    Returns:
        Any: Mode (valeur la plus représentée) de *data* (nombre réel ou type hachable).
    """
    data = list(data) if not isinstance(data, list) else data
    n = len(data)
    if n == 0:
        raise StatisticsError("Attention entrée vide")
    D = {}
    for x in data:
        if x not in D:
            D[x] = 1
        else:
            D[x] += 1
    m = max(D.values())
    for a,b in D.items():
        if b == m:
            return a

def multimode(data: Iterable[Any]) -> List[Any]:
    """Renvoie la liste des modes de *data* ou une liste vide si *data* est vide.

    Args:
        data (Iterable[Any]): Échantillon dont on veut les modes.

    Returns:
        List[Any]: Liste des modes de *data* (nombres réels ou types hachables).
    """
    data = list(data) if not isinstance(data, list) else data
    n = len(data)
    if n == 0:
        return list()
    D = {}
    for x in data:
        if x not in D:
            D[x] = 1
        else:
            D[x] += 1
    m = max(D.values())
    L = []
    for a,b in D.items():
        if b == m:
            L.append(a)
    return L

#=== Mesures de dispersion ===

def pvariance(data: Iterable[float], mu: Union[float, None] = None) -> float:
    """Renvoie la variance de la population *data*.

    Args:
        data (Iterable[float]): Population de nombres réels.
        mu (float, optional): Moyenne de la population *data*. Defaults to None.

    Raises:
        StatisticsError: Lorsque *data* est vide.

    Returns:
        float: Variance de la population.
    """
    data = list(data) if not isinstance(data, list) else data
    n = len(data)
    if n == 0:
        raise StatisticsError("Attention entrée vide")
    if mu is None:
        mu = mean(data)
    return sum((x - mu) ** 2 for x in data) / n

def variance(data: Iterable[float], xbar: Union[float, None] = None) -> float:
    """Renvoie la variance de l'échantillon de la population *data* (avec correction de Bessel).

    Args:
        data (Iterable[float]): Échantillon de nombres réels de la population de données.
        xbar (float, optional): Moyenne de l'échantillon *data*. Defaults to None.

    Raises:
        StatisticsError: Lorsque la taille de *data* est trop petite.

    Returns:
        float: Variance de l'échantillon de population *data*.
    """
    data = list(data) if not isinstance(data, list) else data
    n = len(data)
    if n < 2:
        raise StatisticsError("Attention taille de l'entrée trop petite")
    if xbar is None:
        xbar = mean(data)
    return sum((x - xbar) ** 2 for x in data) / (n - 1)

def pstdev(data: Iterable[float], mu: Union[float, None] = None) -> float:
    """Renvoie l'écart-type de la population *data*.

    Args:
        data (Iterable[float]): Population de nombres réels.
        mu (float, optional): Moyenne de la population *data*. Defaults to None.

    Raises:
        StatisticsError: Lorsque *data* est vide.

    Returns:
        float: Écart-type de la population *data*.
    """
    data = list(data) if not isinstance(data, list) else data
    return sqrt(pvariance(data, mu))

def stdev(data: Iterable[float], xbar: Union[float, None] = None) -> float:
    """Renvoie l'écart-type de l'échantillon de la population *data* (avec correction de Bessel).

    Args:
        data (Iterable[float]): Échantillon de nombres réels de la population de données.
        xbar (float, optional): Moyenne de l'échantillon *data*. Defaults to None.

    Raises:
        StatisticsError: Lorsque la taille de *data* est trop petite.

    Returns:
        float: Écart-type de l'échantillon de population *data*.
    """
    data = list(data) if not isinstance(data, list) else data
    return sqrt(variance(data, xbar))

def mean_absolute_deviation(data: Iterable[float]) -> float:
    """Renvoie la mean absolute deviation (MAD) de *data*.

    Args:
        data (Iterable[float]): Échantillon de nombres réels.

    Raises:
        StatisticsError: Lorsque *data* est vide.

    Returns:
        float: Mean absolute deviation de *data*.
    """
    data = list(data) if not isinstance(data, list) else data
    n = len(data)
    if n == 0 :
        raise StatisticsError("Attention entrée vide")
    m = mean(data)
    return sum(abs(x - m) for x in data) / n

def median_absolute_deviation(data: Iterable[float]) -> float:
    """Renvoie la median absolute deviation (MAD) de *data*.

    Args:
        data (Iterable[float]): Échantillon de nombres réels.

    Raises:
        StatisticsError: Lorsque *data* est vide.

    Returns:
        float: Median absolute deviation de *data*.
    """
    data = list(data) if not isinstance(data, list) else data
    n = len(data)
    if n == 0 :
        raise StatisticsError("Attention entrée vide")
    m = median(data)
    deviations = [abs(x - m) for x in data]
    return median(deviations)

def range_(data: Iterable[float]) -> float:
    """Renvoie la range de *data*.

    Args:
        data (Iterable[float]): Échantillon de nombres réels.

    Raises:
        StatisticsError: Lorsque *data* est vide.

    Returns:
        float: Range de *data*.
    """
    data = sorted(list(data)) if not isinstance(data, list) else sorted(data)
    n = len(data)
    if n == 0:
        raise StatisticsError("Attention entrée vide")
    return data[-1] - data[0]

def midrange(data: Iterable[float]) -> float:
    """Renvoie la moitié de l'étendue de *data*.

    Args:
        data (Iterable[float]): Échantillon de nombres réels.

    Raises:
        StatisticsError: Lorsque *data* est vide.

    Returns:
        float: Moitié de la range de *data*.
    """
    data = sorted(list(data)) if not isinstance(data, list) else sorted(data)
    n = len(data)
    if n == 0:
        raise StatisticsError("Attention entrée vide")
    return (data[-1] + data[0]) / 2

def cv(data: Iterable[float], method: str = 'sample') -> float:
    """Renvoie le coefficient de variation de *data* pour une population ou un échantillon.

    Args:
        data (Iterable[float]): Population ou échantillon de nombres réels.
        method (str, optional): Type d'échantillon utilisé. Defaults to 'sample'.

    Raises:
        StatisticsError: Lorsque *data* est vide.
        StatisticsError: Moyenne de *data* est nulle.
        StatisticsError: Lorsque *method* est non valide.

    Returns:
        float: Coefficient de variation de *data*.
    """
    data = list(data) if not isinstance(data, list) else data
    n = len(data)
    if n == 0:
        raise StatisticsError("Attention entrée vide")
    m = mean(data)
    if m == 0.0 :
        raise StatisticsError("Attention le coefficient de variation est indéfini pour une moyenne nulle.")
    if method == 'sample':
        return stdev(data) / m
    if method == 'population':
        return pstdev(data) / m
    raise StatisticsError("Attention type non valide, method doit être 'sample' ou 'population'")

def z_score(data: Iterable[float], method: str = 'sample') -> List[float]:
    """Renvoie *data* sous forme d'une liste standardisée.

    Args:
        data (Iterable[float]): Population ou échantillon de nombres réels.
        method (str, optional): Type d'échantillon utilisé. Defaults to 'sample'.

    Raises:
        StatisticsError: Lorsque *data* est vide.
        StatisticsError: Lorsque *method* est non valide.
        StatisticsError: Lorsque l'écart-type est nul.

    Returns:
        List[float]: *data* standardisé.
    """
    data = list(data) if not isinstance(data, list) else data
    if not data:
        raise StatisticsError("Attention entrée vide")

    m = mean(data)
    if method == 'population':
        sd = pstdev(data, mu=m)
    elif method == 'sample':
        sd = stdev(data, xbar=m)
    else:
        raise StatisticsError("Attention type non valide, method doit être 'sample' ou 'population'")

    if sd == 0.0:
        raise StatisticsError("Attention la variable est constante")

    return [(x - m) / sd for x in data]

def skewness(data: Iterable[float], method: str = 'sample') -> float:
    """Renvoie le coefficient d'asymétrie (skewness) de *data*.

    Args:
        data (Iterable[float]): Échantillon ou population de nombres réels.
        method (str, optional): 'population' pour le coefficient brut g1, 'sample' pour la version corrigée G1. Defaults to 'sample'.

    Raises:
        StatisticsError: Lorsque *data* est vide.
        StatisticsError: Lorsque l'écart-type de la population est nul.
        StatisticsError: Lorsque la taille de l'entrée est trop petite pour 'sample'.
        StatisticsError: Lorsque *method* est non valide.

    Returns:
        float: Coefficient d'asymétrie de *data*.
    """
    data = list(data) if not isinstance(data, list) else data
    n = len(data)
    if n == 0:
        raise StatisticsError("Attention entrée vide")
    m = mean(data)
    m2 = sum((x - m) ** 2 for x in data) / n
    m3 = sum((x - m) ** 3 for x in data) / n
    if m2 == 0.0:
        raise StatisticsError("Attention écart-type nul")
    g1 = m3 / (m2 ** 1.5)
    if method == 'population':
        return g1
    elif method == 'sample':
        if n < 3:
            raise StatisticsError("Attention taille de l'entrée trop petite")
        return (sqrt(n * (n - 1)) / (n - 2)) * g1
    else:
        raise StatisticsError("Attention method non valide, method doit être 'sample' ou 'population'")

def kurtosis(data: Iterable[float], method: str = 'sample') -> float:
    """Renvoie le coefficient d'aplatissement (excess kurtosis) de *data*.

    Args:
        data (Iterable[float]): Échantillon ou population de nombres réels.
        method (str, optional): 'population' pour le coefficient brut g2, 'sample' pour la version corrigée G2. Defaults to 'sample'.

    Raises:
        StatisticsError: Lorsque *data* est vide.
        StatisticsError: Lorsque l'écart-type de la population est nul.
        StatisticsError: Lorsque la taille de l'entrée est trop petite pour 'sample'.
        StatisticsError: Lorsque *method* est non valide.

    Returns:
        float: Coefficient d'aplatissement (excess kurtosis) de *data*, 0 pour une loi normale.
    """
    data = list(data) if not isinstance(data, list) else data
    n = len(data)
    if n == 0:
        raise StatisticsError("Attention entrée vide")
    m = mean(data)
    m2 = sum((x - m) ** 2 for x in data) / n
    m4 = sum((x - m) ** 4 for x in data) / n
    if m2 == 0.0:
        raise StatisticsError("Attention écart-type nul")
    g2 = m4 / (m2 ** 2) - 3
    if method == 'population':
        return g2
    elif method == 'sample':
        if n < 4:
            raise StatisticsError("Attention taille de l'entrée trop petite")
        return ((n - 1) / ((n - 2) * (n - 3))) * ((n + 1) * g2 + 6)
    else:
        raise StatisticsError("Attention method non valide, method doit être 'sample' ou 'population'")

#=== Entre deux entrées ===

def covariance(x: Iterable[float], y: Iterable[float], method: str = 'sample') -> float:
    """Renvoie la covariance entre les deux échantillons *x* et *y*.

    Args:
        x (Iterable[float]): Premier échantillon de nombres réels.
        y (Iterable[float]): Deuxième échantillon de nombres réels.
        method (str, optional): Type d'échantillon utilisé. Defaults to 'sample'.

    Raises:
        StatisticsError: Lorsque les échantillons sont trop petits.
        StatisticsError: Lorsque les échantillons n'ont pas la même dimension.
        StatisticsError: Lorsque *method* est non valide.

    Returns:
        float: Covariance entre *x* et *y*.
    """
    x = list(x) if not isinstance(x, list) else x
    y = list(y) if not isinstance(y, list) else y
    n = len(x)
    m = len(y)
    if n < 2 or m < 2 :
        raise StatisticsError("Attention taille de l'entrée trop petite")
    if n != m :
        raise StatisticsError("Attention entrées avec des dimensions différentes")
    xbar = mean(x)
    ybar = mean(y)
    if method == 'sample':
        return sum((x[i] - xbar) * (y[i] - ybar) for i in range(n)) / (n - 1)
    elif method == 'population':
        return sum((x[i] - xbar) * (y[i] - ybar) for i in range(n)) / n
    else :
        raise StatisticsError("Attention methode non valide, method doit être 'sample' ou 'population'")

def correlation(x: Iterable[float], y: Iterable[float], method: str = 'linear') -> float:
    """Renvoie la corrélation de Pearson ou de Spearman entre les deux échantillons *x* et *y*.

    Args:
        x (Iterable[float]): Premier échantillon de nombres réels.
        y (Iterable[float]): Deuxième échantillon de nombres réels.
        method (str, optional): Représente le type de corrélation utilisée 'linear' -> Pearson, 'ranked' -> Spearman. Defaults to 'linear'.

    Raises:
        StatisticsError: Lorsque les échantillons sont trop petits.
        StatisticsError: Lorsque les échantillons n'ont pas la même dimension.
        StatisticsError: Lorsqu'une des deux entrées est constante.
        StatisticsError: Lorsque *method* est non valide.

    Returns:
        float: Corrélation de Pearson ou de Spearman de *x* et *y*.
    """
    x = list(x) if not isinstance(x, list) else x
    y = list(y) if not isinstance(y, list) else y
    n = len(x)
    m = len(y)
    if n < 2 or m < 2 :
        raise StatisticsError("Attention taille de l'entrée trop petite")
    if n != m :
        raise StatisticsError("Attention entrées avec des dimensions différentes")
    if method == 'linear':
        std_x = stdev(x)
        std_y = stdev(y)
        if std_x == 0.0 or std_y == 0.0 :
            raise StatisticsError("Attention une variable est constante")
        return covariance(x,y) / (std_x * std_y)
    elif method == 'ranked':
        def rankdata(data: List[float]) -> List[float]:
            p = len(data)
            sorted_data = sorted(enumerate(data), key = lambda x: x[1])
            ranks = [0.0] * p
            i = 0
            while i < p:
                j = i
                while j < p - 1 and sorted_data[j][1] == sorted_data[j + 1][1]:
                    j += 1
                avg_rank = (i + j + 2) / 2.0
                for k in range(i, j + 1):
                    ranks[sorted_data[k][0]] = avg_rank
                i = j + 1
            return ranks
        ranks_x  = rankdata(x)
        ranks_y  = rankdata(y)
        return correlation(ranks_x, ranks_y, method = 'linear')
    else:
        raise StatisticsError("Attention méthode non valide, method doit être 'linear' ou 'ranked'")

def kendall_tau(x: Iterable[float], y: Iterable[float], method: str = 'type_a') -> float:
    """Renvoie le Tau-a ou Tau-b de Kendall de deux échantillons *x* et *y*.

    Args:
        x (Iterable[float]): Premier échantillon de nombres réels.
        y (Iterable[float]): Deuxième échantillon de nombres réels.
        method (str, optional): Type du Tau de Kendall. Defaults to 'type_a'.

    Raises:
        StatisticsError: Lorsque les échantillons sont trop petits.
        StatisticsError: Lorsque les échantillons n'ont pas la même dimension.
        StatisticsError: Lorsque toutes les valeurs sont liées.
        StatisticsError: Lorsque *method* est non valide.

    Returns:
        float: Tau-a ou Tau-b de Kendall de *x* et *y*.
    """
    x = list(x) if not isinstance(x, list) else x
    y = list(y) if not isinstance(y, list) else y
    n = len(x)
    if n != len(y):
        raise StatisticsError("Attention entrées avec des dimensions différentes")
    if n < 2:
        raise StatisticsError("Attention taille de l'entrée trop petite")
    concordant = 0
    discordant = 0
    if method == 'type_a':
        for i in range(n - 1):
            for j in range(i + 1,n):
                dx = x[i] - x[j]
                dy = y[i] - y[j]
                if dx == 0.0 or dy == 0.0:
                    continue
                elif dx * dy > 0.0:
                    concordant += 1
                else:
                    discordant += 1
        if concordant + discordant == 0:
            raise StatisticsError("Attention toutes les valeurs sont liées.")
        return 2 * (concordant - discordant) / (n * (n -1))
    elif method == 'type_b':
        ties_x = 0
        ties_y = 0
        for i in range(n - 1):
            for j in range(i + 1, n):
                dx = x[i] - x[j]
                dy = y[i] - y[j]
                if dx == 0.0 and dy == 0.0:
                    continue
                elif dx == 0.0:
                    ties_x += 1
                elif dy == 0.0:
                    ties_y += 1
                elif dx * dy > 0.0:
                    concordant += 1
                else:
                    discordant += 1
        denom = sqrt((concordant + discordant + ties_x) * (concordant + discordant + ties_y))
        if denom == 0.0:
            raise StatisticsError("Attention toutes les valeurs sont liées.")
        return (concordant - discordant) / denom
    else:
        raise StatisticsError("Attention méthode non valide, method doit être 'type_a' ou 'type_b'")

def linear_regression(x: Iterable[float], y: Iterable[float], proportional: bool = False) -> Tuple[float, float]:
    """Renvoie la pente et l'ordonnée à l'origine de la régression linéaire de *x* et *y*.
    Soit a et b dans l'équation y = a * x + b .

    Args:
        x (Iterable[float]): Premier échantillon de nombres réels.
        y (Iterable[float]): Deuxième échantillon de nombres réels.
        proportional (bool, optional): True si *x* et *y* sont proportionnels, False si non ou si on ne sait pas. Defaults to False.

    Raises:
        StatisticsError: Lorsque les échantillons n'ont pas la même dimension.
        StatisticsError: Lorsque la taille des échantillons n'est pas assez grande.
        StatisticsError: Lorsque *x* est constant, sa variance est nulle.
        StatisticsError: Lorsque, pour une régression proportionnelle, toutes les valeurs de *x* sont nulles.

    Returns:
        Tuple[float, float]: Pente et l'ordonnée à l'origine de la régression linéaire.
    """
    x = list(x) if not isinstance(x, list) else x
    y = list(y) if not isinstance(y, list) else y
    n = len(x)
    if n != len(y):
        raise StatisticsError("Attention aux dimensions")
    if n < 2:
        raise StatisticsError("Attention taille de l'entrée trop petite")
    if not proportional:
        var_x = variance(x)
        if var_x == 0.0:
            raise StatisticsError("Attention x est constant")
        slope = covariance(x,y) / var_x
        intercept = mean(y) - slope * mean(x)
        return slope, intercept
    denom = sum(xi * xi for xi in x)
    if denom == 0.0 :
        raise StatisticsError("Attention tous les x sont égaux à zéro")
    slope = sum(xi * yi for xi, yi in zip(x, y)) / denom
    intercept = 0.0
    return slope, intercept

def r_squared(x: Iterable[float], y: Iterable[float], proportional: bool = False) -> float:
    """Renvoie le coefficient de détermination R² de la régression linéaire de *y* sur *x*.

    Args:
        x (Iterable[float]): Variable explicative (nombre réel).
        y (Iterable[float]): Variable expliquée (nombre réel).
        proportional (bool, optional): True si la régression est forcée à passer par zéro. Defaults to False.

    Raises:
        StatisticsError: Lorsque les échantillons n'ont pas la même dimension.
        StatisticsError: Lorsque la taille des échantillons n'est pas assez grande.
        StatisticsError: Lorsque *y* est constant (variance totale nulle).

    Returns:
        float: Coefficient de détermination R².
    """
    x = list(x) if not isinstance(x, list) else x
    y = list(y) if not isinstance(y, list) else y
    n = len(x)
    if n != len(y):
        raise StatisticsError("Attention aux dimensions")
    if n < 2:
        raise StatisticsError("Attention taille de l'entrée trop petite")
    slope, intercept = linear_regression(x, y, proportional=proportional)
    ybar = mean(y)
    ss_tot = sum((yi - ybar) ** 2 for yi in y)
    if ss_tot == 0.0:
        raise StatisticsError("Attention y est constant")
    ss_res = sum((yi - (slope * xi + intercept)) ** 2 for xi, yi in zip(x, y))
    return 1 - ss_res / ss_tot

#=== Quantiles ===

def quantiles(data: Iterable[float], n: int = 4, method: str = 'exclusive') -> List[float]:
    """Divise *data* en *n* groupes de même probabilité et renvoie la liste des *n-1* bornes.

    Args:
        data (Iterable[float]): Échantillon de nombres réels.
        n (int, optional): Nombre de groupes en lesquels on veut diviser *data*. Defaults to 4.
        method (str, optional): Méthode qui va être utilisée pour diviser *data*. Defaults to 'exclusive'.

    Raises:
        StatisticsError: Lorsque la taille de l'échantillon *data* n'est pas assez grande.
        StatisticsError: Lorsque n n'est pas un entier non nul.
        StatisticsError: Lorsque la taille de l'échantillon *data* n'est pas assez grande par rapport à *n*.
        StatisticsError: Lorsque *method* n'est pas valide.

    Returns:
        List[float]: Liste des bornes des *n* groupes.
    """
    data = list(data) if not isinstance(data, list) else data
    N  = len(data)
    if N < 2 :
        raise StatisticsError("Attention taille de l'entrée trop petite")
    if n < 1 or not isinstance(n, int):
        raise StatisticsError("Attention n doit être un entier non nul positif")
    if n > N :
        raise StatisticsError("Attention taille de l'entrée trop petite par rapport à n ")
    if method not in ('inclusive', 'exclusive'):
        raise StatisticsError("Attention méthode non valide, method doit être 'inclusive' ou 'exclusive'")
    L = sorted(data)
    result =[]
    for i in range(1,n):
        p = i / n
        if method == 'inclusive':
            r = p * (N - 1) + 1
        else:       # method == "exclusive"
            r = p * (N + 1)
        k = int(r)
        d = r - k
        if k <= 0:
            q = L[0]
        elif k >= N:
            q = L[-1]
        else:
            q = L[k-1] + d * (L[k] - L[k-1])
        result.append(q)
    return result

#=== Kernel ===

def kde(data: Iterable[float], h: float, kernel: str = 'normal', cumulative: bool = False):
    """Renvoie une fonction de distribution continue ou une fonction de distribution cumulative (CDF) depuis des données discrètes.

    Args:
        data (Iterable[float]): Échantillon de nombres réels.
        h (float): Bande-passante contrôlant la régularité de la fonction renvoyée.
        kernel (str, optional): Nature du noyau qui va être utilisé. Defaults to 'normal'.
        cumulative (bool, optional): Si True, renvoie la CDF. Defaults to False.

    Raises:
        StatisticsError: Lorsque *data* est vide.
        StatisticsError: Lorsque *h* est négatif ou nul.
        StatisticsError: Lorsque *kernel* n'est pas valide.

    Returns:
        Callable: Fonction de distribution ou fonction de distribution cumulative (CDF).
    """
    data = list(data) if not isinstance(data, list) else data
    n = len(data)
    if n == 0:
        raise StatisticsError("Attention entrée vide")
    if h <= 0:
        raise StatisticsError("Attention h doit être strictement positif")
    if kernel == 'normal':
        def density(x):
            total = 0.0
            for xi in data:
                u = (x - xi) / h
                k = exp(-0.5 * u * u) / sqrt(2 * pi)
                total += k
            return total / (n * h)
        def cdf(x):
            total = 0.0
            for xi in data:
                u = (x - xi) / h
                k = 0.5 * (1.0 + erf(u / sqrt(2.0)))
                total += k
            return total / n
    elif kernel == 'logistic':
        def density(x):
            total = 0.0
            for xi in data:
                u = (x - xi) / h
                t = exp(-u)
                k = t / ((1 + t) ** 2)
                total += k
            return total / (n * h)
        def cdf(x):
            total = 0.0
            for xi in data:
                u = (x - xi) / h
                k = 1.0 / (1.0 + exp(-u))
                total += k
            return total / n
    elif kernel == 'sigmoid':
        def density(x):
            total = 0.0
            for xi in data:
                u = (x - xi) / h
                k = 1.0 / (pi * cosh(u))
                total += k
            return total / (n * h)
        def cdf(x):
            total = 0.0
            for xi in data:
                u = (x - xi) / h
                k = 0.5 + atan(sinh(u)) / pi
                total += k
            return total / n
    elif kernel == 'rectangular':
        def density(x):
            total = 0.0
            for xi in data:
                u = (x - xi) / h
                k = 0.5 if abs(u) <= 1.0 else 0.0
                total += k
            return total / (n * h)
        def cdf(x):
            total = 0.0
            for xi in data:
                u = (x - xi) / h
                if u < -1.0:
                    k = 0.0
                elif u > 1.0:
                    k = 1.0
                else :
                    k =(u + 1) / 2
                total += k
            return total / n
    elif kernel == 'triangular':
        def density(x):
            total = 0.0
            for xi in data:
                u = (x - xi) / h
                k = 1.0 - abs(u) if abs(u) <= 1.0 else 0.0
                total += k
            return total / (n * h)
        def cdf(x):
            total = 0.0
            for xi in data:
                u = (x - xi) / h
                if u < -1.0:
                    k = 0.0
                elif u > 1.0:
                    k = 1.0
                elif u < 0.0:
                    k = 0.5 * (u + 1) * (u + 1)
                else :
                    k = 1.0 - 0.5 * (1 - u) * (1 - u)
                total += k
            return total / n
    elif kernel == 'parabolic':
        def density(x):
            total = 0.0
            for xi in data:
                u = (x - xi) / h
                k = (1.0 - u * u) if abs(u) <= 1.0 else 0.0
                total += k
            return (total * 0.75) / (n * h)
        def cdf(x):
            total = 0.0
            for xi in data:
                u =(x - xi) / h
                if u < -1.0:
                    k = 0.0
                elif u > 1.0:
                    k = 1.0
                else :
                    k = 0.5 + 0.75 * u - 0.25 * (u ** 3)
                total += k
            return total / n
    elif kernel == 'quartic':
        def density(x):
            total = 0.0
            for xi in data:
                u = (x - xi) / h
                k = (1.0 - u * u) ** 2 if abs(u) <= 1 else 0.0
                total += k
            return (total * 15) / (n * h * 16)
        def cdf(x):
            total = 0.0
            for xi in data:
                u = (x - xi) / h
                if u < -1.0:
                    k = 0.0
                elif u > 1.0:
                    k = 1.0
                else :
                    k = 0.5 + (15/16) * u - (5/8) * u**3 + (3/16) * u**5
                total += k
            return total / n
    elif kernel == 'triweight':
        def density(x):
            total = 0.0
            for xi in data:
                u = (x - xi) / h
                k = (1.0 - u * u) ** 3 if abs(u) <= 1.0 else 0.0
                total += k
            return (total * 35) / (n * h * 32)
        def cdf(x):
            total = 0.0
            for xi in data:
                u = (x - xi) / h
                if u < -1.0:
                    k = 0.0
                elif u > 1.0:
                    k = 1.0
                else :
                    k = 0.5 + (35/32) * u - (35/32) * u**3 + (21/32) * u**5 - (5/32) * u**7
                total += k
            return total / n
    elif kernel == 'cosine':
        def density(x):
            total = 0.0
            for xi in data:
                u = (x - xi) / h
                k = cos( (pi * u) / 2 ) if abs(u) <= 1.0 else 0.0
                total += k
            return (total * pi) / (n * h * 4)
        def cdf(x):
            total = 0.0
            for xi in data:
                u = (x - xi) / h
                if u < -1.0:
                    k = 0.0
                elif u > 1.0:
                    k = 1.0
                else :
                    k = 0.5 * (1.0 + sin(pi * u / 2))
                total += k
            return total / n
    else:
        raise StatisticsError("Attention kernel non valide")
    if not cumulative:
        return density
    return cdf
