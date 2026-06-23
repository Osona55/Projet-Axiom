# -*- coding: utf-8 -*-
# @autor : Osona

#===Importation des modules===
from math import pi, exp, log, sqrt, cos, sin, cosh, sinh, erf, arctan

#===Error===

class StatisticsError(Exception):
    """"Erreur spécifique aux fonctions de ce module"""
    pass

#===Moyennes===

def mean(data):
    """Renvoie la moyenne arithmétique de *data* sous la forme d'un float, ou un int dans les cas possibles.

    Args:
        data (iterable): Échantillon dont on veut la moyenne arithmétique.

    Raises:
        ValueError: Lorsque *data* est vide.

    Returns:
        int or float: Moyenne arithmétique de *data*.
    """
    n : int = len(data)
    if n == 0:
        raise StatisticsError("Attention entré vide")
    mean : float = sum(data)/n
    if mean % 1 == 0:
        return int(mean)
    return mean

def fmean(data, weights = None) -> float :
    """Renvoie la moyenne arithmétique de *data* pondérée par *weights* sous la forme d'un float.

    Args:
        data (iterable): Échantillon dont on veut la moyenne arthmétique pondérée.
        weights (iterable, optional): Poids de la moyenne. Defaults to None.

    Raises:
        StatisticsError: Lorsque *data* est vide.
        StatisticsError: Lorsque *weights* est vide.
        StatisticsError: Lorsque *data* et *weights* n'ont pas la même dimension.

    Returns:
        float: Moyenne arithmétique de *data* pondérée par *weights*.
    """
    n : int = len(data)
    if n == 0:
        raise StatisticsError("Attention entré vide")
    if weights is None:
        return sum(data)/n
    m : int = len(weights)
    if m == 0:
        raise StatisticsError("Attention entré vide")
    if n != m:
        raise StatisticsError("Attention entrées avec des dimensions différentes")    
    somme = 0
    for i in range(n):
        somme += data[i] * weights[i]
    return somme / sum(weight)

def geometric_mean(data) -> float :
    """Renvoie la moyenne géométrique de *data* sous la forme d'un float.

    Args:
        data (iterable): Échantillon dont on veut la moyenne géométrique.

    Raises:
        StatisticsError: Lorsque *data* est vide.
        StatisticsError: Lorsqu'une valeur de *data* est nulle ou négative.

    Returns:
        float: Moyenne géométrique de *data*.
    """
    n : int = len(data)
    if n==0:
        raise StatisticsError("Attention entré vide")
    p : float = 1.0
    for x in data:
        if x <= 0:
            raise StatisticsError("Attention valeur négative ou nulle en entré")
        p*=x
    return p**(1/n)
    
def harmonic_mean(data, weights = None) -> float :
    """Renvoie la moyenne harmonique de *data* pondérée par *weights* sous la forme d'un float.

    Args:
        data (iterable): Échantillon dont on veut la moyenne harmonique pondérée.
        weights (iterable, optional): Poids de la moyenne. Defaults to None.

    Raises:
        StatisticsError: Lorsque *data* est vide.
        StatisticsError: Lorsque *data* et *weights* n'ont pas la même dimension.
        StatisticsError: Lorsqu'un poids est négatif.

    Returns:
        float: Moyenne harmonique de *data* pondérée par *weights*.
    """
    n : int = len(data)
    if n == 0:
        raise StatisticsError("Attention entré vide")
    if weights is None:
        somme : float = 0
        for x in data:
            if x == 0:
                return 0
            somme += 1/x
        return n / somme
    m : int = len(weights)
    if n!=m:
        raise StatisticsError("Attention entrées avec des dimensions différentes")
    somme : float = 0
    s_weights : float = 0
    for i in range(n):
        x = data[i]
        w = weights[i]
        if x == 0:
            return 0
        if w<0:
            raise StatisticsError("Attention poids négatif")
        somme += (1/x)*w
        s_weights += w
    return s_weights / somme

#===Médianes===

def median(data):
    """Renvoie la médiane de *data*.

    Args:
        data (iterable): Échantillon dont on veut la médiane.

    Raises:
        StatisticsError: Lorsque *data* est vide.

    Returns:
        Any: Médiane de *data*.
    """
    n : int = len(data)
    if n == 0:
        raise StatisticsError("Attention entré vide")
    L : list = sorted(data)
    mid : int = n // 2
    if n%2 == 0:
        return (L[mid-1]+L[mid])/2
    return L[mid]

