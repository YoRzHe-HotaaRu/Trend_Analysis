import React, { useEffect, useState } from 'react'
import { MapContainer, TileLayer, Marker, Popup, useMap } from 'react-leaflet'
import { 
  Box, 
  Typography, 
  Chip, 
  Button, 
  ButtonGroup,
  CircularProgress,
  Alert,
  Card,
  CardContent
} from '@mui/material'
import {
  DirectionsTransit,
  LocationOn,
  ShoppingCart,
  Restaurant,
  TheaterComedy,
} from '@mui/icons-material'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import { useDataFetch } from '../../hooks/useDataFetch.js'
import TransitLayer from './TransitLayer.jsx'
import AttractionLayer from './AttractionLayer.jsx'

// Fix for default markers in react-leaflet
delete L.Icon.Default.prototype._getIconUrl
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png',
})

// Custom icons for different categories
const createCustomIcon = (color, icon) => {
  return L.divIcon({
    html: `
      <div style="
        background-color: ${color};
        width: 20px;
        height: 20px;
        border-radius: 50%;
        border: 2px solid white;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.3);
      ">
        <span style="color: white; font-size: 12px;">${icon}</span>
      </div>
    `,
    className: 'custom-div-icon',
    iconSize: [24, 24],
    iconAnchor: [12, 12],
  })
}

const transitIcon = createCustomIcon('#1976d2', 'T')
const mallIcon = createCustomIcon('#f50057', 'M')
const restaurantIcon = createCustomIcon('#4caf50', 'R')
const entertainmentIcon = createCustomIcon('#ff9800', 'E')

function InteractiveMap({ selectedTimeRange, selectedDate }) {
  const [activeLayers, setActiveLayers] = useState({
    transit: true,
    attractions: true,
    malls: false,
    restaurants: false,
    entertainment: false,
  })
  const [mapCenter, setMapCenter] = useState([3.139, 101.6869]) // Kuala Lumpur center

  // Fetch transit data
  const {
    data: transitData,
    isLoading: transitLoading,
    error: transitError,
    refetch: refetchTransit
  } = useDataFetch(`/api/transit/real-time`, {
    enabled: activeLayers.transit,
  })

  // Fetch attraction data
  const {
    data: attractionData,
    isLoading: attractionLoading,
    error: attractionError,
    refetch: refetchAttractions
  } = useDataFetch(`/api/attractions/active`, {
    enabled: activeLayers.attractions,
    params: { timeRange: selectedTimeRange, date: selectedDate }
  })

  const handleLayerToggle = (layer) => {
    setActiveLayers(prev => ({
      ...prev,
      [layer]: !prev[layer]
    }))
  }

  const refreshData = () => {
    if (activeLayers.transit) refetchTransit()
    if (activeLayers.attractions) refetchAttractions()
  }

  return (
    <Box sx={{ height: '100%', position: 'relative' }}>
      {/* Map Controls */}
      <Box sx={{ position: 'absolute', top: 10, right: 10, zIndex: 1000 }}>
        <Card sx={{ mb: 2 }}>
          <CardContent sx={{ pb: 1 }}>
            <Typography variant="h6" sx={{ mb: 1 }}>
              Map Layers
            </Typography>
            <ButtonGroup orientation="vertical" size="small">
              <Button
                variant={activeLayers.transit ? 'contained' : 'outlined'}
                startIcon={<DirectionsTransit />}
                onClick={() => handleLayerToggle('transit')}
              >
                Transit Stations
              </Button>
              <Button
                variant={activeLayers.malls ? 'contained' : 'outlined'}
                startIcon={<ShoppingCart />}
                onClick={() => handleLayerToggle('malls')}
              >
                Shopping Malls
              </Button>
              <Button
                variant={activeLayers.restaurants ? 'contained' : 'outlined'}
                startIcon={<Restaurant />}
                onClick={() => handleLayerToggle('restaurants')}
              >
                Restaurants
              </Button>
              <Button
                variant={activeLayers.entertainment ? 'contained' : 'outlined'}
                startIcon={<TheaterComedy />}
                onClick={() => handleLayerToggle('entertainment')}
              >
                Entertainment
              </Button>
            </ButtonGroup>
            <Button
              variant="outlined"
              size="small"
              onClick={refreshData}
              sx={{ mt: 1, width: '100%' }}
            >
              Refresh Data
            </Button>
          </CardContent>
        </Card>
      </Box>

      {/* Map Container */}
      <MapContainer
        center={mapCenter}
        zoom={12}
        style={{ height: '100%', width: '100%' }}
        zoomControl={true}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          maxZoom={19}
        />

        {/* Transit Layer */}
        {activeLayers.transit && (
          <TransitLayer
            data={transitData}
            loading={transitLoading}
            error={transitError}
            icon={transitIcon}
          />
        )}

        {/* Attraction Layers */}
        {activeLayers.malls && (
          <AttractionLayer
            data={attractionData?.malls || []}
            loading={attractionLoading}
            icon={mallIcon}
            type="mall"
          />
        )}
        
        {activeLayers.restaurants && (
          <AttractionLayer
            data={attractionData?.restaurants || []}
            loading={attractionLoading}
            icon={restaurantIcon}
            type="restaurant"
          />
        )}
        
        {activeLayers.entertainment && (
          <AttractionLayer
            data={attractionData?.entertainment || []}
            loading={attractionLoading}
            icon={entertainmentIcon}
            type="entertainment"
          />
        )}
      </MapContainer>

      {/* Loading Overlay */}
      {(transitLoading || attractionLoading) && (
        <Box sx={{
          position: 'absolute',
          top: '50%',
          left: '50%',
          transform: 'translate(-50%, -50%)',
          zIndex: 1000,
          backgroundColor: 'rgba(255, 255, 255, 0.9)',
          p: 3,
          borderRadius: 2,
          textAlign: 'center'
        }}>
          <CircularProgress />
          <Typography variant="body2" sx={{ mt: 1 }}>
            Loading map data...
          </Typography>
        </Box>
      )}

      {/* Error Display */}
      {(transitError || attractionError) && (
        <Box sx={{ position: 'absolute', bottom: 10, left: 10, zIndex: 1000 }}>
          <Alert severity="warning">
            Some data may not be available. Please check your connection.
          </Alert>
        </Box>
      )}
    </Box>
  )
}

export default InteractiveMap