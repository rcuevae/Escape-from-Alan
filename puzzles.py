# puzzles.py
import time
import estado
import re
import audio
from audio import reproducir_sfx

def print_slow(text, delay=0.015):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def intentar_reparar(room, item_requerido, titulo_error, mensaje_error,
                     pregunta, mensaje_exito, mensaje_falta_item):
    """
    Lógica común a los niveles 2, 3 y 4: si la sala está 'incompleto',
    revisa si el jugador tiene el ítem necesario, lo instala con su
    confirmación y deja la sala en estado 'listo' para iniciar el puzzle.
    Devuelve True si la reparación se completó, False en caso contrario.
    """
    print_slow(f"\n{titulo_error}")
    print_slow(mensaje_error)

    if item_requerido not in estado.player["inventory"]:
        print_slow(mensaje_falta_item)
        return False

    print(f"\n[!] Tienes el '{item_requerido}' en tu inventario.")
    if input(f"{pregunta} (s/n) > ").strip().lower() != 's':
        return False

    estado.player["inventory"].remove(item_requerido)
    room["puzzle_status"] = "listo"
    reproducir_sfx("gear.mp3", esperar=True)      # gear suena ANTES del texto de éxito
    print_slow(f"\n {mensaje_exito}")
    return True

# ==================== NIVEL 1: REGEX ====================
def puzzle_regex():
    room = estado.rooms["seguridad"]
    if room["puzzle_status"] == "resuelto":
        print_slow(" Este firewall ya fue vulnerado. La caja fuerte está abierta.")
        return True

    print_slow("\n [NIVEL 1: EXPRESIONES REGULARES]")
    if estado.dificultad == "facil":
        patron = r"^[ab]*c$"
        print_slow("Patrón: ^(a|b)*c$")
        print_slow("(Debe iniciar con 'a' o 'b', terminando con una sola 'c')")
    else:
        patron = r"^(0|1)*00(0|1)*$"
        print_slow("Patrón: ^(0|1)*00(0|1)*$")

    intentos = 3
    while intentos > 0:
        cadena = input("\nIntroduce la cadena > ").strip().lower()
        if re.fullmatch(patron, cadena):
            print_slow("\n ¡SINTAXIS ACEPTADA! La caja fuerte de seguridad se abre.")
            reproducir_sfx("lock.mp3", esperar=True)  # lock suena ANTES de mostrar el ítem
            print_slow("Has extraído el componente: 'chip_determinista'.")
            estado.player["inventory"].append("chip_determinista")
            room["puzzle_status"] = "resuelto"
            return True
        else:
            intentos -= 1
            print(f" La IA rechaza el código. Patrón no coincide. Intentos restantes: {intentos}")
    return "GAME_OVER"

