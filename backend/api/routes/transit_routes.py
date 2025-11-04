from flask import Blueprint, jsonify, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import logging
from datetime import datetime, timedelta
import json

# Import services
from external_apis.grab_api import GrabAPIService
from external_apis.osm_api import OpenStreetMapService
from api.services.temporal_processing import TemporalProcessor
from utils.data_cache import cache_manager
from models.database import TransitStation, TransitRoute, db

transit_bp = Blueprint('transit', __name__)
logger = logging.getLogger(__name__)

# Initialize services
grab_service = GrabAPIService()
osm_service = OpenStreetMapService()
temporal_processor = TemporalProcessor()

@transit_bp.route('/real-time')
def get_real_time_transit():
    """Get real-time transit data"""
    try:
        # Check cache first
        cache_key = 'transit_real_time'
        cached_data = cache_manager.get(cache_key)
        if cached_data:
            return jsonify(cached_data)

        # Fetch real-time data from multiple sources
        stations = []
        routes = []
        
        # Get LRT/MRT station data (simulated - would integrate with real APIs)
        lrt_stations = get_lrt_stations()
        mrt_stations = get_mrt_stations()
        brt_stations = get_brt_stations()
        
        # Get KTM Komuter data
        ktm_stations = get_ktm_stations()
        
        stations.extend(lrt_stations)
        stations.extend(mrt_stations)  
        stations.extend(brt_stations)
        stations.extend(ktm_stations)
        
        # Get route information
        routes = get_transit_routes()
        
        # Process and combine data
        result = {
            'timestamp': datetime.now().isoformat(),
            'stations': stations,
            'routes': routes,
            'summary': {
                'total_stations': len(stations),
                'operational_routes': len([r for r in routes if r.get('status') == 'operational']),
                'total_passengers': sum([s.get('passenger_count', 0) for s in stations]),
                'average_delay': calculate_average_delay(stations)
            }
        }
        
        # Cache for 2 minutes
        cache_manager.set(cache_key, result, timeout=120)
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error fetching real-time transit data: {str(e)}")
        return jsonify({'error': 'Failed to fetch transit data'}), 500

@transit_bp.route('/stations')
def get_transit_stations():
    """Get all transit stations with optional filtering"""
    try:
        line = request.args.get('line')
        status = request.args.get('status')
        
        # Get stations from database or external sources
        stations = get_all_transit_stations(line=line, status=status)
        
        return jsonify({
            'stations': stations,
            'count': len(stations),
            'filters': {
                'line': line,
                'status': status
            }
        })
        
    except Exception as e:
        logger.error(f"Error fetching transit stations: {str(e)}")
        return jsonify({'error': 'Failed to fetch stations'}), 500

@transit_bp.route('/status')
def get_transit_status():
    """Get current transit system status"""
    try:
        # Get current status of all transit lines
        status_data = {
            'lrt': {
                'line': 'LRT',
                'status': 'operational',
                'active_routes': 3,
                'total_stations': 51,
                'delays': 2,
                'incidents': 0
            },
            'mrt': {
                'line': 'MRT', 
                'status': 'operational',
                'active_routes': 2,
                'total_stations': 35,
                'delays': 1,
                'incidents': 0
            },
            'brt': {
                'line': 'BRT',
                'status': 'operational', 
                'active_routes': 1,
                'total_stations': 25,
                'delays': 0,
                'incidents': 0
            },
            'ktm': {
                'line': 'KTM Komuter',
                'status': 'operational',
                'active_routes': 2,
                'total_stations': 67,
                'delays': 1,
                'incidents': 0
            }
        }
        
        return jsonify({
            'timestamp': datetime.now().isoformat(),
            'status': status_data,
            'overall_status': 'operational'
        })
        
    except Exception as e:
        logger.error(f"Error fetching transit status: {str(e)}")
        return jsonify({'error': 'Failed to fetch transit status'}), 500

def get_lrt_stations():
    """Get LRT stations with real-time data"""
    # This would integrate with actual LRT APIs or GTFS feeds
    stations = []
    
    # Sample LRT stations in Klang Valley
    lrt_stations_data = [
        {'id': 'lrt_001', 'name': 'KLCC', 'latitude': 3.1478, 'longitude': 101.6953, 'line': 'Kelana Jaya'},
        {'id': 'lrt_002', 'name': 'Pasar Seni', 'latitude': 3.1478, 'longitude': 101.6947, 'line': 'Kelana Jaya'},
        {'id': 'lrt_003', 'name': 'KL Sentral', 'latitude': 3.1347, 'longitude': 101.6869, 'line': 'Kelana Jaya'},
        {'id': 'lrt_004', 'name': 'Kuala Lumpur', 'latitude': 3.1390, 'longitude': 101.6869, 'line': 'Ampang'},
        {'id': 'lrt_005', 'name': 'Majlis Ahor南区', 'latitude': 3.1007, 'longitude': 101.6854, 'line': 'Sri Petaling'},
    ]
    
    for station_data in lrt_stations_data:
        # Simulate real-time data
        stations.append({
            **station_data,
            'status': 'operational',
            'passenger_count': hash(station_data['id']) % 1000 + 200,
            'next_arrival': f"{hash(station_data['id']) % 4 + 1} min",
            'last_updated': datetime.now().isoformat()
        })
    
    return stations

