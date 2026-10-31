import hashlib
import requests
from Crypto.Hash import MD4

URL_RANGE = "https://api.pwnedpasswords.com/range/"
URL_BREACHES = "https://haveibeenpwned.com/api/v3/breaches"
CABECERAS = {"user-agent": "practica-paradigmas"}

ERRORES = {
    400: "Peticion incorrecta",
    404: "Recurso no encontrado",
    429: "Demasiadas peticiones, espera un momento",
    503: "Servicio no disponible",
}