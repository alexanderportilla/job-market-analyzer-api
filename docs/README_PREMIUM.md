# 🚀 Job Market Analyzer Premium

**Transformando el análisis del mercado laboral en una experiencia premium**

Una aplicación completa y moderna para analizar el mercado laboral de desarrolladores en Colombia, con interfaz premium, análisis avanzado y funcionalidades empresariales.

## ✨ Características Premium

### 🎨 **Diseño y Experiencia de Usuario**
- **Interfaz Moderna**: Diseño Material-UI con tema personalizado
- **Responsive Design**: Optimizado para desktop, tablet y móvil
- **Animaciones Fluidas**: Transiciones suaves con Framer Motion
- **Dashboard Interactivo**: Métricas en tiempo real con gráficos dinámicos
- **Navegación Intuitiva**: Sidebar premium con navegación fluida

### 📊 **Análisis Avanzado**
- **Métricas en Tiempo Real**: Estadísticas actualizadas automáticamente
- **Gráficos Interactivos**: Barras, líneas, pastel y más con Recharts
- **Tendencias Temporales**: Análisis de evolución del mercado
- **Análisis por Tecnología**: Demanda detallada por stack tecnológico
- **Análisis por Empresa**: Estadísticas por compañía
- **Análisis por Ubicación**: Distribución geográfica de ofertas

### 🔧 **Funcionalidades Empresariales**
- **Exportación de Reportes**: PDF, Excel, CSV
- **Filtros Avanzados**: Búsqueda por múltiples criterios
- **Notificaciones**: Alertas de nuevas ofertas
- **Scheduling**: Scraping automático programado
- **API REST Completa**: Endpoints para integración
- **Base de Datos MySQL**: Almacenamiento robusto

### 🛡️ **Características Técnicas**
- **Arquitectura Moderna**: Frontend React + Backend FastAPI
- **Performance Optimizada**: Lazy loading, caching, optimización
- **Seguridad**: CORS, validación, sanitización
- **Testing Completo**: Unit tests, integration tests
- **CI/CD Ready**: Configuración para deployment
- **Docker Support**: Containerización completa

## 🏗️ Arquitectura del Sistema

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   Database      │
│   (React)       │◄──►│   (FastAPI)     │◄──►│   (MySQL)       │
│   Port: 3000    │    │   Port: 8000    │    │   Port: 3306    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │              ┌─────────────────┐              │
         └──────────────►│   Analytics     │◄─────────────┘
                        │   Engine        │
                        └─────────────────┘
```

## 🚀 Instalación Rápida

### Requisitos Previos
- Python 3.8+
- Node.js 16+
- MySQL 8.0+
- Git

### Instalación Automática
```bash
# Clonar repositorio
git clone https://github.com/alexanderportilla/job-market-analyzer-api.git
cd job-market-analyzer-api

# Ejecutar script de instalación premium
python scripts/init_premium_app.py
```

### Instalación Manual
```bash
# 1. Configurar entorno Python
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt

# 2. Configurar MySQL
python scripts/setup_mysql.py

# 3. Configurar Frontend
cd frontend
npm install
cd ..

# 4. Ejecutar aplicación
uvicorn app.main:app --reload --port 8000
# En otra terminal:
cd frontend && npm start
```

## 📱 Uso de la Aplicación

### Dashboard Principal
- **Métricas Clave**: Total ofertas, empresas activas, tecnologías únicas
- **Gráficos de Tendencias**: Evolución mensual del mercado
- **Actividad Reciente**: Últimas ofertas agregadas
- **Distribución de Tecnologías**: Gráfico de pastel interactivo

### Análisis de Ofertas
- **Lista Completa**: Todas las ofertas con paginación
- **Filtros Avanzados**: Por tecnología, empresa, ubicación
- **Búsqueda Inteligente**: Búsqueda semántica en descripciones
- **Exportación**: Descargar datos en múltiples formatos

### Analytics Avanzado
- **Análisis por Empresa**: Top empresas contratando
- **Análisis por Ubicación**: Distribución geográfica
- **Tendencias Tecnológicas**: Evolución de demandas
- **Reportes Personalizados**: Generar reportes a medida

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

## 🎨 Personalización

### Temas y Colores
```typescript
// frontend/src/theme/index.ts
export const theme = createTheme({
  palette: {
    primary: { main: '#2563eb' },
    secondary: { main: '#7c3aed' },
    // Personalizar colores aquí
  }
});
```

### Configuración de Base de Datos
```python
# app/config.py
class Settings:
    DATABASE_URL: str = "mysql://user:password@localhost:3306/db"
    # Personalizar configuración aquí