def median_low(data):
    """Renvoie la médiane basse de *data*, fonctionne même si les données ne sont pas numériques mais peuvent être triées.

    Args:
        data (iterable): Échantillon dont on veut la médiane basse.

    Raises:
        StatisticsError: Lorsque *data* est vide.

    Returns:
        Any: Médiane basse de *data*.
    """
    n : int = len(data)
    if n==0:
        raise StatisticsError("Attention entré vide")
    L=sorted(data)
    mid : int = n // 2
    if n%2==0:
        return L[mid-1]
    return L[mid]

def median_high(data):
    """Renvoie la médiane haute de *data*, fonctionne même si les données ne sont pas numériques mais peuvent être triées.

    Args:
        data (iterable): Échantillon dont on veut la médiane haute.

    Raises:
        StatisticsError: Lorsque *data* est vide.

    Returns:
        Any: Médiane haute de *data*.
    """
    n: int = len(data)
    if n == 0:
        raise StatisticsError("Attention entré vide")
    L=sorted(data)
    mid : int = n // 2
    return L[mid]

def median_grouped(data, interval=1.0):
    """Renvoie la médiane groupée d'un ensemble de données *data*.

    Args:
        data (_type_): Ensemble des observations numériques. Les données ne doivent pas être vides.
        interval (float, optional): Largeur supposée des classes. Doit être strictement positive. Defaults to 1.0.

    Raises:
        StatisticsError: Lorsque *data* est vide.

    Returns:
        _type_: Médiane estimée.
    """
    n : int = len(data)
    if n == 0:
        raise StatisticsError("Attention entré vide")
    DATA=sorted(data)
    m = DATA[n // 2]
    L = m - interval / 2
    f_m = DATA.count(m)
    CF = sum(1 for v in DATA if v < m)
    return L + ((n/2 - CF) / f_m) * interval

#===Mode===

def mode(data):
    """Renvoie la valeur la plus représentée (la première apparue si il y en a plusieurs) dans l'échantillon *data*.

    Args:
        data (iterable of hashable): Échantillon dont on veut le mode.

    Raises:
        StatisticsError: Lorsque *data* est vide.

    Returns:
        _type_: Mode (valeur la plus représentée) de *data*.
    """
    n : int = len(data)
    if n==0:
        raise StatisticsError("Attention entré vide")
    D : dict = {}
    for x in data:
        if x not in D:
            D[x]=1
        else:
            D[x]+=1
    m=max(D.values())
    for a,b in D.items():
        if b==m:
            return a
        
def multimode(data) -> list :
    """Renvoie la liste des modes de *data* ou une liste vide si *data* est vide.

    Args:
        data (iterable of hashable): Échantillon dont on veut les modes.

    Returns:
        list: Liste des modes de *data*.
    """
    n : int = len(data)
    if n == 0:
        return list()
    D : dict = {}
    for x in data:
        if x not in D:
            D[x]=1
        else:
            D[x]+=1
    m=max(D.values())
    L : list = []
    for a,b in D.items():
        if b==m:
            L.append(a)
    return L

#===Variance et écart-type===

def pvariance(data, mu = None) -> float :
    """Renvoie la variance de la population *data*.

    Args:
        data (iterable): Population de données.
        mu (int or float, optional): Moyenne de la population *data*. Defaults to None.

    Raises:
        StatisticsError: Lorsque *data* est vide.

    Returns:
        float: Variance de la population.
    """
    n : int = len(data)
    if n == 0:
        raise StatisticsError("Attention entré vide")
    if mu is None:
        mu = fmean(data)
    return sum((x-mu)**2 for x in data) / n

def variance(data, xbar = None) -> float :    #Variance avec la correction de Bessel
    """Renvoie la variance de l'échantillon de la population *data*.

    Args:
        data (iterable): Échantillon de la population de données.
        xbar (int or float, optional): Moyenne de l'échantillon *data*. Defaults to None.

    Raises:
        StatisticsError: Lorsque *data* est vide.

    Returns:
        float: Variance de l'échantillon de population *data*.
    """
    n : int = len(data)
    if n < 2:
        raise StatisticsError("Attention taille de l'entré trop petite")
    if xbar is None:
        xbar = fmean(data)
    return sum((x-xbar)**2 for x in data) / (n-1)

def pstdev(data, mu = None) -> float :
    """Renvoie l'écart-type de la population *data*.

    Args:
        data (iterable): Population de données.
        mu (int or float, optional): Moyenne de la population *data*. Defaults to None.

    Raises:
        StatisticsError: Lorsque *data* est vide.

    Returns:
        float: Écart-type de la population *data*.
    """
    return sqrt(pvariance(data, mu))

def stdev(data, xbar = None) -> float:        #Écart-type avec la correction de Bessel
    """Renvoie l'écart-type de l'échantillon de la population *data*.

    Args:
        data (iterable): Échantillon de la population de données.
        xbar (int or float, optional): Moyenne de l'échantillon *data*. Defaults to None.

    Raises:
        StatisticsError: Lorsque *data* est vide.

    Returns:
        float: ÉCcart-type de l'échantillon de population *data*.
    """
    return sqrt(variance(data, xbar))

#===Entre deux entrées===

def covariance(x, y, type : str = 'sample') -> float :
    """Renvoie la covariance entre les deux échantillons *x* et *y*.

    Args:
        x (iterable): Premier échantillon de données.
        y (iterable): Deuxième échantillon de données.
        type (str, optional): Type de m'échantillon utilisé. Defaults to 'sample'.

    Raises:
        StatisticsError: Lorsque les échantillons sont trop petits.
        StatisticsError: Lorsque les échantillons n'ont pas la même dimension.
        StatisticsError: Lorsque *type* est non valide.

    Returns:
        float: Covariance entre *x* et *y*.
    """
    n : int = len(x)
    m : int = len(y)
    if n < 2 or m < 2 :
        raise StatisticsError("Attention taille de l'entré trop petite")
    if n != m :
        raise StatisticsError("Attention entrées avec des dimensions différentes")
    xbar : float = fmean(x)
    ybar : float = fmean(y)
    if type == 'sample':    #Correction de Bessel
        return sum((x[i]-xbar)*(y[i]-ybar) for i in range(n)) / (n-1)
    elif type == 'population':
        return sum((x[i]-xbar)*(y[i]-ybar) for i in range(n)) / n
    else :
        raise StatisticsError("Attention type non valide, method doit être 'sample' ou 'population'")

def correlation(x, y, method : str = 'linear') -> float :
    """Renvoie la covariance de Pearson ou de Spearman entre les deux échantillons *x* et *y*.

    Args:
        x (iteerable): Premier échantillon de données.
        y (iterable): Deuxième échantillon de données.
        method (str, optional): Represente le type de corrélation utilisée 'linear' -> Pearson, 'ranked' -> Spearman. Defaults to 'linear'.

    Raises:
        StatisticsError: Lorsque les échantillons sont trop petits.
        StatisticsError: Lorsque les échantillons n'ont pas la même dimension.
        ZeroDivisionError: Lorsque une des deux entrées est constante.

    Returns:
        float: Correlation de Pearson ou de Spearman de *x* et *y*.
    """
    n : int = len(x)
    m : int = len(y)
    if n < 2 or m < 2 :
        raise StatisticsError("Attention taille de l'entré trop petite")
    if n != m :
        raise StatisticsError("Attention entrées avec des dimensions différentes")
    if method == 'linear':      #Corrélation de Pearson
        std_x : float = stdev(x)
        std_y : float = stdev(y)
        if std_x == 0.0 or std_y == 0.0 :
            raise ZeroDivisionError("Attention une variable est constante")
        return covariance(x,y) / (std_x*std_y)
    elif method == 'ranked':     #Corrélation de Spearman
        def rankdata(data) -> list :
            p : int = len(data)
            sorted_data : list = sorted(enumerate(data), key=lambda x: x[1])
            ranks : list = [0] * p
            i : int = 0
            while i < p:
                j : int = i
                while j < p - 1 and sorted_data[j][1] == sorted_data[j + 1][0]:
                    j += 1
                avg_rank : float = (i + j + 2) / 2.0
                for k in range(i, j + 1):
                    ranks[sorted_data[k][0]] = avg_rank
                i = j + 1
            return ranks
        ranks_x  : list = rankdata(x)
        ranks_y  : list = rankdata(y)
        return correlation(ranks_x, ranks_y, method = 'linear')

def linear_regression(x, y, proportional : bool = False) -> float:
    """Renvoie la pente et l'intersection à zéro de la régréssion linéaire de *x* et *y*.
    Soit a et b dans l'équation y = a*x+b .

    Args:
        x (iterable): Premier échantillon de données.
        y (iterable): Deuxième échantillon de données.
        proportional (bool, optional): True si *x* et *y* sont proportionnels, False si non ou si on ne sait pas. Defaults to False.

    Raises:
        StatisticsError: Lorsque les échantillons n'ont pas la même dimension.
        StatisticsError: Lorsque la taille des échatillons n'est pas assez grande.
        ZeroDivisionError: Lorsque *x* est constant, sa variance est nulle.
        ZeroDivisionError: Lorsque *x* est un échantillon de zéro.

    Returns:
        float,float: Pente et intersection à zéro de la régression linéaire.
    """
    n : int = len(x)
    if n != len(y):
        raise StatisticsError("Attention aux dimensions")
    if n < 2:
        raise StatisticsError("Attention taille de l'entré trop petite")
    if not proportional:
        var_x : float = variance(x)
        if var_x == 0:
            raise ZeroDivisionError("Attention x est constant")
        slope : float = covariance(x,y)/var_x
        intercept : float = fmean(y)-slope*fmean(x)
        return slope, intercept
    denom=sum(xi*xi for xi in x)
    if denom == 0:
        raise ZeroDivisionError("Attention tous les x sont égaux à zéro")
    slope = sum(xi*yi for xi, yi in zip(x, y))/denom
    intercept = 0
    return slope, intercept

#===Quantiles===

def quantiles(data, n : int = 4, method : str = 'exclusive') -> list :
    """Divise *data* en *n* groupes de même probabilité et renvoie la liste des *n-1* bornes. 

    Args:
        data (iterable): Échantillon de donnés.
        n (int, optional): Nombre de groupe en lesquels on veut diviser *data*. Defaults to 4.
        method (str, optional): Méthode qui va être utilisée pour diviser *data*. Defaults to 'exclusive'.

    Raises:
        StatisticsError: Lorsque la taille de l'échatillon *data* n'est pas assez grande.
        StatisticsError: Lorsque n n'est pas un entier non nul.
        StatisticsError: Lorsque la taille de l'échatillon *data* n'est pas assez grande par rapport à *n*.
        StatisticsError: Lorsque *method* n'est pas valide.

    Returns:
        list: Liste des bornes des *n* groupes.
    """
    N  : int = len(data)
    if N < 2 :
        raise StatisticsError("Attention taille de l'entré trop petite")
    if n < 1 or type(n) != int:
        raise StatisticsError("n doit être un entier non nul positif")
    if n > N :
        raise StatisticsError("Attention taille de l'entré trop petite par rapport à n ")
    L : list = sorted(data)
    result : list = []
    for i in range(1,n):
        p : float = i/n
        if method == 'inclusive':
            r : float = p * (N - 1) + 1
        elif method == 'exclusive':
            r : float = p * (N + 1)
        else:
            raise StatisticsError("Attention method non valide, method doit être 'inclusive' ou 'exclusive'")
        k : int = int(r)        # partie entière
        d : float = r - k       # partie décimale
        if k <= 0:
            q = L[0]
        elif k >= N:
            q = L[-1]
        else:
            q = L[k-1] + d * (L[k] - L[k-1])
        result.append(q)
    return result

#===Kernel===

def kde(data, h, kernel : str = 'normal', cumulative : bool = False) :
    """Renvoie une fonction de distribution continue ou une fonction de distribution cumulative (CDF) depuis des données discrètes.

    Args:
        data (iterable): Échantillon de donnés.
        h (int or float): Bande-passante controlant la régularité de la fonction renvoyée.
        kernel (str, optional): Nature du noyau qui va être utilisé. Defaults to 'normal'.
        cumulative (bool, optional): _description_. Defaults to False.

    Raises:
        StatisticsError: Lorsque *data* est vide.
        StatisticsError: Lorsque *h* est négatif ou nul.
        StatisticsError: Lorsque *kernel* n'est pas valide.

    Returns:
        function: Fonction de distribution ou fonction de distribution cumulative (CDF).
    """
    n : int = len(data)
    if n == 0:
        raise StatisticsError("Attention entrée vide")
    if h <= 0:
        raise StatisticsError("h doit être strictement positif")
    if kernel == 'normal':          #Kernel (noyau) normal ou gaussien
        def density(x):
            total : float = 0.0
            for xi in data:
                u : float = (x - xi) / h
                k : float = exp(-0.5 * u * u) / sqrt(2 * pi)
                total += k
            return total / (n * h)
        def cdf(x):
            total : float = 0.0
            for xi in data:
                u : float = (x - xi) / h
                k : float = 0.5 * (1.0 + erf(u / sqrt(2.0)))
                total += k
            return total / n
    elif kernel == 'logistic':      #Kernel (noyau) logistique
        def density(x):
            total : float = 0.0
            for xi in data:
                u : float = (x - xi) / h
                t : float = exp(-u)
                k : float = t / ((1 + t) ** 2)
                total += k
            return total / (n * h)
        def cdf(x):
            total : float = 0.0
            for xi in data:
                u : float = (x - xi) / h
                k : float = 1.0 / (1.0 + exp(-u))
                total += k
            return total / n
    elif kernel == 'sigmoid':       #Kernel (noyau) sigmoid
        def density(x):
            total : float = 0.0
            for xi in data:
                u : float = (x - xi) / h
                k : float = 1.0 / (pi * cosh(u))
                total += k
            return total / (n * h)
        def cdf(x):
            total : float = 0.0
            for xi in data:
                u : float = (x - xi) / h
                k : float = 0.5 + arctan(sinh(u)) / pi
                total += k
            return total / n
    elif kernel == 'rectangular':   #Kernel (noyau) rectangulaire ou uniform
        def density(x):
            total : float = 0.0
            for xi in data:
                u : float = (x - xi) / h
                k : float = 0.5 if abs(u) <= 1 else 0.0
                total += k
            return total / (n * h)
        def cdf(x):
            total : float = 0.0
            for xi in data:
                u : float = (x - xi) / h
                if u < -1:
                    k : float = 0.0
                elif u > 1 :
                    k : float = 1.0
                else :
                    k : float = (u + 1) / 2
                total += k
            return total / n
    elif kernel == 'triangular':    #Kernel (noyau) triangulaire
        def density(x):
            total : float = 0.0
            for xi in data:
                u : float = (x - xi) / h
                k : float = 1.0 - abs(u) if abs(u) <= 1 else 0.0
                total += k
            return total / (n * h)
        def cdf(x):
            total : float = 0.0
            for xi in data:
                u : float = (x - xi) / h
                if u < -1:
                    k : float = 0.0
                elif u > 1 :
                    k : float = 1.0
                elif u < 0 :
                    k : float = (u + 1) * (u + 1) / 2
                else :
                    k : float = 1.0 - (u + 1) * (u + 1) / 2
                total += k
            return total / n
    elif kernel == 'parabolic':     #Kernel (noyau) parabolique ou Epanechnikov
        def density(x):
            total : float = 0.0
            for xi in data:
                u : float = (x - xi) / h
                k : float = (1.0 - u * u) if abs(u) <= 1 else 0.0
                total += k
            return (total * 0.75) / (n * h)
        def cdf(x):
            total : float = 0.0
            for xi in data:
                u : float = (x - xi) / h
                if u < -1:
                    k : float = 0.0
                elif u > 1 :
                    k : float = 1.0
                else :
                    k : float = 0.5 + 0.75 * u - 0.25 * (u ** 3)
                total += k
            return total / n
    elif kernel == 'quartic':       #Kernel (noyau) quadratique
        def density(x):
            total : float = 0.0
            for xi in data:
                u : float = (x - xi) / h
                k : float = (1.0 - u * u) ** 2 if abs(u) <= 1 else 0.0
                total += k
            return (total * 15) / (n * h * 16)
        def cdf(x):
            total : float = 0.0
            for xi in data:
                u : float = (x - xi) / h
                if u < -1:
                    k : float = 0.0
                elif u > 1 :
                    k : float = 1.0
                else :
                    k : float =  0.5 + (5/8) * u - (5/4) * u**3 + (3/8) * u**5
                total += k
            return total / n
    elif kernel == 'triweight':     #Kernel (noyau) cubique
        def density(x):
            total : float = 0.0
            for xi in data:
                u : float = (x - xi) / h
                k : float = (1.0 - u * u) ** 3 if abs(u) <= 1 else 0.0
                total += k
            return (total * 35) / (n * h * 32)
        def cdf(x):
            total : float = 0.0
            for xi in data:
                u : float = (x - xi) / h
                if u < -1:
                    k : float = 0.0
                elif u > 1 :
                    k : float = 1.0
                else :
                    k : float =  0.5 + (35/32) * u - (35/32) * u**3 + (21/32) * u**5 - (5/32) * u**7
                total += k
            return total / n
    elif kernel == 'cosine':        #Kernel (noyau) sinusoïdal
        def density(x):
            total : float = 0.0
            for xi in data:
                u : float = (x - xi) / h
                k : float = cos( (pi * u) / 2 ) if abs(u) <= 1 else 0.0
                total += k
            return (total * pi) / (n * h * 4)
        def cdf(x):
            total : float = 0.0
            for xi in data:
                u : float = (x - xi) / h
                if u < -1:
                    k : float = 0.0
                elif u > 1 :
                    k : float = 1.0
                else :
                    k : float =  0.5 * (1.0 + sin(pi * u / 2))
                total += k
            return total / n
    else:
        raise StatisticsError("Attention kernel non valide")
    if not cumulative:
        return density
    return cdf
