# 🐍 Job Market Analyzer - Backend

**Backend principal del Job Market Analyzer Premium**

API REST desarrollada en FastAPI para el análisis del mercado laboral de desarrolladores en Colombia.

## 🚀 Características

- **FastAPI**: Framework web moderno y rápido
- **SQLAlchemy**: ORM para MySQL
- **Web Scraping**: Extracción de ofertas de Computrabajo
- **Análisis de Datos**: Procesamiento con Pandas
- **MySQL**: Base de datos robusta
- **Docker**: Containerización completa

## 📁 Estructura

```
backend/
├── app/                    # Código principal de la aplicación
│   ├── main.py            # Punto de entrada de FastAPI
│   ├── config.py          # Configuración centralizada
│   ├── database.py        # Configuración de base de datos
│   ├── models.py          # Modelos SQLAlchemy
│   ├── schemas.py         # Esquemas Pydantic
│   ├── scraper.py         # Web scraper
│   └── analyzer.py        # Análisis de datos
├── scripts/               # Scripts de utilidad
│   ├── setup_mysql.py     # Configuración MySQL
│   └── init_premium_app.py # Setup completo
├── tests/                 # Tests unitarios
├── requirements.txt       # Dependencias Python
├── Dockerfile            # Containerización
└── pyproject.toml        # Configuración de herramientas
```

## 🛠️ Instalación

### Requisitos Previos
- Python 3.8+
- MySQL 8.0+
- Git

### Instalación Rápida

```bash
# 1. Clonar repositorio
git clone <repository-url>
cd job-market-analyzer-api-main/backend

# 2. Crear entorno virtual
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar MySQL
python scripts/setup_mysql.py

# 5. Ejecutar aplicación
uvicorn app.main:app --reload --port 8000
```

## 🔌 API Endpoints

### Core Endpoints
- `GET /` - Información de la API
- `POST /scrape/` - Ejecutar scraper
- `GET /offers/` - Listar ofertas
- `GET /offers/search/` - Buscar ofertas

### Dashboard Endpoints
- `GET /dashboard/stats/` - Estadísticas del dashboard
- `GET /dashboard/recent-activity/` - Actividad reciente

### Analytics Endpoints
- `GET /stats/technologies/` - Estadísticas de tecnologías
- `GET /analytics/company-stats/` - Estadísticas por empresa
- `GET /analytics/location-stats/` - Estadísticas por ubicación

### Health & Monitoring
- `GET /health/` - Health check
- `GET /docs` - Documentación Swagger

## 🗄️ Base de Datos

### Configuración MySQL
```bash
# Usuario: root
# Contraseña: 2024
# Base de datos: job_market
# Puerto: 3306
```

### Estructura de Tablas
```sql
CREATE TABLE job_offers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    company VARCHAR(255),
    location VARCHAR(255),
    description TEXT,
    url VARCHAR(500) UNIQUE,
    source VARCHAR(100),
    scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🧪 Testing

```bash
# Ejecutar tests
pytest

# Tests con cobertura
pytest --cov=app

# Tests específicos
pytest tests/test_analyzer.py
```

## 🐳 Docker

```bash
# Construir imagen
docker build -t job-market-backend .

# Ejecutar contenedor
docker run -p 8000:8000 job-market-backend

# Con docker-compose (desde la raíz del proyecto)
docker-compose up backend
```

## 🔧 Desarrollo

### Comandos Útiles

```bash
# Formatear código
black app/ tests/

# Linting
flake8 app/ tests/

# Type checking
mypy app/

# Instalar pre-commit hooks
pre-commit install
```

### Variables de Entorno

```bash
# .env
DATABASE_URL=mysql+mysqlconnector://root:2024@localhost:3306/job_market
API_HOST=localhost
API_PORT=8000
LOG_LEVEL=INFO
ENVIRONMENT=development
```

## 📊 Monitoreo

- **Health Check**: `GET /health/`
- **Documentación**: `GET /docs`
- **Logs**: Configurados con logging estructurado
- **Métricas**: Prometheus client integrado

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

## 📄 Licencia

MIT License - ver archivo LICENSE para más detalles.

---

**Desarrollado con ❤️ por Alexander Portilla** 