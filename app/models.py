from datetime import datetime

from sqlalchemy import Column, DateTime, Float, Integer, String

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(String, unique=True, index=True, nullable=False)

    email = Column(String, unique=True, index=True, nullable=False)

    password_hash = Column(String, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)


class Calculation(Base):
    __tablename__ = "calculations"

    id = Column(Integer, primary_key=True, index=True)

    a = Column(Float, nullable=False)

    b = Column(Float, nullable=False)

    type = Column(String, nullable=False)

    result = Column(Float, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)