# -*- coding: utf-8 -*-
#@author: Osona

#=== Importation des modules ===
import time
from math import pi, cos, log, exp, acos, sqrt

#=== Error ===

class RandomError(Exception):
    """Erreur spécifique aux fonctions de ce module"""
    pass

#=== Seed (LCG) ===

# paramètres du LCG
M : int = 2**32
B : int = 1664525
C : int = 1013904223

# état initial
state : int = int(time.time())

def seed(a : int = None):
    """Initialise le générateur LCG.

    Args:
        a (int, optional): Key qui va initialiser le générateur, sinon il utilise l'heure actuelle. Defaults to None.
        
    Raises:
        RandomError: Lorsque l'argument n'est ni None ni entier.
    """
    global state

    if a is None:
        state = int(time.time())
    elif type(a) != int:
        raise RandomError("Attention argument non entier")
    else:
        state = a
        
def getstate() -> int:
    """Renvoie l'état actuel du générateur.

    Returns:
        int: État actuel du générateur.
    """
    return state

def setstate(_state : int) -> None:
    """Met l'état interne du générateur à l'état *_state*.

    Args:
        _state (int): État dans lequel on veut mettre le générateur.

    Raises:
        RandomError: Lorsque *_state* n'est pas un entier.
    """
    if type(_state) != int:
        raise RandomError("Attention _state doit être un entier")
    global state
    state = _state
    

#=== Classique ===

def random() -> float:
    """Renvoie un flottant aléatoirement uniforme dans [0,1) par génération LGC.

    Returns:
        float: flottant aléatoirement uniforme dans [0,1).
    """
    global state

    state = (B * state + C) % M
    return state / M

#=== Fonctions pour des entiers ===

def randrange(start : int , stop : int = None, step : int = 1) -> int:
    """Renvoie un entier aléatoirement uniforme dans range(start, stop, step).
    Aussi randrange(10) renvoie randrange(0,10,1).

    Args:
        start (int): Borne inférieure du *range*.
        stop (int, optional): Borne supérieure du *range*. Defaults to None.
        step (int, optional): Pas du *range*. Defaults to 1.

    Raises:
        RandomError: Lorsque les arguments ne sont pas des entiers.
        RandomError: Lorsque *step* est nul.
        RandomError: Lorsque le *range* est vide.

    Returns:
        int: Entier aléatoirement uniforme dans range(start, stop, step)
    """
    if stop is None:
        stop = start
        start = 0
    if type(start) != int or type(stop) != int or type(step) != int:
        raise RandomError("Attention arguments non entiers.")
    if step == 0:
        raise RandomError("Attention *step* ne peut pas être nul.")
    if step > 0:
        n = (stop - start + step - 1) // step
    else:
        n = (stop - start + step + 1) // step
    if n <= 0:
        raise RandomError("Attention *range* vide pour randrange().")
    k = int(random() * n)
    return start + k * step

def randint(a : int, b : int) -> int:
    """Renvoie un élément entier aléatoirement uniforme dans [a,b]. Renvoie a si a=b.

    Args:
        a (int): Borne inférieure de l'ensemble.
        b (int): Borne supérieure de l'ensemble.

    Raises:
        RandomError: Lorsque les arguments ne sont pas des entiers.
        RandomError: Lorsque la borne inférieure est plus grande que la borne supérieure.

    Returns:
        int: Entier aléatoirement uniforme dans [a,b].
    """
    if type(a) != int or type(b) != int :
        raise RandomError("Attention les arguments ne sont pas entiers")
    if a > b:
        raise RandomError("Attention la borne inférieure est plus grande que la borne supérieure")
    elif a == b:
        return a
    else:
        return a + int(random() * (b - a + 1))

#=== Fonctions pour des séquences ===

def choice(L):
    """Renvoie un élément aléatoirement uniforme dans *L*.

    Args:
        L (sequence): Séquence dont on veut un élément uniforme.

    Raises:
        RandomError: Lorsque *L* est vide.

    Returns:
        _type_: Élément aléatoirement uniforme dans *L*.
    """
    n : int = len(L)
    if n == 0:
        raise RandomError("Attention l'argument *L* est vide") 
    return L[randrange(n)]

