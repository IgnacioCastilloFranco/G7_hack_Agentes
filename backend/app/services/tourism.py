import requests
from typing import List, Dict, Any

# Endpoints de datos abiertos del Ayuntamiento de Madrid
MADRID_API_ENDPOINTS: Dict[str, str] = {
    "monumentos": "https://datos.madrid.es/egob/catalogo/300356-0-monumentos-ciudad-madrid.json",
    "museos": "https://datos.madrid.es/egob/catalogo/201132-0-museos.json",
    "salas_estudio": "https://datos.madrid.es/egob/catalogo/217921-0-salas-estudio.json",
    "parques": "https://datos.madrid.es/egob/catalogo/200761-0-parques-jardines.json",
    "templos_catolicos": "https://datos.madrid.es/egob/catalogo/209426-0-templos-catolicas.json",
    "templos_otros": "https://datos.madrid.es/egob/catalogo/209434-0-templos-otros.json",
    "actividades_culturales": "https://datos.madrid.es/egob/catalogo/206974-0-agenda-eventos-culturales-100.json",
    "actividades_bibliotecas": "https://datos.madrid.es/egob/catalogo/206717-0-agenda-eventos-bibliotecas.json",
    "bibliotecas": "https://datos.madrid.es/egob/catalogo/201747-0-bibliobuses-bibliotecas.json",
    "edificios_monumentales": "https://datos.madrid.es/egob/catalogo/208844-0-monumentos-edificios.json",
    "teatros": "https://datos.madrid.es/egob/catalogo/208862-7650046-ocio_salas.json",
    "cines": "https://datos.madrid.es/egob/catalogo/208862-7650164-ocio_salas.json",
    "auditorios": "https://datos.madrid.es/egob/catalogo/208862-7650180-ocio_salas.json",
}

def _safe_get(url: str) -> Dict[str, Any]:
    try:
        resp = requests.get(url, timeout=15)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        return {"__error__": str(e)}

def _extract_items(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    if not isinstance(payload, dict):
        return []
    for key in ("@graph", "graph", "items", "results", "data"):
        if isinstance(payload.get(key), list):
            return payload[key]
    # A veces el JSON es ya una lista o está bajo otra clave
    if isinstance(payload, list):
        return payload  # type: ignore
    return []

def _normalize_item(item: Dict[str, Any]) -> Dict[str, Any]:
    name = item.get("title") or item.get("nombre") or item.get("name") or item.get("dc:title")
    desc = item.get("description") or item.get("descripcion") or item.get("dc:description")
    address = None
    for k in ("address", "direccion", "location", "addressLocality"):
        v = item.get(k)
        if isinstance(v, dict):
            address = v.get("street-address") or v.get("address") or v.get("locality") or v.get("addressLocality")
        elif isinstance(v, str):
            address = v
        if address:
            break
    url = item.get("link") or item.get("contentUrl") or item.get("url")
    return {
        "name": str(name) if name else None,
        "description": str(desc) if desc else None,
        "address": str(address) if address else None,
        "url": str(url) if url else None,
        "raw": item,
    }

def search_madrid_data(query: str, limit_per_category: int = 5) -> List[Dict[str, Any]]:
    q = (query or "").lower().strip()
    tokens = {t for t in q.replace(",", " ").replace(".", " ").split() if t}

    # Mapear palabras clave a categorías preferidas
    keyword_to_categories: Dict[str, List[str]] = {
        "evento": ["actividades_culturales", "actividades_bibliotecas"],
        "eventos": ["actividades_culturales", "actividades_bibliotecas"],
        "cultural": ["actividades_culturales"],
        "culturales": ["actividades_culturales"],
        "museo": ["museos"],
        "museos": ["museos"],
        "parque": ["parques"],
        "parques": ["parques"],
        "teatro": ["teatros", "auditorios"],
        "teatros": ["teatros", "auditorios"],
        "auditorio": ["auditorios"],
        "auditorios": ["auditorios"],
        "cine": ["cines"],
        "cines": ["cines"],
        "monumento": ["monumentos", "edificios_monumentales"],
        "monumentos": ["monumentos", "edificios_monumentales"],
        "biblioteca": ["bibliotecas", "actividades_bibliotecas"],
        "bibliotecas": ["bibliotecas", "actividades_bibliotecas"],
    }
    preferred_categories: List[str] = []
    for t in tokens:
        preferred_categories.extend(keyword_to_categories.get(t, []))
    # Únicas, preservando orden
    preferred_categories = list(dict.fromkeys(preferred_categories))

    categories_iter = (
        ((c, MADRID_API_ENDPOINTS[c]) for c in preferred_categories)
        if preferred_categories else MADRID_API_ENDPOINTS.items()
    )

    results: List[Dict[str, Any]] = []
    for category, url in categories_iter:
        payload = _safe_get(url)
        if "__error__" in payload:
            continue
        items = _extract_items(payload)
        if not items:
            continue
        matched: List[Dict[str, Any]] = []
        for it in items:
            norm = _normalize_item(it)
            if not tokens:
                norm["category"] = category
                matched.append(norm)
            else:
                haystack_text = " ".join([
                    norm.get("name") or "",
                    norm.get("description") or "",
                    norm.get("address") or "",
                ]).lower()
                haystack_tokens = set(haystack_text.replace(",", " ").replace(".", " ").split())
                has_overlap = bool(tokens & haystack_tokens)
                if has_overlap:
                    norm["category"] = category
                    matched.append(norm)
                elif category in ("actividades_culturales", "actividades_bibliotecas") and ("evento" in tokens or "eventos" in tokens or "cultural" in tokens or "culturales" in tokens):
                    # Relajar el filtrado para consultas de eventos
                    norm["category"] = category
                    matched.append(norm)
            if len(matched) >= limit_per_category:
                break
        results.extend(matched)
    return results

def format_results_for_agent(items: List[Dict[str, Any]], max_items: int = 15) -> str:
    if not items:
        return "No he encontrado resultados en las APIs oficiales de Madrid."
    lines: List[str] = []
    for i, it in enumerate(items[:max_items], start=1):
        parts = [
            f"{i}. [{it.get('category')}] {it.get('name') or 'Sin título'}",
        ]
        if it.get("address"):
            parts.append(f"Dirección: {it['address']}")
        if it.get("description"):
            parts.append(f"Descripción: {it['description'][:240]}...")
        if it.get("url"):
            parts.append(f"Más info: {it['url']}")
        lines.append(" | ".join(parts))
    return "\n".join(lines)