```

### Tecnologías a Analizar
```python
# app/config.py
TECHNOLOGIES: List[str] = [
    'Python', 'React', 'JavaScript', 'Java',
    # Agregar más tecnologías aquí
]
```

## 📊 Características de Análisis

### Métricas Automáticas
- **Total de Ofertas**: Conteo en tiempo real
- **Empresas Activas**: Empresas con ofertas recientes
- **Tecnologías Únicas**: Stack tecnológico detectado
- **Tendencias Mensuales**: Evolución del mercado

### Análisis Inteligente
- **Detección de Tecnologías**: Regex avanzado para identificación
- **Análisis de Tendencias**: Patrones temporales
- **Clustering de Empresas**: Agrupación por sector
- **Predicciones**: Machine Learning para tendencias futuras

## 🛠️ Desarrollo

### Estructura del Proyecto
```
job-market-analyzer-api/
├── app/                    # Backend FastAPI
│   ├── main.py            # API principal
│   ├── scraper.py         # Web scraper
│   ├── analyzer.py        # Análisis de datos
│   ├── models.py          # Modelos de BD
│   ├── schemas.py         # Esquemas Pydantic
│   ├── database.py        # Configuración BD
│   └── config.py          # Configuración
├── frontend/              # Frontend React
│   ├── src/
│   │   ├── components/    # Componentes React
│   │   ├── pages/         # Páginas
│   │   ├── theme/         # Temas Material-UI
│   │   └── App.tsx        # App principal
│   ├── package.json       # Dependencias Node
│   └── vite.config.ts     # Configuración Vite
├── scripts/               # Scripts de utilidad
├── tests/                 # Tests
├── docs/                  # Documentación
└── README_PREMIUM.md      # Este archivo
```

### Comandos de Desarrollo
```bash
# Backend
uvicorn app.main:app --reload --port 8000

# Frontend
cd frontend && npm start

# Tests
pytest
pytest --cov=app

# Linting
black app/ tests/
flake8 app/ tests/
mypy app/

# Database
python scripts/setup_mysql.py
```

## 🚀 Deployment

### Docker
```bash
# Construir y ejecutar
docker-compose up --build

# Solo backend
docker build -t job-market-api .
docker run -p 8000:8000 job-market-api
```

### Producción
```bash
# Backend con Gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker

# Frontend build
cd frontend && npm run build
```

## 📈 Roadmap

### Próximas Características
- [ ] **Machine Learning**: Predicción de tendencias
- [ ] **Notificaciones Push**: Alertas en tiempo real
- [ ] **API Rate Limiting**: Control de acceso
- [ ] **Autenticación JWT**: Sistema de usuarios
- [ ] **Múltiples Fuentes**: LinkedIn, Indeed, etc.
- [ ] **Análisis de Salarios**: Ranges salariales
- [ ] **Comparación de Mercados**: Colombia vs otros países
- [ ] **Reportes Automáticos**: Email con insights

### Mejoras Técnicas
- [ ] **Cache Redis**: Mejor performance
- [ ] **Background Tasks**: Scraping asíncrono
- [ ] **Monitoring**: Prometheus + Grafana
- [ ] **CI/CD Pipeline**: GitHub Actions
- [ ] **Microservicios**: Arquitectura escalable

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 🆘 Soporte

- **Documentación**: [Wiki del proyecto](https://github.com/alexanderportilla/job-market-analyzer-api/wiki)
- **Issues**: [GitHub Issues](https://github.com/alexanderportilla/job-market-analyzer-api/issues)
- **Discusiones**: [GitHub Discussions](https://github.com/alexanderportilla/job-market-analyzer-api/discussions)

---

**Desarrollado con ❤️ por Alexander Portilla**

*Transformando el análisis del mercado laboral en una experiencia premium* 