def shuffle(L) -> list :
    """Renvoie une liste copie de *L* mélangée par le mélange de Fisher-Yates. 

    Args:
        L (sequence): Séquence que l'on veut mélanger.

    Returns:
        list: Copie de *L* mélangée.
    """
    n : int = len(L)
    if n == 0:
        return []
    liste : list = []
    for x in L:
        liste.append(x)
    for i in range(n-1,0,-1):
        j=randint(0,i)
        liste[j],liste[i]=liste[i],liste[j]
    return liste

def sample(L, n : int) -> list:
    """Renvoie une liste de *n* éléments aléatoires de *L*.

    Args:
        L (sequence): Séquence dont on veut *n* éléments.
        n (int): Nombre d'éléments tirés aléatoirement de *L*.

    Raises:
        RandomError: Lorsque *n* n'est pas un entier.
        RandomError: Lorsque *n* est soit négatif ou nul, soit trop grand pour *L*.

    Returns:
        list: Liste de *n* éléments aléatoires de *L*.
    """
    if type(n) != int:
        raise RandomError("Attention n n'est pas un entier")
    if len(L) == 0:
        return []
    if n <= 0 or n > len(L):
        raise RandomError("Attention n doit être positif strictement et inférieur ou égal à la taille de *L*")
    return shuffle(L)[:n]

#=== Octets et Bits ===

def getrandbits(k: int) -> int:
    """Génère un nombre avec *k* bits aléatoires.

    Args:
        k (int): Nombre de bits aléatoire.

    Raises:
        RandomError: Lorsque *k* n'est pas entier ou est strictement négatif.

    Returns:
        int: Nombre avec *k* bits aléatoires.
    """
    if type(k) != int or k < 0:
        raise RandomError("Attention *k* doit être un entier positif ou nul")
    return randint(0, (1 << k) - 1)

def randbytes(n : int) -> bytes:
    """Génère *n* octets aléatoires.

    Args:
        n (int): Nombre d'octets aléatoire.

    Raises:
        RandomError: Lorsque *n* n'est pas entier ou est strictement négatif.

    Returns:
        bytes: *n* octets aléatoires.
    """
    if type(n) != int or n < 0:
        raise RandomError("Attention *n* doit être un entier positif")
    return getrandbits(n * 8).to_bytes(n, "little")

#=== Loi de distribution ===

def uniform(a : float, b : float) -> float:
    """Génère un flottant aléatoirement unforme dans [a,b).

    Args:
        a (float): Première borne de l'ensemble.
        b (float): Deuxième borne de l'ensemble.

    Returns:
        float: Flottant aléatoirement unforme dans [a,b).
    """
    if a == b:
        return a
    elif a > b:
        return b + (a - b) * random()
    else :
        return a + (b - a) * random()
    
def binomialvariate(n : int = 1, p : float = 0.5) -> int:
    """Génère un résultat aléatoire d'une succéssion de *n* épreuves indépendantes de Bernoulli de paramètre *p*.

    Args:
        n (int, optional): Nombre de répétition des épreuves. Defaults to 1.
        p (float, optional): Paramètre des épreuves. Defaults to 0.5.

    Raises:
        RandomError: Lorsque *n* n'est pas un entier positif.
        RandomError: Lorsque *p* ne vérifie pas *0 <= p <= 1*.

    Returns:
        int: Résultat aléatoire d'une succéssion de *n* épreuves indépendantes de Bernoulli de paramètre *p*.
    """
    if type(n) != int or n < 0:
        raise RandomError("Attention n n'est pas un entier positif")
    if n == 0:
        return 0
    if p < 0 or p > 1:
        raise RandomError("Attention p doit être compris entre 0 et 1")
    return sum(random() < p for _ in range(n))

def triangular(low : float, high : float, mode : float = None) -> float:
    """Génère un résultat aléatoire suivant une loi Triangulaire entre *low* et *high*  ainsi que de sommet *mode*.

    Args:
        low (float): Borne inférieure de la base du Tirangle.
        high (float): Borne supérieure de la base du Tirangle.
        mode (float, optional): Sommet du Triangle. Defaults to None.

    Raises:
        RandomError: Lorsque *high* est inférieur ou égal à *low*.
        RandomError: Lorsque *mode* n'est pas compris entre *high* et *low*.

    Returns:
        float: Résultat aléatoire suivant une loi Triangulaire entre *low* et *high*  ainsi que de sommet *mode*.
    """
    if high <= low:
        raise RandomError("Attention high doit être supérieur low")
    if mode is None:
        mode : float = (low + high) / 2
    if not (low <= mode <= high):
        raise RandomError("Attention mode doit être entre low et high")
    u : float = random()
    c : float = (mode - low) / (high - low)
    if u < c:
        return low + sqrt(u * (high - low) * (mode - low))
    else:
        return high - sqrt((1 - u) * (high - low) * (high - mode))

