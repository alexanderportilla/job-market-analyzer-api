import React from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  Grid,
  Switch,
  FormControlLabel,
  TextField,
  Button,
  Divider,
} from '@mui/material';
import { Save, Refresh, Download } from '@mui/icons-material';

const Settings: React.FC = () => {
  return (
    <Box>
      <Typography variant="h4" fontWeight="bold" gutterBottom>
        Configuración
      </Typography>
      <Typography variant="body1" color="text.secondary" sx={{ mb: 4 }}>
        Personaliza tu experiencia de análisis del mercado laboral
      </Typography>

      <Grid container spacing={3}>
        {/* General Settings */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" fontWeight="bold" sx={{ mb: 3 }}>
                Configuración General
              </Typography>
              
              <Box sx={{ mb: 3 }}>
                <FormControlLabel
                  control={<Switch defaultChecked />}
                  label="Notificaciones automáticas"
                />
              </Box>
              
              <Box sx={{ mb: 3 }}>
                <FormControlLabel
                  control={<Switch defaultChecked />}
                  label="Actualización automática de datos"
                />
              </Box>
              
              <Box sx={{ mb: 3 }}>
                <FormControlLabel
                  control={<Switch />}
                  label="Modo oscuro"
                />
              </Box>
              
              <TextField
                fullWidth
                label="Intervalo de actualización (minutos)"
                type="number"
                defaultValue={30}
                sx={{ mb: 3 }}
              />
              
              <Button
                variant="contained"
                startIcon={<Save />}
                fullWidth
              >
                Guardar Configuración
              </Button>
            </CardContent>
          </Card>
        </Grid>

        {/* Data Settings */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" fontWeight="bold" sx={{ mb: 3 }}>
                Configuración de Datos
              </Typography>
              
              <Box sx={{ mb: 3 }}>
                <FormControlLabel
                  control={<Switch defaultChecked />}
                  label="Scraping automático"
                />
              </Box>
              
              <Box sx={{ mb: 3 }}>
                <FormControlLabel
                  control={<Switch />}
                  label="Exportar datos automáticamente"
                />
              </Box>
              
              <TextField
                fullWidth
                label="Número máximo de páginas a scrapear"
                type="number"
                defaultValue={10}
                sx={{ mb: 3 }}
              />
              
              <Button
                variant="outlined"
                startIcon={<Refresh />}
                fullWidth
                sx={{ mb: 2 }}
              >
                Actualizar Datos Ahora
              </Button>
              
              <Button
                variant="outlined"
                startIcon={<Download />}
                fullWidth
              >
                Exportar Datos
              </Button>
            </CardContent>
          </Card>
        </Grid>

        {/* API Configuration */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" fontWeight="bold" sx={{ mb: 3 }}>
                Configuración de API
              </Typography>
              
              <Grid container spacing={2}>
                <Grid item xs={12} md={6}>
                  <TextField
                    fullWidth
                    label="URL de la API"
                    defaultValue="http://localhost:8000"
                    sx={{ mb: 2 }}
                  />
                </Grid>
                <Grid item xs={12} md={6}>
                  <TextField
                    fullWidth
                    label="Puerto de la API"
                    defaultValue="8000"
                    sx={{ mb: 2 }}
                  />
                </Grid>
                <Grid item xs={12} md={6}>
                  <TextField
                    fullWidth
                    label="Timeout (segundos)"
                    defaultValue="30"
                    sx={{ mb: 2 }}
                  />
                </Grid>
                <Grid item xs={12} md={6}>
                  <TextField
                    fullWidth
                    label="Rate Limit (requests/min)"
                    defaultValue="60"
                    sx={{ mb: 2 }}
                  />
                </Grid>
              </Grid>
              
              <Divider sx={{ my: 2 }} />
              
              <Box sx={{ display: 'flex', gap: 2 }}>
                <Button variant="contained" startIcon={<Save />}>
                  Guardar Configuración API
                </Button>
                <Button variant="outlined">
                  Probar Conexión
                </Button>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Settings; 