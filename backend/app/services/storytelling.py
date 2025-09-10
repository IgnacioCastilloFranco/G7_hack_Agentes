from typing import List, Optional, Dict, Any
import random


def generate_magical_story(
    location: str,
    age_range: str = "4-8",
    interests: Optional[List[str]] = None,
    previous_locations: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Genera una historia mágica sobre un lugar de Madrid sin depender del agente.
    """
    
    story_starters = [
        "Hace mucho, mucho tiempo, en el corazón de {location}, vivía un pequeño ratón que no era otro que...",
        "Pocos saben que {location} esconde un secreto mágico. Cada noche, cuando la ciudad duerme...",
        "La leyenda cuenta que el primer diente que recogí fue en {location}, y la historia es así de increíble..."
    ]
    
    magical_elements = {
        "palacio real": ["armaduras que bailan chotis", "un trono que concede deseos si le dejas un diente debajo", "fantasmas de reyes que juegan al escondite"],
        "parque del retiro": ["barcos en el estanque que navegan solos", "un Palacio de Cristal donde viven hadas de las flores", "árboles cuyas hojas susurran secretos"],
        "plaza mayor": ["estatuas que cobran vida para contar historias", "balcones desde donde se pueden ver otros tiempos", "un mercado secreto de objetos mágicos a medianoche"],
        "puerta del sol": ["un reloj que puede detener el tiempo por un segundo", "el Oso y el Madroño que protegen un tesoro", "un túnel secreto bajo el Kilómetro Cero"]
    }

    starter = random.choice(story_starters).format(location=location.title())
    elements = magical_elements.get(location.lower(), ["duendes traviesos", "hechizos de alegría", "tesoros escondidos"])
    
    content = (
        f"{starter} "
        f"Resulta que en este lugar encantado, existen {random.choice(elements)} y también {random.choice(elements)}. "
        f"Yo, el Ratoncito Pérez, lo sé porque una vez tuve que organizar una misión secreta para encontrar un diente de oro perdido. "
        f"Fue una aventura increíble llena de misterio y magia."
    )
    
    fun_facts = [
        f"¿Sabías que {location.title()} tiene más de 100 años de historias secretas?",
        "El color favorito de los duendes que viven allí es el azul brillante.",
        "Si escuchas con atención, a veces puedes oír risas mágicas flotando en el aire."
    ]

    return {
        "title": f"El Secreto Mágico de {location.title()}",
        "content": content,
        "fun_facts": fun_facts,
        "image_prompts": [
            f"A magical mouse detective in {location}",
            f"Secret magical elements hidden in {location} at night"
        ]
    }
