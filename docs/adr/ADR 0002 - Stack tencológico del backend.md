
## Estado

Aceptada - 2026-06-01
## Contexto

El Documento de Visión recoge la definición del proyecto ChemLab: un laboratorio virtual de química accesible desde el navegador. Para el MVP (Fase 1) se requiere construir una API REST que sirva información estructurada sobre los elementos de la tabla periódica. Es fundamental implementar una solución escalable, que sirva de base para construir módulos de aprendizaje y ejercicios con compuestos y reacciones.

La decisión prioritaria en este momento es el stack tecnológico que va a condicionar el resto del desarrollo. Conviene hacerlo de forma precisa, ya que un cambio en el stack en una fase posterior puede implicar refactorizaciones costosas o reescrituras completas, en el peor de los casos.

Asimismo, el stack debe ser coherente con las restricciones planteadas en el Documento de Visión: desarrollo unipersonal en horario parcial, dominio principal del autor en Python y necesidad de cumplir RGPD en fases futuras.

El presente ADR cubre las decisiones sobre:
- Versión de Python
- Framework backend
- Gestión de dependencias
- ORM y base de datos relacional
- Validación de datos
- Herramientas de testing y calidad de código (linter/formatter)
- Servidor ASGI
- Contenerización

Quedan fuera del alcance y se documentarán en ADRs específicos:
-  Framework frontend
-  Estrategia de migraciones de BBDD
-  Estrategia de autenticación y autorización
-  Plataforma de despliegue y CI/CD
## Decisión

##### 1. Lenguaje y runtime - Python 3.12

Se elige Python 3.12 por ser una versión estable consolidada, con soporte oficial hasta octubre de 2028 y compatibilidad madura con el ecosistema de librerías del stack (FastAPI, SQLAlchemy 2.0, Pydantic v2).

##### 2. Framework backend - FastAPI

Se decide usar FastAPI por su enfoque API-first con soporte nativo async/await (relevante para escalar I/O concurrente y para una futura integración con frontend desacoplado). FastAPI genera la especificación OpenAPI automáticamente, lo que reduce costes de mantenimiento de la documentación de API sincronizada.
##### 3. Gestor de dependencias - uv

Se elige uv como gestor unificado de dependencias, entornos virtuales y versiones de Python. Sustituye al stack tradicional pip + virtualenv + pyenv en una única herramienta con reproducibilidad vía `uv.lock`y rendimiento muy superior gracias a su núcleo en Rust. Se valora positivamente la coherencia con Ruff, ambos del mismo proveedor (Astral), para reducir la heterogeneidad del stack.
##### 4. ORM y base de datos - SQLAlchemy 2.0 (async) + PostgreSQL

Para implementar un modelo de datos relacional para elementos químicos se elige PostgreSQL como SGBD debido a la solidez que aporta su estructura relacional y tipado fuerte. Además, el soporte nativo de JSONB permite almacenar datos semi-estructurados (propiedades variables, metadatos de ejercicios) sin renunciar al modelo relacional. y sus características de extensibilidad facilitan el escalado hacia nuevos modelos de datos científicos. También se valora positivamente su licencia open source permisiva (PostgreSQL License) sin costes ni vendor lock-in.

Para implementar un ORM se elige el estándar en Python SQLAlchemy 2.0, ya que aporta madurez consolidada para operaciones CRUD, consultas asíncronas y prevención automática de inyecciones SQL al usar consultas parametrizadas. Esta solución es agnóstica respecto al motor de BD, lo que la hace compatible con un escalado hacia un modelo de datos complementario no relacional.
##### 5. Validación - Pydantic v2

Se elige Pydantic v2 por su integración nativa con FastAPI (validación de entradas y serialización de salidas declarativa vía type hints) y su rendimiento, gracias a un núcleo reescrito en Rust que reduce significativamente el coste de validación frente a v1.
##### 6. Servidor ASGI - Uvicorn (dev) | Gunicorn + Uvicorn workers (producción)

Uvicorn es la implementación de referencia de ASGI y el servidor recomendado oficialmente por FastAPI. En desarrollo se ejecuta de forma directa (`uvicorn --reload`). En producción se ejecuta bajo Gunicorn como gestor de procesos, lo que permite levantar múltiples workers para aprovechar varios núcleos, gestionar reinicios automáticos ante fallos y desacoplar el ciclo de vida del proceso del servidor ASGI.

