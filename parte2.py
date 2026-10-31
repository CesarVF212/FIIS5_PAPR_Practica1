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

def hash_sha1(contrasena):
    return hashlib.sha1(contrasena.encode("utf-8")).hexdigest().upper()


def hash_ntlm(contrasena):
    return MD4.new(contrasena.encode("utf-16le")).hexdigest().upper()


MODOS_HASH = {
    "1": (hash_ntlm, "?mode=ntlm"),
    "2": (hash_sha1, ""),
}


def mensaje_error(codigo):
    return ERRORES.get(codigo, f"Error inesperado (codigo {codigo})")


def hacer_peticion(url, callback_ok, callback_error):
    try:
        respuesta = requests.get(url, headers=CABECERAS, timeout=10)

    # CASO: Fallo de conexión.
    except requests.exceptions.RequestException:
        return callback_error("No se pudo conectar con el servidor")

    # CASO: Acierto.
    if respuesta.status_code == 200:
        return callback_ok(respuesta)

    # Caso: Error.
    return callback_error(mensaje_error(respuesta.status_code))


def obtener_cuenta(texto, sufijo):
    coincidencias = list(filter(lambda linea: linea.split(":")[0] == sufijo, texto.splitlines()))
    return int(coincidencias[0].split(":")[1]) if coincidencias else 0


def mensaje_contrasena(cuenta):
    if cuenta == 0:
        return "La contrasena no aparece en ninguna filtracion"
    return f"La contrasena ha aparecido {cuenta} veces en filtraciones"


def comprobar_contrasena(contrasena, funcion_hash, parametro):
    hash_completo = funcion_hash(contrasena)
    prefijo = hash_completo[:5]
    sufijo = hash_completo[5:]

    return hacer_peticion(
        f"{URL_RANGE}{prefijo}{parametro}",
        lambda respuesta: mensaje_contrasena(obtener_cuenta(respuesta.text, sufijo)),
        lambda mensaje: f"Error: {mensaje}",
    )


def mensaje_brechas(brechas):

    if not brechas:
        return "No hay filtraciones asociadas a este dominio"

    lineas = map(lambda b: f"- {b['Name']} ({b['BreachDate']}): {b['PwnCount']} cuentas", brechas)
    return "\n".join(lineas)


def comprobar_dominio(dominio):

    return hacer_peticion(
        f"{URL_BREACHES}?Domain={dominio}",
        lambda respuesta: mensaje_brechas(respuesta.json()),
        lambda mensaje: f"Error: {mensaje}",
    )


def modo_contrasenas():

    opcion = input("Formato del hash (1: Windows NTLM, 2: estandar SHA1): ")

    if opcion not in MODOS_HASH:
        print("Opcion no valida")
        return

    contrasena = input("Contrasena: ")
    funcion_hash, parametro = MODOS_HASH[opcion]

    print(comprobar_contrasena(contrasena, funcion_hash, parametro))


def modo_dominios():

    dominio = input("Dominio: ")
    print(comprobar_dominio(dominio))


MODOS = {
    "1": modo_contrasenas,
    "2": modo_dominios,
}


def main():

    opcion = input("Modo (1: contrasenas, 2: dominios): ")

    if opcion not in MODOS:
        print("Opcion no valida")
        return

    MODOS[opcion]()


def pruebas():

    print("hash_sha1")
    print(hash_sha1("password"))
    print(hash_sha1("123456"))
    print(hash_sha1("admin"))
    print(hash_sha1(""))
    print(hash_sha1("qwerty"))

    print("\nhash_ntlm")
    print(hash_ntlm("password"))
    print(hash_ntlm("123456"))
    print(hash_ntlm("admin"))
    print(hash_ntlm(""))
    print(hash_ntlm("qwerty"))

    print("\nmensaje_error")
    print(mensaje_error(400))
    print(mensaje_error(404))
    print(mensaje_error(429))
    print(mensaje_error(503))
    print(mensaje_error(500))

    print("\nobtener_cuenta")
    texto = "AAA:3\nBBB:10\nCCC:1"
    print(obtener_cuenta(texto, "AAA"))
    print(obtener_cuenta(texto, "BBB"))
    print(obtener_cuenta(texto, "CCC"))
    print(obtener_cuenta(texto, "DDD"))
    print(obtener_cuenta("", "AAA"))

    print("\nmensaje_contrasena")
    print(mensaje_contrasena(0))
    print(mensaje_contrasena(1))
    print(mensaje_contrasena(25))
    print(mensaje_contrasena(1000))
    print(mensaje_contrasena(3))

    print("\nhacer_peticion")
    print(hacer_peticion(f"{URL_RANGE}5BAA6", lambda r: r.status_code, lambda m: m))
    print(hacer_peticion(f"{URL_RANGE}21BD1", lambda r: r.status_code, lambda m: m))
    print(hacer_peticion(f"{URL_RANGE}ABCDE", lambda r: len(r.text) > 0, lambda m: m))
    print(hacer_peticion(f"{URL_RANGE}XYZ", lambda r: r.status_code, lambda m: m))
    print(hacer_peticion("https://dominio-que-no-existe-12345.com", lambda r: r.status_code, lambda m: m))

    print("\ncomprobar_contrasena")
    print(comprobar_contrasena("password", hash_sha1, ""))
    print(comprobar_contrasena("123456", hash_sha1, ""))
    print(comprobar_contrasena("password", hash_ntlm, "?mode=ntlm"))
    print(comprobar_contrasena("123456", hash_ntlm, "?mode=ntlm"))
    print(comprobar_contrasena("k8#Vq2!zLp9$wXr7mT", hash_sha1, ""))

    print("\nmensaje_brechas")
    print(mensaje_brechas([]))
    print(mensaje_brechas([{"Name": "Adobe", "BreachDate": "2013-10-04", "PwnCount": 152445165}]))
    print(mensaje_brechas([{"Name": "A", "BreachDate": "2020-01-01", "PwnCount": 1}, {"Name": "B", "BreachDate": "2021-01-01", "PwnCount": 2}]))
    print(mensaje_brechas([{"Name": "C", "BreachDate": "2019-05-05", "PwnCount": 300}]))
    print(mensaje_brechas([]))

    print("\ncomprobar_dominio")
    print(comprobar_dominio("adobe.com"))
    print(comprobar_dominio("linkedin.com"))
    print(comprobar_dominio("dropbox.com"))
    print(comprobar_dominio("tumblr.com"))
    print(comprobar_dominio("dominio-que-no-existe-12345.com"))


if __name__ == "__main__":
    pruebas()
    print()
    main()