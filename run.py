from app import app
from db import db

db.init_app(app)

# Create DB Tables
@app.before_first_request
def create_table():
  db.create_all()