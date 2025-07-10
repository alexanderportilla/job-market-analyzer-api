# Job Market Analyzer API

Este proyecto es un scraper y API para analizar el mercado laboral de desarrolladores Python en Colombia, extrayendo ofertas de [Computrabajo](https://www.computrabajo.com.co/).

## Requisitos

- Python 3.8 o superior
- pip
- Git
- (Opcional) Entorno virtual recomendado

## Instalación

1. **Clona el repositorio:**

   ```sh
   git clone https://github.com/alexanderportilla/job-market-analyzer-api.git
   cd job-market-analyzer-api
   ```

2. **Crea y activa un entorno virtual (opcional pero recomendado):**

   ```sh
   python -m venv venv
   venv\Scripts\activate   # En Windows
   # source venv/bin/activate   # En Linux/Mac
   ```

3. **Instala las dependencias:**

   ```sh
   pip install -r requirements.txt
   ```

## Configuración

1. **Configura la base de datos:**

   Por defecto, el proyecto usa SQLite. Puedes modificar la configuración en el archivo `app/database.py` si deseas usar otro motor.

2. **Crea las tablas de la base de datos:**

   Si usas SQLAlchemy, normalmente basta con ejecutar el script principal o el archivo de inicialización de la base de datos.

## Ejecución del Scraper

Para ejecutar el scraper y guardar las ofertas en la base de datos:

```sh
python -m app.scraper
```

O bien, si el scraper está integrado en una API FastAPI, puedes ejecutar el servidor:

```sh
uvicorn app.main:app --reload
```

Y luego acceder a los endpoints definidos.

## Estructura del Proyecto

```
app/
  ├── scraper.py        # Scraper principal
  ├── models.py         # Modelos de la base de datos
  ├── schemas.py        # Esquemas Pydantic
  ├── database.py       # Configuración de la base de datos
  └── main.py           # (Opcional) API principal
requirements.txt
README.md
```

## Personalización

- Puedes cambiar el número de páginas a scrapear modificando el parámetro `pages` en la función `scrape_job_offers`.
- Para cambiar la palabra clave de búsqueda, edita la variable `BASE_URL` en `scraper.py`.

## Notas

- El scraper puede dejar de funcionar si Computrabajo cambia su estructura HTML.
- Respeta los términos de uso de los sitios web que scrapeas.

---

**Autor:** Alexander Portilla  
**Repositorio:** [https://github.com/alexanderportilla/job-market-analyzer-api](https://github.com/alexanderportilla/job-market-analyzer-api)
