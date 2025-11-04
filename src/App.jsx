import React, { useState } from 'react'
import {
  Box,
  AppBar,
  Toolbar,
  Typography,
  Drawer,
  IconButton,
  Grid,
  Card,
  CardContent,
  useMediaQuery,
  useTheme,
  Divider,
  Chip,
  Avatar,
} from '@mui/material'
import {
  Menu as MenuIcon,
  Dashboard as DashboardIcon,
  Timeline as TimelineIcon,
  Map as MapIcon,
  Train as TrainIcon,
  School as SchoolIcon,
  Person as PersonIcon,
} from '@mui/icons-material'
import InteractiveMap from './components/Map/InteractiveMap.jsx'
import TrendCharts from './components/Dashboard/TrendCharts.jsx'
import RealTimeStats from './components/Dashboard/RealTimeStats.jsx'
import TemporalController from './components/Map/TemporalController.jsx'

const drawerWidth = 280

function App() {
  const theme = useTheme()
  const isMobile = useMediaQuery(theme.breakpoints.down('lg'))
  const [mobileOpen, setMobileOpen] = useState(false)
  const [activeView, setActiveView] = useState('map')
  const [selectedTimeRange, setSelectedTimeRange] = useState('realtime')

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen)
  }

  const drawer = (
    <Box sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      {/* Header */}
      <Box sx={{ p: 3, textAlign: 'center', background: 'linear-gradient(135deg, #1976d2 0%, #42a5f5 100%)', color: 'white' }}>
        <Typography variant="h6" sx={{ fontWeight: 'bold', mb: 1 }}>
          KV Transit Analytics
        </Typography>
        <Typography variant="caption" sx={{ opacity: 0.9 }}>
          Klang Valley Transportation Hub
        </Typography>
      </Box>
      
      <Divider />
      
      {/* Navigation */}
      <Box sx={{ p: 2, flexGrow: 1 }}>
        <Typography variant="subtitle2" sx={{ mb: 2, color: 'text.secondary', textTransform: 'uppercase', fontSize: '0.75rem', fontWeight: 'bold' }}>
          Navigation
        </Typography>
        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 0.5 }}>
          <IconButton
            color={activeView === 'map' ? 'primary' : 'inherit'}
            onClick={() => setActiveView('map')}
            sx={{
              justifyContent: 'flex-start',
              px: 2,
              py: 1,
              borderRadius: 2,
              '&:hover': {
                backgroundColor: activeView === 'map' ? 'primary.main' : 'action.hover'
              }
            }}
          >
            <MapIcon sx={{ mr: 2 }} />
            <Typography variant="body2">Interactive Map</Typography>
          </IconButton>
          <IconButton
            color={activeView === 'dashboard' ? 'primary' : 'inherit'}
            onClick={() => setActiveView('dashboard')}
            sx={{
              justifyContent: 'flex-start',
              px: 2,
              py: 1,
              borderRadius: 2,
              '&:hover': {
                backgroundColor: activeView === 'dashboard' ? 'primary.main' : 'action.hover'
              }
            }}
          >
            <DashboardIcon sx={{ mr: 2 }} />
            <Typography variant="body2">Real-time Dashboard</Typography>
          </IconButton>
          <IconButton
            color={activeView === 'trends' ? 'primary' : 'inherit'}
            onClick={() => setActiveView('trends')}
            sx={{
              justifyContent: 'flex-start',
              px: 2,
              py: 1,
              borderRadius: 2,
              '&:hover': {
                backgroundColor: activeView === 'trends' ? 'primary.main' : 'action.hover'
              }
            }}
          >
            <TimelineIcon sx={{ mr: 2 }} />
            <Typography variant="body2">Trend Analysis</Typography>
          </IconButton>
        </Box>
      </Box>

      <Divider />
      
      {/* Credits */}
      <Box sx={{ p: 2, backgroundColor: 'grey.50' }}>
        <Typography variant="subtitle2" sx={{ mb: 1, fontWeight: 'bold', color: 'text.secondary' }}>
          Credits
        </Typography>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
          <PersonIcon sx={{ fontSize: 16, mr: 1, color: 'text.secondary' }} />
          <Typography variant="caption" color="text.secondary">
            Amir Hafizi Bin Musa
          </Typography>
        </Box>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
          <SchoolIcon sx={{ fontSize: 16, mr: 1, color: 'text.secondary' }} />
          <Typography variant="caption" color="text.secondary">
            UiTM Computer Science Student
          </Typography>
        </Box>
        <Chip
          size="small"
          icon={<TrainIcon />}
          label="Transportation Analytics"
          variant="outlined"
          sx={{ width: '100%', fontSize: '0.7rem' }}
        />
      </Box>
    </Box>
  )

  return (
    <Box sx={{ display: 'flex', height: '100vh' }}>
      <AppBar
        position="fixed"
        elevation={2}
        sx={{
          width: { sm: `calc(100% - ${drawerWidth}px)` },
          ml: { sm: `${drawerWidth}px` },
          background: 'linear-gradient(135deg, #1976d2 0%, #42a5f5 100%)',
        }}
      >
        <Toolbar sx={{ minHeight: '70px !important' }}>
          <IconButton
            color="inherit"
            aria-label="open drawer"
            edge="start"
            onClick={handleDrawerToggle}
            sx={{ mr: 2, display: { sm: 'none' } }}
          >
            <MenuIcon />
          </IconButton>
          
          <Avatar
            sx={{
              mr: 2,
              bgcolor: 'rgba(255, 255, 255, 0.2)',
              border: '2px solid rgba(255, 255, 255, 0.3)'
            }}
          >
            <TrainIcon />
          </Avatar>
          
          <Box sx={{ flexGrow: 1 }}>
            <Typography
              variant="h5"
              noWrap
              component="div"
              sx={{
                fontWeight: 'bold',
                textShadow: '0 1px 2px rgba(0,0,0,0.2)'
              }}
            >
              KV Transit Analytics
            </Typography>
            <Typography
              variant="caption"
              sx={{
                opacity: 0.9,
                display: 'block',
                fontSize: '0.75rem'
              }}
            >
              Klang Valley Transportation & Attractions Hub
            </Typography>
          </Box>
          
          <Box sx={{ display: { xs: 'none', sm: 'block' } }}>
            <Chip
              label="Realtime Analytics"
              color="secondary"
              variant="filled"
              size="small"
              sx={{
                fontWeight: 'bold',
                backgroundColor: 'rgba(255, 255, 255, 0.2)',
                color: 'white',
                '& .MuiChip-label': {
                  fontWeight: 'bold'
                }
              }}
            />
          </Box>
        </Toolbar>
      </AppBar>

      <Box
        component="nav"
        sx={{ width: { sm: drawerWidth }, flexShrink: { sm: 0 } }}
      >
        <Drawer
          variant="temporary"
          open={mobileOpen}
          onClose={handleDrawerToggle}
          ModalProps={{
            keepMounted: true, // Better open performance on mobile.
          }}
          sx={{
            display: { xs: 'block', sm: 'none' },
            '& .MuiDrawer-paper': {
              boxSizing: 'border-box',
              width: drawerWidth,
            },
          }}
        >
          {drawer}
        </Drawer>
        <Drawer
          variant="permanent"
          sx={{
            display: { xs: 'none', sm: 'block' },
            '& .MuiDrawer-paper': {
              boxSizing: 'border-box',
              width: drawerWidth,
              borderRight: '1px solid rgba(0, 0, 0, 0.08)',
            },
          }}
          open
        >
          {drawer}
        </Drawer>
      </Box>

      <Box
        component="main"
        sx={{
          flexGrow: 1,
          p: 3,
          width: { sm: `calc(100% - ${drawerWidth}px)` },
          mt: 8,
          backgroundColor: 'grey.50',
          minHeight: 'calc(100vh - 70px)',
        }}
      >
        {/* Page Header */}
        <Box sx={{ mb: 3 }}>
          <Typography
            variant="h4"
            sx={{
              fontWeight: 'bold',
              color: 'primary.main',
              mb: 1,
              display: 'flex',
              alignItems: 'center',
              gap: 1
            }}
          >
            {activeView === 'map' && (
              <>
                <MapIcon />
                Interactive Map View
              </>
            )}
            {activeView === 'dashboard' && (
              <>
                <DashboardIcon />
                Real-time Dashboard
              </>
            )}
            {activeView === 'trends' && (
              <>
                <TimelineIcon />
                Trend Analysis
              </>
            )}
          </Typography>
          <Typography variant="body1" color="text.secondary">
            {activeView === 'map' && 'Explore transportation networks and attractions across Klang Valley with real-time data visualization.'}
            {activeView === 'dashboard' && 'Monitor live statistics, performance metrics, and transit distribution in real-time.'}
            {activeView === 'trends' && 'Analyze historical patterns and trends to understand transportation behavior over time.'}
          </Typography>
        </Box>

        <Grid container spacing={3}>
          {/* Temporal Controller */}
          <Grid item xs={12}>
            <Card elevation={1}>
              <CardContent>
                <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                  <TimelineIcon color="primary" />
                  Time Controls
                </Typography>
                <TemporalController
                  selectedTimeRange={selectedTimeRange}
                  onTimeRangeChange={setSelectedTimeRange}
                />
              </CardContent>
            </Card>
          </Grid>

          {/* Main Content Area */}
          {activeView === 'map' && (
            <Grid item xs={12}>
              <Card sx={{ height: '70vh' }} elevation={2}>
                <CardContent sx={{ height: '100%', p: 0 }}>
                  <InteractiveMap
                    selectedTimeRange={selectedTimeRange}
                    selectedDate={new Date()}
                  />
                </CardContent>
              </Card>
            </Grid>
          )}

          {activeView === 'dashboard' && (
            <>
              <Grid item xs={12} md={4}>
                <RealTimeStats selectedTimeRange={selectedTimeRange} />
              </Grid>
              <Grid item xs={12} md={8}>
                <Card sx={{ height: '400px' }} elevation={2}>
                  <CardContent sx={{ height: '100%' }}>
                    <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                      <DashboardIcon color="primary" />
                      Transit Activity Trends
                    </Typography>
                    <TrendCharts selectedTimeRange={selectedTimeRange} />
                  </CardContent>
                </Card>
              </Grid>
            </>
          )}

          {activeView === 'trends' && (
            <Grid item xs={12}>
              <Card sx={{ height: '60vh' }} elevation={2}>
                <CardContent sx={{ height: '100%' }}>
                  <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <TimelineIcon color="primary" />
                    Historical Trend Analysis
                  </Typography>
                  <TrendCharts
                    selectedTimeRange={selectedTimeRange}
                    showHistorical={true}
                  />
                </CardContent>
              </Card>
            </Grid>
          )}
        </Grid>

        {/* Footer */}
        <Box
          sx={{
            mt: 4,
            pt: 3,
            borderTop: '1px solid rgba(0, 0, 0, 0.1)',
            textAlign: 'center',
            backgroundColor: 'background.paper',
            borderRadius: 2,
            p: 2
          }}
        >
          <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
            Created with ❤️ by{' '}
            <Typography
              variant="body2"
              component="span"
              sx={{
                fontWeight: 'bold',
                color: 'primary.main',
                display: 'inline-flex',
                alignItems: 'center',
                gap: 0.5
              }}
            >
              <PersonIcon sx={{ fontSize: 16 }} />
              Amir Hafizi Bin Musa
            </Typography>
          </Typography>
          <Typography variant="caption" color="text.secondary" sx={{ display: 'block' }}>
            UiTM Computer Science Student • Transportation Analytics Project
          </Typography>
        </Box>
      </Box>
    </Box>
  )
}

export default App