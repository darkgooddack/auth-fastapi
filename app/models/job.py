import pytz
from sqlalchemy import Column, Integer, String, DateTime
from app.models.base import Base
from datetime import datetime

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.now(pytz.timezone('Europe/Moscow')), nullable=False)
    status = Column(String)
    company_name = Column(String)
    company_address = Column(String)
    logo_url = Column(String)
    description = Column(String)