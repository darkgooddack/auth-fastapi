from pydantic import BaseModel
from typing import Optional

class JobCreate(BaseModel):
    title: str
    status: str
    company_name: str
    company_address: str
    logo_url: str
    description: str

    class Config:
        from_attributes = True

class JobUpdate(BaseModel):
    title: Optional[str] = None
    status: Optional[str] = None
    company_name: Optional[str] = None
    company_address: Optional[str] = None
    logo_url: Optional[str] = None
    description: Optional[str] = None

    class Config:
        from_attributes = True

class JobOut(BaseModel):
    id: int
    title: str
    status: str
    company_name: str
    company_address: str
    logo_url: str
    description: str

    class Config:
        from_attributes = True
