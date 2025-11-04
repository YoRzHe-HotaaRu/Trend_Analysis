import React, { useMemo } from 'react'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  Filler
} from 'chart.js'
import { Line, Bar, Doughnut } from 'react-chartjs-2'
import { 
  Box, 
  Typography, 
  Grid, 
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  ToggleButton,
  ToggleButtonGroup
} from '@mui/material'
import { useDataFetch } from '../../hooks/useDataFetch.js'

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  Filler
)

function TrendCharts({ selectedTimeRange, showHistorical = false }) {
  const [chartType, setChartType] = React.useState('line')
  const [metric, setMetric] = React.useState('passenger_count')

  // Fetch trend data based on selected time range
  const {
    data: trendData,
    isLoading,
    error
  } = useDataFetch(`/api/analysis/trends`, {
    params: {
      timeRange: selectedTimeRange,
      metric: metric,
      historical: showHistorical
    }
  })

  // Process data for charts
  const processedData = useMemo(() => {
    if (!trendData) return null

    const labels = trendData.labels || []
    const values = trendData.values || []
    const datasets = trendData.datasets || []

    return {
      labels,
      datasets: [{
        label: `Transit ${metric.replace('_', ' ').toUpperCase()}`,
        data: values,
        borderColor: 'rgb(25, 118, 210)',
        backgroundColor: 'rgba(25, 118, 210, 0.1)',
        fill: true,
        tension: 0.4,
      }]
    }
  }, [trendData, metric])

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: showHistorical ? 'Historical Trends' : 'Current Trends'
      },
      tooltip: {
        mode: 'index',
        intersect: false,
        callbacks: {
          label: (context) => {
            const value = context.parsed.y
            const metricLabel = metric === 'passenger_count' ? 'Passengers' : 
                               metric === 'delay_minutes' ? 'Delay (min)' : 'Active Routes'
            return `${metricLabel}: ${value.toLocaleString()}`
          }
        }
      }
    },
    scales: {
      x: {
        display: true,
        title: {
          display: true,
          text: selectedTimeRange === 'realtime' ? 'Time' : 'Date'
        }
      },
      y: {
        display: true,
        title: {
          display: true,
          text: metric === 'passenger_count' ? 'Passenger Count' : 
                metric === 'delay_minutes' ? 'Delay (Minutes)' : 'Active Routes'
        }
      }
    },
    interaction: {
      mode: 'nearest',
      axis: 'x',
      intersect: false
    }
  }

  const doughnutData = {
    labels: ['LRT', 'MRT', 'BRT', 'KTM'],
    datasets: [{
      data: trendData?.distribution || [25, 35, 20, 20],
      backgroundColor: [
        '#1976d2',
        '#f50057',
        '#4caf50',
        '#ff9800'
      ],
      borderWidth: 2,
      borderColor: '#ffffff'
    }]
  }

  if (isLoading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%' }}>
        <Typography>Loading trend data...</Typography>
      </Box>
    )
  }

  if (error) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%' }}>
        <Typography color="error">Error loading trend data</Typography>
      </Box>
    )
  }

  return (
    <Box>
      {/* Chart Controls */}
      <Box sx={{ mb: 2, display: 'flex', gap: 2, alignItems: 'center', flexWrap: 'wrap' }}>
        <ToggleButtonGroup
          value={chartType}
          exclusive
          onChange={(e, newType) => newType && setChartType(newType)}
          size="small"
        >
          <ToggleButton value="line">Line Chart</ToggleButton>
          <ToggleButton value="bar">Bar Chart</ToggleButton>
          <ToggleButton value="doughnut">Distribution</ToggleButton>
        </ToggleButtonGroup>

        <FormControl size="small" sx={{ minWidth: 150 }}>
          <InputLabel>Metric</InputLabel>
          <Select
            value={metric}
            onChange={(e) => setMetric(e.target.value)}
            label="Metric"
          >
            <MenuItem value="passenger_count">Passenger Count</MenuItem>
            <MenuItem value="delay_minutes">Delay Minutes</MenuItem>
            <MenuItem value="active_routes">Active Routes</MenuItem>
          </Select>
        </FormControl>
      </Box>

      {/* Chart Display */}
      <Box sx={{ height: '300px' }}>
        {chartType === 'doughnut' ? (
          <Doughnut data={doughnutData} options={chartOptions} />
        ) : chartType === 'bar' ? (
          <Bar data={processedData} options={chartOptions} />
        ) : (
          <Line data={processedData} options={chartOptions} />
        )}
      </Box>

      {/* Additional Stats */}
      {trendData?.statistics && (
        <Grid container spacing={2} sx={{ mt: 2 }}>
          <Grid item xs={6} sm={3}>
            <Box sx={{ textAlign: 'center', p: 1 }}>
              <Typography variant="h6" color="primary">
                {trendData.statistics.avg_passengers || '0'}
              </Typography>
              <Typography variant="caption" color="textSecondary">
                Avg Passengers
              </Typography>
            </Box>
          </Grid>
          <Grid item xs={6} sm={3}>
            <Box sx={{ textAlign: 'center', p: 1 }}>
              <Typography variant="h6" color="success.main">
                {trendData.statistics.peak_hours || '0'}
              </Typography>
              <Typography variant="caption" color="textSecondary">
                Peak Hours
              </Typography>
            </Box>
          </Grid>
          <Grid item xs={6} sm={3}>
            <Box sx={{ textAlign: 'center', p: 1 }}>
              <Typography variant="h6" color="warning.main">
                {trendData.statistics.avg_delay || '0'}
              </Typography>
              <Typography variant="caption" color="textSecondary">
                Avg Delay (min)
              </Typography>
            </Box>
          </Grid>
          <Grid item xs={6} sm={3}>
            <Box sx={{ textAlign: 'center', p: 1 }}>
              <Typography variant="h6" color="error.main">
                {trendData.statistics.efficiency || '0'}%
              </Typography>
              <Typography variant="caption" color="textSecondary">
                Efficiency
              </Typography>
            </Box>
          </Grid>
        </Grid>
      )}
    </Box>
  )
}

export default TrendCharts