def geometric(p : float) -> int:
    """Génère un résultat aléatoire suivant une loi Géométrique de paramètre *p*.

    Args:
        p (float): Paramètre de la loi Géométrique

    Raises:
        RandomError: Lorsque *p* est négatif ou supérieur ou égal à 1.

    Returns:
        int: Résultat aléatoire suivant une loi Géométrique de paramètre *p*.
    """
    if p <= 0 or p >= 1:
        raise RandomError("Attention p doit être compris entre 0 et 1 exclus")    
    u : float = random()
    return int(log(1-u) / log(1-p)) + 1

def expovariate(lmbda : float = 1.0) -> float:
    """Génère un résultat aléatoire suivant une loi Exponentielle de paramètres *lmbda*.

    Args:
        lmbda (float, optional): Paramètre de la loi Exponentielle. Defaults to 1.0.

    Raises:
        RandomError: Lorsque *lmbda* est négatif.

    Returns:
        float: Résultat aléatoire suivant une loi Exponentielle de paramètre *lmbda*.
    """
    if lmbda <= 0.0:
        raise RandomError("Attention l'argument doit être strictement positif")
    return -log(1.0 - random()) / lmbda

def gammavariate(alpha : float, beta : float = 1.0) -> float:
    """Génère un résultat aléatoire suivant une loi Gamma de paramètres *alpha* et *beta*.

    Args:
        alpha (float): Paramètre strictement positif de forme (shape).
        beta (float, optional): Paramètre strictement positif d'échelle inverse (rate). Defaults to 1.0.

    Raises:
        RandomError: Lorsqu'*alpha* ou *beta* est négatif.

    Returns:
        float: Résultat aléatoire suivant une loi Gamma de paramètres *alpha* et *beta*.
    """
    if alpha <= 0.0 or beta <= 0.0:
        raise RandomError("Attention alpha et beta doivent être strictement positifs")
    if alpha < 1.0:     # Transformation d'Ahrens & Dieter
        return gammavariate(alpha + 1.0, beta) * (random() ** (1.0 / alpha))
    d : float = alpha - 1.0 / 3.0
    c : float = 1.0 / (9 * d) ** 0.5
    while True:
        z : float = (-2.0 * log(random())) ** 0.5 * cos(2 * pi * random())
        v : float = (1 + c * z) ** 3
        if v > 0:
            u = random()
            if u < 1 - 0.0331 * (z ** 4) or log(u) < 0.5 * z * z + d * (1 - v + log(v)):
                return d * v / beta
            
def betavariate(alpha : float, beta : float) -> float:
    """Génère une résultat aléatoire suivant une loi Beta de paramètres *alpha* et *beta*, construite à partir de deux lois Gamma indépendantes.

    Args:
        alpha (float): Paramètre strictement positif de forme (shape) de la première loi Gamma.
        beta (float): Paramètre strictement positif de forme (shape) de la seconde loi Gamma.

    Raises:
        RandomError: Lorsqu'*alpha* ou *beta* est négatif.

    Returns:
        float: Résultat aléatoire suivant une loi Beta de paramètres *alpha* et *beta*.
    """
    if alpha <= 0.0 or beta <= 0.0:
        raise RandomError("Attention alpha et beta doivent être strictement positifs")
    x : float = gammavariate(alpha, 1.0)
    y : float = gammavariate(beta, 1.0)
    while x + y == 0.0:
        x = gammavariate(alpha, 1.0)
        y = gammavariate(beta, 1.0)
    return x / (x + y)

