from flask import Blueprint, jsonify, request
from flask_limiter import Limiter
import logging
from datetime import datetime, timedelta
import json

from utils.data_cache import cache_manager

dashboard_bp = Blueprint('dashboard', __name__)
logger = logging.getLogger(__name__)

@dashboard_bp.route('/stats')
def get_dashboard_stats():
    """Get dashboard statistics for real-time display"""
    try:
        # Check cache first
        cache_key = 'dashboard_stats'
        cached_data = cache_manager.get(cache_key)
        if cached_data:
            return jsonify(cached_data)
        
        # Generate real-time statistics
        stats = generate_realtime_stats()
        
        result = {
            'timestamp': datetime.now().isoformat(),
            'active_routes': stats['active_routes'],
            'total_passengers': stats['total_passengers'],
            'busy_stations': stats['busy_stations'],
            'busy_attractions': stats['busy_attractions'],
            'avg_delay': stats['avg_delay'],
            'efficiency_rate': stats['efficiency_rate'],
            'on_time_percentage': stats['on_time_percentage'],
            'transit_distribution': stats['transit_distribution'],
            'system_status': stats['system_status'],
            'weather': stats['weather'],
            'alerts': stats['alerts']
        }
        
        # Cache for 1 minute
        cache_manager.set(cache_key, result, timeout=60)
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error fetching dashboard stats: {str(e)}")
        return jsonify({'error': 'Failed to fetch dashboard statistics'}), 500

@dashboard_bp.route('/summary')
def get_dashboard_summary():
    """Get overall system summary"""
    try:
        summary = {
            'system_overview': {
                'status': 'operational',
                'uptime': '99.8%',
                'last_incident': '2024-10-15 14:30:00',
                'total_locations_tracked': 178,
                'active_data_sources': 5
            },
            'today_summary': {
                'total_passengers': 125430,
                'peak_passenger_hour': '08:00-09:00',
                'busiest_station': 'KL Sentral',
                'most_popular_attraction': 'Suria KLCC',
                'average_delay': 3.2,
                'system_efficiency': 94.5
            },
            'weekly_summary': {
                'total_passengers': 875301,
                'average_daily_passengers': 125043,
                'busiest_day': 'Friday',
                'trend': 'increasing'
            },
            'monthly_summary': {
                'total_passengers': 3852140,
                'growth_rate': 5.2,
                'projected_growth': 8.1,
                'seasonal_trend': 'positive'
            },
            'quick_stats': {
                'real_time_updates': True,
                'data_freshness': '< 30 seconds',
                'api_health': 'healthy',
                'last_data_update': datetime.now().isoformat()
            }
        }
        
        return jsonify(summary)
        
    except Exception as e:
        logger.error(f"Error fetching dashboard summary: {str(e)}")
        return jsonify({'error': 'Failed to fetch dashboard summary'}), 500

@dashboard_bp.route('/alerts')
def get_dashboard_alerts():
    """Get current system alerts and notifications"""
    try:
        alerts = [
            {
                'id': 'alert_001',
                'type': 'transit',
                'severity': 'warning',
                'title': 'MRT SBK Line Minor Delays',
                'message': 'Due to technical issues, expect 5-8 minute delays on SBK Line',
                'location': 'Bandar Utama - Suria KLCC',
                'timestamp': datetime.now().isoformat(),
                'estimated_duration': '45 minutes',
                'affected_services': ['MRT SBK'],
                'recommendations': ['Consider alternate routes', 'Allow extra travel time']
            },
            {
                'id': 'alert_002', 
                'type': 'attraction',
                'severity': 'info',
                'title': 'Suria KLCC High Crowds',
                'message': 'Higher than normal crowds expected due to school holidays',
                'location': 'Suria KLCC',
                'timestamp': datetime.now().isoformat(),
                'estimated_duration': '2 hours',
                'affected_services': ['Shopping Mall'],
                'recommendations': ['Visit after 14:00', 'Use parking level B3-B5']
            },
            {
                'id': 'alert_003',
                'type': 'weather',
                'severity': 'info',
                'title': 'Light Rain Expected',
                'message': 'Light rain expected in KL area from 16:00-18:00',
                'location': 'Klang Valley Region',
                'timestamp': datetime.now().isoformat(),
                'estimated_duration': '2 hours',
                'affected_services': ['All outdoor attractions'],
                'recommendations': ['Carry umbrellas', 'Indoor attractions recommended']
            }
        ]
        
        return jsonify({
            'alerts': alerts,
            'count': len(alerts),
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error fetching dashboard alerts: {str(e)}")
        return jsonify({'error': 'Failed to fetch dashboard alerts'}), 500

def generate_realtime_stats():
    """Generate realistic real-time statistics"""
    import random
    from datetime import datetime
    
    # Simulate realistic variations in real-time data
    base_time = datetime.now()
    
    # Generate passenger counts with realistic patterns
    current_hour = base_time.hour
    hour_multiplier = 1.0
    
    if 7 <= current_hour <= 9 or 17 <= current_hour <= 19:  # Peak hours
        hour_multiplier = 1.8
    elif 10 <= current_hour <= 16:  # Business hours
        hour_multiplier = 1.4
    elif 22 <= current_hour or current_hour <= 6:  # Night hours
        hour_multiplier = 0.5
    
    return {
        'active_routes': random.randint(22, 26),
        'total_passengers': int(50000 * hour_multiplier) + random.randint(-5000, 5000),
        'busy_stations': random.randint(6, 12),
        'busy_attractions': random.randint(12, 18),
        'avg_delay': round(random.uniform(1.2, 5.8), 1),
        'efficiency_rate': round(random.uniform(88.5, 97.2), 1),
        'on_time_percentage': round(random.uniform(82.3, 94.7), 1),
        'transit_distribution': {
            'lrt': random.randint(22, 32),
            'mrt': random.randint(30, 40),
            'brt': random.randint(18, 28),
            'ktm': random.randint(12, 22)
        },
        'system_status': {
            'overall': 'operational',
            'lrt': 'operational',
            'mrt': 'operational', 
            'brt': 'operational',
            'ktm': 'operational'
        },
        'weather': {
            'condition': 'partly_cloudy',
            'temperature': random.randint(26, 32),
            'humidity': random.randint(65, 85),
            'rainfall_chance': random.randint(10, 40)
        },
        'alerts': {
            'active': random.randint(0, 3),
            'total_today': random.randint(1, 8),
            'resolved_today': random.randint(1, 6)
        }
    }