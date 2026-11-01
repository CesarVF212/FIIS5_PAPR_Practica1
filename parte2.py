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

def hash_sha1(contrasena: str) -> str:
    """Calcula el hash SHA-1 de una contraseña.

    Args:
        contrasena (str): Contraseña en texto plano.

    Returns:
        str: Hash SHA-1 en formato hexadecimal y en mayúsculas.
    """
    return hashlib.sha1(contrasena.encode("utf-8")).hexdigest().upper()


def hash_ntlm(contrasena: str) -> str:
    """Calcula el hash NTLM de una contraseña.

    Args:
        contrasena (str): Contraseña en texto plano.

    Returns:
        str: Hash NTLM en formato hexadecimal y en mayúsculas.
    """
    return MD4.new(contrasena.encode("utf-16le")).hexdigest().upper()


MODOS_HASH = {
    "1": (hash_ntlm, "?mode=ntlm"),
    "2": (hash_sha1, ""),
}


def mensaje_error(codigo: int) -> str:
    """Devuelve un mensaje descriptivo según el código de error HTTP recibido.

    Args:
        codigo (int): Código de estado HTTP.

    Returns:
        str: Mensaje de error correspondiente.
    """
    return ERRORES.get(codigo, f"Error inesperado (codigo {codigo})")


def hacer_peticion(url: str, callback_ok, callback_error):
    """Realiza una petición HTTP GET manejando errores de conexión y códigos de estado.

    Args:
        url (str): URL de destino.
        callback_ok (callable): Función a ejecutar si la respuesta es exitosa (código 200).
        callback_error (callable): Función a ejecutar si ocurre un error o fallo de conexión.

    Returns:
        El resultado de invocar el callback correspondiente.
    """
    try:
        respuesta = requests.get(url, headers=CABECERAS, timeout=10)

    except requests.exceptions.RequestException:
        return callback_error("No se pudo conectar con el servidor")

    if respuesta.status_code == 200:
        return callback_ok(respuesta)

    return callback_error(mensaje_error(respuesta.status_code))


def obtener_cuenta(texto: str, sufijo: str) -> int:
    """Busca un sufijo de hash en la respuesta y extrae el número de veces filtrada.

    Args:
        texto (str): Respuesta en texto plano de la API.
        sufijo (str): Sufijo del hash que se está buscando.

    Returns:
        int: Número de veces que aparece la contraseña en filtraciones, o 0 si no se encuentra.
    """
    coincidencias = list(filter(lambda linea: linea.split(":")[0] == sufijo, texto.splitlines()))
    return int(coincidencias[0].split(":")[1]) if coincidencias else 0


def mensaje_contrasena(cuenta: int) -> str:
    """Genera el mensaje correspondiente según el número de filtraciones de una contraseña.

    Args:
        cuenta (int): Número de veces que ha aparecido la contraseña.

    Returns:
        str: Mensaje informativo sobre la filtración.
    """
    if cuenta == 0:
        return "La contrasena no aparece en ninguna filtracion"
    return f"La contrasena ha aparecido {cuenta} veces en filtraciones"


def comprobar_contrasena(contrasena: str, funcion_hash, parametro: str) -> str:
    """Comprueba si una contraseña ha sido filtrada utilizando su hash.

    Args:
        contrasena (str): Contraseña a comprobar.
        funcion_hash (callable): Función para calcular el hash (SHA-1 o NTLM).
        parametro (str): Parámetro adicional para la URL.

    Returns:
        str: Resultado de la comprobación en forma de mensaje.
    """
    hash_completo = funcion_hash(contrasena)
    prefijo = hash_completo[:5]
    sufijo = hash_completo[5:]

    return hacer_peticion(
        f"{URL_RANGE}{prefijo}{parametro}",
        lambda respuesta: mensaje_contrasena(obtener_cuenta(respuesta.text, sufijo)),
        lambda mensaje: f"Error: {mensaje}",
    )


def mensaje_brechas(brechas: list[dict]) -> str:
    """Formatea la lista de brechas de seguridad obtenidas para un dominio.

    Args:
        brechas (list of dict): Lista de diccionarios con la información de las filtraciones.

    Returns:
        str: Texto formateado con las brechas encontradas o mensaje de que no hay.
    """
    if not brechas:
        return "No hay filtraciones asociadas a este dominio"

    lineas = map(lambda b: f"- {b['Name']} ({b['BreachDate']}): {b['PwnCount']} cuentas", brechas)
    return "\n".join(lineas)


def comprobar_dominio(dominio: str) -> str:
    """Comprueba las brechas de seguridad asociadas a un dominio específico.

    Args:
        dominio (str): Nombre del dominio a consultar.

    Returns:
        str: Mensaje con las brechas encontradas o error.
    """
    return hacer_peticion(
        f"{URL_BREACHES}?Domain={dominio}",
        lambda respuesta: mensaje_brechas(respuesta.json()),
        lambda mensaje: f"Error: {mensaje}",
    )


def modo_contrasenas() -> None:
    """Ejecuta el modo interactivo para comprobar contraseñas."""
    opcion = input("Formato del hash (1: Windows NTLM, 2: estandar SHA1): ")

    if opcion not in MODOS_HASH:
        print("Opcion no valida")
        return

    contrasena = input("Contrasena: ")
    funcion_hash, parametro = MODOS_HASH[opcion]

    print(comprobar_contrasena(contrasena, funcion_hash, parametro))


def modo_dominios() -> None:
    """Ejecuta el modo interactivo para comprobar dominios."""
    dominio = input("Dominio: ")
    print(comprobar_dominio(dominio))


MODOS = {
    "1": modo_contrasenas,
    "2": modo_dominios,
}


def main() -> None:
    """Punto de entrada principal para la ejecución interactiva del programa."""
    opcion = input("Modo (1: contrasenas, 2: dominios): ")

    if opcion not in MODOS:
        print("Opcion no valida")
        return

    MODOS[opcion]()


def pruebas() -> None:
    """Ejecuta una batería de pruebas para verificar el funcionamiento de los módulos."""
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