def get_mrt_stations():
    """Get MRT stations with real-time data"""
    stations = []
    
    mrt_stations_data = [
        {'id': 'mrt_001', 'name': 'Kajang', 'latitude': 2.9897, 'longitude': 101.7857, 'line': 'SBK'},
        {'id': 'mrt_002', 'name': 'Bandar Utama', 'latitude': 3.1478, 'longitude': 101.4209, 'line': 'SBK'},
        {'id': 'mrt_003', 'name': 'KL Sentral', 'latitude': 3.1347, 'longitude': 101.6869, 'line': 'SBK'},
        {'id': 'mrt_004', 'name': 'Suria KLCC', 'latitude': 3.1478, 'longitude': 101.6953, 'line': 'PYL'},
    ]
    
    for station_data in mrt_stations_data:
        stations.append({
            **station_data,
            'status': 'operational',
            'passenger_count': hash(station_data['id']) % 800 + 300,
            'next_arrival': f"{hash(station_data['id']) % 5 + 2} min",
            'last_updated': datetime.now().isoformat()
        })
    
    return stations

def get_brt_stations():
    """Get BRT stations with real-time data"""
    stations = []
    
    brt_stations_data = [
        {'id': 'brt_001', 'name': 'Klang Sentral', 'latitude': 3.0653, 'longitude': 101.2942, 'line': 'BRT Sunway'},
        {'id': 'brt_002', 'name': 'USJ 1', 'latitude': 3.0517, 'longitude': 101.1917, 'line': 'BRT Sunway'},
    ]
    
    for station_data in brt_stations_data:
        stations.append({
            **station_data,
            'status': 'operational',
            'passenger_count': hash(station_data['id']) % 400 + 100,
            'next_arrival': f"{hash(station_data['id']) % 3 + 1} min",
            'last_updated': datetime.now().isoformat()
        })
    
    return stations

def get_ktm_stations():
    """Get KTM Komuter stations with real-time data"""
    stations = []
    
    ktm_stations_data = [
        {'id': 'ktm_001', 'name': 'KL Sentral', 'latitude': 3.1347, 'longitude': 101.6869, 'line': 'Port Klang'},
        {'id': 'ktm_002', 'name': 'Batu Caves', 'latitude': 3.2379, 'longitude': 101.6841, 'line': 'Port Klang'},
    ]
    
    for station_data in ktm_stations_data:
        stations.append({
            **station_data,
            'status': 'operational',
            'passenger_count': hash(station_data['id']) % 600 + 150,
            'next_arrival': f"{hash(station_data['id']) % 8 + 3} min",
            'last_updated': datetime.now().isoformat()
        })
    
    return stations

def get_transit_routes():
    """Get transit route information"""
    routes = [
        {
            'id': 'route_001',
            'name': 'Kelana Jaya Line',
            'type': 'LRT',
            'stations': ['lrt_001', 'lrt_002', 'lrt_003'],
            'status': 'operational',
            'frequency': '3-5 min',
            'operating_hours': '05:00 - 23:30'
        },
        {
            'id': 'route_002',
            'name': 'SBK Line',
            'type': 'MRT',
            'stations': ['mrt_001', 'mrt_002', 'mrt_003'],
            'status': 'operational',
            'frequency': '4-6 min',
            'operating_hours': '06:00 - 23:00'
        }
    ]
    
    return routes

def get_all_transit_stations(line=None, status=None):
    """Get all transit stations with optional filtering"""
    # Combine all stations
    all_stations = []
    all_stations.extend(get_lrt_stations())
    all_stations.extend(get_mrt_stations())
    all_stations.extend(get_brt_stations())
    all_stations.extend(get_ktm_stations())
    
    # Apply filters
    if line:
        all_stations = [s for s in all_stations if s['line'] == line]
    if status:
        all_stations = [s for s in all_stations if s.get('status') == status]
    
    return all_stations

def calculate_average_delay(stations):
    """Calculate average delay across all stations"""
    delays = [s.get('delay_minutes', 0) for s in stations if 'delay_minutes' in s]
    if delays:
        return sum(delays) / len(delays)
    return 0