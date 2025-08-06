import React, { useState } from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  Grid,
  CircularProgress,
  Alert,
  Tabs,
  Tab,
  Chip,
  Avatar,
  List,
  ListItem,
  ListItemText,
  ListItemAvatar,
  Divider,
} from '@mui/material';
import {
  Business,
  LocationOn,
  TrendingUp,
  Work,
} from '@mui/icons-material';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, ResponsiveContainer, PieChart, Pie, Cell, LineChart, Line } from 'recharts';
import { motion } from 'framer-motion';
import { useQuery } from '@tanstack/react-query';
import { apiService, CompanyStat, LocationStat, TechnologyStat } from '../services/api';

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`analytics-tabpanel-${index}`}
      aria-labelledby={`analytics-tab-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ pt: 3 }}>{children}</Box>}
    </div>
  );
}

const Analytics: React.FC = () => {
  const [tabValue, setTabValue] = useState(0);

  const { data: companyStats, isLoading: companyLoading, error: companyError } = useQuery({
    queryKey: ['company-stats'],
    queryFn: () => apiService.getCompanyStats(),
  });

  const { data: locationStats, isLoading: locationLoading, error: locationError } = useQuery({
    queryKey: ['location-stats'],
    queryFn: () => apiService.getLocationStats(),
  });

  const { data: techStats, isLoading: techLoading, error: techError } = useQuery({
    queryKey: ['technology-stats'],
    queryFn: () => apiService.getTechnologyStats(),
  });

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  const COLORS = ['#2563eb', '#7c3aed', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#06b6d4', '#84cc16'];

  if (companyLoading || locationLoading || techLoading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', py: 8 }}>
        <CircularProgress />
      </Box>
    );
  }

  if (companyError || locationError || techError) {
    return (
      <Box>
        <Alert severity="error" sx={{ mb: 3 }}>
          Error cargando datos de analytics
        </Alert>
      </Box>
    );
  }

  return (
    <Box>
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" fontWeight="bold" gutterBottom>
          Analytics
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Análisis detallado del mercado laboral tech en Colombia
        </Typography>
      </Box>

      <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 3 }}>
        <Tabs value={tabValue} onChange={handleTabChange} aria-label="analytics tabs">
          <Tab label="Empresas" />
          <Tab label="Ubicaciones" />
          <Tab label="Tecnologías" />
        </Tabs>
      </Box>

      {/* Empresas Tab */}
      <TabPanel value={tabValue} index={0}>
        <Grid container spacing={3}>
          <Grid item xs={12} md={8}>
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
            >
              <Card>
                <CardContent>
                  <Typography variant="h6" fontWeight="bold" sx={{ mb: 3 }}>
                    Ofertas por Empresa
                  </Typography>
                  <ResponsiveContainer width="100%" height={400}>
                    <BarChart data={companyStats?.slice(0, 10) || []}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis 
                        dataKey="company" 
                        angle={-45}
                        textAnchor="end"
                        height={100}
                        interval={0}
                      />
                      <YAxis />
                      <RechartsTooltip />
                      <Bar dataKey="offer_count" fill="#2563eb" radius={[4, 4, 0, 0]} />
                    </BarChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>
            </motion.div>
          </Grid>

          <Grid item xs={12} md={4}>
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.1 }}
            >
              <Card>
                <CardContent>
                  <Typography variant="h6" fontWeight="bold" sx={{ mb: 3 }}>
                    Top Empresas
                  </Typography>
                  <List>
                    {companyStats?.slice(0, 8).map((company, index) => (
                      <React.Fragment key={company.company}>
                        <ListItem>
                          <ListItemAvatar>
                            <Avatar sx={{ bgcolor: COLORS[index % COLORS.length] }}>
                              <Business />
                            </Avatar>
                          </ListItemAvatar>
                          <ListItemText
                            primary={company.company}
                            secondary={`${company.offer_count} ofertas`}
                          />
                          <Chip 
                            label={`#${index + 1}`} 
                            size="small" 
                            color="primary" 
                            variant="outlined"
                          />
                        </ListItem>
                        {index < 7 && <Divider />}
                      </React.Fragment>
                    ))}
                  </List>
                </CardContent>
              </Card>
            </motion.div>
          </Grid>
        </Grid>
      </TabPanel>

      {/* Ubicaciones Tab */}
      <TabPanel value={tabValue} index={1}>
        <Grid container spacing={3}>
          <Grid item xs={12} md={8}>
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
            >
              <Card>
                <CardContent>
                  <Typography variant="h6" fontWeight="bold" sx={{ mb: 3 }}>
                    Ofertas por Ubicación
                  </Typography>
                  <ResponsiveContainer width="100%" height={400}>
                    <BarChart data={locationStats?.slice(0, 10) || []}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis 
                        dataKey="location" 
                        angle={-45}
                        textAnchor="end"
                        height={100}
                        interval={0}
                      />
                      <YAxis />
                      <RechartsTooltip />
                      <Bar dataKey="offer_count" fill="#10b981" radius={[4, 4, 0, 0]} />
                    </BarChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>
            </motion.div>
          </Grid>

          <Grid item xs={12} md={4}>
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.1 }}
            >
              <Card>
                <CardContent>
                  <Typography variant="h6" fontWeight="bold" sx={{ mb: 3 }}>
                    Top Ubicaciones
                  </Typography>
                  <List>
                    {locationStats?.slice(0, 8).map((location, index) => (
                      <React.Fragment key={location.location}>
                        <ListItem>
                          <ListItemAvatar>
                            <Avatar sx={{ bgcolor: COLORS[index % COLORS.length] }}>
                              <LocationOn />
                            </Avatar>
                          </ListItemAvatar>
                          <ListItemText
                            primary={location.location}
                            secondary={`${location.offer_count} ofertas`}
                          />
                          <Chip 
                            label={`#${index + 1}`} 
                            size="small" 
                            color="success" 
                            variant="outlined"
                          />
                        </ListItem>
                        {index < 7 && <Divider />}
                      </React.Fragment>
                    ))}
                  </List>
                </CardContent>
              </Card>
            </motion.div>
          </Grid>
        </Grid>
      </TabPanel>

      {/* Tecnologías Tab */}
      <TabPanel value={tabValue} index={2}>
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
            >
              <Card>
                <CardContent>
                  <Typography variant="h6" fontWeight="bold" sx={{ mb: 3 }}>
                    Distribución de Tecnologías
                  </Typography>
                  <ResponsiveContainer width="100%" height={400}>
                    <PieChart>
                      <Pie
                        data={techStats?.slice(0, 8) || []}
                        cx="50%"
                        cy="50%"
                        labelLine={false}
                        label={({ technology, percentage }) => `${technology} ${percentage.toFixed(1)}%`}
                        outerRadius={120}
                        fill="#8884d8"
                        dataKey="count"
                      >
                        {techStats?.slice(0, 8).map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                        ))}
                      </Pie>
                      <RechartsTooltip />
                    </PieChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>
            </motion.div>
          </Grid>

          <Grid item xs={12} md={6}>
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.1 }}
            >
              <Card>
                <CardContent>
                  <Typography variant="h6" fontWeight="bold" sx={{ mb: 3 }}>
                    Top Tecnologías
                  </Typography>
                  <List>
                    {techStats?.slice(0, 10).map((tech, index) => (
                      <React.Fragment key={tech.technology}>
                        <ListItem>
                          <ListItemAvatar>
                            <Avatar sx={{ bgcolor: COLORS[index % COLORS.length] }}>
                              <Work />
                            </Avatar>
                          </ListItemAvatar>
                          <ListItemText
                            primary={tech.technology}
                            secondary={`${tech.count} ofertas (${tech.percentage.toFixed(1)}%)`}
                          />
                          <Chip 
                            label={`#${index + 1}`} 
                            size="small" 
                            color="warning" 
                            variant="outlined"
                          />
                        </ListItem>
                        {index < 9 && <Divider />}
                      </React.Fragment>
                    ))}
                  </List>
                </CardContent>
              </Card>
            </motion.div>
          </Grid>

          <Grid item xs={12}>
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.2 }}
            >
              <Card>
                <CardContent>
                  <Typography variant="h6" fontWeight="bold" sx={{ mb: 3 }}>
                    Tendencias de Tecnologías
                  </Typography>
                  <ResponsiveContainer width="100%" height={300}>
                    <BarChart data={techStats?.slice(0, 15) || []}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis 
                        dataKey="technology" 
                        angle={-45}
                        textAnchor="end"
                        height={100}
                        interval={0}
                      />
                      <YAxis />
                      <RechartsTooltip />
                      <Bar dataKey="count" fill="#7c3aed" radius={[4, 4, 0, 0]} />
                    </BarChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>
            </motion.div>
          </Grid>
        </Grid>
      </TabPanel>
    </Box>
  );
};

export default Analytics; 