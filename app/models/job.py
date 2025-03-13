from sqlalchemy import Column, Integer, String
from app.models.base import Base

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    created_at = Column(String)
    status = Column(String)
    company_name = Column(String)
    company_address = Column(String)
    logo_url = Column(String)
    description = Column(String)