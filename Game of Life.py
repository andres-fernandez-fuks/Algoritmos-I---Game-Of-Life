def main():
    """
    Función principal del programa. Crea el estado inicial de Game of LIfe
    y muestra la simulación paso a paso mientras que el usuaio presione
    Enter.
    """
    life = life_crear([
        '..........',
        '..........',
        '..........',
        '.....#....',
        '......#...',
        '....###...',
        '..........',
        '..........',
    ])
    print(life)
    while True:
        for linea in life_mostrar(life):
            print(linea)
        print()
        input("Presione Enter para continuar, CTRL+C para terminar")
        print()
        life = life_siguiente(life)

#-----------------------------------------------------------------------------

def life_crear(mapa):
    """
    Crea el estado inicial de Game of life a partir de una disposición
    representada con los caracteres '.' y '#'.

    `mapa` debe ser una lista de cadenas, donde cada cadena representa una
    fila del tablero, y cada caracter puede ser '.' (vacío) o '#' (célula).
    Todas las filas deben tener la misma cantidad de caracteres.

    Devuelve el estado del juego, que es una lista de listas donde cada
    sublista representa una fila, y cada elemento de la fila es False (vacío)
    o True (célula).
    """
    nueva_lista = []
    for cadena in mapa:
        nueva_sub_lista = []
        for letra in cadena:
            nueva_sub_lista.append(letra == '#')
        nueva_lista.append(nueva_sub_lista)
    return nueva_lista


def pruebas_life_crear():
    """Prueba el correcto funcionamiento de life_crear()."""
    # Para cada prueba se utiliza la instrucción `assert <condición>`, que
    # evalúa que la <condición> sea verdadera, y lanza un error en caso
    # contrario.
    assert life_crear([]) == []
    assert life_crear(['.']) == [[False]]
    assert life_crear(['#']) == [[True]]
    assert life_crear(['#.', '.#']) == [[True, False], [False, True]]

#-----------------------------------------------------------------------------

def life_mostrar(life):
    """
    Crea una representación del estado del juego para mostrar en pantalla.

    Recibe el estado del juego (inicialmente creado con life_crear()) y
    devuelve una lista de cadenas con la representación del tablero para
    mostrar en la pantalla. Cada una de las cadenas representa una fila
    y cada caracter debe ser '.' (vacío) o '#' (célula).
    """
    listado_final = []
    for fila in life:
        nueva_cadena = ''
        for estado in fila:
            if estado:
                nueva_cadena += '#'
            else:
                nueva_cadena += '.'
        listado_final.append(nueva_cadena)
    return listado_final


def pruebas_life_mostrar():
    """Prueba el correcto funcionamiento de life_mostrar()."""
    assert life_mostrar([]) == []
    assert life_mostrar([[False]]) == ['.']
    assert life_mostrar([[True]]) == ['#']
    assert life_mostrar([[True, False], [False, True]]) == ['#.', '.#']

#-----------------------------------------------------------------------------

def cant_adyacentes(life, f, c):
    """
    Calcula la cantidad de células adyacentes a la celda en la fila `f` y la
    columna `c`.

    Importante: El "tablero" se considera "infinito": las celdas del borde
    izquierdo están conectadas a la izquierda con las celdas del borde
    derecho, y viceversa. Las celdas del borde superior están conectadas hacia
    arriba con las celdas del borde inferior, y viceversa.
    """
    celula = life[f][c]
    if f == 0:
        if f == len(life)-1:
            ''' 
            Tuve que agregar este caso para que no me diera error la primera prueba de la función.
            El error era un "Fuera de Rango", no un "Assertion Error".'''
            f_ant = f
            f_sig = f
        else:
            f_ant = len(life)-1
            f_sig = f+1
    elif f == len(life)-1:
        f_ant = f-1
        f_sig = 0
    else:
        f_ant = f-1
        f_sig = f+1
    if c == 0:
        if c == len(life[f])-1:
            ''' 
            Tuve que agregar este caso para que no me diera error la primera prueba de la función.
            El error era un "Fuera de Rango", no un "Assertion Error".'''
            c_ant = c
            c_sig = c
        else:
            c_ant = len(life[f])-1
        c_sig = c+1
    if c == len(life[f])-1:
        c_ant = c-1
        c_sig = 0
    else:
        c_ant = c-1
        c_sig = c+1

    mapa_reducido = []
    mapa_reducido.append([life[f_ant][c_ant],life[f_ant][c],life[f_ant][c_sig]])
    mapa_reducido.append([life[f][c_ant],life[f][c],life[f][c_sig]])
    mapa_reducido.append([life[f_sig][c_ant],life[f_sig][c],life[f_sig][c_sig]])
    contador_celulas = 0
    for i,fila in enumerate(mapa_reducido):
        for j, estado in enumerate(fila):
            if (i,j) != (1,1):
                if estado:
                    contador_celulas +=1
    return contador_celulas


