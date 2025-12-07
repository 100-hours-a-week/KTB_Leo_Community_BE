import os
import sys

# Add src to python path to allow imports from src
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, "src")
sys.path.append(src_dir)

from database.connection import engine
from database.orm import Base

def init_db():
    print("Initializing Database...")
    print("Target Database:", engine.url)
    
    print("Dropping all tables to ensure clean schema...")
    Base.metadata.drop_all(bind=engine)
    
    print("Creating all tables...")
    # This will create tables for all models imported above that inherit from Base
    Base.metadata.create_all(bind=engine)
    print("Database initialization completed successfully.")

if __name__ == "__main__":
    init_db()
