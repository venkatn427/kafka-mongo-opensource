# Superset config overrides

from superset.config import *

# Database connection string
SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://superset:superset@postgres:5432/superset'

# Enable Flask debug if needed
DEBUG = True

# Secret Key (should match env SUPERSET_SECRET_KEY)
SECRET_KEY = 'supersecretkey'

# Add any other custom config here
