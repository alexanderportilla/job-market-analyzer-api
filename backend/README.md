# 🚀 Job Market Analyzer API - Backend

**Backend completo para el análisis del mercado laboral con integración MySQL**

Una API robusta que extrae, analiza y almacena datos del mercado laboral de desarrolladores en Colombia con base de datos MySQL y funcionalidades premium.

## 🏗️ Arquitectura

```
backend/
├── app/                    # 🐍 Código principal de la aplicación
│   ├── main.py            # FastAPI application
│   ├── models.py          # Modelos SQLAlchemy
│   ├── schemas.py         # Esquemas Pydantic
│   ├── database.py        # Configuración de base de datos
│   ├── scraper.py         # Web scraper para Computrabajo
│   ├── analyzer.py        # Análisis de datos
│   ├── config.py          # Configuración centralizada
│   └── auth.py            # Autenticación (futuro)
├── scripts/               # 🔧 Scripts de utilidad
│   └── setup_mysql.py     # Configuración MySQL
├── tests/                 # 🧪 Tests unitarios
├── requirements.txt       # Dependencias Python
└── start_with_mysql.py   # Script de inicio automático
```

## ✨ Características

### 🗄️ **Base de Datos MySQL**
- Configuración automática de MySQL
- Tablas optimizadas para consultas rápidas
- Backup y restauración automática
- Estadísticas en tiempo real

### 🔍 **Web Scraping Inteligente**
- Extracción automática de Computrabajo
- Detección de duplicados
- Manejo de errores robusto
- Respeta rate limits del servidor

### 📊 **Análisis Avanzado**
- Análisis de tecnologías más demandadas
- Estadísticas por empresa y ubicación
- Tendencias temporales del mercado
- Predicciones de demanda

### 🔌 **API REST Completa**
- Documentación automática (Swagger)
- Endpoints para todas las funcionalidades
- Autenticación y autorización
- Rate limiting y caching

## 🚀 Instalación Rápida

### Requisitos Previos
- Python 3.8+
- MySQL 8.0+
- Git

### Instalación Automática

```bash
# 1. Clonar repositorio
git clone https://github.com/alexanderportilla/job-market-analyzer-api.git
cd job-market-analyzer-api/backend

# 2. Ejecutar script de inicio automático
python start_with_mysql.py
```

El script automático:
- ✅ Verifica instalación de MySQL
- ✅ Configura la base de datos
- ✅ Instala dependencias
- ✅ Ejecuta tests de integración
- ✅ Inicia la aplicación

### Instalación Manual

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Configurar MySQL
python scripts/setup_mysql.py --setup

# 3. Probar integración
python test_mysql_integration.py

# 4. Iniciar aplicación
uvicorn app.main:app --reload --port 8000
```

## 🗄️ Configuración MySQL

### Instalación de MySQL

1. **Descargar MySQL Server:**
   - [MySQL Community Server](https://dev.mysql.com/downloads/mysql/)
   - Instalar con configuración por defecto
   - Establecer contraseña root: `2024`

2. **Descargar MySQL Workbench:**
   - [MySQL Workbench](https://dev.mysql.com/downloads/workbench/)
   - Conectar a `localhost:3306`

### Configuración Automática

```bash
# Configurar base de datos
python scripts/setup_mysql.py --setup

# Probar conexión
python scripts/setup_mysql.py --test

# Ver información de la base de datos
python test_mysql_integration.py --info
```

### Configuración Manual

```sql
-- Conectar a MySQL
mysql -u root -p2024

-- Crear base de datos
CREATE DATABASE job_market;
USE job_market;

-- Las tablas se crean automáticamente al iniciar la aplicación
```

## 🔧 Uso de la API

### Endpoints Principales

#### Scraping
```bash
# Ejecutar scraper
POST /scrape/?pages=3

# Verificar estado
GET /health/
```

#### Consultas de Datos
```bash
# Obtener todas las ofertas
GET /offers/

# Búsqueda avanzada
GET /offers/search/?q=python&location=bogota&company=techcorp

# Estadísticas de tecnologías
GET /stats/technologies/
```

#### Dashboard
```bash
# Estadísticas del dashboard
GET /dashboard/stats/

# Actividad reciente
GET /dashboard/recent-activity/
```

#### Analytics
```bash
# Estadísticas por empresa
GET /analytics/company-stats/

# Estadísticas por ubicación
GET /analytics/location-stats/

# Análisis de experiencia
GET /analytics/experience-analysis/
```

### Ejemplos de Uso

#### 1. Ejecutar Scraper
```bash
curl -X POST "http://localhost:8000/scrape/?pages=2"
```

#### 2. Obtener Estadísticas
```bash
curl "http://localhost:8000/dashboard/stats/"
```

#### 3. Buscar Ofertas
```bash
curl "http://localhost:8000/offers/search/?q=react&location=medellin"
```

## 📊 Estructura de la Base de Datos

### Tablas Principales

#### `job_offers`
```sql
CREATE TABLE job_offers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    company VARCHAR(255),
    location VARCHAR(255),
    description TEXT,
    url VARCHAR(1000) UNIQUE,
    source VARCHAR(100),
    scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_title (title),
    INDEX idx_company (company),
    INDEX idx_location (location),
    INDEX idx_scraped_at (scraped_at)
);
```

#### `users`
```sql
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    is_premium BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

