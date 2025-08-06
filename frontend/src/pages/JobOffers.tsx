import React, { useState } from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  Grid,
  Chip,
  Avatar,
  TextField,
  InputAdornment,
  IconButton,
  CircularProgress,
  Alert,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Link,
} from '@mui/material';
import { Work, Business, LocationOn, Search, OpenInNew } from '@mui/icons-material';
import { useQuery } from '@tanstack/react-query';
import { apiService, JobOffer } from '../services/api';

const JobOffers: React.FC = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedOffer, setSelectedOffer] = useState<JobOffer | null>(null);
  const [isDialogOpen, setIsDialogOpen] = useState(false);

  const { data: offers, isLoading, error } = useQuery({
    queryKey: ['job-offers'],
    queryFn: () => apiService.getAllOffers(),
  });

  const filteredOffers = offers?.filter(offer =>
    offer.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
    offer.company.toLowerCase().includes(searchTerm.toLowerCase()) ||
    offer.description.toLowerCase().includes(searchTerm.toLowerCase())
  ) || [];

  const handleOfferClick = (offer: JobOffer) => {
    setSelectedOffer(offer);
    setIsDialogOpen(true);
  };

  const handleCloseDialog = () => {
    setIsDialogOpen(false);
    setSelectedOffer(null);
  };

  const extractTechnologies = (description: string): string[] => {
    const techKeywords = [
      'Python', 'JavaScript', 'React', 'Node.js', 'Java', 'C#', 'PHP', 'Ruby',
      'Go', 'Rust', 'TypeScript', 'Angular', 'Vue', 'Django', 'Flask', 'Express',
      'Spring', 'Laravel', 'Rails', 'Docker', 'Kubernetes', 'AWS', 'Azure',
      'MongoDB', 'PostgreSQL', 'MySQL', 'Redis', 'GraphQL', 'REST', 'API'
    ];
    
    return techKeywords.filter(tech => 
      description.toLowerCase().includes(tech.toLowerCase())
    );
  };

  if (isLoading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', py: 8 }}>
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Box>
        <Alert severity="error" sx={{ mb: 3 }}>
          Error cargando ofertas de trabajo: {error.message}
        </Alert>
      </Box>
    );
  }

  return (
    <Box>
      <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 4 }}>
        <Box>
          <Typography variant="h4" fontWeight="bold" gutterBottom>
            Ofertas de Trabajo
          </Typography>
          <Typography variant="body1" color="text.secondary">
            Explora las mejores oportunidades en el mercado laboral tech
          </Typography>
        </Box>
        <Typography variant="body2" color="text.secondary">
          {filteredOffers.length} ofertas encontradas
        </Typography>
      </Box>

      <TextField
        fullWidth
        variant="outlined"
        placeholder="Buscar por título, empresa o tecnología..."
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
        sx={{ mb: 4 }}
        InputProps={{
          startAdornment: (
            <InputAdornment position="start">
              <Search />
            </InputAdornment>
          ),
        }}
      />

      {filteredOffers.length === 0 && searchTerm && (
        <Alert severity="info" sx={{ mb: 3 }}>
          No se encontraron ofertas que coincidan con "{searchTerm}"
        </Alert>
      )}

      <Grid container spacing={3}>
        {filteredOffers.map((offer) => {
          const technologies = extractTechnologies(offer.description);
          
          return (
            <Grid item xs={12} md={6} lg={4} key={offer.id}>
              <Card 
                sx={{ 
                  height: '100%', 
                  cursor: 'pointer', 
                  '&:hover': { 
                    transform: 'translateY(-2px)', 
                    transition: 'transform 0.2s',
                    boxShadow: 3
                  } 
                }}
                onClick={() => handleOfferClick(offer)}
              >
                <CardContent>
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                    <Avatar sx={{ bgcolor: 'primary.main', mr: 2 }}>
                      <Work />
                    </Avatar>
                    <Box sx={{ flexGrow: 1 }}>
                      <Typography variant="h6" fontWeight="bold" sx={{ 
                        overflow: 'hidden',
                        textOverflow: 'ellipsis',
                        display: '-webkit-box',
                        WebkitLineClamp: 2,
                        WebkitBoxOrient: 'vertical',
                      }}>
                        {offer.title}
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        {offer.company || 'Empresa no especificada'}
                      </Typography>
                    </Box>
                  </Box>

                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                    <LocationOn sx={{ fontSize: 16, color: 'text.secondary', mr: 1 }} />
                    <Typography variant="body2" color="text.secondary">
                      {offer.location || 'Ubicación no especificada'}
                    </Typography>
                  </Box>

                  <Typography variant="body2" sx={{ 
                    mb: 2,
                    overflow: 'hidden',
                    textOverflow: 'ellipsis',
                    display: '-webkit-box',
                    WebkitLineClamp: 3,
                    WebkitBoxOrient: 'vertical',
                  }}>
                    {offer.description}
                  </Typography>

                  <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5, mb: 2 }}>
                    {technologies.slice(0, 4).map((tech) => (
                      <Chip
                        key={tech}
                        label={tech}
                        size="small"
                        variant="outlined"
                        color="primary"
                      />
                    ))}
                    {technologies.length > 4 && (
                      <Chip
                        label={`+${technologies.length - 4} más`}
                        size="small"
                        variant="outlined"
                        color="secondary"
                      />
                    )}
                  </Box>

                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <Typography variant="caption" color="text.secondary">
                      {new Date(offer.scraped_at).toLocaleDateString()}
                    </Typography>
                    <IconButton size="small">
                      <OpenInNew />
                    </IconButton>
                  </Box>
                </CardContent>
              </Card>
            </Grid>
          );
        })}
      </Grid>

      {/* Job Offer Detail Dialog */}
      <Dialog 
        open={isDialogOpen} 
        onClose={handleCloseDialog}
        maxWidth="md"
        fullWidth
      >
        {selectedOffer && (
          <>
            <DialogTitle>
              <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <Typography variant="h6" fontWeight="bold">
                  {selectedOffer.title}
                </Typography>
                <IconButton onClick={handleCloseDialog}>
                  <OpenInNew />
                </IconButton>
              </Box>
            </DialogTitle>
            <DialogContent>
              <Box sx={{ mb: 3 }}>
                <Typography variant="h6" color="primary" gutterBottom>
                  {selectedOffer.company || 'Empresa no especificada'}
                </Typography>
                <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                  <LocationOn sx={{ fontSize: 16, mr: 0.5, verticalAlign: 'middle' }} />
                  {selectedOffer.location || 'Ubicación no especificada'}
                </Typography>
              </Box>

              <Typography variant="body1" sx={{ mb: 3 }}>
                {selectedOffer.description}
              </Typography>

              <Box sx={{ mb: 3 }}>
                <Typography variant="h6" gutterBottom>
                  Tecnologías Detectadas
                </Typography>
                <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                  {extractTechnologies(selectedOffer.description).map((tech) => (
                    <Chip
                      key={tech}
                      label={tech}
                      color="primary"
                      variant="filled"
                    />
                  ))}
                </Box>
              </Box>

              <Box>
                <Typography variant="body2" color="text.secondary">
                  Escaneado el: {new Date(selectedOffer.scraped_at).toLocaleString()}
                </Typography>
              </Box>
            </DialogContent>
            <DialogActions>
              <Button onClick={handleCloseDialog}>Cerrar</Button>
              {selectedOffer.url && (
                <Button 
                  variant="contained" 
                  startIcon={<OpenInNew />}
                  onClick={() => window.open(selectedOffer.url, '_blank')}
                >
                  Ver Oferta Original
                </Button>
              )}
            </DialogActions>
          </>
        )}
      </Dialog>
    </Box>
  );
};

export default JobOffers; 