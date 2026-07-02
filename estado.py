# estado.py
dificultad = "facil"

player = {
    "inventory": [],
    "current_room": "vestibulo"
}

rooms = {
    "vestibulo": {
        "name": "Vestíbulo Principal",
        "desc": "La puerta metálica tiembla. A.L.A.N. está intentando entrar. Hay 4 pasillos hacia las terminales de escape.",
        "exits": {"seguridad": "seguridad", "cocina": "cocina", "sotano": "sotano", "laboratorio": "laboratorio"},
        "puzzle": None
    },
    "seguridad": {
        "name": "Sala de Seguridad",
        "desc": "Un cuarto blindado. Hay un panel operativo esperando una Expresión Regular.",
        "exits": {"vestibulo": "vestibulo"},
        "puzzle": "regex",
        "puzzle_status": "listo"
    },
    "cocina": {
        "name": "La Cocina",
        "desc": "Los escombros cubren el suelo. Hay un panel con un AFD controlando la energía de las puertas.",
        "exits": {"vestibulo": "vestibulo"},
        "puzzle": "afd",
        "puzzle_status": "incompleto"
    },
    "sotano": {
        "name": "El Sótano",
        "desc": "El frío es intenso. Una computadora que aloja un AFND parpadea en rojo.",
        "exits": {"vestibulo": "vestibulo"},
        "puzzle": "afnd",
        "puzzle_status": "incompleto"
    },
    "laboratorio": {
        "name": "Laboratorio de Cómputo",
        "desc": "El núcleo de la cápsula de escape. Su servidor principal requiere un Autómata de Pila.",
        "exits": {"vestibulo": "vestibulo"},
        "puzzle": "pila",
        "puzzle_status": "incompleto"
    }
}