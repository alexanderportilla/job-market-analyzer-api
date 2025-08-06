import React from 'react';
import {
  Grid,
  Card,
  CardContent,
  Typography,
  Box,
  Chip,
  LinearProgress,
  Avatar,
  IconButton,
  Tooltip,
  Alert,
  CircularProgress,
  Button,
} from '@mui/material';
import {
  TrendingUp,
  Work,
  Business,
  LocationOn,
  Refresh,
  Download,
  Share,
  PlayArrow,
} from '@mui/icons-material';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import { motion } from 'framer-motion';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { apiService, DashboardStats, RecentActivity, TechnologyStat } from '../services/api';

const StatCard = ({ title, value, icon, color, trend, loading }: any) => (
  <motion.div
    initial={{ opacity: 0, y: 20 }}
    animate={{ opacity: 1, y: 0 }}
    transition={{ duration: 0.5 }}
  >
    <Card sx={{ height: '100%' }}>
      <CardContent>
        <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <Box>
            <Typography color="text.secondary" gutterBottom variant="body2">
              {title}
            </Typography>
            {loading ? (
              <CircularProgress size={24} />
            ) : (
              <Typography variant="h4" component="div" fontWeight="bold">
                {value}
              </Typography>
            )}
            {trend && !loading && (
              <Box sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
                <TrendingUp sx={{ color: 'success.main', fontSize: 16, mr: 0.5 }} />
                <Typography variant="body2" color="success.main">
                  +{trend}% este mes
                </Typography>
              </Box>
            )}
          </Box>
          <Avatar sx={{ bgcolor: color, width: 56, height: 56 }}>
            {icon}
          </Avatar>
        </Box>
      </CardContent>
    </Card>
  </motion.div>
);

const TechnologyCard = () => {
  const { data: techStats, isLoading, error } = useQuery({
    queryKey: ['technology-stats'],
    queryFn: () => apiService.getTechnologyStats(),
  });

  if (isLoading) {
    return (
      <Card>
        <CardContent>
          <Box sx={{ display: 'flex', justifyContent: 'center', py: 4 }}>
            <CircularProgress />
          </Box>
        </CardContent>
      </Card>
    );
  }

  if (error) {
    return (
      <Card>
        <CardContent>
          <Alert severity="error">Error cargando estadísticas de tecnologías</Alert>
        </CardContent>
      </Card>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: 0.1 }}
    >
      <Card>
        <CardContent>
          <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 3 }}>
            <Typography variant="h6" fontWeight="bold">
              Tecnologías Más Demandadas
            </Typography>
            <IconButton size="small">
              <Refresh />
            </IconButton>
          </Box>
          
          {techStats?.slice(0, 5).map((tech, index) => (
            <Box key={tech.technology} sx={{ mb: 2 }}>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                <Typography variant="body2" fontWeight="medium">
                  {tech.technology}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {tech.count} ofertas
                </Typography>
              </Box>
              <LinearProgress
                variant="determinate"
                value={tech.percentage}
                sx={{
                  height: 8,
                  borderRadius: 4,
                  bgcolor: 'grey.100',
                  '& .MuiLinearProgress-bar': {
                    borderRadius: 4,
                    bgcolor: `primary.${index % 2 === 0 ? 'main' : 'light'}`,
                  },
                }}
              />
            </Box>
          ))}
        </CardContent>
      </Card>
    </motion.div>
  );
};

const RecentActivityCard = () => {
  const { data: recentActivity, isLoading, error } = useQuery({
    queryKey: ['recent-activity'],
    queryFn: () => apiService.getRecentActivity(),
  });

  if (isLoading) {
    return (
      <Card>
        <CardContent>
          <Box sx={{ display: 'flex', justifyContent: 'center', py: 4 }}>
            <CircularProgress />
          </Box>
        </CardContent>
      </Card>
    );
  }

  if (error) {
    return (
      <Card>
        <CardContent>
          <Alert severity="error">Error cargando actividad reciente</Alert>
        </CardContent>
      </Card>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: 0.2 }}
    >
      <Card>
        <CardContent>
          <Typography variant="h6" fontWeight="bold" sx={{ mb: 3 }}>
            Actividad Reciente
          </Typography>
          
          {recentActivity?.slice(0, 5).map((activity, index) => (
            <Box
              key={index}
              sx={{
                display: 'flex',
                alignItems: 'center',
                py: 1.5,
                borderBottom: index < (recentActivity?.length || 0) - 1 ? '1px solid' : 'none',
                borderColor: 'divider',
              }}
            >
              <Avatar sx={{ width: 40, height: 40, mr: 2, bgcolor: 'primary.main' }}>
                <Business />
              </Avatar>
              <Box sx={{ flexGrow: 1 }}>
                <Typography variant="body2" fontWeight="medium">
                  {activity.position}
                </Typography>
                <Typography variant="caption" color="text.secondary">
                  {activity.company} • {activity.time}
                </Typography>
              </Box>
              <Chip label="Nueva" size="small" color="success" />
            </Box>
          ))}
        </CardContent>
      </Card>
    </motion.div>
  );
};

