from database import engine, Base
from models import User, Choice

print("Creating tables...")

Base.metadata.create_all(bind=engine)

print("Finished!")