#### `job_alerts`
```sql
CREATE TABLE job_alerts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    keywords TEXT,
    location VARCHAR(255),
    company VARCHAR(255),
    frequency VARCHAR(50) DEFAULT 'daily',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_sent TIMESTAMP NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

#### `saved_jobs`
```sql
CREATE TABLE saved_jobs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    job_offer_id INT,
    saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    notes TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (job_offer_id) REFERENCES job_offers(id)
);
```

## 🔍 Funcionalidades del Scraper

### Características del Scraper
- **Extracción automática** de Computrabajo
- **Detección de duplicados** por URL
- **Manejo de errores** robusto
- **Rate limiting** para respetar el servidor
- **Logging detallado** de operaciones
- **Commit por página** para evitar pérdida de datos

### Configuración del Scraper
```python
# En app/config.py
BASE_URL = "https://www.computrabajo.com.co/ofertas-de-trabajo/?q=python"
MAX_PAGES = 10
REQUEST_TIMEOUT = 15
DELAY_BETWEEN_REQUESTS = 1.0
```

### Uso del Scraper
```python
from app.scraper import scrape_job_offers
from app.database import get_db

# Ejecutar scraper
db = next(get_db())
result = scrape_job_offers(db, pages=3)
print(result)
```

## 📈 Análisis de Datos

### Funciones de Análisis
```python
from app.analyzer import analyze_technology_demand

# Analizar demanda de tecnologías
tech_stats = analyze_technology_demand(db)
for tech in tech_stats:
    print(f"{tech.technology}: {tech.percentage}%")
```

### Estadísticas Disponibles
- **Tecnologías más demandadas**
- **Empresas más activas**
- **Ubicaciones con más oportunidades**
- **Tendencias temporales**
- **Análisis de experiencia requerida**

## 🧪 Testing

### Tests de Integración
```bash
# Ejecutar todos los tests
python test_mysql_integration.py

# Test específico
python test_mysql_integration.py --connection
python test_mysql_integration.py --insert
python test_mysql_integration.py --scraping
```

### Tests Unitarios
```bash
# Ejecutar tests unitarios
pytest tests/

# Con coverage
pytest --cov=app tests/
```

## 🐳 Docker

### Construir Imagen
```bash
docker build -t job-market-analyzer-backend .
```

### Ejecutar con Docker Compose
```bash
docker-compose up --build
```

### Variables de Entorno
```bash
# .env
DATABASE_URL=mysql+mysqlconnector://root:2024@mysql:3306/job_market
API_HOST=0.0.0.0
API_PORT=8000
ENVIRONMENT=production
```

## 🔧 Configuración Avanzada

### Variables de Entorno
```bash
# Base de datos
DATABASE_URL=mysql+mysqlconnector://root:2024@localhost:3306/job_market

# API
API_HOST=localhost
API_PORT=8000
ENVIRONMENT=development

# Scraping
BASE_URL=https://www.computrabajo.com.co/ofertas-de-trabajo/?q=python
MAX_PAGES=10
REQUEST_TIMEOUT=15
DELAY_BETWEEN_REQUESTS=1.0
```

### Logging
```python
# Configurar logging
import logging
logging.basicConfig(level=logging.INFO)
```

### Performance
```python
# Optimizar consultas
from sqlalchemy import create_engine
engine = create_engine(DATABASE_URL, pool_pre_ping=True, pool_recycle=300)
```

## 🚀 Deployment

### Producción
```bash
# Instalar dependencias de producción
pip install -r requirements.txt

# Configurar base de datos
python scripts/setup_mysql.py --setup

# Ejecutar con Gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Cloud Platforms
- **Heroku**: Configurar add-on MySQL
- **Railway**: Deploy automático
- **DigitalOcean**: Droplet con MySQL
- **AWS**: RDS MySQL + EC2

## 📚 Documentación API

### Swagger UI
- **URL**: http://localhost:8000/docs
- **Documentación interactiva**
- **Pruebas de endpoints**

### ReDoc
- **URL**: http://localhost:8000/redoc
- **Documentación alternativa**

## 🤝 Contribución

1. Fork el proyecto
2. Crear rama feature (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 🆘 Soporte

- **Issues**: [GitHub Issues](https://github.com/alexanderportilla/job-market-analyzer-api/issues)
- **Documentación**: [Wiki del proyecto](https://github.com/alexanderportilla/job-market-analyzer-api/wiki)
- **Email**: alexander.portilla@example.com

---

**Desarrollado con ❤️ por Alexander Portilla**

*Transformando el análisis del mercado laboral en una experiencia premium* 