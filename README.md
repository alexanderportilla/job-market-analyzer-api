# 🚀 Job Market Analyzer Premium

**Análisis completo del mercado laboral de desarrolladores en Colombia**

Una aplicación premium para analizar, visualizar y entender las tendencias del mercado laboral tech con interfaz moderna y análisis avanzado.

## 🏗️ Arquitectura del Proyecto

```
job-market-analyzer-api-main/
├── backend/                 # 🐍 Backend Python (Principal)
│   ├── app/                # Código de la aplicación
│   ├── scripts/            # Scripts de utilidad
│   ├── tests/              # Tests unitarios
│   └── requirements.txt    # Dependencias Python
├── frontend/               # ⚛️ Frontend React
│   ├── src/                # Código React
│   └── package.json        # Dependencias Node.js
├── docs/                   # 📚 Documentación
├── docker-compose.yml      # 🐳 Orquestación completa
└── README.md               # Este archivo
```

## ✨ Características Premium

### 🎨 **Interfaz Moderna**
- Dashboard interactivo con métricas en tiempo real
- Gráficos y visualizaciones avanzadas
- Diseño responsive y animaciones fluidas
- Tema Material-UI personalizado

### 📊 **Análisis Avanzado**
- Web scraping automático de Computrabajo
- Análisis de tecnologías más demandadas
- Estadísticas por empresa y ubicación
- Tendencias temporales del mercado

### 🔧 **Funcionalidades Empresariales**
- API REST completa con documentación
- Base de datos MySQL robusta
- Exportación de reportes
- Sistema de notificaciones

## 🚀 Instalación Rápida

### Requisitos Previos
- Python 3.8+
- Node.js 16+
- MySQL 8.0+
- Git

### Instalación Automática

```bash
# 1. Clonar repositorio
git clone <repository-url>
cd job-market-analyzer-api-main

# 2. Verificar configuración
python scripts/verify_setup.py

# 3. Configurar backend
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
python scripts/setup_mysql.py

# 4. Configurar frontend
cd ../frontend
npm install

# 5. Ejecutar aplicación
# Terminal 1 - Backend
cd backend
uvicorn app.main:app --reload --port 8000

# Terminal 2 - Frontend
cd frontend
npm start
```

### Acceso a la Aplicación
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Documentación API**: http://localhost:8000/docs

## 📚 Documentación

- **[Backend](./backend/README.md)**: Documentación completa del backend Python
- **[Frontend](./frontend/README.md)**: Documentación del frontend React
- **[Documentación Premium](./docs/README_PREMIUM.md)**: Guía completa de características premium

## 🔌 API Endpoints Principales

### Core
- `GET /` - Información de la API
- `POST /scrape/` - Ejecutar scraper
- `GET /offers/` - Listar ofertas
- `GET /offers/search/` - Buscar ofertas

### Dashboard
- `GET /dashboard/stats/` - Estadísticas del dashboard
- `GET /dashboard/recent-activity/` - Actividad reciente

### Analytics
- `GET /stats/technologies/` - Estadísticas de tecnologías
- `GET /analytics/company-stats/` - Estadísticas por empresa
- `GET /analytics/location-stats/` - Estadísticas por ubicación

## 🛠️ Desarrollo

### Backend (Python)
```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

### Frontend (React)
```bash
cd frontend
npm start
```

### Tests
```bash
# Backend tests
cd backend
pytest

# Frontend tests (configurar)
cd frontend
npm test
```

## 🐳 Docker

### Ejecutar con Docker Compose
```bash
docker-compose up --build
```

### Servicios
- **Backend**: Puerto 8000
- **Frontend**: Puerto 3000
- **MySQL**: Puerto 3306

## 📊 Características de Análisis

### Métricas Automáticas
- Total de ofertas de trabajo
- Empresas activas contratando
- Tecnologías más demandadas
- Tendencias temporales

### Análisis Inteligente
- Detección automática de tecnologías
- Análisis de patrones temporales
- Clustering de empresas
- Predicciones de tendencias

## 🎯 Casos de Uso

### Para Desarrolladores
- Identificar tecnologías más demandadas
- Encontrar empresas que contratan
- Analizar tendencias del mercado
- Preparar CV según demandas

### Para Empresas
- Analizar competencia
- Identificar talento disponible
- Entender tendencias del mercado
- Optimizar estrategias de contratación

## 🔧 Configuración

### Variables de Entorno
```bash
# Backend (.env en backend/)
DATABASE_URL=mysql+mysqlconnector://root:2024@localhost:3306/job_market
API_HOST=localhost
API_PORT=8000

# Frontend (.env en frontend/)
VITE_API_URL=http://localhost:8000
VITE_APP_TITLE=Job Market Analyzer Premium
```

### Base de Datos
- **MySQL**: Puerto 3306
- **Usuario**: root
- **Contraseña**: 2024
- **Base de datos**: job_market

## 🚀 Deployment

### Producción
```bash
# Backend
cd backend
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker

# Frontend
cd frontend
npm run build
```

### Cloud Deployment
- **Backend**: Heroku, Railway, DigitalOcean
- **Frontend**: Vercel, Netlify, GitHub Pages
- **Base de datos**: AWS RDS, Google Cloud SQL

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📈 Roadmap

### Próximas Características
- [ ] Machine Learning para predicciones
- [ ] Notificaciones push en tiempo real
- [ ] Múltiples fuentes de datos (LinkedIn, Indeed)
- [ ] Análisis de salarios
- [ ] Comparación de mercados internacionales

### Mejoras Técnicas
- [ ] Cache Redis para mejor performance
- [ ] Background tasks con Celery
- [ ] Monitoring con Prometheus + Grafana
- [ ] CI/CD pipeline con GitHub Actions

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 🆘 Soporte

- **Issues**: [GitHub Issues](https://github.com/alexanderportilla/job-market-analyzer-api/issues)
- **Discusiones**: [GitHub Discussions](https://github.com/alexanderportilla/job-market-analyzer-api/discussions)
- **Documentación**: [Wiki del proyecto](https://github.com/alexanderportilla/job-market-analyzer-api/wiki)

---

**Desarrollado con ❤️ por Alexander Portilla**

*Transformando el análisis del mercado laboral en una experiencia premium*
