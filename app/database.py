import psycopg2
from psycopg2.extras import RealDictCursor
from config import settings


def get_db():
    conn = psycopg2.connect(settings.database_url, cursor_factory=RealDictCursor)
    return conn
