from flask import Blueprint, jsonify, request
from flask_limiter import Limiter
import logging
from datetime import datetime, timedelta
import json

# Import services
from external_apis.google_places import GooglePlacesService
from external_apis.foursquare_api import FoursquareService
from external_apis.osm_api import OpenStreetMapService
from utils.data_cache import cache_manager

attraction_bp = Blueprint('attractions', __name__)
logger = logging.getLogger(__name__)

# Initialize services
google_places_service = GooglePlacesService()
foursquare_service = FoursquareService()
osm_service = OpenStreetMapService()

@attraction_bp.route('/active')
def get_active_attractions():
    """Get currently active attractions based on time range"""
    try:
        time_range = request.args.get('timeRange', 'realtime')
        date = request.args.get('date')
        
        # Check cache first
        cache_key = f'attractions_active_{time_range}'
        cached_data = cache_manager.get(cache_key)
        if cached_data:
            return jsonify(cached_data)
        
        # Get attractions by category
        malls = get_shopping_malls()
        restaurants = get_restaurants()
        entertainment = get_entertainment_venues()
        landmarks = get_tourist_landmarks()
        
        # Filter based on time range
        if time_range != 'realtime':
            # Apply time-based filtering logic
            filtered_malls = filter_by_time_range(malls, time_range, date)
            filtered_restaurants = filter_by_time_range(restaurants, time_range, date)
            filtered_entertainment = filter_by_time_range(entertainment, time_range, date)
        else:
            filtered_malls = malls
            filtered_restaurants = restaurants
            filtered_entertainment = entertainment
        
        result = {
            'timestamp': datetime.now().isoformat(),
            'time_range': time_range,
            'malls': filtered_malls,
            'restaurants': filtered_restaurants,
            'entertainment': filtered_entertainment,
            'landmarks': landmarks,
            'summary': {
                'total_malls': len(filtered_malls),
                'total_restaurants': len(filtered_restaurants),
                'total_entertainment': len(filtered_entertainment),
                'total_landmarks': len(landmarks),
                'busy_locations': len([a for a in filtered_malls + filtered_restaurants + filtered_entertainment if a.get('popularity_score', 0) > 70])
            }
        }
        
        # Cache for 5 minutes
        cache_manager.set(cache_key, result, timeout=300)
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error fetching active attractions: {str(e)}")
        return jsonify({'error': 'Failed to fetch attractions data'}), 500

