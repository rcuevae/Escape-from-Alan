# diagnostico_audio.py
# Ejecutar desde la misma carpeta que el proyecto para diagnosticar el audio.
import os, sys

print("=" * 50)
print("     DIAGNÓSTICO DE AUDIO")
print("=" * 50)

# 1. ¿Pygame está instalado?
try:
    import pygame
    print(f"\n[OK] pygame encontrado — versión {pygame.version.ver}")
except ImportError as e:
    print(f"\n[FALLO] pygame no está instalado: {e}")
    print("        Solución: pip install pygame")
    sys.exit()

# 2. ¿Se inicializa el mixer?
try:
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.mixer.init()
    freq, size, channels = pygame.mixer.get_init()
    print(f"[OK] mixer inicializado — {freq}Hz, size={size}, canales={channels}")
except Exception as e:
    print(f"[FALLO] mixer no pudo inicializarse: {e}")
    sys.exit()

# 3. ¿Existe la carpeta assets?
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
assets_dir = os.path.join(BASE_DIR, "assets")
print(f"\n[INFO] Buscando assets en: {assets_dir}")

if os.path.isdir(assets_dir):
    encontrados = os.listdir(assets_dir)
    print(f"[OK] Carpeta 'assets' encontrada — contiene: {encontrados}")
else:
    print("[FALLO] La carpeta 'assets' NO existe en esa ruta.")
    print("        Asegúrate de que esté junto a los archivos .py")
    sys.exit()

# 4. Probar cada archivo esperado
archivos = ["fondo.mp3", "puerta.mp3", "gear.mp3",
            "lock.mp3", "pasos.mp3", "click.mp3", "risa.mp3"]

print()
todos_ok = True
for nombre in archivos:
    ruta = os.path.join(assets_dir, nombre)

    if not os.path.exists(ruta):
        print(f"[FALTA]  {nombre}")
        todos_ok = False
        continue

    # Probar como Sound (usado para SFX)
    try:
        s = pygame.mixer.Sound(ruta)
        print(f"[OK] Sound — {nombre}  ({s.get_length():.2f}s)")
    except Exception as e:
        print(f"[FALLO] Sound — {nombre}  ← {e}")
        todos_ok = False

    # Probar como Music (usado para fondo)
    try:
        pygame.mixer.music.load(ruta)
        print(f"[OK] Music — {nombre}")
    except Exception as e:
        print(f"[FALLO] Music — {nombre}  ← {e}")
        todos_ok = False

print()
if todos_ok:
    print("[RESULTADO] Todo cargó correctamente. El problema es en el código.")
else:
    print("[RESULTADO] Hay archivos que fallan. Revisa los [FALLO] de arriba.")

print("=" * 50)
input("\nPresiona ENTER para salir...")