# ==================== NIVEL 2: AFD ====================
def puzzle_afd():
    room = estado.rooms["cocina"]
    if room["puzzle_status"] == "resuelto":
        print_slow(" El sistema de energía principal ya está enrutado correctamente.")
        return True

    # --- PANTALLA DE HARDWARE ROTO (CON BIFURCACIÓN DE DIFICULTAD) ---
    if room["puzzle_status"] == "incompleto":
        print("\n" + "="*70)
        print("   MONITOR DE CONTROL (COCINA) - ¡ALERTA DE CIRCUITO DEGRADADO!")
        print("="*70)
        print_slow("Leyendo arquitectura de transiciones del hardware...")
        time.sleep(0.5)
        
        if estado.dificultad == "facil":
            print("""
         HARDWARE CORRUPTO - TRANSICIONES DETERMINISTAS INCOMPLETAS:
        
          ->(q0) ---a---> (q1) - - X - - > ((??)) [ESTADO INALCANZABLE]
             ^             |
             | - - X - - - +
             |                            
             + - - - - - - - - X - - - - - - - +
            """)
            pista_item = " PISTA: El mapa indica conexiones rotas (X). Necesitas el 'chip_determinista' de la Sala de Seguridad para reparar este panel."
        else:
            print("""
         HARDWARE CORRUPTO [MODO SUPERVIVENCIA] - RED DETERMINISTA COLAPSADA:

          + - - - X - - - +
          |               v
       ->(q0) ---a---> (q1) - - X - -> ((??)) [META DESENERGIZADA]
          ^             |              |
          |             X              X
          |             v              |
          + - - X - - (??) < - - - - - +
                      |
                      + - - X - > [POZO DE ERROR DESCONECTADO]
            """)
            pista_item = " CRÍTICO: Se requiere unidad lógica externa para reconectar los 4 nodos."

        print("""
        [ERROR]: Falta coprocesador de estados lógicos.
        [DIAGNÓSTICO]: Las rutas de retorno y el estado de aceptación están desenergizados.
        """)
        
        if not intentar_reparar(
            room,
            item_requerido="chip_determinista",
            titulo_error=" [SISTEMA CORRUPTO: AFD]",
            mensaje_error=" ERROR: Falta unidad lógica de un solo camino. El autómata no puede procesar los nodos.",
            pregunta="¿Deseas instalar el chip para reparar el sistema?",
            mensaje_exito="Hardware aceptado. Reiniciando secuencia determinista...",
            mensaje_falta_item=pista_item
        ):
            return False

    # --- INICIO DEL PUZZLE REPARADO ---
    if estado.dificultad == "facil":
        print_slow("\n [NIVEL 2: AUTÓMATA FINITO DETERMINISTA]")
        print("""
      ->(q0) ---a---> (q1) ---b---> ((q2)) [META]
         ^             |              |
         |---a---------+              |
         |                            |
         +-------------a--------------+
        """)
        print_slow("Ingresa una cadena de 'a' y 'b' (mínimo 4 caracteres) que termine en ((q2)).")
    else:
        print_slow("\n [MODO DIFÍCIL: AFD CON POZO TRAMPA]")
        print("""
          +-------b-------+
          |               v
       ->(q0) ---a---> (q1) ---a---> ((q2)) [META]
          ^             |              |
          |             b              b
          |             v              |
          +----a---- (q3) <------------+
                      |
                      +---b---> [ERROR FATAL]
        """)
        print_slow("Ingresa una cadena (mínimo 5 caracteres). ¡Evita la sobrecarga en q3!")

    intentos = 3
    while intentos > 0:
        cadena = input("\nIntroduce la cadena > ").strip().lower()
        
        if estado.dificultad == "facil" and len(cadena) < 4:
            print(" Demasiado corta. Deben ser al menos 4 caracteres.")
            continue
        elif estado.dificultad == "dificil" and len(cadena) < 5:
            print(" Demasiado corta. En modo difícil deben ser al menos 5 caracteres.")
            continue

        estado_actual = "q0"
        camino = [estado_actual]
        valida = True

        for char in cadena:
            if char not in ['a', 'b']: valida = False; break
            
            if estado.dificultad == "facil":
                if estado_actual == "q0": estado_actual = "q1" if char == 'a' else "q0"
                elif estado_actual == "q1": estado_actual = "q0" if char == 'a' else "q2"
                elif estado_actual == "q2":
                    if char == 'a': estado_actual = "q0"
                    else: valida = False; break
            else:
                if estado_actual == "q0": estado_actual = "q1" if char == 'a' else "q0"
                elif estado_actual == "q1": estado_actual = "q2" if char == 'a' else "q3"
                elif estado_actual == "q2": estado_actual = "q2" if char == 'a' else "q3"
                elif estado_actual == "q3":
                    if char == 'a': estado_actual = "q0"
                    else: valida = False; break

            camino.append(estado_actual)

        if not valida:
            print(" Cadena rechazada: Carácter inválido o transición no definida en el autómata.")
        else:
            print(f" Nodos: {' -> '.join(camino)}")
            if estado_actual == "q2":
                print_slow("\n ¡ENERGÍA RESTABLECIDA! Un panel de la pared se cae.")
                print_slow("Encuentras tecnología experimental: 'emisor_cuantico_afnd'.")
                estado.player["inventory"].append("emisor_cuantico_afnd")
                room["puzzle_status"] = "resuelto"
                return True
            else:
                intentos -= 1
                print(f" Terminaste en {estado_actual}. Intentos restantes: {intentos}")
                
    return "GAME_OVER"

