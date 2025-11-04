from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class TransitStation(db.Model):
    """Model for transit stations"""
    __tablename__ = 'transit_stations'
    
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    line = db.Column(db.String(100), nullable=False)
    station_type = db.Column(db.String(50))  # lrt, mrt, brt, ktm
    status = db.Column(db.String(50), default='operational')
    facilities = db.Column(db.Text)  # JSON array of facilities
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Real-time data (separate table for performance)
    real_time_data = db.relationship('TransitRealTime', backref='station', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'line': self.line,
            'station_type': self.station_type,
            'status': self.status,
            'facilities': json.loads(self.facilities) if self.facilities else [],
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class TransitRealTime(db.Model):
    """Model for real-time transit data"""
    __tablename__ = 'transit_realtime'
    
    id = db.Column(db.Integer, primary_key=True)
    station_id = db.Column(db.String(50), db.ForeignKey('transit_stations.id'), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    passenger_count = db.Column(db.Integer, default=0)
    delay_minutes = db.Column(db.Float, default=0)
    next_arrival = db.Column(db.String(50))
    occupancy_percentage = db.Column(db.Float, default=0)
    
    def to_dict(self):
        return {
            'id': self.id,
            'station_id': self.station_id,
            'timestamp': self.timestamp.isoformat(),
            'passenger_count': self.passenger_count,
            'delay_minutes': self.delay_minutes,
            'next_arrival': self.next_arrival,
            'occupancy_percentage': self.occupancy_percentage
        }

class Attraction(db.Model):
    """Model for attractions"""
    __tablename__ = 'attractions'
    
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    address = db.Column(db.Text)
    rating = db.Column(db.Float)
    operating_hours = db.Column(db.String(200))
    facilities = db.Column(db.Text)  # JSON array of facilities
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Real-time data
    real_time_data = db.relationship('AttractionRealTime', backref='attraction', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'address': self.address,
            'rating': self.rating,
            'operating_hours': self.operating_hours,
            'facilities': json.loads(self.facilities) if self.facilities else [],
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class AttractionRealTime(db.Model):
    """Model for real-time attraction data"""
    __tablename__ = 'attraction_realtime'
    
    id = db.Column(db.Integer, primary_key=True)
    attraction_id = db.Column(db.String(50), db.ForeignKey('attractions.id'), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    popularity_score = db.Column(db.Integer, default=50)  # 0-100
    current_occupancy = db.Column(db.Float, default=0)  # 0-100
    estimated_wait_time = db.Column(db.Integer, default=0)  # minutes
    
    def to_dict(self):
        return {
            'id': self.id,
            'attraction_id': self.attraction_id,
            'timestamp': self.timestamp.isoformat(),
            'popularity_score': self.popularity_score,
            'current_occupancy': self.current_occupancy,
            'estimated_wait_time': self.estimated_wait_time
        }

class TransitRoute(db.Model):
    """Model for transit routes"""
    __tablename__ = 'transit_routes'
    
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    route_type = db.Column(db.String(50), nullable=False)  # lrt, mrt, brt, ktm
    status = db.Column(db.String(50), default='operational')
    frequency = db.Column(db.String(50))  # e.g., "3-5 min"
    operating_hours = db.Column(db.String(100))
    station_ids = db.Column(db.Text)  # JSON array of station IDs
    coordinates = db.Column(db.Text)  # JSON array of coordinate pairs
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'route_type': self.route_type,
            'status': self.status,
            'frequency': self.frequency,
            'operating_hours': self.operating_hours,
            'station_ids': json.loads(self.station_ids) if self.station_ids else [],
            'coordinates': json.loads(self.coordinates) if self.coordinates else [],
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class TrendAnalysis(db.Model):
    """Model for trend analysis data"""
    __tablename__ = 'trend_analysis'
    
    id = db.Column(db.Integer, primary_key=True)
    entity_type = db.Column(db.String(50), nullable=False)  # station, attraction, route
    entity_id = db.Column(db.String(50), nullable=False)
    time_period = db.Column(db.String(50), nullable=False)  # hour, day, week, month
    metric_type = db.Column(db.String(50), nullable=False)  # passenger_count, popularity_score, etc.
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    value = db.Column(db.Float, nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'entity_type': self.entity_type,
            'entity_id': self.entity_id,
            'time_period': self.time_period,
            'metric_type': self.metric_type,
            'timestamp': self.timestamp.isoformat(),
            'value': self.value
        }

def init_db():
    """Initialize database tables"""
    try:
        db.create_all()
        print("Database tables created successfully")
    except Exception as e:
        print(f"Error creating database tables: {e}")