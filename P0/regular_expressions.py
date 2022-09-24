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
    -0.000001
    -1.
"""
caso_decimal_pos = "(" + caso_enteros + ")" + "\.[0-9]*"
caso_decimal_neg = "(" + "(" + caso_enteros + "|)" + "\.[0-9]+" + "|" + "(" + caso_enteros + "|-0|-)" + "\.[0-9]*[1-9][0-9]*" + ")"

RE2 = caso_enteros + "|" + caso_decimal_pos + "|" + caso_decimal_neg

prefijo = "(www\.uam\.es|moodle\.uam\.es)/"
extension = "(([A-Za-z]+(/|))*)"
RE3 = prefijo +  extension

num = "([1-9][1-9]*)"
operando = "(\+|-|\*|/)"
RE4 = "("+ num + operando + ")*" + num #cuenta como un solo numero una expresion aritmetica

# 7*(3+12-36)
# a * b
expr_aritm = "("+ num + operando + ")*" + num
numero_suelto = num
numero_parentesis = "\(" + expr_aritm + "\)"
RE5 = "(" + numero_suelto + operando + "|" + numero_parentesis + operando + ")*" + "(" + numero_suelto + "|" + numero_parentesis +")"

"""
Recuerda que puedes usar el fichero test_p0.py para probar tus
expresiones regulares.
"""

