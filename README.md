# Subastas Clase

Proyecto realizado con Django y Django REST Framework para exponer una API orientada a la gestion de categorias, anuncios, ofertas y usuarios dentro de una plataforma de subastas.

El trabajo fue creciendo por pull requests. Al principio dividimos responsabilidades por funcionalidad para poder avanzar en paralelo, y despues empezamos a trabajar en ramas compartidas Paula-Valentino para integrar mejoras mas grandes, revisar compatibilidad entre endpoints y dejar cada entrega funcionando sobre `main`.

## Dinamica general de trabajo

- Usamos ramas `feature/...` para separar cada entrega o bloque funcional.
- Cada pull request incorporo una parte concreta del sistema y dejo registro de los archivos tocados.
- Cuando una funcionalidad dependia de otra, primero cerramos la base y despues avanzamos sobre validaciones, viewsets, filtros, permisos y documentacion.
- En las ramas compartidas fuimos dividiendo tareas: una persona avanzaba sobre una capa del backend y la otra completaba la integracion, ajustes o endpoints relacionados.
- En varios PRs quedaron commits de correccion para adaptar lo anterior a la nueva estructura sin romper compatibilidad.

## Historial de commits y pull requests

### Commit inicial - `57d8e0b`

Valentino creo la base inicial del proyecto Django.

Cambios principales:
- Creacion del proyecto `subastas_clase`.
- Alta de las apps `anuncio` y `usuario`.
- Definicion de modelos iniciales para categorias, anuncios, ofertas y seguimiento.
- Generacion de migraciones iniciales.
- Alta de `manage.py` y `db.sqlite3`.

Archivos relevantes creados:
- `manage.py`
- `subastas_clase/settings.py`
- `subastas_clase/urls.py`
- `apps/anuncio/models.py`
- `apps/usuario/models.py`
- `apps/anuncio/migrations/0001_initial.py`
- `apps/usuario/migrations/0001_initial.py`

### PR #1 - `feature/Paula` - merge `9c111b1`

Paula tomo la primera funcionalidad de API y completo el CRUD de categorias. Este PR sirvio como primer paso para conectar Django REST Framework con los modelos del proyecto.

Commit del branch:
- `0f27d27`: `Categoria completo`

Cambios incorporados:
- Se agrego Django REST Framework a `INSTALLED_APPS`.
- Se configuro `REST_FRAMEWORK` con renderers JSON y Browsable API.
- Se creo la primera capa de API para `Categoria` usando `APIView`.
- Se creo el serializer de categorias.
- Se definieron rutas especificas para la app `anuncio`.
- Se ajusto `__str__` en `Anuncio`.
- Se agrego `.gitignore` para entorno virtual, sqlite y caches.

Archivos tocados:
- `.gitignore`
- `apps/anuncio/api.py`
- `apps/anuncio/models.py`
- `apps/anuncio/serializers.py`
- `apps/anuncio/url.py`
- `subastas_clase/settings.py`
- `subastas_clase/urls.py`

### PR #2 - `feature/Valentino` - merge `329848b`

Valentino avanzo sobre la funcionalidad complementaria: el CRUD de anuncios. Con esto la API ya no quedaba limitada a categorias y empezaba a cubrir el flujo principal de la subasta.

Commit del branch:
- `298d60b`: `Implementacion CRUD de anuncios con APIView y asignacion forzada de publicado_por en alta de anuncio`

Cambios incorporados:
- Se extendio la API con CRUD de `Anuncio` usando `APIView`.
- En el alta de anuncio, `publicado_por` se asignaba inicialmente de forma forzada con `Usuario` id=1.
- Se ampliaron rutas en `apps/anuncio/url.py` para endpoints de anuncio.
- Se actualizo `db.sqlite3` con datos de prueba.

Archivos tocados:
- `apps/anuncio/api.py`
- `apps/anuncio/url.py`
- `db.sqlite3`

### PR #3 - `feature/paula-valentino-pair` - merge `a2b6b17`

En este PR empezamos a trabajar en conjunto sobre la relacion entre anuncios y categorias. La necesidad era que la API expusiera categorias completas en lectura, pero recibiera ids al crear o editar anuncios.

Commit del branch:
- `519843f`: `categorias_ids con write_only en AnuncioSerializer`

Cambios incorporados:
- Se agrego `categorias_ids` como campo `write_only` en `AnuncioSerializer`.
- La creacion y actualizacion de anuncios paso a recibir categorias existentes por id.
- El serializer expone `categorias` en lectura y recibe `categorias_ids` en escritura.
- Se agrego el primer `README.md` para documentar el avance del trabajo.
- Se agrego `docs/pruebas_postman.png` como evidencia visual de pruebas manuales.

Archivos tocados:
- `README.md`
- `apps/anuncio/serializers.py`
- `docs/pruebas_postman.png`

### PR #5 - `feature/Paula-Valentino-TP3` - merge `d136e95`

En TP3 trabajamos la evolucion desde APIViews hacia herramientas mas propias de DRF. Paula avanzo con generic views y viewsets; Valentino completo el comportamiento de creacion con `perform_create` y agrego una accion custom para calcular el tiempo restante de un anuncio.

