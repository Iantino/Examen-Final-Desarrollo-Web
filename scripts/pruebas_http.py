"""Ejecuta las seis solicitudes sobre el servidor local y guarda respuestas reales."""
import json
from pathlib import Path
import requests

BASE = 'http://127.0.0.1:8000/api/vehiculos/'
OUT = Path(__file__).resolve().parent.parent / 'evidencia'
OUT.mkdir(exist_ok=True)
results = []

def call(title, method, url, expected, payload=None):
    response = requests.request(method, url, json=payload, timeout=15)
    response.raise_for_status() if response.status_code >= 500 else None
    result = {'titulo': title, 'metodo': method, 'url': url, 'enviado': payload,
              'estado': response.status_code, 'respuesta': response.json() if response.content else None}
    results.append(result)
    assert response.status_code == expected, result
    print(f'{method} {url} -> {response.status_code}')
    return result['respuesta']

vehicle = {'marca': 'Toyota', 'modelo': 'Corolla', 'anio': 2024, 'color': 'Blanco'}
created = call('01 Crear vehículo', 'POST', BASE, 201, vehicle)
detail = f"{BASE}{created['id']}/"
listing = call('02 Listar vehículos', 'GET', BASE, 200)
assert any(v['id'] == created['id'] for v in listing)
call('03 Consultar por ID', 'GET', detail, 200)
updated = call('04 Actualizar vehículo', 'PUT', detail, 200, {**vehicle, 'color': 'Azul'})
assert updated['color'] == 'Azul'
call('05 Validar datos inválidos', 'POST', BASE, 400, {'marca': '', 'anio': 1800})
call('06 Eliminar vehículo', 'DELETE', detail, 204)
assert requests.get(detail, timeout=15).status_code == 404
(OUT / 'pruebas-http.json').write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding='utf-8')
print('Seis pruebas correctas; eliminación confirmada con GET 404.')
