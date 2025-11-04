import React from 'react'
import {
  Box,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Button,
  ButtonGroup,
  Typography,
  TextField,
  Grid
} from '@mui/material'
import {
  PlayArrow,
  Pause,
  Refresh,
  Schedule,
  Today,
  CalendarToday,
  TrendingUp
} from '@mui/icons-material'
import { format, subDays, subMonths } from 'date-fns'

function TemporalController({ selectedTimeRange, onTimeRangeChange }) {
  const [customStartDate, setCustomStartDate] = React.useState('')
  const [customEndDate, setCustomEndDate] = React.useState('')
  const [isPlaying, setIsPlaying] = React.useState(false)
  const [playbackSpeed, setPlaybackSpeed] = React.useState(1000) // milliseconds

  const timeRangeOptions = [
    { value: 'realtime', label: 'Real-time', icon: <Today /> },
    { value: 'last_hour', label: 'Last Hour', icon: <Schedule /> },
    { value: 'today', label: 'Today', icon: <Today /> },
    { value: 'last_week', label: 'Last Week', icon: <CalendarToday /> },
    { value: 'last_month', label: 'Last Month', icon: <CalendarToday /> },
    { value: 'custom', label: 'Custom Range', icon: <TrendingUp /> }
  ]

  const handleTimeRangeChange = (event) => {
    const newRange = event.target.value
    onTimeRangeChange(newRange)
    
    if (newRange === 'custom') {
      // Set default custom dates
      const today = new Date()
      const lastWeek = subDays(today, 7)
      setCustomStartDate(format(lastWeek, 'yyyy-MM-dd'))
      setCustomEndDate(format(today, 'yyyy-MM-dd'))
    }
  }

  const handlePlayPause = () => {
    setIsPlaying(!isPlaying)
  }

  const handleRefresh = () => {
    // Trigger data refresh
    window.location.reload()
  }

  const handleSpeedChange = (speed) => {
    setPlaybackSpeed(speed)
  }

  return (
    <Box>
      <Grid container spacing={2} alignItems="center">
        {/* Time Range Selector */}
        <Grid item xs={12} md={4}>
          <FormControl fullWidth>
            <InputLabel>Time Range</InputLabel>
            <Select
              value={selectedTimeRange}
              onChange={handleTimeRangeChange}
              label="Time Range"
            >
              {timeRangeOptions.map((option) => (
                <MenuItem key={option.value} value={option.value}>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    {option.icon}
                    {option.label}
                  </Box>
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        </Grid>

        {/* Custom Date Range */}
        {selectedTimeRange === 'custom' && (
          <Grid item xs={12} md={4}>
            <Box sx={{ display: 'flex', gap: 1 }}>
              <TextField
                label="Start Date"
                type="date"
                value={customStartDate}
                onChange={(e) => setCustomStartDate(e.target.value)}
                InputLabelProps={{ shrink: true }}
                size="small"
                fullWidth
              />
              <TextField
                label="End Date"
                type="date"
                value={customEndDate}
                onChange={(e) => setCustomEndDate(e.target.value)}
                InputLabelProps={{ shrink: true }}
                size="small"
                fullWidth
              />
            </Box>
          </Grid>
        )}

        {/* Playback Controls */}
        <Grid item xs={12} md={4}>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <ButtonGroup size="small">
              <Button
                variant={isPlaying ? 'contained' : 'outlined'}
                onClick={handlePlayPause}
                startIcon={isPlaying ? <Pause /> : <PlayArrow />}
              >
                {isPlaying ? 'Pause' : 'Play'}
              </Button>
              <Button
                variant="outlined"
                onClick={handleRefresh}
                startIcon={<Refresh />}
              >
                Refresh
              </Button>
            </ButtonGroup>
            
            {isPlaying && (
              <FormControl size="small" sx={{ minWidth: 80 }}>
                <InputLabel>Speed</InputLabel>
                <Select
                  value={playbackSpeed}
                  onChange={(e) => handleSpeedChange(e.target.value)}
                  label="Speed"
                >
                  <MenuItem value={500}>0.5x</MenuItem>
                  <MenuItem value={1000}>1x</MenuItem>
                  <MenuItem value={2000}>2x</MenuItem>
                  <MenuItem value={5000}>5x</MenuItem>
                </Select>
              </FormControl>
            )}
          </Box>
        </Grid>
      </Grid>

      {/* Time Range Info */}
      <Box sx={{ mt: 2, p: 1, bgcolor: 'grey.50', borderRadius: 1 }}>
        <Typography variant="caption" color="textSecondary">
          <strong>Current Selection:</strong>{' '}
          {selectedTimeRange === 'realtime' && 'Live data updates'}
          {selectedTimeRange === 'last_hour' && 'Data from the last 60 minutes'}
          {selectedTimeRange === 'today' && 'Data from today'}
          {selectedTimeRange === 'last_week' && 'Data from the last 7 days'}
          {selectedTimeRange === 'last_month' && 'Data from the last 30 days'}
          {selectedTimeRange === 'custom' && 
            `Custom range: ${customStartDate} to ${customEndDate}`
          }
          {isPlaying && ` | Playing at ${playbackSpeed === 500 ? '0.5x' : 
            playbackSpeed === 1000 ? '1x' : 
            playbackSpeed === 2000 ? '2x' : '5x'} speed`
          }
        </Typography>
      </Box>
    </Box>
  )
}

export default TemporalController