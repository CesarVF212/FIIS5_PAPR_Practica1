from functools import reduce

def es_palindromo(texto):
    # Limpiamos, quitando las mayúsculas y los espacios.
    limpio = "".join(filter(str.isalnum, texto.lower()))

    # Vemos si da los mismos caracteres a nivel individual al recorrerlo del derecho y del revés.
    return limpio == limpio[::-1]


def palindromos(lista):
    return list(map(es_palindromo, lista))


def cuadrados_sumados(n):
    return sum(map(lambda x: x ** 2, range(1, n + 1)))


def factorial(n):
    # Llamamos con un reduce (acumulador) a todos los valores inferiores al número hasta 1. 
    # 5! = 5 * 4 * 3 * 2 * 1
    return reduce(lambda a, b: a * b, range(1, n + 1), 1)


def promedio(estudiante):
    notas = estudiante["calificaciones"]
    return sum(notas) / len(notas)


def estudiantes_aprobados(estudiantes):
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