from flask import Blueprint, jsonify, request
from flask_limiter import Limiter
import logging
from datetime import datetime, timedelta
import json
import numpy as np
import pandas as pd
from collections import defaultdict

from api.services.temporal_processing import TemporalProcessor
from utils.data_cache import cache_manager

analysis_bp = Blueprint('analysis', __name__)
logger = logging.getLogger(__name__)

@analysis_bp.route('/trends')
def get_trend_analysis():
    """Get trend analysis based on time range and metric"""
    try:
        time_range = request.args.get('timeRange', 'today')
        metric = request.args.get('metric', 'passenger_count')
        historical = request.args.get('historical', 'false').lower() == 'true'
        
        # Check cache first
        cache_key = f'trends_{time_range}_{metric}_{historical}'
        cached_data = cache_manager.get(cache_key)
        if cached_data:
            return jsonify(cached_data)
        
        # Generate trend data based on time range
        if time_range == 'realtime':
            trend_data = generate_realtime_trends(metric)
        elif time_range == 'last_hour':
            trend_data = generate_hourly_trends(metric)
        elif time_range == 'today':
            trend_data = generate_daily_trends(metric)
        elif time_range == 'last_week':
            trend_data = generate_weekly_trends(metric)
        elif time_range == 'last_month':
            trend_data = generate_monthly_trends(metric)
        else:
            trend_data = generate_daily_trends(metric)
        
        # Calculate statistics
        statistics = calculate_trend_statistics(trend_data['values'])
        
        result = {
            'timestamp': datetime.now().isoformat(),
            'time_range': time_range,
            'metric': metric,
            'historical': historical,
            'labels': trend_data['labels'],
            'values': trend_data['values'],
            'distribution': trend_data.get('distribution', [25, 35, 20, 20]),
            'statistics': statistics
        }
        
        # Cache for 10 minutes
        cache_manager.set(cache_key, result, timeout=600)
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error in trend analysis: {str(e)}")
        return jsonify({'error': 'Failed to generate trend analysis'}), 500