const Dashboard: React.FC = () => {
  const queryClient = useQueryClient();

  const { data: dashboardStats, isLoading: statsLoading, error: statsError } = useQuery({
    queryKey: ['dashboard-stats'],
    queryFn: () => apiService.getDashboardStats(),
  });

  const scrapeMutation = useMutation({
    mutationFn: (pages: number) => apiService.triggerScraping(pages),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['dashboard-stats'] });
      queryClient.invalidateQueries({ queryKey: ['recent-activity'] });
      queryClient.invalidateQueries({ queryKey: ['technology-stats'] });
    },
  });

  const handleScrape = () => {
    scrapeMutation.mutate(1);
  };

  return (
    <Box>
      <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 4 }}>
        <Box>
          <Typography variant="h4" fontWeight="bold" gutterBottom>
            Dashboard
          </Typography>
          <Typography variant="body1" color="text.secondary">
            Análisis completo del mercado laboral en tiempo real
          </Typography>
        </Box>
        <Box sx={{ display: 'flex', gap: 1 }}>
          <Button
            variant="contained"
            startIcon={<PlayArrow />}
            onClick={handleScrape}
            disabled={scrapeMutation.isPending}
          >
            {scrapeMutation.isPending ? 'Escaneando...' : 'Escanear Ofertas'}
          </Button>
          <Tooltip title="Descargar Reporte">
            <IconButton>
              <Download />
            </IconButton>
          </Tooltip>
          <Tooltip title="Compartir">
            <IconButton>
              <Share />
            </IconButton>
          </Tooltip>
        </Box>
      </Box>

      {scrapeMutation.isSuccess && (
        <Alert severity="success" sx={{ mb: 3 }}>
          ¡Escaneo completado exitosamente! Los datos se han actualizado.
        </Alert>
      )}

      {scrapeMutation.isError && (
        <Alert severity="error" sx={{ mb: 3 }}>
          Error durante el escaneo: {scrapeMutation.error?.message}
        </Alert>
      )}

      <Grid container spacing={3}>
        {/* Stats Cards */}
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Total de Ofertas"
            value={dashboardStats?.total_offers?.toLocaleString() || '0'}
            icon={<Work />}
            color="primary.main"
            loading={statsLoading}
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Empresas Activas"
            value={dashboardStats?.unique_companies || '0'}
            icon={<Business />}
            color="secondary.main"
            loading={statsLoading}
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Tecnologías Únicas"
            value={dashboardStats?.unique_technologies || '0'}
            icon={<TrendingUp />}
            color="success.main"
            loading={statsLoading}
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Ofertas Recientes"
            value={dashboardStats?.recent_offers || '0'}
            icon={<LocationOn />}
            color="warning.main"
            loading={statsLoading}
          />
        </Grid>

        {/* Charts */}
        <Grid item xs={12} md={8}>
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.3 }}
          >
            <Card>
              <CardContent>
                <Typography variant="h6" fontWeight="bold" sx={{ mb: 3 }}>
                  Tendencias Mensuales
                </Typography>
                {statsLoading ? (
                  <Box sx={{ display: 'flex', justifyContent: 'center', py: 4 }}>
                    <CircularProgress />
                  </Box>
                ) : (
                  <ResponsiveContainer width="100%" height={300}>
                    <BarChart data={dashboardStats?.monthly_trend || []}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="month" />
                      <YAxis />
                      <RechartsTooltip />
                      <Bar dataKey="offers" fill="#2563eb" radius={[4, 4, 0, 0]} />
                    </BarChart>
                  </ResponsiveContainer>
                )}
              </CardContent>
            </Card>
          </motion.div>
        </Grid>

        {/* Technology Distribution */}
        <Grid item xs={12} md={4}>
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.4 }}
          >
            <Card>
              <CardContent>
                <Typography variant="h6" fontWeight="bold" sx={{ mb: 3 }}>
                  Distribución de Tecnologías
                </Typography>
                {statsLoading ? (
                  <Box sx={{ display: 'flex', justifyContent: 'center', py: 4 }}>
                    <CircularProgress />
                  </Box>
                ) : (
                  <ResponsiveContainer width="100%" height={300}>
                    <PieChart>
                      <Pie
                        data={dashboardStats?.monthly_trend || []}
                        cx="50%"
                        cy="50%"
                        labelLine={false}
                        label={({ month, offers }) => `${month} ${offers}`}
                        outerRadius={80}
                        fill="#8884d8"
                        dataKey="offers"
                      >
                        {dashboardStats?.monthly_trend?.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={['#2563eb', '#7c3aed', '#10b981', '#f59e0b', '#ef4444'][index]} />
                        ))}
                      </Pie>
                      <RechartsTooltip />
                    </PieChart>
                  </ResponsiveContainer>
                )}
              </CardContent>
            </Card>
          </motion.div>
        </Grid>

        {/* Technology Stats */}
        <Grid item xs={12} md={6}>
          <TechnologyCard />
        </Grid>

        {/* Recent Activity */}
        <Grid item xs={12} md={6}>
          <RecentActivityCard />
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dashboard; 