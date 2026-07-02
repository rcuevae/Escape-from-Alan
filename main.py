# main.py
import estado
import puzzles
import audio
from audio import reproducir_sfx
import os
import msvcrt
import time
import sys

# VARIABLES GLOBALES
TIEMPO_LIMITE_SEGUNDOS = 600  # 10 Minutos
tiempo_inicio = 0  # Se inicializa al darle a "Jugar"

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def obtener_tiempo_restante():
    segundos_transcurridos = time.time() - tiempo_inicio
    segundos_restantes = TIEMPO_LIMITE_SEGUNDOS - segundos_transcurridos
    if segundos_restantes <= 0:
        return 0
    return int(segundos_restantes)

def formatear_reloj(segundos_totales):
    m = int(segundos_totales // 60)
    s = int(segundos_totales % 60)
    return f"{m:02d}:{s:02d}"

def mostrar_pantalla_gameover(titulo, lineas):
    """Pantalla de Game Over reutilizable (por tiempo o por intentos agotados)."""
    audio.detener_musica()
    limpiar_pantalla()
    reproducir_sfx("risa.mp3", esperar=True)   # risa suena en pantalla negra
    print("\n\033[1;31m" + "="*60)
    print(f"  {titulo}  ")
    for linea in lineas:
        print(f" {linea}")
    print("="*60 + "\033[0m")
    sys.exit()

def mostrar_pantalla_victoria():
    """Pantalla final: se dispara cuando el último puzzle (pila) devuelve 'VICTORIA'."""
    limpiar_pantalla()
    audio.detener_musica()
    reproducir_sfx("puerta.mp3", esperar=True)   # puerta suena ANTES del texto
    puzzles.print_slow("\n [SISTEMA]: COMPUERTAS DE ESCAPE ABIERTAS. INICIANDO DESPEGUE.")
    puzzles.print_slow("Escapas en la cápsula justo antes de que A.L.A.N. destruya el complejo.")
    time.sleep(1)
    puzzles.print_slow("\n==================================================")
    puzzles.print_slow("    ¡MISIÓN CUMPLIDA! HAS SOBREVIVIDO A A.L.A.N.   ")
    puzzles.print_slow("==================================================")
    sys.exit()

def menu_inicio():
    """Maneja el menú de título con Arte ASCII usando las flechas."""
    arte_ascii = """\033[0;32m                    \033[1;32m[SYSTEM PROTOCOL ENCRYPTED...]\033[0;32m                    
\033[0;32m                         A8$BF81 0E16D6 D%AD9F0                       
\033[0;32m                   C5 &%&8#3D5&6 9C13@&EA25C@D09## 2                  
\033[0;32m \033[1;32m0xCAFEBABE\033[0;32m        %6$7%1941%F0CC20$9580E%F2C4CEC&$F820%  \033[1;32mMEM_CORRUPT\033[0;32m 
\033[0;32m \033[1;32mFAILED\033[0;32m    ,-~  7$@ 08%83AEC0BC42#7$9E8458350AC3C7@B6&3D9( ~          
\033[0;32m        (.])    0 4A #&5$@6185E6CF\033[0;31m...\033[0;32m9674AFC01##58D8#49 DA$           
\033[0;32m         < ;><0@E   %@F4&E$CF1634\033[0;31m.###.\033[0;32m45$2DC@%&4 %%#AF3CD/    ~( .    
\033[0;32m       ]    .^0@&E8B1 FDE1%D@6%1\033[0;31m.#####.\033[0;32m5&2@6F8CC D&@@%#0 95~,    .:   
\033[0;32m         +(      E3@$5 A6#83068 \033[0;31m##\033[1;31m@@@\033[0;31m##\033[0;32m E%FB110C@8568#75D +>][)       
\033[0;32m              $6F9 1#1&4AD30E88 \033[0;31m.#####.\033[0;32m 17&3032124B18%0#C ::       .  
\033[0;32m    :   ;; ~: 5  0A6%1  FE482F#7 \033[0;31m.###.\033[0;32m 82D%B02&C%9D#7 #5 #B30+ ~*  :  
\033[0;32m       ~^.>[[  $64E21##6%21725E&26\033[0;31m...\033[0;32m9@4320D8CD3BE7E840&D%E *: [<     
\033[0;32m            /<572@@6$7B%0$93@6&D2AA2A9$196A @%6C   B1D61A +-          
\033[0;32m           :^  FCF@B  9%52D#6&7B92093A#&$AFD66 #1C$  C0DF~.)          
\033[0;32m                6$92C5%#2D2C373##2&E452%5$@7E2@830  28B               
\033[0;32m \033[1;32m0xCAFEBABE\033[0;32m          B851B #B9&@0$1496BFD7A57%#3&F$5      \033[1;32mMEM_CORRUPT\033[0;32m 
\033[0;32m \033[1;32mFAILED\033[0;32m                 A9E35EFC84A@05E6  871C6                       
\033[0;32m                               #@ 910$B7F                             
\033[0;32m                                 #02&5                                \033[0m

    \033[1;32m                    E S C A P E   F R O M\033[0m

    \033[1;31m ███      █          ███      █   █    
    █   █     █         █   █     ██  █    
    █   █     █         █   █     █ █ █    
    █████     █         █████     █  ██    
    █   █     █         █   █     █   █    
    █   █     █         █   █     █   █    
    █   █  █  █████  █  █   █  █  █   █  █ \033[0m

    \033[1;31m==================================================\033[0m
    """
    opciones = ["Iniciar Secuencia (Jugar)", "Protocolos (Instrucciones)", "Abortar (Salir)"]
    seleccion = 0

    while True:
        limpiar_pantalla()
        print(arte_ascii)

        for idx, opcion in enumerate(opciones):
            if idx == seleccion:
                print(f"    --> 🔘 \033[1;32m{opcion}\033[0m")
            else:
                print(f"        ⚪ {opcion}")

        print("\n  [Usa las flechas ↑ / ↓ y presiona ENTER]")

        tecla = msvcrt.getch()
        if tecla in [b'\xe0', b'\x00']:
            flecha = msvcrt.getch()
            if flecha == b'H':    # Arriba
                seleccion = (seleccion - 1) % len(opciones)
            elif flecha == b'P':  # Abajo
                seleccion = (seleccion + 1) % len(opciones)
        elif tecla in [b'\r', b'\n']:
            reproducir_sfx("click.mp3")
            return seleccion

def menu_interactivo(titulo, opciones, con_temporizador=True):
    """Maneja el menú dentro del juego (Gameplay).

    con_temporizador=False se usa para menús previos a iniciar la partida
    (selección de dificultad, manual, etc.), donde 'tiempo_inicio' todavía
    no tiene un valor válido y por lo tanto NO debe evaluarse el límite
    de tiempo (si no, se dispara un Game Over falso apenas se muestra
    el menú, porque tiempo_inicio=0 hace que el cálculo dé negativo).
    """
    seleccion = 0
    ultimo_segundo_dibujado = -1

    while True:
        segundos_restantes = obtener_tiempo_restante() if con_temporizador else None

        # Game Over por tiempo (solo aplica si estamos en partida)
        if con_temporizador and segundos_restantes <= 0:
            mostrar_pantalla_gameover(
                "¡TIEMPO AGOTADO!",
                [
                    "La puerta principal ha cedido. A.L.A.N. ha tomado el control.",
                    "SISTEMA APAGADO."
                ]
            )

        # Solo refrescamos cuando cambia el segundo (o siempre, si no hay temporizador)
        if not con_temporizador or segundos_restantes != ultimo_segundo_dibujado:
            limpiar_pantalla()

            if con_temporizador:
                room = estado.rooms[estado.player["current_room"]]
                reloj_str = formatear_reloj(segundos_restantes)

                print("="*70)
                print(f"  ZONA ACTUAL: {room['name'].upper()}")
                print(f"  ALERTA: A.L.A.N. rompiendo defensas.")
                color_reloj = "\033[1;31m" if segundos_restantes < 60 else "\033[1;33m"
                print(f" ⏱ INTEGRIDAD DEL COMPLEJO: {color_reloj}[ {reloj_str} ]\033[0m minutos restantes")
                print(f"  Inventario: {estado.player['inventory'] if estado.player['inventory'] else '[Vacío]'}")
                print("="*70)
                print(f"  {room['desc']}")
                print("="*70)

            print(f"\n{titulo}")
            for idx, opcion in enumerate(opciones):
                if idx == seleccion:
                    print(f"  --> 🔘 \033[1;32m{opcion}\033[0m")
                else:
                    print(f"      ⚪ {opcion}")
            print("\n[Usa las flechas ↑ / ↓ y presiona ENTER para elegir]")

            if con_temporizador:
                ultimo_segundo_dibujado = segundos_restantes

        if msvcrt.kbhit():
            tecla = msvcrt.getch()
            if tecla in [b'\xe0', b'\x00']:
                flecha = msvcrt.getch()
                if flecha == b'H':    # Arriba
                    seleccion = (seleccion - 1) % len(opciones)
                    ultimo_segundo_dibujado = -1
                elif flecha == b'P':  # Abajo
                    seleccion = (seleccion + 1) % len(opciones)
                    ultimo_segundo_dibujado = -1
            elif tecla in [b'\r', b'\n']:
                reproducir_sfx("click.mp3")
                return seleccion

        time.sleep(0.05)

def main():
    global tiempo_inicio
    global TIEMPO_LIMITE_SEGUNDOS 

    # fondo.mp3 arranca aquí — antes del menú, desde el primer frame
    audio.iniciar_musica_fondo()

    # Bucle del Menú Principal
    while True:
        limpiar_pantalla()
        sel_menu = menu_inicio()  # 0 = Jugar, 1 = Instrucciones, 2 = Salir

        if sel_menu == 0:  # Iniciar Secuencia (Jugar) -> ahora sí pide dificultad
            opciones_dificultad = [
                "Fácil (10 min)",
                "Difícil (8 min)",
                "Atrás"
            ]
            sel_dif = menu_interactivo("SELECCIONA LA DIFICULTAD:", opciones_dificultad, con_temporizador=False)

            if sel_dif == 0:  # Fácil
                limpiar_pantalla()
                print("Iniciando simulación en modo FÁCIL...")
                estado.dificultad = "facil"
                TIEMPO_LIMITE_SEGUNDOS = 600  # 10 minutos
                time.sleep(1)
                tiempo_inicio = time.time()  # El reloj comienza AQUÍ
                break  # Rompe el bucle del menú e inicia el juego

            elif sel_dif == 1:  # Difícil
                limpiar_pantalla()
                print("Iniciando simulación en modo DIFÍCIL... ¡Prepárate!")
                estado.dificultad = "dificil"
                TIEMPO_LIMITE_SEGUNDOS = 480  # 8 minutos
                time.sleep(1)
                tiempo_inicio = time.time()  # El reloj comienza AQUÍ
                break  # Rompe el bucle del menú e inicia el juego

            # sel_dif == 2 (Atrás): no hace nada, vuelve al menú principal (while True)

        elif sel_menu == 1:  # Protocolos (Instrucciones) -> muestra el manual directo
            limpiar_pantalla()
            print("="*60)
            print("                 MANUAL DE SUPERVIVENCIA")
            print("="*60)
            print(" 1. Eres un ingeniero atrapado en las instalaciones de Turing-Tech.")
            print(" 2. La IA 'A.L.A.N.' se ha corrompido y quiere eliminarte.")
            print(" 3. Completa los desafíos antes de que el reloj del sistema llegue a 00:00.")
            print(" 4. Explora las salas, repara los autómatas y procesa las cadenas.")
            print(" 5. Usa las FLECHAS DIRECCIONALES para navegar y ENTER para confirmar.")
            print("="*60)
            print("\n[Presiona cualquier tecla para volver al menú...]")
            msvcrt.getch()  # Espera a que presione una tecla y vuelve a empezar el bucle

        elif sel_menu == 2:  # Abortar (Salir)
            limpiar_pantalla()
            print("Ejecución abortada. Hasta luego.")
            sys.exit()
    # Bucle Principal del Juego (Gameplay)
    while True:
        room = estado.rooms[estado.player["current_room"]]
        opciones_menu = []
        acciones = []

        if room["exits"]:
            opciones_menu.append("Explorar otra zona (Moverse)")
            acciones.append("moverse")
        if room["puzzle"]:
            opciones_menu.append("Acceder a la terminal de la sala")
            acciones.append("puzzle")

        opciones_menu.append("Rendirse y apagar consola (Salir)")
        acciones.append("salir")

        sel = menu_interactivo("¿QUÉ ORDEN EJECUTARÁS?", opciones_menu)
        accion = acciones[sel]

        if accion == "moverse":
            opciones_sub = list(room["exits"].keys())
            sel_sub = menu_interactivo("¿A DÓNDE TE DIRIGES?", opciones_sub + ["Atrás"])
            if sel_sub < len(opciones_sub):
                destino = opciones_sub[sel_sub]
                reproducir_sfx("pasos.mp3", esperar=True)   # pasos suenan ANTES de cambiar sala
                estado.player["current_room"] = room["exits"][destino]

        elif accion == "puzzle":
            limpiar_pantalla()
            resultado = None
            if room["puzzle"] == "regex":
                resultado = puzzles.puzzle_regex()
            elif room["puzzle"] == "afd":
                resultado = puzzles.puzzle_afd()
            elif room["puzzle"] == "afnd":
                resultado = puzzles.puzzle_afnd()
            elif room["puzzle"] == "pila":
                resultado = puzzles.puzzle_pila()

            if resultado == "VICTORIA":
                mostrar_pantalla_victoria()
            elif resultado == "GAME_OVER":
                mostrar_pantalla_gameover(
                    "¡FALLO CRÍTICO DE SEGURIDAD!",
                    [
                        "Has agotado tus intentos. A.L.A.N. detecta la intrusión fallida.",
                        "Los sistemas de contención se cierran a tu alrededor.",
                        "SISTEMA APAGADO."
                    ]
                )

            print("\n[Presiona cualquier tecla para volver a la zona...]")
            msvcrt.getch()

        elif accion == "salir":
            limpiar_pantalla()
            print("Has desconectado la simulación. A.L.A.N. ha ganado.")
            break

if __name__ == "__main__":
    main()