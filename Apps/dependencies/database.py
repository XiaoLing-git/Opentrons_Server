from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import redis

SQLALCHEMY_DATABASE_URL = "sqlite:///./Apps.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()




redis_host = "127.0.0.1"
redis_port = "6379"
redis_poor = redis.ConnectionPool(host = redis_host, port = redis_port)
redis_instance = redis.Redis(connection_pool=redis_poor,decode_responses=True)