from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User, engine, Base  # Ensure you import your engine and Base

# Create a Session class and a session instance
Session = sessionmaker(bind=engine)

def seed_data():
    session = Session()  # Create a new session instance
    
    # Example seed data
    user1 = User(name="Anne", email="anne@gmail.com", password="12345")
    user2 = User(name="Garvin", email="garvin@gmail.com", password="67890")

    session.add(user1)
    session.add(user2)
    
    session.commit()  # Commit the changes to the database
    session.close()   # Close the session

if __name__ == "__main__":
    Base.metadata.create_all(engine)  # Create tables if they don't exist
    seed_data()
