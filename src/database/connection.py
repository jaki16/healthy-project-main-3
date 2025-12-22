"""
Database Connection Manager
Handles SQLite database initialization and operations
"""
import os
from pathlib import Path
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

# IMPORTANT: Use relative import to avoid circular import
from .models import (
    Base, User, HealthRecord, NutritionLog, 
    ActivityLog, SleepRecord, WaterIntake, 
    Medication, HealthGoal, Achievement
)

# Database configuration
DATABASE_DIR = Path(__file__).parent.parent.parent / "data"
DATABASE_PATH = DATABASE_DIR / "healthtrack.db"
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

# Create engine and session
engine = None
SessionLocal = None


def init_database():
    """Initialize database connection and create tables"""
    global engine, SessionLocal
    
    try:
        # Create data directory if not exists
        DATABASE_DIR.mkdir(parents=True, exist_ok=True)
        
        # Create engine
        engine = create_engine(
            DATABASE_URL,
            connect_args={"check_same_thread": False},
            echo=False  # Set to True for SQL debugging
        )
        
        # Create session factory
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        
        print(f"✓ Database connected: {DATABASE_PATH}")
        print("✓ Database tables created!")
        
        return True
        
    except Exception as e:
        print(f"❌ Database initialization error: {e}")
        return False


def get_db() -> Session:
    """Get database session"""
    if SessionLocal is None:
        init_database()
    
    db = SessionLocal()
    try:
        return db
    except Exception as e:
        print(f"❌ Session error: {e}")
        db.close()
        raise


def add_sample_data():
    """Add sample data for testing"""
    db = get_db()
    
    try:
        # Check if user already exists
        existing_user = db.query(User).filter_by(email="john.doe@example.com").first()
        if existing_user:
            print("✓ Sample data already exists!")
            return
        
        # Create sample user
        user = User(
            email="john.doe@example.com",
            username="johndoe",
            full_name="John Doe",
            date_of_birth=datetime(1990, 1, 1),
            gender="Male",
            height=175.0,
            weight=75.0,
            target_weight=70.0
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        
        # Add health record
        health_record = HealthRecord(
            user_id=user.id,
            steps=5420,
            calories_burned=217,
            heart_rate=72,
            sleep_hours=7.5,
            water_intake=2000
        )
        db.add(health_record)
        
        # Add nutrition log
        nutrition = NutritionLog(
            user_id=user.id,
            meal_type="Breakfast",
            food_name="Oatmeal with Banana",
            calories=350,
            protein=12.0,
            carbs=60.0,
            fats=8.0
        )
        db.add(nutrition)
        
        # Add activity log
        activity = ActivityLog(
            user_id=user.id,
            activity_type="Walking",
            duration_minutes=30,
            calories_burned=150,
            distance_km=2.5
        )
        db.add(activity)
        
        # Add sleep record
        sleep = SleepRecord(
            user_id=user.id,
            sleep_start=datetime.now().replace(hour=22, minute=0),
            sleep_end=datetime.now().replace(hour=6, minute=30),
            duration_hours=7.5,
            quality_score=85
        )
        db.add(sleep)
        
        # Add water intake
        water = WaterIntake(
            user_id=user.id,
            amount_ml=2000
        )
        db.add(water)
        
        # Add health goal
        goal = HealthGoal(
            user_id=user.id,
            goal_type="Weight Loss",
            target_value=70.0,
            current_value=75.0,
            deadline=datetime.now() + timedelta(days=90),
            status="Active"
        )
        db.add(goal)
        
        db.commit()
        print("✓ Sample data added!")
        
    except Exception as e:
        print(f"❌ Error adding sample data: {e}")
        db.rollback()
    finally:
        db.close()


def check_database():
    """Check database status and content"""
    db = get_db()
    
    try:
        # Count records
        user_count = db.query(User).count()
        health_count = db.query(HealthRecord).count()
        nutrition_count = db.query(NutritionLog).count()
        
        print(f"\n📊 Database Statistics:")
        print(f"   👤 Users: {user_count}")
        print(f"   📈 Health Records: {health_count}")
        print(f"   🍎 Nutrition Logs: {nutrition_count}")
        
        # Get latest user
        if user_count > 0:
            user = db.query(User).first()
            print(f"\n👤 Latest User:")
            print(f"   Name: {user.full_name}")
            print(f"   Email: {user.email}")
            print(f"   Weight: {user.weight} kg")
            
        return True
        
    except Exception as e:
        print(f"❌ Database check error: {e}")
        return False
    finally:
        db.close()


def get_user_stats(user_id: int):
    """Get user statistics"""
    db = get_db()
    
    try:
        user = db.query(User).filter_by(id=user_id).first()
        if not user:
            return None
        
        # Get latest health record
        latest_health = db.query(HealthRecord).filter_by(user_id=user_id).order_by(
            HealthRecord.recorded_at.desc()
        ).first()
        
        # Calculate total steps this month
        month_start = datetime.now().replace(day=1, hour=0, minute=0, second=0)
        monthly_records = db.query(HealthRecord).filter(
            HealthRecord.user_id == user_id,
            HealthRecord.recorded_at >= month_start
        ).all()
        
        total_steps = sum(record.steps for record in monthly_records)
        
        stats = {
            'user': user,
            'latest_health': latest_health,
            'monthly_steps': total_steps,
            'monthly_records_count': len(monthly_records)
        }
        
        return stats
        
    except Exception as e:
        print(f"❌ Error getting stats: {e}")
        return None
    finally:
        db.close()