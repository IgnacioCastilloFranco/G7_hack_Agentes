from typing import Dict, Any, List

# Base de datos simulada con información de Madrid.
# Esto evita la dependencia circular al no necesitar importar el agente.
MADRID_DATA: Dict[str, Dict[str, Any]] = {
    "palacio real": {
        "name": "Palacio Real de Madrid",
        "description": "La residencia oficial de la Familia Real Española, aunque ahora solo se utiliza para ceremonias de estado. Es el palacio real en funcionamiento más grande de Europa.",
        "historical_data": {
            "construction": "1738-1755",
            "style": "Barroco clasicista",
            "architects": ["Filippo Juvarra", "Juan Bautista Sachetti"]
        },
        "legends": [
            {
                "title": "El fantasma del rey",
                "story": "Se dice que el espíritu del rey Carlos III a veces pasea por el Salón del Trono, asegurándose de que todo esté en orden."
            }
        ],
        "magical_connection": "El Ratoncito Pérez tiene una pequeña puerta secreta detrás del trono principal, donde guarda los dientes de leche de todos los príncipes y princesas de la historia de España."
    },
    "parque del retiro": {
        "name": "Parque de El Retiro",
        "description": "Un gran y popular parque en el corazón de Madrid. Lleno de hermosos jardines, un lago y monumentos impresionantes.",
        "historical_data": {
            "opened_to_public": "1868",
            "main_attractions": ["Estanque Grande", "Palacio de Cristal", "Monumento a Alfonso XII"]
        },
        "legends": [
            {
                "title": "El duende del Retiro",
                "story": "Cuentan las leyendas que un pequeño duende llamado 'Trasgo' vive en el Palacio de Cristal y pule los cristales cada noche para que brillen con la luz del sol."
            }
        ],
        "magical_connection": "En el fondo del Estanque Grande, hay una ciudad submarina para ratones mágicos donde celebran fiestas las noches de luna llena. ¡Yo soy el invitado de honor!"
    }
}

def get_madrid_location_info(location_name: str, with_magic: bool = True) -> Dict[str, Any]:
    """
    Obtiene información sobre un lugar de Madrid de nuestra base de datos.
    """
    location_key = location_name.lower().strip()
    
    if location_key in MADRID_DATA:
        info = MADRID_DATA[location_key].copy()
        if not with_magic:
            info.pop("magical_connection", None)
            info.pop("legends", None)
        return info
    else:
        # Si no se encuentra, devuelve una respuesta genérica en lugar de un error.
        return {
            "name": location_name.title(),
            "description": f"Un lugar fascinante en Madrid lleno de posibles aventuras mágicas. Aún estoy investigando sus secretos más profundos.",
            "historical_data": {},
            "legends": [],
            "magical_connection": "¡Cada rincón de Madrid tiene magia, y estoy seguro de que este lugar tiene una historia increíble que está esperando ser descubierta!"
        }
