import random

# Base de datos de acertijos
RIDDLES = {
    "palacio real": [
        "Tengo miles de ventanas pero no soy el cielo, y en mis salones, los reyes pasearon su anhelo. ¿Qué soy?",
        "Mi piel es de piedra blanca y brillante, y guardo tesoros de reyes en cada estante. ¿Quién soy?"
    ],
    "parque del retiro": [
        "Tengo un palacio de cristal que no se puede romper, y barcas que navegan en mi estanque sin llover. ¿Dónde puedes verme?",
        "Soy el pulmón verde de la ciudad, donde puedes remar, correr y encontrar la paz de verdad. ¿Qué lugar soy?"
    ],
    "plaza mayor": [
        "Tengo forma cuadrada y balcones por doquier, fui escenario de fiestas y mercados de ayer. ¿Qué plaza soy?",
        "En mi centro, un rey a caballo vigila sin cesar, y en Navidad me lleno de luces para celebrar. ¿Quién soy?"
    ],
    "puerta del sol": [
        "Tengo un oso y un madroño que no dan fruto, y un reloj famoso que da la bienvenida al año con tumulto. ¿Qué lugar soy?",
        "Desde mí empiezan todos los caminos de España, y bajo mi suelo, el Ratoncito Pérez guarda sus hazañas. ¿Dónde estás?"
    ]
}

DEFAULT_RIDDLE = "¿Qué tiene dientes y no come? ¡Un peine! Jeje, este es un clásico de los ratones."

def get_riddle_for_place(place_name: str) -> str:
    """
    Devuelve un acertijo aleatorio para un lugar específico de Madrid.
    """
    key = place_name.lower().strip()
    
    for place_key, riddle_list in RIDDLES.items():
        if place_key in key:
            return random.choice(riddle_list)
            
    return DEFAULT_RIDDLE