# ==================== NIVEL 3: AFND ====================
def puzzle_afnd():
    room = estado.rooms["sotano"]
    if room["puzzle_status"] == "resuelto":
        print_slow(" El firewall secundario ya fue destruido.")
        return True

    # --- PANTALLA DE HARDWARE ROTO (CON BIFURCACIÓN DE DIFICULTAD) ---
    if room["puzzle_status"] == "incompleto":
        print("\n" + "="*70)
        print("  COMPUTADORA CENTRAL DEL SÓTANO - MATRIZ CUÁNTICA DESACTIVADA")
        print("="*70)
        print_slow("Leyendo arquitectura de transiciones paralelizadas...")
        time.sleep(0.5)
        
        if estado.dificultad == "facil":
            print("""
         ERROR: No determinismo físico desconectado.
        
           (q0) --- 0 ---> (??) - - X - - > ((q2)) [ESTADO DE ACEPTACIÓN INALCANZABLE]
            """)
            pista_item = " PISTA: El mapa indica conexiones cuánticas rotas. Necesitas el 'emisor_cuantico_afnd' de la Cocina."
        else:
            print("""
         ERROR: No determinismo físico desconectado [MODO SUPERVIVENCIA].
        
           X,X (Bucle Caído)
          +- -+
          |   v
        ->(q0) - - X - -> (??) --- 0,1 ---> (??) - - X - -> ((??)) [NÚCLEO FRAGMENTADO]
            """)
            pista_item = " CRÍTICO: Ausencia de emisor de realidades múltiples. Sistema estancado."

        print("""
        [DIAGNÓSTICO]: Las líneas de computación paralela están caídas.
        """)
        
        if not intentar_reparar(
            room,
            item_requerido="emisor_cuantico_afnd",
            titulo_error="  [SISTEMA CORRUPTO: AFND]",
            mensaje_error=" ERROR DE BIFURCACIÓN: Imposible clonar estados de memoria. Pieza faltante.",
            pregunta="¿Conectar emisor para habilitar el No Determinismo?",
            mensaje_exito="Realidades múltiples conectadas. AFND En línea.",
            mensaje_falta_item=pista_item
        ):
            return False

    # --- INICIO DEL PUZZLE REPARADO ---
    if estado.dificultad == "facil":
        print_slow("\n  [NIVEL 3: AUTÓMATA FINITO NO DETERMINISTA]")
        print("""
          +--- 0,1 ---+
          |           |
          v           |
        (q0) --- 0 ---> (q1) --- 1 ---> ((q2)) --- 0,1 ---+
                                           ^              |
                                           +--------------+
        """)
        print_slow("Ingresa una cadena binaria ('0' y '1') que contenga la subcadena '01' para penetrar el escudo.")
    else:
        print_slow("\n [MODO DIFÍCIL: AFND DE ANTICIPACIÓN]")
        print("""
           0,1
          +---+
          |   v
        ->(q0) --- 1 ---> (q1) --- 0,1 ---> (q2) --- 0,1 ---> ((q3)) [META]
        """)
        print_slow("Sobrecarga cuántica detectada. Para que un clon sobreviva y alcance la meta (q3)...")
        print_slow("El 3er carácter contando desde el FINAL de tu cadena debe ser estrictamente un '1'.")
    
    intentos = 3
    while intentos > 0:
        cadena = input("\nIntroduce la binaria > ").strip()
        estados_actuales = {"q0"}
        valida = True
        
        for char in cadena:
            if char not in ['0', '1']: valida = False; break
            nuevos_estados = set()
            for est in estados_actuales:
                if estado.dificultad == "facil":
                    if est == "q0":
                        nuevos_estados.add("q0")
                        if char == '0': nuevos_estados.add("q1")
                    elif est == "q1":
                        if char == '1': nuevos_estados.add("q2")
                    elif est == "q2":
                        nuevos_estados.add("q2")
                else:
                    if est == "q0":
                        nuevos_estados.add("q0")
                        if char == '1': nuevos_estados.add("q1")
                    elif est == "q1":
                        nuevos_estados.add("q2")
                    elif est == "q2":
                        nuevos_estados.add("q3")
                    elif est == "q3":
                        pass # El clon muere
                        
            estados_actuales = nuevos_estados
            print(f"[{char}] -> Clones activos en: {estados_actuales if estados_actuales else 'Vacío'}")
            
        if not valida:
            print(" Usa solo '0' y '1'.")
        else:
            meta = "q2" if estado.dificultad == "facil" else "q3"
            if meta in estados_actuales:
                print_slow("\n ¡FIREWALL CAÍDO! La computadora te otorga acceso de administrador.")
                print_slow("Expulsa una unidad de almacenamiento pesado: 'modulo_memoria_z0'.")
                estado.player["inventory"].append("modulo_memoria_z0")
                room["puzzle_status"] = "resuelto"
                return True
            else:
                intentos -= 1
                print(f" Ningún clon alcanzó la meta. Intentos restantes: {intentos}")
                                  
    return "GAME_OVER"
