import logging
from datetime import datetime, timedelta
from collections import defaultdict
import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)

class TemporalProcessor:
    """Service for processing temporal/spatio-temporal data"""
    
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def process_time_series(self, data, time_column, value_column):
        """Process time series data for trend analysis"""
        try:
            # Convert to DataFrame for easier processing
            df = pd.DataFrame(data)
            df[time_column] = pd.to_datetime(df[time_column])
            df = df.sort_values(time_column)
            
            # Calculate basic statistics
            result = {
                'data_points': len(df),
                'time_range': {
                    'start': df[time_column].min().isoformat(),
                    'end': df[time_column].max().isoformat()
                },
                'statistics': {
                    'mean': float(df[value_column].mean()),
                    'median': float(df[value_column].median()),
                    'std': float(df[value_column].std()),
                    'min': float(df[value_column].min()),
                    'max': float(df[value_column].max()),
                },
                'trend': self._calculate_trend(df[time_column], df[value_column])
            }
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error processing time series: {e}")
            return None
    
    def _calculate_trend(self, time_series, values):
        """Calculate trend direction and strength"""
        try:
            # Simple linear regression to determine trend
            x = np.arange(len(values))
            slope = np.polyfit(x, values, 1)[0]
            
            if abs(slope) < 0.01:
                trend = 'stable'
            elif slope > 0:
                trend = 'increasing'
            else:
                trend = 'decreasing'
            
            return {
                'direction': trend,
                'strength': abs(slope),
                'slope': float(slope)
            }
            
        except Exception as e:
            self.logger.error(f"Error calculating trend: {e}")
            return {'direction': 'unknown', 'strength': 0, 'slope': 0}
    
    def calculate_peak_hours(self, data, time_column, value_column):
        """Calculate peak hours from time series data"""
        try:
            df = pd.DataFrame(data)
            df[time_column] = pd.to_datetime(df[time_column])
            df['hour'] = df[time_column].dt.hour
            
            # Group by hour and calculate average values
            hourly_avg = df.groupby('hour')[value_column].mean().sort_values(ascending=False)
            
            # Find peak hours (top 20% of hours)
            peak_threshold = hourly_avg.quantile(0.8)
            peak_hours = hourly_avg[hourly_avg >= peak_threshold]
            
            return {
                'peak_hours': peak_hours.index.tolist(),
                'peak_values': peak_hours.values.tolist(),
                'threshold': float(peak_threshold),
                'total_hours_analyzed': len(hourly_avg)
            }
            
        except Exception as e:
            self.logger.error(f"Error calculating peak hours: {e}")
            return {'peak_hours': [], 'peak_values': [], 'threshold': 0, 'total_hours_analyzed': 0}
    
    def generate_temporal_features(self, timestamp):
        """Generate temporal features from a timestamp"""
        try:
            dt = datetime.fromisoformat(timestamp) if isinstance(timestamp, str) else timestamp
            
            return {
                'hour': dt.hour,
                'day_of_week': dt.weekday(),
                'month': dt.month,
                'quarter': (dt.month - 1) // 3 + 1,
                'is_weekend': dt.weekday() >= 5,
                'is_business_hour': 9 <= dt.hour <= 17,
                'is_peak_hour': (7 <= dt.hour <= 9) or (17 <= dt.hour <= 19)
            }
            
        except Exception as e:
            self.logger.error(f"Error generating temporal features: {e}")
            return {}
    
    def aggregate_by_period(self, data, time_column, value_column, period='hour'):
        """Aggregate data by time period"""
        try:
            df = pd.DataFrame(data)
            df[time_column] = pd.to_datetime(df[time_column])
            
            if period == 'hour':
                df['period'] = df[time_column].dt.floor('H')
            elif period == 'day':
                df['period'] = df[time_column].dt.floor('D')
            elif period == 'week':
                df['period'] = df[time_column].dt.floor('W')
            elif period == 'month':
                df['period'] = df[time_column].dt.floor('M')
            else:
                raise ValueError(f"Unsupported period: {period}")
            
            # Aggregate values
            grouped = df.groupby('period')[value_column].agg(['mean', 'sum', 'count']).reset_index()
            grouped['period'] = grouped['period'].dt.isoformat()
            
            return grouped.to_dict('records')
            
        except Exception as e:
            self.logger.error(f"Error aggregating by {period}: {e}")
            return []
    
    def detect_anomalies(self, data, value_column, threshold=2.0):
        """Detect anomalies in time series data using z-score"""
        try:
            if not data or len(data) < 3:
                return []
            
            values = [item[value_column] for item in data]
            mean_val = np.mean(values)
            std_val = np.std(values)
            
            anomalies = []
            for i, item in enumerate(data):
                z_score = abs((item[value_column] - mean_val) / std_val) if std_val > 0 else 0
                if z_score > threshold:
                    anomalies.append({
                        'index': i,
                        'value': item[value_column],
                        'z_score': z_score,
                        'timestamp': item.get('timestamp', ''),
                        'anomaly_type': 'high' if item[value_column] > mean_val else 'low'
                    })
            
            return anomalies
            
        except Exception as e:
            self.logger.error(f"Error detecting anomalies: {e}")
            return []