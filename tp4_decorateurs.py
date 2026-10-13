import time
from functools import wraps

def chronometrer(fonction):
    @wraps(fonction)
    def enveloppe(*args, **kwargs):
        debut = time.perf_counter()
        resultat = fonction(*args, **kwargs)
        fin = time.perf_counter()
        print(f"{fonction.__name__} a pris {fin - debut:.2f} s")
        return resultat
    return enveloppe

@chronometrer
def lente():
    time.sleep(1)
    return "fini"


def majuscules(fonction):
    @wraps(fonction)
    def enveloppe(*args, **kwargs):
        resultat = fonction(*args, **kwargs)
        return resultat.upper() if isinstance(resultat, str) else resultat
    return enveloppe


def compter_appels(fonction):
    @wraps(fonction)
    def enveloppe(*args, **kwargs):
        enveloppe.appels += 1
        return fonction(*args, **kwargs)
    enveloppe.appels = 0
    return enveloppe


def verifier_positifs(fonction):
    @wraps(fonction)
    def enveloppe(*args, **kwargs):
        for arg in args:
            if isinstance(arg, (int, float)) and arg < 0:
                raise ValueError("Les arguments numériques doivent être positifs")
        for k, v in kwargs.items():
            if isinstance(v, (int, float)) and v < 0:
                raise ValueError(f"L'argument {k} doit être positif")
        return fonction(*args, **kwargs)
    return enveloppe

def chronometrer_param(unite="s"):
    def decorateur(fonction):
        @wraps(fonction)
        def enveloppe(*args, **kwargs):
            debut = time.perf_counter()
            resultat = fonction(*args, **kwargs)
            fin = time.perf_counter()
            duree = (fin - debut) * 1000 if unite == "ms" else (fin - debut)
            print(f"{fonction.__name__} a pris {duree:.2f} {unite}")
            return resultat
        return enveloppe
    return decorateur


def memoriser(fonction):
    cache = {}
    @wraps(fonction)
    def enveloppe(*args, **kwargs):
        cle = (args, tuple(kwargs.items()))
        if cle not in cache:
            cache[cle] = fonction(*args, **kwargs)
        return cache[cle]
    return enveloppe