# ==================== NIVEL 4: AUTÓMATA DE PILA ====================
def puzzle_pila():
    room = estado.rooms["laboratorio"]

    if room["puzzle_status"] == "incompleto":
        print("\n" + "="*70)
        print("  TERMINAL DE ESCAPE - CONTROLADOR LIFO INESTABLE")
        print("="*70)
        print_slow("Verificando integridad del búfer de almacenamiento...")
        time.sleep(0.5)
        print("""
         ERROR CRÍTICO: Fondo de memoria inaccesible.

           [ PILA CORRUPTA ] -> [ X ] -> [ X ] -> [ ?? ] (Falta Símbolo Inicial Z0)

        [DIAGNÓSTICO]: Estructura LIFO colapsada. Sin el símbolo inicial, la pila sufre subdesbordamiento.
        """)
        pista_item = " PISTA: Necesitas el 'modulo_memoria_z0' del Sótano." if estado.dificultad == "facil" else " Falta hardware crítico para iniciar."

        if not intentar_reparar(
            room,
            item_requerido="modulo_memoria_z0",
            titulo_error=" [SISTEMA CORRUPTO: AUTÓMATA DE PILA]",
            mensaje_error=" ERROR CRÍTICO: Memoria RAM dinámica inexistente. Imposible retener datos LIFO.",
            pregunta="¿Insertar el módulo para inicializar el fondo de pila?",
            mensaje_exito="Servidor central en línea. Inicializando pila con Z0...",
            mensaje_falta_item=pista_item
        ):
            return False

    print_slow("\n [NIVEL 4: AUTÓMATA DE PILA]")
    
    # BIFURCACIÓN DE DIFICULTAD PARA EL TEXTO
    if estado.dificultad == "facil":
        print("""
              REGLAS DE OPERACIÓN EN PILA (LIFO) - MODO FÁCIL:
             • Entrada '0' (en q0) -> PUSH 'X' (Se apila 1 elemento)
             • Entrada '1'         -> POP 'X'  (Se desapila 1 elemento y se pasa a q1)
             • Estado de Éxito     -> Pila limpia, quedando únicamente el fondo [Z0]
        """)
        print_slow("Último bloqueo de A.L.A.N. Balancea los comandos para liberar la cápsula de escape.")
        print_slow("Lenguaje requerido: L = { 0^n 1^n | n >= 1 }")
    else:
        print("""
              REGLAS DE OPERACIÓN EN PILA (LIFO) - MODO DIFÍCIL:
             • Entrada '0' (en q0) -> PUSH 'X', 'X' (Se apilan 2 elementos por cada '0')
             • Entrada '1'         -> POP 'X'       (Se desapila 1 elemento y se pasa a q1)
             • Estado de Éxito     -> Pila limpia, quedando únicamente el fondo [Z0]
        """)
        print_slow("Último bloqueo de A.L.A.N. Balancea los comandos para liberar la cápsula de escape.")
        print_slow("Lenguaje requerido: L = { 0^n 1^2n | n >= 1 }")
        print_slow("ADVERTENCIA: Por cada comando '0', el sistema exige DOS comandos '1' de cierre.")

    intentos = 3
    while intentos > 0:
        cadena = input("\nIntroduce la cadena balanceada > ").strip()
        pila = ["Z0"]
        estado_actual = "q0"
        rechazada = False

        for char in cadena:
            if char == '0' and estado_actual == "q0":
                # BIFURCACIÓN DE LÓGICA DE DIFICULTAD AL APILAR
                if estado.dificultad == "facil":
                    pila.append("X")
                    print(f"Entrada '0' -> Push 'X' | Pila: {pila}")
                else:
                    # MODO DIFÍCIL: Por cada '0', ingresa DOS 'X' a la pila
                    pila.append("X")
                    pila.append("X")
                    print(f"Entrada '0' -> Push 'X', 'X' | Pila: {pila}")
                    
            elif char == '1':
                if estado_actual == "q0":
                    estado_actual = "q1"
                if pila[-1] == "X":
                    pila.pop()
                    print(f"Entrada '1' -> Pop 'X'  | Pila: {pila}")
                else:
                    rechazada = True
                    break
            else:
                rechazada = True
                break

        if not rechazada and estado_actual == "q1" and len(pila) == 1 and pila[0] == "Z0":
            print_slow("\n¡SINTAXIS PERFECTA! La pila se ha vaciado limpiamente.")
            room["puzzle_status"] = "resuelto"
            return "VICTORIA"
        else:
            intentos -= 1
            print(f" Desbalance detectado o sintaxis inválida. Intentos restantes: {intentos}")
            
    return "GAME_OVER"