@analysis_bp.route('/patterns')
def get_pattern_analysis():
    """Get pattern analysis for transit and attraction usage"""
    try:
        time_range = request.args.get('timeRange', 'last_week')
        
        # Generate pattern data
        patterns = {
            'peak_hours': {
                'morning': '07:00-09:00',
                'evening': '17:00-19:00',
                'lunch': '12:00-14:00'
            },
            'daily_patterns': {
                'weekday': generate_weekday_patterns(),
                'weekend': generate_weekend_patterns()
            },
            'seasonal_patterns': {
                'dry_season': {'trend': 'increasing', 'peak_months': ['March', 'April', 'May']},
                'wet_season': {'trend': 'decreasing', 'peak_months': ['November', 'December', 'January']}
            },
            'transit_patterns': {
                'lrt_usage': 'High during peak hours, moderate off-peak',
                'mrt_usage': 'Consistent throughout day with morning/evening peaks',
                'brt_usage': 'Focused on specific routes, morning/evening peaks'
            },
            'attraction_patterns': {
                'malls': 'Peak during weekends and holidays',
                'restaurants': 'Peak during lunch (12-14) and dinner (19-21) times',
                'entertainment': 'Peak during weekends and evening hours'
            }
        }
        
        return jsonify({
            'time_range': time_range,
            'patterns': patterns,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error in pattern analysis: {str(e)}")
        return jsonify({'error': 'Failed to generate pattern analysis'}), 500

@analysis_bp.route('/correlations')
def get_correlation_analysis():
    """Get correlation analysis between transit and attraction usage"""
    try:
        time_range = request.args.get('timeRange', 'last_week')
        
        # Generate correlation data
        correlations = {
            'transit_attraction': {
                'correlation_strength': 0.75,
                'description': 'Strong positive correlation between transit usage and attraction footfall',
                'insights': [
                    'Higher transit usage correlates with increased mall activity',
                    'Restaurant peaks align with lunch/dinner transit schedules',
                    'Entertainment venues show strong evening transit correlation'
                ]
            },
            'peak_correlations': {
                'morning_peak': {
                    'transit': 'High',
                    'malls': 'Moderate',
                    'restaurants': 'Low',
                    'entertainment': 'Low'
                },
                'evening_peak': {
                    'transit': 'High',
                    'malls': 'High',
                    'restaurants': 'High',
                    'entertainment': 'Moderate'
                }
            },
            'seasonal_correlations': {
                'ramadan': {
                    'transit_usage': 'decreased',
                    'mall_footfall': 'decreased',
                    'restaurant_activity': 'shifted',
                    'note': 'Late-night shopping increases'
                },
                'festivals': {
                    'transit_usage': 'increased',
                    'attraction_activity': 'significantly_increased'
                }
            }
        }
        
        return jsonify({
            'time_range': time_range,
            'correlations': correlations,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error in correlation analysis: {str(e)}")
        return jsonify({'error': 'Failed to generate correlation analysis'}), 500

def generate_realtime_trends(metric):
    """Generate real-time trends (last 30 minutes)"""
    current_time = datetime.now()
    labels = []
    values = []
    
    for i in range(30):
        time_point = current_time - timedelta(minutes=29-i)
        labels.append(time_point.strftime('%H:%M'))
        
        # Simulate real-time values with some randomness
        base_value = {
            'passenger_count': 500,
            'delay_minutes': 2,
            'active_routes': 24
        }.get(metric, 500)
        
        value = base_value + np.random.randint(-50, 50)
        values.append(max(0, value))
    
    return {'labels': labels, 'values': values}

def generate_hourly_trends(metric):
    """Generate hourly trends (last 24 hours)"""
    current_time = datetime.now()
    labels = []
    values = []
    
    for i in range(24):
        time_point = current_time - timedelta(hours=23-i)
        labels.append(time_point.strftime('%H:00'))
        
        # Simulate hourly patterns
        hour = time_point.hour
        base_multiplier = 1.0
        if 7 <= hour <= 9 or 17 <= hour <= 19:  # Peak hours
            base_multiplier = 1.5
        elif 10 <= hour <= 16:  # Business hours
            base_multiplier = 1.2
        elif 22 <= hour or hour <= 6:  # Night hours
            base_multiplier = 0.6
        
        base_value = {
            'passenger_count': 800,
            'delay_minutes': 3,
            'active_routes': 24
        }.get(metric, 800)
        
        value = int(base_value * base_multiplier) + np.random.randint(-100, 100)
        values.append(max(0, value))
    
    return {'labels': labels, 'values': values}

def generate_daily_trends(metric):
    """Generate daily trends (last 7 days)"""
    labels = []
    values = []
    
    for i in range(7):
        date_point = datetime.now() - timedelta(days=6-i)
        labels.append(date_point.strftime('%m/%d'))
        
        # Simulate daily patterns (weekend vs weekday)
        is_weekend = date_point.weekday() >= 5
        base_multiplier = 1.3 if is_weekend else 1.0
        
        base_value = {
            'passenger_count': 50000,
            'delay_minutes': 2.5,
            'active_routes': 24
        }.get(metric, 50000)
        
        value = int(base_value * base_multiplier) + np.random.randint(-5000, 5000)
        values.append(max(0, value))
    
    return {'labels': labels, 'values': values}

def generate_weekly_trends(metric):
    """Generate weekly trends (last 4 weeks)"""
    labels = []
    values = []
    
    for i in range(4):
        week_point = datetime.now() - timedelta(weeks=3-i)
        labels.append(week_point.strftime('Week %d' % (i+1)))
        
        base_value = {
            'passenger_count': 350000,
            'delay_minutes': 2.8,
            'active_routes': 24
        }.get(metric, 350000)
        
        value = base_value + np.random.randint(-30000, 30000)
        values.append(max(0, value))
    
    return {'labels': labels, 'values': values}

def generate_monthly_trends(metric):
    """Generate monthly trends (last 12 months)"""
    labels = []
    values = []
    
    current_month = datetime.now().month
    for i in range(12):
        month_offset = 11 - i
        month = ((current_month - month_offset - 1) % 12) + 1
        year = datetime.now().year - (1 if month_offset >= current_month else 0)
        
        labels.append(f"{year}-{month:02d}")
        
        # Simulate monthly patterns with some seasonality
        seasonal_multiplier = 1.0
        if month in [12, 1, 2]:  # Holiday season
            seasonal_multiplier = 1.2
        elif month in [6, 7, 8]:  # School holidays
            seasonal_multiplier = 1.1
        
        base_value = {
            'passenger_count': 1500000,
            'delay_minutes': 3.0,
            'active_routes': 24
        }.get(metric, 1500000)
        
        value = int(base_value * seasonal_multiplier) + np.random.randint(-100000, 100000)
        values.append(max(0, value))
    
    return {'labels': labels, 'values': values}

def calculate_trend_statistics(values):
    """Calculate statistics for trend data"""
    if not values:
        return {}
    
    values_array = np.array(values)
    
    return {
        'avg_passengers': int(np.mean(values_array)),
        'peak_hours': int(np.max(values_array)),
        'min_value': int(np.min(values_array)),
        'avg_delay': round(np.mean(values_array) / 1000, 1) if max(values) > 1000 else round(np.mean(values_array), 1),
        'efficiency': round(100 - (np.std(values_array) / np.mean(values_array)) * 10, 1),
        'trend_direction': 'increasing' if values[-1] > values[0] else 'decreasing',
        'growth_rate': round(((values[-1] - values[0]) / values[0]) * 100, 1) if values[0] > 0 else 0
    }

def generate_weekday_patterns():
    """Generate weekday usage patterns"""
    return {
        'peak_morning': '07:30-09:30',
        'peak_evening': '17:30-19:30',
        'moderate_hours': '10:00-16:00',
        'low_hours': '20:00-06:00'
    }

def generate_weekend_patterns():
    """Generate weekend usage patterns"""
    return {
        'shopping_peak': '14:00-18:00',
        'dining_peak': '12:00-14:00, 19:00-21:00',
        'entertainment_peak': '20:00-23:00',
        'transit_moderate': 'Throughout day with evening peak'
    }