##### 7. Contenerización - Docker + Docker Compose

Se adopta Docker + Docker Compose desde el inicio del proyecto. Permite paridad en los entornos de desarrollo, CI y producción. Compose orquesta los servicios necesarios (API, PostgreSQL, futuros: cache, mensajería) y reduce el onboarding de colaboradores a un solo comando (`docker compose up`). Además, sienta la base técnica para la integración futura de CI/CD y despliegue contenedorizado.

##### 8. Testing - pytest + pytest-asyncio + pytest-cov + httpx

Se decide utilizar pytest como framework de testing por su madurez en el ecosistema Python, su sintaxis declarativa y su sistema de fixtures, que permite inyectar dependencias reutilizables en los test (cliente HTTP, sesión de BBDD de prueba, datos seed) de forma explícita y componible.

Plugins adicionales:
-  **pytest-asyncio:** permite escribir test asíncronos. Es necesario ya que FastAPI es un framework async.
-  **pytest-cov:** mide la cobertura de código ejecutada por los test y genera reportes (terminal, HTML, XML para CI). Permite establecer un umbral mínimo de cobertura como criterio de calidad.
-  **httpx:** cliente HTTP usado para invocar los endpoints de FastAPI desde los tests ( a través de `TestClient` o `AsyncClient`), validando el comportamiento extremo a extremo de la API sin necesidad de levantar un servidor real.

##### 9. Calidad de código - Ruff (linter + formatter) + mypy

Se adopta Ruff como linter y formateador unificado. Sustituye al stack tradicional Black (formateo) + isort (orden de imports) + Flake8 y sus plugins (linting), centralizando en una única herramienta configurable vía `pyproject.toml`. Su núcleo en Rust ofrece tiempos de ejecución varios órdenes de magnitud por debajo de las herramientas que reemplaza, lo que permite integrarlo de forma fluida en pre-commit hooks y CI. Adicionalemente, comparte proveedor (Astral) con uv, lo que reduce la heterogeneidad del tooling.

Se adopta mypy como verificador de tipos estáticos. A diferencia de Pydantic (que valida datos externos en tiempo de ejecución), mypy analiza el código fuente sin ejecutarlo y detecta inconsistencias de tipos en tiempo de desarrollo (variables `None` no comprobadas, llamadas con tipos incorrectos, etc.). El uso combinado con Pydantic v2 es especialmente fluido, ya que sus modelos generan tipos que mypy interpreta nativamente.

## Consecuencias

##### Positivas

-  **Reproducibilidad de entornos:** Docker + uv garantizan que cualquier colaborador (o el pipeline de CI/CD) levante exactamente el mismo entorno con un único comando, eliminando errores de funcionamiento dependientes de la máquina.

-  **Extensibilidad funcional:** el enfoque API-first de FastAPI permite añadir un frontend desacoplado (Vue/React) o integrar consumidores adicionales (móvil, scripts, otras APIs) sin modificar la capa de lógica. PostgreSQL, por su parte, soporta crecimiento del modelo de datos sin migración a otro motor.

-  **Calidad técnica blindada desde el día 1:** linter, formateador, validación tipada (mypy) y testing automatizado se aplican en pre-commit y CI, detectando errores antes de llegar a producción y forzando un estándar de calidad homogéneo durante todo el desarrollo.

-  **Documentación automática de la API:** los endpoints quedan documentados automáticamente por FastAPI vía OpenAPI/Swagger en `/docs`. Esto elimina la necesidad de mantener documentación de API en herramientas externas y garantiza que la documentación nunca se desincronice del código.

- **Async desde el día 1:** El stack elegido permite manejar múltiples operaciones I/O concurrentes sin bloqueo. Esta base es fundamental para integrar en el futuro llamadas a APIs externas (PubChem, datasets químicos) o procesos asíncronos largos sin necesidad de refactorización.

- **Aprendizaje alineado con el mercado:** El stack elegido para este proyecto (FastAPI, Pydantic v2, SQLAlchemy 2.0 async, Ruff, uv) coincide con herramientas habituales en ofertas actuales de desarrollo backend con Python. Esto alinea el desarrollo unipersonal del proyecto con la trayectoria profesional del autor, convirtiendo el aprendizaje invertido en activo de empleabilidad.

##### Trade-offs asumidos