def gauss(mu : float = 0.0, sigma : float = 1.0) -> float:
    """Génère un résultat aléatoire suivant une loi Normale de paramètres *mu* et *sigma*.
    Utilise la transformation de Box-Muller (forme trigonométrique).

    Args:
        mu (float, optional): Moyenne de la loi Normale. Defaults to 0.0.
        sigma (float, optional): Écart-type de la loi Normale. Defaults to 1.0.

    Returns:
        float: Résultat aléatoire suivant une loi Normale de paramètres *mu* et *sigma*.
    """
    x2pi = random() * 2 * pi
    g2rad = (-2.0 * log(1.0 - random())) ** 0.5
    return mu + cos(x2pi) * g2rad * sigma

def lognormvariate(mu : float, sigma : float) -> float:
    """Génère un résultat aléatoire suivant une loi Log-Normale de paramètres *mu* et *sigma*.

    Args:
        mu (float): Moyenne de la loi Normale.
        sigma (float): Écart-type de la loi Normale.

    Returns:
        float: Résultat aléatoire suivant une loi Log-Normale de paramètres *mu* et *sigma*.
    """
    return exp(gauss(mu, sigma))

def normalvariate(mu : float = 0.0, sigma : float = 1.0) -> float:
    """Génère un résultat aléatoire suivant une loi Normale de paramètres *mu* et *sigma*.
    Utilise la méthode du ratio d'uniformes de Kinderman & Monahan.

    Args:
        mu (float, optional): Moyenne de la loi Normale. Defaults to 0.0.
        sigma (float, optional): Écart-type de la loi Normale. Defaults to 1.0.

    Returns:
        float: Résultat aléatoire suivant une loi Normale de paramètres *mu* et *sigma*.
    """
    NVCONST : float = 4 * exp(-0.5) / (2.0 ** 0.5)
    while True:
        u1 : float = random()
        u2  : float = 1.0 - random()
        z : float = NVCONST * (u1 - 0.5) / u2
        x = z * z / 4.0
        if x <= -log(u2):
            return mu + sigma * z

def paretovariate(alpha : float) -> float:
    """Génère un résultat aléatoire suivant une distribution de Pareto de paramètre *alpha*.

    Args:
        alpha (float): Paramètre de forme (shape) de la distribution de Pareto.
        
    Raises:
        RandomError: Lorsqu'*alpha* est négatif.

    Returns:
        float: Résultat aléatoire suivant une distribution de Pareto de paramètre *alpha*.
    """
    if alpha <= 0.0:
        raise RandomError("Attention alpha doit être strictement positif")
    u : float = 1.0 - random()
    return u ** (-1.0 / alpha)

def weibullvariate(alpha : float, beta : float) -> float:
    """Génère un résultat aléatoire suivant une distribution de Weibull de paramètres *alpha* et *beta*.

    Args:
        alpha (float): Paramètre d'échelle (scale) de la distribution de Weibull.
        beta (float): Paramètre de forme (shape) de la distribution de Weibull.

    Raises:
        RandomError: Lorsqu'*alpha* ou *beta* est négatif.

    Returns:
        float: Résultat aléatoire suivant une distribution de Weibull de paramètres *alpha* et *beta*.
    """
    if alpha <= 0.0 or beta <= 0.0:
        raise RandomError("Attention alpha et beta doivent etre positifs")
    u : float = 1.0 - random()   # évite log(0) si u=1 exactement
    return beta * (-log(u)) ** (1.0 / alpha)

def vonmisesvariate(mu : float, kappa : float) -> float:       
    """Génère un résultat aléatoire suivant une distribution de Von Mises de paramètres *mu* et *kappa*.

    Args:
        mu (float): Paramètre de l'angle moyen (radian) de la distribution de Von Mises.
        kappa (float): Paramètre de concentration de la distribution de Von Mises.

    Returns:
        float: Résultat aléatoire suivant une distribution de Von Mises de paramètres *mu* et *kappa*.
    """
    if kappa <= 1e-6:
        return 2 * pi * random()
    s : float = 0.5 / kappa
    r : float = s + sqrt(1.0 + s * s)
    while True:
        u1 : float = random()
        z : float = cos(pi * u1)
        d : float = z / (r + z)
        u2 : float = random()
        if u2 < 1.0 - d * d or u2 <= (1.0 - d) * exp(d):
            break
    q : float = 1.0 / r
    f : float = (q + z) / (1.0 + q * z)
    u3 : float = random()
    if u3 > 0.5:
        theta : float = (mu + acos(f)) % (2 * pi)
    else:
        theta : float = (mu - acos(f)) % (2 * pi)
    return theta