@attraction_bp.route('/search')
def search_attractions():
    """Search attractions by name, category, or location"""
    try:
        query = request.args.get('q', '')
        category = request.args.get('category')
        latitude = request.args.get('lat')
        longitude = request.args.get('lng')
        radius = request.args.get('radius', 5000)  # Default 5km radius
        
        if not query and not category:
            return jsonify({'error': 'Search query or category required'}), 400
        
        # Search using multiple services
        results = []
        
        if query:
            # Search by name/keyword
            google_results = google_places_service.search_places(query, latitude, longitude, radius)
            results.extend(google_results)
            
            foursquare_results = foursquare_service.search_venues(query, latitude, longitude, radius)
            results.extend(foursquare_results)
            
        if category:
            # Search by category
            category_results = search_by_category(category, latitude, longitude, radius)
            results.extend(category_results)
        
        # Remove duplicates based on coordinates
        unique_results = remove_duplicate_locations(results)
        
        return jsonify({
            'query': query,
            'category': category,
            'results': unique_results,
            'count': len(unique_results),
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error searching attractions: {str(e)}")
        return jsonify({'error': 'Failed to search attractions'}), 500

@attraction_bp.route('/popularity')
def get_attraction_popularity():
    """Get popularity metrics for attractions"""
    try:
        time_range = request.args.get('timeRange', 'today')
        
        # Calculate popularity metrics
        popularity_data = {
            'time_range': time_range,
            'top_malls': [
                {
                    'name': 'Suria KLCC',
                    'popularity_score': 85,
                    'current_occupancy': 78,
                    'estimated_wait_time': 15,
                    'latitude': 3.1478,
                    'longitude': 101.6953
                },
                {
                    'name': 'Pavilion KL',
                    'popularity_score': 82,
                    'current_occupancy': 74,
                    'estimated_wait_time': 12,
                    'latitude': 3.1478,
                    'longitude': 101.6956
                }
            ],
            'top_restaurants': [
                {
                    'name': 'Trader Vic\'s',
                    'popularity_score': 76,
                    'current_occupancy': 65,
                    'estimated_wait_time': 25,
                    'latitude': 3.1478,
                    'longitude': 101.6953
                }
            ],
            'peak_hours': ['12:00-14:00', '19:00-21:00'],
            'average_occupancy': 68,
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(popularity_data)
        
    except Exception as e:
        logger.error(f"Error fetching attraction popularity: {str(e)}")
        return jsonify({'error': 'Failed to fetch popularity data'}), 500

def get_shopping_malls():
    """Get shopping malls in Klang Valley"""
    malls = [
        {
            'id': 'mall_001',
            'name': 'Suria KLCC',
            'category': 'Shopping Mall',
            'latitude': 3.1478,
            'longitude': 101.6953,
            'address': 'Kuala Lumpur City Centre, 50088 Kuala Lumpur',
            'rating': 4.5,
            'popularity_score': 85,
            'current_occupancy': 78,
            'estimated_wait_time': 15,
            'facilities': ['Parking', 'Food Court', 'Playground', 'ATM'],
            'operating_hours': '10:00 - 22:00',
            'last_updated': datetime.now().isoformat()
        },
        {
            'id': 'mall_002',
            'name': 'Pavilion Kuala Lumpur',
            'category': 'Shopping Mall',
            'latitude': 3.1478,
            'longitude': 101.6956,
            'address': '168, Bukit Bintang Street, Bukit Bintang, 55100 Kuala Lumpur',
            'rating': 4.4,
            'popularity_score': 82,
            'current_occupancy': 74,
            'estimated_wait_time': 12,
            'facilities': ['Parking', 'Luxury Shopping', 'Cinema', 'Restaurants'],
            'operating_hours': '10:00 - 22:00',
            'last_updated': datetime.now().isoformat()
        },
        {
            'id': 'mall_003',
            'name': 'Mid Valley Megamall',
            'category': 'Shopping Mall',
            'latitude': 3.1179,
            'longitude': 101.6788,
            'address': 'Mid Valley City, Lingkaran Syed Putra, 58000 Kuala Lumpur',
            'rating': 4.2,
            'popularity_score': 79,
            'current_occupancy': 71,
            'estimated_wait_time': 10,
            'facilities': ['Parking', 'Anchor Store', 'Garden Mall', 'The Gardens Mall'],
            'operating_hours': '10:00 - 22:00',
            'last_updated': datetime.now().isoformat()
        }
    ]
    
    return malls

def get_restaurants():
    """Get restaurants in Klang Valley"""
    restaurants = [
        {
            'id': 'rest_001',
            'name': 'Trader Vic\'s',
            'category': 'Fine Dining',
            'latitude': 3.1478,
            'longitude': 101.6953,
            'address': 'Suria KLCC, Lot C01.02.00, Concourse Level',
            'rating': 4.3,
            'popularity_score': 76,
            'current_occupancy': 65,
            'estimated_wait_time': 25,
            'cuisine': 'International',
            'price_range': '$$$',
            'operating_hours': '17:00 - 01:00',
            'last_updated': datetime.now().isoformat()
        },
        {
            'id': 'rest_002',
            'name': 'Skull House',
            'category': 'Thai Cuisine',
            'latitude': 3.1478,
            'longitude': 101.6959,
            'address': '92-96 Jalan Alor, Bukit Bintang',
            'rating': 4.0,
            'popularity_score': 68,
            'current_occupancy': 58,
            'estimated_wait_time': 15,
            'cuisine': 'Thai',
            'price_range': '$$',
            'operating_hours': '11:00 - 02:00',
            'last_updated': datetime.now().isoformat()
        }
    ]
    
    return restaurants

def get_entertainment_venues():
    """Get entertainment venues in Klang Valley"""
    entertainment = [
        {
            'id': 'ent_001',
            'name': 'GSC Mid Valley',
            'category': 'Cinema',
            'latitude': 3.1179,
            'longitude': 101.6788,
            'address': 'Mid Valley Megamall, 58000 Kuala Lumpur',
            'rating': 4.1,
            'popularity_score': 72,
            'current_occupancy': 45,
            'estimated_wait_time': 8,
            'facilities': ['Premium Cinema', 'IMAX', 'Parking'],
            'operating_hours': '10:00 - 23:00',
            'last_updated': datetime.now().isoformat()
        },
        {
            'id': 'ent_002',
            'name': 'Aquaria KLCC',
            'category': 'Aquarium',
            'latitude': 3.1478,
            'longitude': 101.6953,
            'address': 'Kuala Lumpur Convention Centre, Jalan Pinang',
            'rating': 4.0,
            'popularity_score': 65,
            'current_occupancy': 52,
            'estimated_wait_time': 5,
            'facilities': ['Marine Life', 'Educational Programs', 'Gift Shop'],
            'operating_hours': '10:00 - 20:00',
            'last_updated': datetime.now().isoformat()
        }
    ]
    
    return entertainment

def get_tourist_landmarks():
    """Get tourist landmarks in Klang Valley"""
    landmarks = [
        {
            'id': 'landmark_001',
            'name': 'Petronas Twin Towers',
            'category': 'Landmark',
            'latitude': 3.1478,
            'longitude': 101.6953,
            'address': 'Kuala Lumpur City Centre, 50088 Kuala Lumpur',
            'rating': 4.6,
            'popularity_score': 95,
            'current_occupancy': 85,
            'estimated_wait_time': 30,
            'facilities': ['Observation Deck', 'Sky Bridge', 'Tourist Center'],
            'operating_hours': '09:00 - 21:00',
            'last_updated': datetime.now().isoformat()
        },
        {
            'id': 'landmark_002',
            'name': 'Batu Caves',
            'category': 'Religious Site',
            'latitude': 3.2379,
            'longitude': 101.6841,
            'address': 'Gombak, 68100 Batu Caves, Selangor',
            'rating': 4.4,
            'popularity_score': 88,
            'current_occupancy': 72,
            'estimated_wait_time': 20,
            'facilities': ['Temple', 'Caves', 'Museum', 'Parking'],
            'operating_hours': '06:00 - 21:00',
            'last_updated': datetime.now().isoformat()
        }
    ]
    
    return landmarks

def filter_by_time_range(attractions, time_range, date):
    """Filter attractions based on time range"""
    # This would implement actual time-based filtering logic
    # For now, return all attractions with some simulated filtering
    
    if time_range == 'today':
        # Filter by today's date
        return [a for a in attractions if is_open_today(a, date)]
    elif time_range == 'last_hour':
        # Filter by last hour activity
        return [a for a in attractions if a.get('popularity_score', 0) > 50]
    else:
        return attractions

def search_by_category(category, latitude, longitude, radius):
    """Search attractions by category"""
    # This would implement category-based searching
    # For now, return filtered results based on category
    
    all_attractions = []
    all_attractions.extend(get_shopping_malls())
    all_attractions.extend(get_restaurants())
    all_attractions.extend(get_entertainment_venues())
    all_attractions.extend(get_tourist_landmarks())
    
    if category.lower() == 'malls':
        return [a for a in all_attractions if a['category'] == 'Shopping Mall']
    elif category.lower() == 'restaurants':
        return [a for a in all_attractions if 'Restaurant' in a['category'] or 'Cuisine' in a['category']]
    elif category.lower() == 'entertainment':
        return [a for a in all_attractions if a['category'] in ['Cinema', 'Aquarium', 'Entertainment']]
    else:
        return all_attractions

def remove_duplicate_locations(results):
    """Remove duplicate locations based on proximity"""
    unique_results = []
    
    for result in results:
        is_duplicate = False
        for unique in unique_results:
            # Check if locations are within 100 meters
            distance = calculate_distance(
                result['latitude'], result['longitude'],
                unique['latitude'], unique['longitude']
            )
            if distance < 100:  # 100 meters
                is_duplicate = True
                break
        
        if not is_duplicate:
            unique_results.append(result)
    
    return unique_results

def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two points in meters"""
    # Simplified distance calculation
    # In production, use proper geopy or haversine formula
    return ((lat1 - lat2) ** 2 + (lon1 - lon2) ** 2) ** 0.5 * 111000  # Rough conversion to meters

def is_open_today(attraction, date):
    """Check if attraction is open today"""
    # Simplified logic - would use actual business hours
    return True