- **Servicios no incluidos en el framework:** FastAPI no proporciona panel de administración, sistema de autenticación, ni gestor de usuarios listos para usar. Estos componentes deberán construirse manualmente o integrarse vía librerías externas (SQLAdmin, fastapi-users, etc.) en las fases correspondientes. **Decisiones pospuestas a sus ADRs específicos**.

- **Coste inicial de configuración:** el tooling profesional (Docker, pre-commit, mypy, Ruff, pytest, configuración de CI) requiere una inversión de tiempo significativa en las primeras semanas antes de empezar a producir código de negocio. Este coste se amortiza a lo largo del proyecto, pero penaliza la velocidad inicial.

- **Fricción continua del tipado y la calidad estricta:** mypy en modo estricto y el linter rechazarán código que en proyectos más laxos pasaría. Esto eleva la calidad media, pero ralentiza puntualmente el desarrollo, especialmente mientras se internalizan las convenciones.

- **Madurez desigual del tooling:** Aunque el grueso del stack es maduro (FastAPI, SQLAlchemy, PostgreSQL, Docker), algunas herramientas son más recientes (como uv y, en menor medida, Ruff). Se asume el riesgo de cambios disruptivos en sus APIs o pérdida de momentum. Se mitiga fijando versiones en `pyproject.toml` y monitorizando los repositorios oficiales.

- **Curva de aprendizaje técnica:** El stack incluye varias tecnologías que el autor no domina aún (SQLAlchemy 2.0 async, asyncio en profundidad, mypy estricto, configuración avanzada de Docker). Se acepta este coste de aprendizaje como inversión formativa alineada con el objetivo profesional del proyecto.

## Alternativas consideradas

##### Framework backend

-  **Django (+ Django REST Framework):** framework maduro con baterías incluidas (ORM propio, panel de administración auto-generado, sistema de autenticación, lplantillas, middleware), ampliamente adoptado en ele mercado laboral español. Se descarta porque ChemLab es un proyecto API-first con frontend planificado desacoplado, lo que deja sin uso buena parte del ecosistema Django (plantillas, sistema de formularios, middleware tradicional). Adicionalemente, el soporte async, la validación tipada con Pydantic y la generación automática de OpenAPI requerirán capas adicionales sobre Django, mientras que FastAPI las ofrece de serie. Se reconoce que Django Admin sería un valor real para el panel docente de la Fase 3; este trade-off ya queda documentado en la sección Consecuencias.

-  **Flask:** framework web minimalista de Python, con gran ecosistema de extensiones y una comunidad muy consolidada. Se descarta porque carece de soporte async como ciudadano de primera clase, validación tipada nativa y generación automática de OpenAPI; todas estas funcionalidades, claves para el proyecto, requerirán integrar librerías externas (Marshmallow, flask-async, flasgger, etc.). El resultado acabaría reproduciendo lo que FastAPI ofrece nativamente, pero con mayor coste de mantenimiento y menor coherencia.
##### Gestor de dependencias

-  **Poetry:** Gestor de dependencias maduro con lockfile, gestión de entornos virtuales, publicación PyPI integrada y características muy valoradas que han hecho que sea un estándar de facto en los últimos años. Se opta por uv porque su núcleo en Rust hace que sea varios órdenes de magnitud más rápido que Poetry (Python). Además uv aporta beneficios extra a este proyecto, como la gestión integrada de versiones de Python y la coherencia con Ruff, con el que comparte proveedor. Se considera Poetry como una alternativa sólida, aunque se ha decidido asumir el riesgo de juventud de uv a cambio de simplicidad y velocidad.

- **Pip + venv tradicional:** combinación estándar histórica de la stdlib de Python. Se descarta para este proyecto porque, sin herramientas adicionales como `pip-tools`, no proporciona lockfile reproducible ni resolución determinista de  dependencias, y requiere orquestar varias herramientas (pip, venv, pyenv) por separado.

##### Calidad de código

- **Black + isort + Flake8 (+pylint)**: Stack tradicional con componentes especializados para formateo, ordenación de imports y linting respectivamente. Se descarta porque Ruff sustitutye a las tres en una sola herramienta, con configuración centralizada en `pyproject.toml` y velocidad muy superior (núcleo Rust). La velocidad es clave para integrar la verificación en pre-commit hooks sin penalizar el flujo de trabajo.
