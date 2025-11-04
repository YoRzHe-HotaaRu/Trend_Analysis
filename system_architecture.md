# System Architecture: Klang Valley Spatio-Temporal Visualization Dashboard

## Overview
A web-based spatio-temporal visualization system for Klang Valley transit and attractions using React frontend and Flask backend.

## Architecture Components

### Frontend (React)
```
src/
├── components/
│   ├── Map/
│   │   ├── InteractiveMap.jsx          # Main map with temporal controls
│   │   ├── TransitLayer.jsx            # Transit stations and routes
│   │   ├── AttractionLayer.jsx         # Attraction markers and clusters
│   │   └── TemporalController.jsx      # Time-based filtering
│   ├── Dashboard/
│   │   ├── TrendCharts.jsx             # Historical trend visualizations
│   │   ├── RealTimeStats.jsx           # Live statistics panel
│   │   └── TimeSeriesAnalysis.jsx      # Temporal pattern analysis
│   └── UI/
│       ├── ThemeProvider.jsx           # Light theme configuration
│       └── ResponsiveLayout.jsx        # Responsive grid system
├── hooks/
│   ├── useDataFetch.js                 # Custom hooks for API calls
│   └── useTemporalData.js              # Temporal data management
├── services/
│   └── apiService.js                   # Backend API communication
└── utils/
    └── dataProcessing.js               # Data transformation utilities
```

### Backend (Flask)
```
backend/
├── app.py                              # Main Flask application
├── api/
│   ├── routes/
│   │   ├── transit_routes.py          # Transit data endpoints
│   │   ├── attraction_routes.py       # Attraction data endpoints
│   │   └── analysis_routes.py         # Trend analysis endpoints
│   └── services/
│       ├── data_collectors.py         # Multi-source data collection
│       ├── temporal_processing.py     # Time-series data processing
│       └── spatial_processing.py      # Geographic data handling
├── models/
│   ├── database.py                    # Database configuration
│   ├── transit_models.py             # Transit data models
│   └── attraction_models.py          # Attraction data models
├── external_apis/
│   ├── grab_api.py                   # Grab ride-hailing data
│   ├── google_places.py              # Google Places API integration
│   ├── foursquare_api.py             # Foursquare venues data
│   └── osm_api.py                    # OpenStreetMap data
└── utils/
    ├── geocoding.py                  # Geographic utilities
    └── data_cache.py                 # Caching strategies
```

## Technology Stack

### Frontend
- **React 18** with functional components and hooks
- **Leaflet** for interactive mapping (open-source alternative to Google Maps)
- **React-Leaflet** for React integration
- **Chart.js/D3.js** for temporal visualizations
- **Material-UI or Chakra UI** for light theme components
- **React Query** for efficient data fetching and caching

### Backend
- **Flask** as the web framework
- **SQLite** for development (easily upgradeable to PostgreSQL)
- **Celery** with Redis for background data collection tasks
- **Pandas** for data processing and analysis
- **Geopandas** for spatial data operations

### External APIs
- **Grab Developer API** for ride-hailing patterns
- **Google Places API** for attraction data
- **Foursquare Places API** for venue information
- **OpenStreetMap Nominatim** for free geocoding

## Data Flow Architecture

### Real-time Data Pipeline
```
External APIs → Data Collectors → Flask API → React Frontend → Real-time Updates
```

### Historical Data Pipeline
```
Data Collection Jobs → Database Storage → Temporal Analysis → Trend Visualization
```

### Spatial Data Processing
```
Raw Coordinates → Geocoding Service → Spatial Index → Map Rendering
```

## Key Features Implementation

### 1. Spatio-Temporal Visualization
- Interactive map with time-based layer controls
- Animated transitions showing temporal changes
- Heat maps for density visualization
- Timeline scrubbing for historical analysis

### 2. Multi-Source Data Integration
- Unified data model for different API sources
- Automatic data validation and cleaning
- Rate limiting and API key management
- Fallback mechanisms for failed API calls

### 3. Real-time Updates
- WebSocket connections for live data streaming
- Automatic refresh intervals for different data types
- User-configurable update frequencies

### 4. Trend Analysis
- Moving averages for temporal smoothing
- Peak hour identification algorithms
- Seasonal pattern detection
- Correlation analysis between transit and attraction usage

## Deployment Architecture

### Development Environment
```
Frontend: Vite dev server (http://localhost:3000)
Backend: Flask dev server (http://localhost:5000)
Database: SQLite local file
```

### Production Environment
```
Frontend: Static files served by nginx
Backend: Gunicorn WSGI server
Database: PostgreSQL with PostGIS extension
Cache: Redis for session and data caching
```

## Performance Considerations

### Frontend Optimization
- Lazy loading of map components
- Data virtualization for large datasets
- Efficient re-rendering with React.memo
- Progressive loading of historical data

### Backend Optimization
- Database indexing on spatial and temporal columns
- API response caching with TTL
- Background job processing for heavy computations
- Connection pooling for database operations

### Data Management
- Spatial indexing with R-tree or similar
- Time-series data partitioning by date ranges
- Compressed storage for historical archives
- Real-time data retention policies

## Security Considerations
- API key management and rotation
- Rate limiting on external API calls
- Input validation and sanitization
- HTTPS enforcement for production deployment