Commits del branch:
- `9c0e25f`: `generic y viewset`
- `6b7217a`: `feat: agregar perform_create y accion tiempo-restante`

Cambios incorporados:
- Se sumaron generic views para categorias y anuncios.
- Se agregaron `CategoriaViewSet` y `AnuncioViewSet`.
- Se creo `subastas_clase/router.py` para registrar viewsets con `DefaultRouter`.
- Se incorporo `perform_create` para centralizar la asignacion de `publicado_por`.
- Se agrego la accion custom `tiempo-restante` en `AnuncioViewSet`.
- Se ajustaron URLs globales para exponer las nuevas rutas del router.
- Se agrego `lavarropas.jpg` y se actualizo `db.sqlite3` como recursos de prueba.

Archivos tocados:
- `apps/anuncio/api.py`
- `apps/anuncio/url.py`
- `subastas_clase/router.py`
- `subastas_clase/urls.py`
- `lavarropas.jpg`
- `db.sqlite3`

### PR #6 - `feature/Paula-Valentino-TP4` - merge `80df423`

En TP4 dividimos el trabajo entre reglas de negocio y experiencia de consulta. Valentino inicio las validaciones de anuncios; Paula avanzo con filtros, orden, versionado por URL y paginacion. Despues se agregaron commits de ajuste para que las APIViews anteriores siguieran funcionando con el nuevo versionado.

Commits del branch:
- `300cfed`: `feat: agregar validaciones a las operaciones de anuncios`
- `1966463`: `feat: agregar filtros y orden en la consulta de categorias y anuncios, versionado por url`
- `e8f78c6`: `paginacion`
- `85ed30c`: `fix: versionado de api, filtros y orden modificados`
- `ec81478`: `fix: compatibilidad de api views con versionado por url`

Cambios incorporados:
- Se agregaron validaciones sobre operaciones de anuncios.
- Se incorporaron filtros y orden para consultas de categorias y anuncios.
- Se agrego versionado de la API por URL.
- Se sumo paginacion.
- Se adapto la compatibilidad de las APIViews con el esquema de versionado.
- Se creo `apps/anuncio/filters.py`.
- Se creo `apps/anuncio/v1_urls.py`.
- Se ajustaron serializers, settings, modelos y URLs globales para soportar esos cambios.
- Se agregaron `analisis_commits_tp4.pdf` y `bici de montaña.jpg` como archivos asociados a esa entrega.

Archivos tocados:
- `apps/anuncio/api.py`
- `apps/anuncio/filters.py`
- `apps/anuncio/models.py`
- `apps/anuncio/serializers.py`
- `apps/anuncio/v1_urls.py`
- `subastas_clase/settings.py`
- `subastas_clase/urls.py`
- `db.sqlite3`
- `analisis_commits_tp4.pdf`
- `bici de montaña.jpg`

### PR #7 - `feature/paula-valentino-tp5` - merge `0d280bd`

En TP5 trabajamos sobre seguridad, permisos y orden interno de la API. Esta etapa fue importante porque reorganizo la app `anuncio`: la API dejo de estar concentrada en un unico `api.py` y paso a una carpeta `apps/anuncio/api/` con responsabilidades separadas.

Commits del branch:
- `eb293fc`: `feat: jwt wip`
- `718b9f2`: `feat(admin): registra modelos y ajusta imports de API`
- `733fa47`: `feat(admin): registra modelos y ajusta imports de API`

Cambios incorporados:
- Se agrego autenticacion JWT con `rest_framework_simplejwt`.
- Se agregaron endpoints para obtener y refrescar token:
  - `api/token/`
  - `api/token/refresh/`
- Se creo la carpeta `apps/anuncio/api/` para separar:
  - `legacy.py`
  - `permissions.py`
  - `serializers.py`
  - `urls.py`
  - `viewsets.py`
- Se mantuvo compatibilidad moviendo la API anterior a `apps/anuncio/api/legacy.py`.
- Se agregaron permisos estrictos por modelo con `StrictModelPermissions`.
- Se agrego permiso de propietario para que solo el creador pueda modificar su anuncio.
- Se agrego `uuid` a `Anuncio` y se configuro como lookup principal en la API nueva.
- Se agrego endpoint para crear ofertas sobre anuncios.
- Se registraron modelos en el admin de Django.
- Se ajustaron imports y URLs para que la nueva estructura quedara integrada.

Archivos tocados:
- `apps/anuncio/admin.py`
- `apps/anuncio/api/__init__.py`
- `apps/anuncio/api/legacy.py`
- `apps/anuncio/api/permissions.py`
- `apps/anuncio/api/serializers.py`
- `apps/anuncio/api/urls.py`
- `apps/anuncio/api/viewsets.py`
- `apps/anuncio/migrations/0002_anuncio_uuid.py`
- `apps/anuncio/models.py`
- `apps/anuncio/url.py`
- `apps/anuncio/v1_urls.py`
- `apps/usuario/admin.py`
- `subastas_clase/router.py`
- `subastas_clase/settings.py`
- `subastas_clase/urls.py`
- `db.sqlite3`