def pruebas_cant_adyacentes():
    """Prueba el correcto funcionamiento de cant_adyacentes()."""
    assert cant_adyacentes(life_crear(['.']), 0, 0) == 0
    assert cant_adyacentes(life_crear(['..', '..']), 0, 0) == 0
    assert cant_adyacentes(life_crear(['..', '..']), 0, 1) == 0
    assert cant_adyacentes(life_crear(['##', '..']), 0, 0) == 2
    assert cant_adyacentes(life_crear(['##', '..']), 0, 1) == 2
    assert cant_adyacentes(life_crear(['#.', '.#']), 0, 0) == 4
    assert cant_adyacentes(life_crear(['##', '##']), 0, 0) == 8
    assert cant_adyacentes(life_crear(['.#.', '#.#', '.#.']), 1, 1) == 4
    assert cant_adyacentes(life_crear(['.#.', '..#', '.#.']), 1, 1) == 3
    assert cant_adyacentes(life_crear(['...', '.#.', '...']), 1, 1) == 0

#-----------------------------------------------------------------------------

def celda_siguiente(life, f, c):
    """
    Calcula el estado siguiente de la celda ubicada en la fila `f` y la
    columna `c`.

    Devuelve True si en la celda (f, c) habrá una célula en la siguiente
    iteración, o False si la celda quedará vacía.
    """
    celda = life[f][c]
    print("Estado: ",celda)
    n = cant_adyacentes(life, f, c)
    print("Células vivas alrededor: ",n)
    if celda:
        if n != 2 and n != 3:
            return False
        return True
    if not celda:
        if n == 3:
            return True
        return False

def pruebas_celda_siguiente():
    """Prueba el correcto funcionamiento de celda_siguiente()."""
    assert celda_siguiente(life_crear(['.']), 0, 0) == False
    assert celda_siguiente(life_crear(['..', '..']), 0, 0) == False
    assert celda_siguiente(life_crear(['..', '..']), 0, 1) == False
    assert celda_siguiente(life_crear(['##', '..']), 0, 0) == True
    assert celda_siguiente(life_crear(['##', '..']), 0, 1) == True
    assert celda_siguiente(life_crear(['#.', '.#']), 0, 0) == False
    assert celda_siguiente(life_crear(['##', '##']), 0, 0) == False
    assert celda_siguiente(life_crear(['.#.', '#.#', '.#.']), 1, 1) == False
    assert celda_siguiente(life_crear(['.#.', '..#', '.#.']), 1, 1) == True
    assert cant_adyacentes(life_crear(['...', '.#.', '...']), 1, 1) == False

#-----------------------------------------------------------------------------

def life_siguiente(life):
    """
    Calcula el siguiente estado del juego.

    Recibe el estado actual del juego (lista de listas de False/True) y
    devuelve un _nuevo_ estado que representa la siguiente iteración según las
    reglas del juego.

    Importante: El "tablero" se considera "infinito": las celdas del borde
    izquierdo están conectadas a la izquierda con las celdas del borde
    derecho, y viceversa. Las celdas del borde superior están conectadas hacia
    arriba con las celdas del borde inferior, y viceversa.
    """
    siguiente = []
    for f in range(len(life)):
        fila = []
        for c in range(len(life[0])):
            fila.append(celda_siguiente(life, f, c))
        siguiente.append(fila)
    return siguiente

#-----------------------------------------------------------------------------

def pruebas():
    """Ejecuta todas las pruebas"""
    pruebas_life_crear()
    pruebas_life_mostrar()
    pruebas_cant_adyacentes()
    pruebas_celda_siguiente()
pruebas()
main()