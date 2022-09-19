"""
Esta es la expresion regular para el ejercicio 0, que se facilita
a modo de ejemplo:
"""
RE0 = "[ab]*a"

"""
Completa a continuacion las expresiones regulares para los
ejercicios 1-5:
"""
caso_ab = "[abc]*a[abc]*b[abc]*"
caso_ba = "[abc]*b[abc]*a[abc]*"
RE1 = caso_ab + "|" +caso_ba


caso_enteros = "(-|)[1-9][0-9]*|0"

"""
    .000000 <- Es válido?
    -0.0000 <- No es válido
    05.0    <- No es válido
"""
caso_decimal = "(" + caso_enteros + "|-0|-|)" + "\.[0-9]+"
caso_decimal2 = "(" + caso_enteros + "|-0|-)" + "\.[0-9]*"

RE2 = caso_enteros + "|" +caso_decimal + "|" + caso_decimal2

prefijo = "(www\.uam\.es|moodle\.uam\.es)/"
extension = "(([A-Za-z]+(/|))*|)"
RE3 = prefijo +  extension

RE4 = ""

RE5 = ""

"""
Recuerda que puedes usar el fichero test_p0.py para probar tus
expresiones regulares.
"""

