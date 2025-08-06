# ⚛️ Job Market Analyzer - Frontend

**Frontend premium del Job Market Analyzer**

Interfaz moderna desarrollada en React con Material-UI para visualizar y analizar el mercado laboral de desarrolladores.

## 🚀 Características

- **React 18**: Framework de interfaz moderna
- **TypeScript**: Tipado estático para mejor desarrollo
- **Material-UI**: Componentes de diseño premium
- **Framer Motion**: Animaciones fluidas
- **Recharts**: Gráficos interactivos
- **Vite**: Build tool rápido
- **Responsive Design**: Optimizado para todos los dispositivos

## 📁 Estructura

```
frontend/
├── src/
│   ├── components/         # Componentes reutilizables
│   │   └── Layout.tsx     # Layout principal
│   ├── pages/             # Páginas de la aplicación
│   │   ├── Dashboard.tsx  # Dashboard principal
│   │   ├── JobOffers.tsx  # Lista de ofertas
│   │   ├── Analytics.tsx  # Análisis avanzado
│   │   └── Settings.tsx   # Configuración
│   ├── theme/             # Configuración de temas
│   │   └── index.ts       # Tema Material-UI
│   ├── App.tsx            # Componente principal
│   ├── main.tsx           # Punto de entrada
│   └── index.css          # Estilos globales
├── package.json           # Dependencias Node.js
├── vite.config.ts         # Configuración Vite
├── tsconfig.json          # Configuración TypeScript
└── index.html             # HTML principal
```

## 🛠️ Instalación

### Requisitos Previos
- Node.js 16+
- npm o yarn
- Backend ejecutándose en puerto 8000

### Instalación Rápida

```bash
# 1. Navegar al directorio frontend
cd frontend

# 2. Instalar dependencias
npm install

# 3. Ejecutar en modo desarrollo
npm start

# 4. Abrir en navegador
# http://localhost:3000
```

## 🎨 Características de Diseño

### Tema Premium
- **Colores**: Paleta azul y púrpura profesional
- **Tipografía**: Inter font family
- **Componentes**: Material-UI personalizado
- **Animaciones**: Transiciones suaves con Framer Motion

### Páginas Principales

#### Dashboard
- Métricas en tiempo real
- Gráficos interactivos
- Actividad reciente
- Distribución de tecnologías

#### Ofertas de Trabajo
- Lista de ofertas con filtros
- Búsqueda avanzada
- Detalles de cada oferta
- Tecnologías requeridas

#### Analytics
- Análisis por empresa
- Estadísticas por ubicación
- Tendencias tecnológicas
- Gráficos comparativos

#### Configuración
- Configuración general
- Configuración de datos
- Configuración de API
- Exportación de datos

## 🔧 Desarrollo

### Comandos Disponibles

```bash
# Desarrollo
npm start          # Servidor de desarrollo
npm run dev        # Alias para start

# Build
npm run build      # Build de producción
npm run preview    # Preview del build

# Linting
npm run lint       # Verificar código
npm run lint:fix   # Corregir automáticamente
```

### Configuración de Desarrollo

```typescript
// vite.config.ts
export default defineConfig({
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''),
      },
    },
  },
})
```

### Variables de Entorno

```bash
# .env
VITE_API_URL=http://localhost:8000
VITE_APP_TITLE=Job Market Analyzer Premium
```

## 🎯 Componentes Principales

### Layout
- Sidebar de navegación
- AppBar con notificaciones
- Diseño responsive
- Tema dinámico

### Dashboard
- Cards de métricas
- Gráficos de barras y pastel
- Actividad reciente
- Indicadores de tendencia

### Charts
- Recharts para visualizaciones
- Gráficos interactivos
- Responsive design
- Temas personalizados

## 📱 Responsive Design

- **Desktop**: Layout completo con sidebar
- **Tablet**: Sidebar colapsable
- **Mobile**: Navegación hamburger
- **Breakpoints**: Material-UI responsive

## 🔌 Integración con Backend

### API Calls
```typescript
// Ejemplo de llamada a la API
const response = await fetch('/api/dashboard/stats/');
const data = await response.json();
```

### Endpoints Utilizados
- `/api/dashboard/stats/` - Estadísticas del dashboard
- `/api/offers/` - Lista de ofertas
- `/api/analytics/company-stats/` - Estadísticas por empresa
- `/api/health/` - Health check

## 🧪 Testing

```bash
# Tests unitarios (configurar)
npm test

# Tests de integración
npm run test:integration

# Coverage
npm run test:coverage
```

## 🚀 Deployment

### Build de Producción
```bash
npm run build
```

### Servir Build
```bash
npm run preview
```

### Docker (opcional)
```bash
# Construir imagen
docker build -t job-market-frontend .

# Ejecutar contenedor
docker run -p 3000:3000 job-market-frontend
```

## 🎨 Personalización

### Temas
```typescript
// src/theme/index.ts
export const theme = createTheme({
  palette: {
    primary: { main: '#2563eb' },
    secondary: { main: '#7c3aed' },
  },
  // Personalizar más aquí
});
```

### Componentes
- Todos los componentes son personalizables
- Sistema de temas consistente
- Props para configuración
- HOCs para funcionalidad adicional

## 📊 Performance

- **Lazy Loading**: Carga bajo demanda
- **Code Splitting**: Chunks optimizados
- **Tree Shaking**: Eliminación de código no usado
- **Caching**: Estrategias de cache optimizadas

## 🔒 Seguridad

- **CORS**: Configurado para backend
- **XSS Protection**: Sanitización de datos
- **HTTPS**: Configuración para producción
- **Environment Variables**: Configuración segura

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