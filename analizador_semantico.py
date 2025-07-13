# Robert Martinez, hecho en PYTHON
import re  # expresiones regulares

# Tabla de símbolos donde se guarda cada variable y su tipo. 
tabla_simbolos = {}

# Este analizador semantico tiene 4 reglas basicas:
# 1-las variables no deben de ser declaradas antes de tiempo.
# 2-no se puede asignar un valor a una variable con un tipo de dato diferente.
# 3-No se puede declarar una variable mas 1 vez.
# 4- caracteres no conocidos saltara error.

# Reglas para declarar
def declaracion(linea):
    coincidencia = re.match(r'(int|float|bool)\s+(\w+);', linea) # Expresion regular.
    if coincidencia:
        var_tipo, var_nombre = coincidencia.groups()
        if var_nombre in tabla_simbolos: # Verificar si ya se encuentra en la tabla de simbolos
            print(f"[Error] Variable '{var_nombre}' ya fue declarada.")
        else:
            tabla_simbolos[var_nombre] = var_tipo # Si no se encuentra, asignarla.
            print(f"[OK] Declarada: {var_tipo} {var_nombre}")
        return True
    return False

# Reglas para asignar
def asignamiento(linea):
    coincidencia = re.match(r'(\w+)\s*=\s*(.+);', linea)
    if coincidencia:
        var_nombre, expression = coincidencia.groups()
        if var_nombre not in tabla_simbolos:
            print(f"[Error] Variable '{var_nombre}' no fue declarada.")
            return True

        expr_tipo = evaluar_expresion(expression)
        if expr_tipo and expr_tipo != tabla_simbolos[var_nombre]:
            print(f"[Error] Tipos incompatibles: {tabla_simbolos[var_nombre]} -- {expr_tipo}")
        else:
            print(f"[OK] Asignación válida a {var_nombre}")
        return True
    return False

# Evaluador básico de expresiones en este caso, solo suma entre variables y números
def evaluar_expresion(expr):
    tokens = expr.split('+') # Se dividen los digitos cada vez que hay un +.
    final_tipo = None
    for token in tokens:
        token = token.strip()
        if re.match(r'^\d+$', token): # Para identificar un entero
            this_tipo = 'int'
        elif re.match(r'^\d+\.\d+$', token): # Si lleva punto el número es float
            this_tipo = 'float'
        elif token in tabla_simbolos:
            this_tipo = tabla_simbolos[token]
        else:
            print(f"[Error] Token '{token}' no reconocido en expresión.")
            return None

        if final_tipo is None:
            final_tipo = this_tipo
        elif final_tipo != this_tipo:
            print(f"[Error] Mezcla de tipos en expresión: {final_tipo} y {this_tipo}")
            return None
    return final_tipo

# Función principal, aqui se llaman todas la otras funciones.
def analizador(code_lines):
    for line in code_lines:
        line = line.strip()
        if not line or line.startswith("//"): # Omitir codigo comentado.
            print("Linea comentada")
            continue
        if declaracion(line):
            continue
        elif asignamiento(line):
            continue
        else:
            print(f"[Error] Línea no reconocida: {line}")

# Ejemplo
if __name__ == "__main__":
    print("Análisis semántico de ejemplo:")
    code = [
        "int x;",
        "float y;",
        "//CodigocomentadoX=1", # linea comentada
        "x = 5;",
        "y = x + 2.5;",
        "z = x + y;",  # z no declarada
        "int x;",      # x ya fue declarada
        "bool flag;",
        "flag = true;" # true no está definido
    ]
    analizador(code)

    print("\nEscribe linea por linea. Recuerda terminar cada linea en ; ...Escribe 'q' para salir.\n")

    # Bucle para entradas del usuario
    while True:
        entrada = input(">> ")
        if entrada.lower() in ["q", "exit", "salir"]:
            print("Finalizando programa...")
            break
        analizador([entrada])
