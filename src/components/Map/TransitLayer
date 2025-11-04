import React from 'react'
import { Marker, Popup, Circle } from 'react-leaflet'
import { Typography, Box, Chip, Alert } from '@mui/material'
import { 
  DirectionsTransit,
  Schedule,
  TrendingUp,
  TrendingDown,
  Remove
} from '@mui/icons-material'

function TransitLayer({ data, loading, error, icon }) {
  if (loading) return null
  if (error) return <Alert severity="error">Error loading transit data</Alert>
  if (!data || !data.stations) return null

  const getStatusColor = (status) => {
    switch (status?.toLowerCase()) {
      case 'operational':
      case 'normal':
        return '#4caf50'
      case 'delayed':
        return '#ff9800'
      case 'disrupted':
        return '#f44336'
      default:
        return '#9e9e9e'
    }
  }

  const getStatusIcon = (status) => {
    switch (status?.toLowerCase()) {
      case 'operational':
      case 'normal':
        return <Remove sx={{ fontSize: 12 }} />
      case 'delayed':
        return <TrendingDown sx={{ fontSize: 12 }} />
      case 'disrupted':
        return <TrendingUp sx={{ fontSize: 12 }} />
      default:
        return <Schedule sx={{ fontSize: 12 }} />
    }
  }

  return (
    <>
      {data.stations.map((station) => (
        <React.Fragment key={station.id}>
          {/* Station Marker */}
          <Marker 
            position={[station.latitude, station.longitude]}
            icon={icon}
          >
            <Popup>
              <Box sx={{ minWidth: 200 }}>
                <Typography variant="h6" gutterBottom>
                  {station.name}
                </Typography>
                
                <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <DirectionsTransit color="primary" fontSize="small" />
                    <Typography variant="body2">
                      {station.line} Line
                    </Typography>
                  </Box>
                  
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <Chip
                      icon={getStatusIcon(station.status)}
                      label={station.status}
                      size="small"
                      sx={{
                        backgroundColor: getStatusColor(station.status),
                        color: 'white',
                      }}
                    />
                  </Box>

                  {station.passenger_count && (
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                      <Typography variant="body2" color="textSecondary">
                        Passengers: {station.passenger_count}
                      </Typography>
                    </Box>
                  )}

                  {station.next_arrival && (
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                      <Schedule fontSize="small" />
                      <Typography variant="body2">
                        Next: {station.next_arrival}
                      </Typography>
                    </Box>
                  )}

                  <Typography variant="caption" color="textSecondary">
                    Last updated: {new Date(station.last_updated).toLocaleTimeString()}
                  </Typography>
                </Box>
              </Box>
            </Popup>
          </Marker>

          {/* Passenger Count Visualization */}
          {station.passenger_count && station.passenger_count > 0 && (
            <Circle
              center={[station.latitude, station.longitude]}
              radius={Math.min(station.passenger_count * 10, 500)} // Scale radius
              fillColor={getStatusColor(station.status)}
              fillOpacity={0.3}
              color={getStatusColor(station.status)}
              weight={1}
              opacity={0.5}
            />
          )}
        </React.Fragment>
      ))}

      {/* Route Lines */}
      {data.routes && data.routes.map((route) => (
        <React.Fragment key={route.id}>
          {route.coordinates && route.coordinates.map((segment, index) => (
            <React.Fragment key={index}>
              {segment.map((point, pointIndex) => (
                <React.Fragment key={pointIndex}>
                  {pointIndex < segment.length - 1 && (
                    <Marker
                      position={[point.lat, point.lng]}
                      icon={icon}
                      opacity={0}
                      eventHandlers={{
                        click: () => {
                          // Handle route click
                          console.log('Route clicked:', route)
                        }
                      }}
                    />
                  )}
                </React.Fragment>
              ))}
            </React.Fragment>
          ))}
        </React.Fragment>
      ))}
    </>
  )
}

export default TransitLayer