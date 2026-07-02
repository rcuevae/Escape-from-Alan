# audio.py
import os
import time

try:
    import pygame
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.mixer.init()
    AUDIO_DISPONIBLE = True
except Exception:
    AUDIO_DISPONIBLE = False

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def reproducir_sfx(archivo_mp3, esperar=False):
    """
    Reproduce un efecto de sonido desde assets/.
    esperar=True bloquea la ejecución hasta que el audio termina,
    útil para que el texto aparezca recién después del sonido.
    """
    if not AUDIO_DISPONIBLE:
        return
    try:
        ruta = os.path.join(BASE_DIR, "assets", archivo_mp3)
        sonido = pygame.mixer.Sound(ruta)
        sonido.play()
        if esperar:
            time.sleep(sonido.get_length())
    except Exception:
        pass

def iniciar_musica_fondo():
    """Carga y lanza fondo.mp3 en bucle infinito desde el inicio del programa."""
    if not AUDIO_DISPONIBLE:
        return
    try:
        ruta = os.path.join(BASE_DIR, "assets", "fondo.mp3")
        pygame.mixer.music.load(ruta)
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)
    except Exception:
        pass

def detener_musica():
    """Detiene la música de fondo."""
    if not AUDIO_DISPONIBLE:
        return
    try:
        pygame.mixer.music.stop()
    except Exception:
        pass