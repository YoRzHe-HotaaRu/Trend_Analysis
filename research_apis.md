# Research: Available APIs for Klang Valley Transit and Attractions

## Transit Systems APIs

### Malaysian Public Transit
1. **MyRapid** (Rapid KL)
   - Website: https://www.myrapid.com.my/
   - API Status: Limited public APIs, mostly web scraping needed
   - Data: LRT, MRT, BRT real-time schedules, station locations
   - Alternative: GTFS feeds potentially available

2. **KTM Berhad**
   - Website: https://www.ktmb.com.my/
   - API Status: Limited public APIs
   - Data: KTM Komuter schedules, station information
   - Alternative: Manual data collection or partner APIs

3. **Grab API**
   - Documentation: https://developer.grab.com/
   - Data: Real-time ride-hailing data, pricing, ETAs
   - Coverage: Whole Klang Valley
   - Authentication: API keys required

### Open Source Transit APIs
1. **OpenTripPlanner**
   - May have Malaysian transit data
   - GTFS format support
   - Community-driven

2. **TransitLand**
   - Transit data aggregator
   - May include Malaysian operators

## Attractions APIs

### Google Places API
- Comprehensive attraction data
- Ratings, reviews, photos, opening hours
- Geographic coverage: Entire Klang Valley
- Requires API key

### Foursquare Places API
- Popular venues, restaurants, entertainment
- Check-ins data for temporal analysis
- Good coverage of Malaysian locations

### TripAdvisor API
- Tourist attractions, hotels, restaurants
- Reviews and ratings
- Geographic data

### OpenStreetMap / Overpass API
- Community-driven data
- Points of interest, amenities
- Free to use
- Good coverage of Malaysian areas

### Malaysian Tourism APIs
1. **Tourism Malaysia Official**
   - Limited API access
   - Official attractions database

2. **Malaysia Truly Asia**
   - Tourism promotion site
   - Manual data extraction needed

## Data Architecture Recommendations

### Real-time Data Sources
1. **Grab API** - Ride-hailing patterns (proxy for human movement)
2. **Google Places API** - Real-time venue status
3. **MyRapid GTFS** - Transit schedules and delays

### Historical Data Sources
1. **Foursquare API** - Historical venue popularity
2. **OpenStreetMap** - Static attraction locations
3. **Custom data collection** - Transit usage patterns

### Spatial Data
1. **Google Maps API** - Base maps, geocoding
2. **OpenStreetMap Nominatim** - Free geocoding
3. **Malaysian coordinate systems** - Handle local projections

## Recommended Implementation Strategy

1. **Primary APIs**: Grab, Google Places, Foursquare
2. **Fallback Sources**: OpenStreetMap, manual data
3. **Data Processing**: Flask backend with temporal caching
4. **Visualization**: React with interactive mapping libraries

## Next Steps
1. Set up API access and authentication
2. Design data collection strategies
3. Plan spatio-temporal data models
4. Create visualization components