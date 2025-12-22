"""
Database Models using SQLAlchemy
File: src/database/models.py

All database tables and relationships
"""

from datetime import datetime
from sqlalchemy import (Column, Integer, String, Float, DateTime, Boolean, 
                       ForeignKey, Text, Date)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    """User profile and settings"""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)  # Added for login
    full_name = Column(String(100), nullable=False)  # Added full_name
    email = Column(String(120), unique=True)
    date_of_birth = Column(Date)  # Added for age calculation
    age = Column(Integer)
    gender = Column(String(20))
    height = Column(Float)  # in cm
    weight = Column(Float)  # in kg
    target_weight = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    health_records = relationship("HealthRecord", back_populates="user", cascade="all, delete-orphan")
    nutrition_logs = relationship("NutritionLog", back_populates="user", cascade="all, delete-orphan")
    activity_logs = relationship("ActivityLog", back_populates="user", cascade="all, delete-orphan")
    sleep_records = relationship("SleepRecord", back_populates="user", cascade="all, delete-orphan")
    water_intakes = relationship("WaterIntake", back_populates="user", cascade="all, delete-orphan")
    medications = relationship("Medication", back_populates="user", cascade="all, delete-orphan")
    health_goals = relationship("HealthGoal", back_populates="user", cascade="all, delete-orphan")
    achievements = relationship("Achievement", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(name='{self.full_name}', email='{self.email}')>"


class HealthRecord(Base):
    """Daily health metrics"""
    __tablename__ = 'health_records'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    recorded_at = Column(DateTime, default=datetime.utcnow)
    
    # Activity metrics
    steps = Column(Integer, default=0)
    calories_burned = Column(Integer, default=0)
    distance_km = Column(Float, default=0.0)
    
    # Vitals
    heart_rate = Column(Integer)  # bpm
    blood_pressure_systolic = Column(Integer)  # mmHg
    blood_pressure_diastolic = Column(Integer)  # mmHg
    blood_sugar = Column(Float)  # mg/dL
    
    # Sleep & Water
    sleep_hours = Column(Float)
    water_intake = Column(Integer)  # ml
    
    # Notes
    notes = Column(Text)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    user = relationship("User", back_populates="health_records")
    
    def __repr__(self):
        return f"<HealthRecord(user_id={self.user_id}, steps={self.steps})>"


class NutritionLog(Base):
    """Food and nutrition tracking"""
    __tablename__ = 'nutrition_logs'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    logged_at = Column(DateTime, default=datetime.utcnow)
    meal_type = Column(String(20))  # breakfast, lunch, dinner, snack
    
    # Food details
    food_name = Column(String(200), nullable=False)
    food_description = Column(Text)
    serving_size = Column(String(50))
    
    # Nutrition facts (grams)
    calories = Column(Float)
    protein = Column(Float)
    carbs = Column(Float)  # Shortened from carbohydrates
    fats = Column(Float)   # Shortened from fat
    fiber = Column(Float)
    sugar = Column(Float)
    
    # Image
    food_image_path = Column(String(500))
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    user = relationship("User", back_populates="nutrition_logs")
    
    def __repr__(self):
        return f"<NutritionLog(food='{self.food_name}', calories={self.calories})>"


class ActivityLog(Base):
    """Physical activity and exercise tracking"""
    __tablename__ = 'activity_logs'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    activity_date = Column(DateTime, default=datetime.utcnow)
    
    # Activity details
    activity_type = Column(String(50), nullable=False)  # walking, running, cycling
    duration_minutes = Column(Integer)
    distance_km = Column(Float)
    calories_burned = Column(Integer)
    
    # Metrics
    avg_heart_rate = Column(Integer)
    max_heart_rate = Column(Integer)
    steps = Column(Integer)
    
    # Notes
    notes = Column(Text)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    user = relationship("User", back_populates="activity_logs")
    
    def __repr__(self):
        return f"<ActivityLog(type='{self.activity_type}', duration={self.duration_minutes}min)>"


class SleepRecord(Base):
    """Sleep tracking"""
    __tablename__ = 'sleep_records'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    # Sleep timing
    sleep_start = Column(DateTime, nullable=False)
    sleep_end = Column(DateTime, nullable=False)
    duration_hours = Column(Float)
    
    # Sleep quality
    quality_score = Column(Integer)  # 0-100
    deep_sleep_hours = Column(Float)
    rem_sleep_hours = Column(Float)
    light_sleep_hours = Column(Float)
    
    # Notes
    notes = Column(Text)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    user = relationship("User", back_populates="sleep_records")
    
    def __repr__(self):
        return f"<SleepRecord(duration={self.duration_hours}h, quality={self.quality_score})>"


class WaterIntake(Base):
    """Water intake tracking"""
    __tablename__ = 'water_intakes'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    logged_at = Column(DateTime, default=datetime.utcnow)
    amount_ml = Column(Integer)  # milliliters
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    user = relationship("User", back_populates="water_intakes")
    
    def __repr__(self):
        return f"<WaterIntake(amount={self.amount_ml}ml)>"


class Medication(Base):
    """Medication tracking"""
    __tablename__ = 'medications'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    # Medication details
    name = Column(String(100), nullable=False)
    dosage = Column(String(50))
    frequency = Column(String(50))  # daily, twice daily, etc.
    
    # Timing
    start_date = Column(Date)
    end_date = Column(Date)
    reminder_time = Column(String(10))  # HH:MM
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Notes
    notes = Column(Text)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    user = relationship("User", back_populates="medications")
    
    def __repr__(self):
        return f"<Medication(name='{self.name}', dosage='{self.dosage}')>"


class HealthGoal(Base):
    """User health goals"""
    __tablename__ = 'health_goals'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    # Goal details
    goal_type = Column(String(50), nullable=False)  # weight, steps, water, etc.
    title = Column(String(100))
    description = Column(Text)
    
    # Targets
    target_value = Column(Float)
    current_value = Column(Float, default=0)
    unit = Column(String(20))  # kg, steps, ml
    
    # Timing
    start_date = Column(Date)
    deadline = Column(Date)
    
    # Status
    status = Column(String(20), default='Active')  # Active, Completed, Paused
    progress_percentage = Column(Float, default=0)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    user = relationship("User", back_populates="health_goals")
    
    def __repr__(self):
        return f"<HealthGoal(type='{self.goal_type}', target={self.target_value})>"


class Achievement(Base):
    """User achievements and badges"""
    __tablename__ = 'achievements'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    # Achievement details
    achievement_type = Column(String(50))  # steps_milestone, weight_goal, streak
    title = Column(String(100))
    description = Column(Text)
    icon = Column(String(50))
    
    # Stats
    earned_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    user = relationship("User", back_populates="achievements")
    
    def __repr__(self):
        return f"<Achievement(type='{self.achievement_type}', title='{self.title}')>"


# Helper functions
def create_tables(engine):
    """Create all database tables"""
    Base.metadata.create_all(engine)
    print("✓ Database tables created successfully!")


def drop_tables(engine):
    """Drop all database tables"""
    Base.metadata.drop_all(engine)
    print("✓ Database tables dropped!")