### PR #8 - `feature/paula-valentino-tp6` - merge `fe72d14`

En TP6 trabajamos con integraciones externas y documentacion automatica. Paula implemento el consumo de una API externa para mostrar usuarios y agrego manejo de errores junto con Swagger/Redoc. Valentino completo la conversion de moneda para anuncios y agrego el resumen de estado de la consulta de tipo de cambio.

Commits del branch:
- `391e82a`: `implementar consumo de API externa en la vista de usuarios`
- `f175420`: `agregar manejo de errores en users y documentacion Swagger/Redoc con drf-spectacular`
- `426baeb`: `feat(anuncios): incluir conversion de moneda y exchange_rate_summary en create/update`

Cambios incorporados:
- Se creo la app `core`.
- Se agrego la vista `/usuarios/`, que consume datos desde `https://jsonplaceholder.typicode.com/users`.
- Se agrego manejo de errores para HTTP, conexion, timeout y errores generales en esa vista.
- Se agrego template `core/usuarios.html`.
- Se integro `drf-spectacular` para documentacion automatica.
- Se agregaron endpoints de documentacion:
  - `api/schema/`
  - `api/docs/swagger/`
  - `api/docs/redoc/`
- Se agrego `exchange_service.py` para consultar una API externa de tipo de cambio.
- Los endpoints de anuncios pueden devolver `precio_inicial_convertido`, `moneda_convertida` y `exchange_rate_summary`.
- Se agrego lectura de variables desde `.env` para configurar la API de tipo de cambio.

Archivos tocados:
- `.env`
- `.gitignore`
- `apps/anuncio/api/exchange_service.py`
- `apps/anuncio/api/serializers.py`
- `apps/anuncio/api/viewsets.py`
- `apps/core/`
- `subastas_clase/settings.py`
- `subastas_clase/urls.py`
- `db.sqlite3`

## Estado funcional actual

La API actual expone principalmente rutas bajo `api/v1/`.

Endpoints principales:
- `POST api/token/`: obtiene access y refresh token JWT.
- `POST api/token/refresh/`: refresca el token JWT.
- `GET/POST api/v1/anuncios/`: lista o crea anuncios.
- `GET/PUT/PATCH/DELETE api/v1/anuncios/<uuid>/`: consulta o modifica un anuncio por UUID.
- `GET api/v1/anuncios/<uuid>/tiempo-restante/`: calcula tiempo restante del anuncio.
- `POST api/v1/anuncios/<uuid>/ofertas/`: crea una oferta para un anuncio.
- `GET api/schema/`: esquema OpenAPI.
- `GET api/docs/swagger/`: documentacion Swagger.
- `GET api/docs/redoc/`: documentacion Redoc.
- `GET usuarios/`: vista HTML con usuarios obtenidos desde una API externa.

Capas incorporadas durante el desarrollo:
- CRUD de categorias con APIViews heredadas.
- CRUD de anuncios con APIViews heredadas.
- Generic views para categorias y anuncios.
- Viewsets para anuncios.
- Versionado por URL.
- Filtros, orden y paginacion.
- Validaciones de anuncios.
- Autenticacion JWT.
- Permisos por modelo y permisos de propietario.
- Creacion de ofertas.
- Lookup de anuncios por UUID en la API nueva.
- Documentacion automatica con Swagger y Redoc.
- Consumo de API externa para usuarios.
- Conversion de moneda para precios de anuncios.

## Variables de entorno

El proyecto lee variables desde `.env` para la integracion de tipo de cambio:

```env
EXCHANGERATE_API_KEY=
EXCHANGERATE_BASE_URL=https://v6.exchangerate-api.com/v6
EXCHANGERATE_SOURCE_CURRENCY=ARS
EXCHANGERATE_TARGET_CURRENCY=USD
```

Si `EXCHANGERATE_API_KEY` no esta configurada, la API responde el anuncio igualmente, pero `exchange_rate_summary` indica el error de configuracion.

## Como ejecutar

Activar el entorno virtual y correr el servidor:

```powershell
env\Scripts\activate
python manage.py runserver
```

Verificar configuracion del proyecto:

```powershell
env\Scripts\python.exe manage.py check
```

## Evidencia manual

![Endpoints probados en Postman](docs/pruebas_postman.png)

## Referencias de pull requests

- PR #1: <https://github.com/valentinomarchettti/desarrollo-apis-tp2/pull/1>
- PR #2: <https://github.com/valentinomarchettti/desarrollo-apis-tp2/pull/2>
- PR #3: <https://github.com/valentinomarchettti/desarrollo-apis-tp2/pull/3>
- PR #5: <https://github.com/valentinomarchettti/desarrollo-apis-tp2/pull/5>
- PR #6: <https://github.com/valentinomarchettti/desarrollo-apis-tp2/pull/6>
- PR #7: <https://github.com/valentinomarchettti/desarrollo-apis-tp2/pull/7>
- PR #8: <https://github.com/valentinomarchettti/desarrollo-apis-tp2/pull/8>
