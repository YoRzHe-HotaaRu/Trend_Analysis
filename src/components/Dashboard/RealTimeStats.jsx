import React, { useEffect, useState } from 'react'
import {
  Box,
  Typography,
  Card,
  CardContent,
  Grid,
  LinearProgress,
  Chip,
  Avatar,
  IconButton,
  Tooltip
} from '@mui/material'
import {
  DirectionsTransit,
  LocationOn,
  ShoppingCart,
  Restaurant,
  TheaterComedy,
  People,
  Schedule,
  TrendingUp,
  TrendingDown,
  AccessTime,
  Refresh
} from '@mui/icons-material'
import { useDataFetch } from '../../hooks/useDataFetch.js'

function RealTimeStats({ selectedTimeRange }) {
  const [lastUpdated, setLastUpdated] = useState(new Date())

  // Fetch real-time statistics
  const {
    data: statsData,
    isLoading,
    error,
    refetch
  } = useDataFetch('/api/dashboard/stats', {
    enabled: selectedTimeRange === 'realtime',
    refetchInterval: 30000, // Refetch every 30 seconds
  })

  const handleRefresh = () => {
    refetch()
    setLastUpdated(new Date())
  }

  const StatCard = ({ icon, title, value, subtitle, color = 'primary', trend = null }) => (
    <Card sx={{ mb: 2 }}>
      <CardContent>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
          <Avatar sx={{ bgcolor: `${color}.main`, mr: 2 }}>
            {icon}
          </Avatar>
          <Box sx={{ flexGrow: 1 }}>
            <Typography variant="h6" component="div">
              {value}
            </Typography>
            <Typography variant="body2" color="textSecondary">
              {title}
            </Typography>
          </Box>
          {trend && (
            <Tooltip title={trend.direction}>
              <IconButton size="small" color={trend.direction === 'up' ? 'success' : 'error'}>
                {trend.direction === 'up' ? <TrendingUp /> : <TrendingDown />}
              </IconButton>
            </Tooltip>
          )}
        </Box>
        {subtitle && (
          <Typography variant="caption" color="textSecondary">
            {subtitle}
          </Typography>
        )}
      </CardContent>
    </Card>
  )

  if (isLoading) {
    return (
      <Box>
        {[1, 2, 3, 4].map((i) => (
          <Card key={i} sx={{ mb: 2 }}>
            <CardContent>
              <LinearProgress />
            </CardContent>
          </Card>
        ))}
      </Box>
    )
  }

  if (error) {
    return (
      <Card sx={{ mb: 2 }}>
        <CardContent>
          <Typography color="error" align="center">
            Error loading real-time stats
          </Typography>
        </CardContent>
      </Card>
    )
  }

  const stats = statsData || {
    active_routes: 24,
    total_passengers: 125430,
    busy_stations: 8,
    busy_attractions: 15,
    avg_delay: 3.2,
    efficiency_rate: 94.5,
    on_time_percentage: 87.3,
    transit_distribution: {
      lrt: 28,
      mrt: 35,
      brt: 22,
      ktm: 15
    }
  }

  const distributionData = [
    { label: 'LRT', value: stats.transit_distribution.lrt, color: '#1976d2' },
    { label: 'MRT', value: stats.transit_distribution.mrt, color: '#f50057' },
    { label: 'BRT', value: stats.transit_distribution.brt, color: '#4caf50' },
    { label: 'KTM', value: stats.transit_distribution.ktm, color: '#ff9800' }
  ]

  return (
    <Box>
      {/* Header with refresh */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
        <Typography variant="h6">Real-time Statistics</Typography>
        <IconButton onClick={handleRefresh} size="small">
          <Refresh />
        </IconButton>
      </Box>

      {/* Main Stats Grid */}
      <Grid container spacing={2}>
        <Grid item xs={6}>
          <StatCard
            icon={<DirectionsTransit />}
            title="Active Routes"
            value={stats.active_routes}
            subtitle="Currently operational"
            color="primary"
            trend={{ direction: 'up' }}
          />
        </Grid>
        <Grid item xs={6}>
          <StatCard
            icon={<People />}
            title="Total Passengers"
            value={stats.total_passengers?.toLocaleString() || '0'}
            subtitle="Today"
            color="success"
            trend={{ direction: 'up' }}
          />
        </Grid>
        <Grid item xs={6}>
          <StatCard
            icon={<LocationOn />}
            title="Busy Stations"
            value={stats.busy_stations}
            subtitle="High activity"
            color="warning"
          />
        </Grid>
        <Grid item xs={6}>
          <StatCard
            icon={<ShoppingCart />}
            title="Busy Attractions"
            value={stats.busy_attractions}
            subtitle="High occupancy"
            color="error"
          />
        </Grid>
      </Grid>

      {/* Performance Metrics */}
      <Card sx={{ mb: 2 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Performance Metrics
          </Typography>
          <Box sx={{ mb: 2 }}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
              <Typography variant="body2">On-time Performance</Typography>
              <Typography variant="body2">{stats.on_time_percentage}%</Typography>
            </Box>
            <LinearProgress
              variant="determinate"
              value={stats.on_time_percentage}
              color="success"
              sx={{ height: 8, borderRadius: 4 }}
            />
          </Box>
          <Box sx={{ mb: 2 }}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
              <Typography variant="body2">Efficiency Rate</Typography>
              <Typography variant="body2">{stats.efficiency_rate}%</Typography>
            </Box>
            <LinearProgress
              variant="determinate"
              value={stats.efficiency_rate}
              color="primary"
              sx={{ height: 8, borderRadius: 4 }}
            />
          </Box>
          <Box>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
              <Typography variant="body2">Average Delay</Typography>
              <Typography variant="body2">{stats.avg_delay} min</Typography>
            </Box>
            <LinearProgress
              variant="determinate"
              value={Math.min((5 - stats.avg_delay) * 20, 100)}
              color={stats.avg_delay <= 3 ? 'success' : stats.avg_delay <= 5 ? 'warning' : 'error'}
              sx={{ height: 8, borderRadius: 4 }}
            />
          </Box>
        </CardContent>
      </Card>

      {/* Transit Distribution */}
      <Card>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Transit Distribution
          </Typography>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
            {distributionData.map((item) => (
              <Box key={item.label} sx={{ display: 'flex', alignItems: 'center' }}>
                <Box
                  sx={{
                    width: 16,
                    height: 16,
                    borderRadius: '50%',
                    bgcolor: item.color,
                    mr: 1
                  }}
                />
                <Box sx={{ flexGrow: 1 }}>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                    <Typography variant="body2">{item.label}</Typography>
                    <Typography variant="body2">{item.value}%</Typography>
                  </Box>
                  <LinearProgress
                    variant="determinate"
                    value={item.value}
                    sx={{
                      height: 4,
                      borderRadius: 2,
                      '& .MuiLinearProgress-bar': {
                        bgcolor: item.color
                      }
                    }}
                  />
                </Box>
              </Box>
            ))}
          </Box>
        </CardContent>
      </Card>

      {/* Last Updated */}
      <Typography variant="caption" color="textSecondary" sx={{ display: 'block', textAlign: 'center', mt: 2 }}>
        Last updated: {lastUpdated.toLocaleTimeString()}
      </Typography>
    </Box>
  )
}

export default RealTimeStats