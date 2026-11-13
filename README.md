# Examen final - Serie 4: API REST de Vehículos

Proyecto académico con **Django REST Framework y MySQL**, sin autenticación.
Incluye CRUD, validación, migraciones, pruebas y colección Postman,
evidencias reales y ejemplo de consumo en React (15 líneas).

## Requisitos e instalación (PowerShell)

Python 3.12 y MySQL 8 o superior, activo en el puerto configurado.

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
Copy-Item .env.example .env
# Editar .env con las credenciales LOCALES de MySQL.
.\.venv\Scripts\python scripts\crear_bd.py
.\.venv\Scripts\python manage.py migrate
.\.venv\Scripts\python manage.py runserver 127.0.0.1:8000
```

API: http://127.0.0.1:8000/api/vehiculos/
Las credenciales y el entorno virtual se excluyen del control de versiones.
La base `examenfinal_vehiculos` se crea sin alterar otras bases.

## Modelo y endpoints

Tabla `vehiculos`: `id`, `marca` (80 caracteres), `modelo` (80), `anio`
(entero entre 1886 y el próximo año), `color` (40), `created_at`, `updated_at`.
Los cuatro atributos son obligatorios; los textos no pueden quedar vacíos.
ID y fechas son de solo lectura; Django administra las fechas automáticamente.

| Método | URL | Resultado |
| --- | --- | --- |
| POST | `/api/vehiculos/` | Crear: 201; validación: 400 |
| GET | `/api/vehiculos/` | Lista JSON: 200 |
| GET | `/api/vehiculos/{id}/` | Detalle: 200 o 404 |
| PUT | `/api/vehiculos/{id}/` | Actualización completa: 200 o 400 |
| PATCH | `/api/vehiculos/{id}/` | Actualización parcial: 200 o 400 |
| DELETE | `/api/vehiculos/{id}/` | Eliminar: 204 sin cuerpo |

Ejemplo de cuerpo para POST/PUT:

```json
{"marca":"Toyota","modelo":"Corolla","anio":2024,"color":"Blanco"}
```

## Pruebas y evidencia

Con el servidor activo, en otra terminal:

```powershell
.\.venv\Scripts\python manage.py check
.\.venv\Scripts\python manage.py test
.\.venv\Scripts\python scripts\pruebas_http.py
```

Las pruebas Django usan una base temporal `test_examenfinal_vehiculos`:
el usuario de pruebas debe poder crearla y eliminarla.
El script HTTP crea un vehículo, lo consulta y modifica, comprueba un POST inválido
y lo elimina. No elimina otros registros. Las respuestas reales quedan en `evidencia/`.
La colección `herramientas/vehiculos.postman_collection.json` se importa en Postman;
ejecutarla en orden para guardar automáticamente el ID del registro creado.

Las seis capturas `evidencia/01.png` a `06.png` provienen de Postman,
ejecutado contra el servidor y MySQL locales. Muestran URL, método, cuerpo,
estado y respuesta. Para repetirlas, importar la colección en Postman, ejecutar
las seis solicitudes en orden y capturar cada respuesta. No se incluye una
aplicación de consumo propia.

## Consumo en React

`react/Vehiculos.jsx` contiene el fragmento de 15 líneas del inciso B.
`useState` conserva la lista y los errores; `useEffect` inicia el GET al montar;
`fetch` consulta la URL local real y comprueba el estado HTTP antes de leer JSON.
`map` transforma cada objeto en un elemento de lista y `key={v.id}` le da una
identidad estable. El controlador cancela la solicitud al desmontar.

El fragmento es un componente para integrar en una aplicación React, no una
aplicación independiente. Debe servirse desde el mismo origen de la API o usar
un proxy de desarrollo; para un origen diferente es necesario configurar CORS.
La URL indicada es local: el repositorio de GitHub no publica el servidor ni MySQL.

## Informe

`entrega/Serie4_Vehiculos.pdf`: portada, seis capturas y explicación de React.
Para regenerar: instalar `requirements-report.txt` y ejecutar
`python scripts/generar_informe.py` después de generar las capturas.

## Referencias

- https://docs.djangoproject.com/en/5.2/ref/databases/
- https://www.django-rest-framework.org/api-guide/serializers/
- https://www.django-rest-framework.org/api-guide/viewsets/

Este proyecto sigue el requisito académico de no implementar autenticación.
La configuración es para uso local; no debe exponerse directamente a Internet.
