from functools import reduce

def es_palindromo(texto):
    
    """
    Determina si un número es palíndromo comprobando si sus caracteres al derecho y la inversa coinciden.
    No es necesario trabajar el texto antes. Se encarga de limpiarlo (eliminar mayúsculas y espacios). 

    Args:
        texto (string): Texto a evaluar.

    Returns:
        boolean: True si es palíndromo, False si no lo es.
    
    """
    limpio = "".join(filter(str.isalnum, texto.lower()))

    return limpio == limpio[::-1]


def palindromos(lista):
    """
        Determina si una lista de palindromos lo son apoyandose en la función de palíndromos.
    
        Args:
            texto (list of str): Listas de textos a evaluar.
    
        Returns:
            list of bool: True si son palíndromos, False si no lo son. Para cada uno de ellos.
    """
    return list(map(es_palindromo, lista))


def cuadrados_sumados(n: int) -> int:
    """Calcula la suma de los cuadrados de los números enteros del 1 al n.

    Esta función genera una secuencia numérica desde el 1 hasta `n`, 
    eleva cada número al cuadrado utilizando una función lambda
    aplicada mediante `map`, y acumula el resultado total 
    con `sum`.

    Args:
        n (int): El número entero máximo hasta el cual se calcularán 
        y sumarán los cuadrados.

    Returns:
        int: La suma total de los cuadrados de todos los números 
        en el rango de 1 a n.
    """
    return sum(map(lambda x: x ** 2, range(1, n + 1)))


def factorial(n: int) -> int:
    """Calcula el factorial de un número entero no negativo n.

    Esta función genera una secuencia de números desde el 1 hasta `n` 
    usando `range()`, y luego utiliza `reduce()` junto con `lambda` 
    para multiplicar acumulativamente todos los elementos de la secuencia, 
    comenzando con un valor inicial de 1.

    Args:
        n (int): El número entero del cual se desea calcular el factorial.

    Returns:
        int: El resultado del factorial de n (n!).
    """
    return reduce(lambda a, b: a * b, range(1, n + 1), 1)


def promedio(estudiante: dict) -> float:
    """Calcula el promedio aritmético de las calificaciones de un estudiante.

    Esta función extrae la lista de notas asociada a la clave "calificaciones" 
    dentro del diccionario del estudiante, suma todos los valores utilizando 
    la función `sum()`, y divide ese total entre la cantidad de elementos 
    obtenida con `len()` para obtener la media.

    Args:
        estudiante (dict): Diccionario que contiene la información del estudiante, 
        el cual debe incluir la clave "calificaciones" con una lista de números 
        (enteros o flotantes).

    Returns:
        float: El promedio de las calificaciones del estudiante.
    """
    notas = estudiante["calificaciones"]
    return sum(notas) / len(notas)


def estudiantes_aprobados(estudiantes: list[dict]) -> list[dict]:
    """Filtra una lista de estudiantes y devuelve aquellos que han aprobado.

    Esta función utiliza la función `filter()` en combinación con una función 
    lambda para evaluar a cada estudiante de la lista utilizando 
    la función auxiliar `promedio()`. Selecciona únicamente a aquellos cuyo 
    promedio es mayor o igual a 6, y acumula los resultados en una lista.

    Args:
        estudiantes (list of dict): Lista de diccionarios, donde cada diccionario 
        representa los datos de un estudiante (incluyendo la clave "calificaciones").

    Returns:
        list of dict: Una nueva lista que contiene únicamente los diccionarios 
        de los estudiantes cuyo promedio de calificaciones es de 6 o superior.
    """
    return list(filter(lambda e: promedio(e) >= 6, estudiantes))


estudiantes = [
    {"nombre": "Juan", "calificaciones": [7, 8, 6, 5]},
    {"nombre": "Ana", "calificaciones": [9, 6, 8]},
    {"nombre": "Pedro", "calificaciones": [4, 5, 3]},
    {"nombre": "Maria", "calificaciones": [10, 9, 9]},
    {"nombre": "Luis", "calificaciones": [3, 2, 5]}
]


print("\n--- PALINDROMOS ---")
print(f"Reconocer -> {es_palindromo('reconocer')}")
print(f"Python -> {es_palindromo('python')}")
print(f"Anita lava la tina -> {es_palindromo('Anita lava la tina')}")
print(f"a -> {es_palindromo('a')}")
print(f"['Reconocer', 'Python', 'Salas'] -> {palindromos(['reconocer', 'python', 'salas'])}")
print(f"['Ana', 'Hola'] -> {palindromos(['ana', 'hola'])}")
print(f"['Neuquen', 'Casa', 'Oso', 'Luz'] -> {palindromos(['Neuquen', 'casa', 'oso', 'luz'])}")
print(f"[] -> {palindromos([])}")
print(f"['Anita lava la tina', 'Radar', 'Programacion'] -> {palindromos(['Anita lava la tina', 'radar', 'programacion'])}")

print("\n--- CUADRADOS SUMADOS ---")
print(f"1 -> {cuadrados_sumados(1)}")
print(f"3 -> {cuadrados_sumados(3)}")
print(f"5 -> {cuadrados_sumados(5)}")
print(f"10 -> {cuadrados_sumados(10)}")
print(f"100 -> {cuadrados_sumados(100)}")

print("\n--- FACTORIAL ---")
print(f"0 -> {factorial(0)}")
print(f"1 -> {factorial(1)}")
print(f"5 -> {factorial(5)}")
print(f"10 -> {factorial(10)}")
print(f"20 -> {factorial(20)}")

print("\n--- ESTUDIANTES APROBADOS ---")

print("Array de estudiantes: ", estudiantes, "\n")
pruebas_estudiantes = [
    estudiantes,
    [],
    [{"nombre": "Eva", "calificaciones": [6, 6]}],
    [{"nombre": "Raul", "calificaciones": [5, 5]}],
    estudiantes[:3],
]

for prueba in pruebas_estudiantes:
    nombres_entrada = list(map(lambda e: e["nombre"], prueba))
    nombres_aprobados = list(map(lambda e: e["nombre"], estudiantes_aprobados(prueba)))
    print(f"{nombres_entrada} -> {nombres_aprobados}")