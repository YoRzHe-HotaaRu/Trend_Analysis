import React from 'react'
import { Marker, Popup, Circle } from 'react-leaflet'
import { Typography, Box, Chip, Rating, Alert } from '@mui/material'
import {
  ShoppingCart,
  Restaurant,
  TheaterComedy,
  Star,
  AccessTime,
  People
} from '@mui/icons-material'

function AttractionLayer({ data, loading, error, icon, type }) {
  if (loading) return null
  if (error) return <Alert severity="error">Error loading {type} data</Alert>
  if (!data || !Array.isArray(data)) return null

  const getTypeIcon = () => {
    switch (type) {
      case 'mall':
        return <ShoppingCart fontSize="small" />
      case 'restaurant':
        return <Restaurant fontSize="small" />
      case 'entertainment':
        return <TheaterComedy fontSize="small" />
      default:
        return <Star fontSize="small" />
    }
  }

  const getTypeColor = () => {
    switch (type) {
      case 'mall':
        return '#f50057'
      case 'restaurant':
        return '#4caf50'
      case 'entertainment':
        return '#ff9800'
      default:
        return '#1976d2'
    }
  }

  const getCrowdLevel = (popularity) => {
    if (popularity >= 80) return { level: 'Very Busy', color: '#f44336' }
    if (popularity >= 60) return { level: 'Busy', color: '#ff9800' }
    if (popularity >= 40) return { level: 'Moderate', color: '#ffeb3b' }
    if (popularity >= 20) return { level: 'Quiet', color: '#4caf50' }
    return { level: 'Very Quiet', color: '#9e9e9e' }
  }

  return (
    <>
      {data.map((attraction) => {
        const crowdInfo = getCrowdLevel(attraction.popularity_score || 50)
        
        return (
          <React.Fragment key={attraction.id}>
            {/* Attraction Marker */}
            <Marker 
              position={[attraction.latitude, attraction.longitude]}
              icon={icon}
            >
              <Popup>
                <Box sx={{ minWidth: 250 }}>
                  <Typography variant="h6" gutterBottom>
                    {attraction.name}
                  </Typography>
                  
                  <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                      {getTypeIcon()}
                      <Typography variant="body2" color="textSecondary">
                        {attraction.category}
                      </Typography>
                    </Box>
                    
                    {attraction.rating && (
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                        <Rating 
                          value={attraction.rating} 
                          readOnly 
                          size="small"
                          precision={0.1}
                        />
                        <Typography variant="body2">
                          {attraction.rating}
                        </Typography>
                      </Box>
                    )}

                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                      <Chip
                        label={crowdInfo.level}
                        size="small"
                        sx={{
                          backgroundColor: crowdInfo.color,
                          color: 'white',
                        }}
                      />
                      <Typography variant="body2" color="textSecondary">
                        Popularity: {attraction.popularity_score || 50}%
                      </Typography>
                    </Box>

                    {attraction.current_occupancy && (
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                        <People fontSize="small" />
                        <Typography variant="body2">
                          Occupancy: {attraction.current_occupancy}%
                        </Typography>
                      </Box>
                    )}

                    {attraction.estimated_wait_time && (
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                        <AccessTime fontSize="small" />
                        <Typography variant="body2">
                          Wait Time: {attraction.estimated_wait_time} min
                        </Typography>
                      </Box>
                    )}

                    {attraction.address && (
                      <Typography variant="body2" color="textSecondary">
                        {attraction.address}
                      </Typography>
                    )}

                    <Typography variant="caption" color="textSecondary">
                      Last updated: {new Date(attraction.last_updated).toLocaleString()}
                    </Typography>
                  </Box>
                </Box>
              </Popup>
            </Marker>

            {/* Popularity Visualization Circle */}
            {attraction.popularity_score && (
              <Circle
                center={[attraction.latitude, attraction.longitude]}
                radius={Math.min((attraction.popularity_score / 100) * 1000, 800)}
                fillColor={getTypeColor()}
                fillOpacity={0.2}
                color={getTypeColor()}
                weight={1}
                opacity={0.4}
              />
            )}
          </React.Fragment>
        )
      })}
    </>
  )
}

export default AttractionLayer