from sqlalchemy.orm import Session
from app.models.job import Job
from app.schemas.job import JobCreate, JobUpdate

def create_job(db: Session, job_data: JobCreate):
    db_job = Job(
        title=job_data.title,
        status=job_data.status,
        company_name=job_data.company_name,
        company_address=job_data.company_address,
        logo_url=job_data.logo_url,
        description=job_data.description
    )
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

def get_job_by_title(db: Session, job_title: str):
    return db.query(Job).filter(Job.title == job_title).first()

def get_job_by_id(db: Session, job_id: str):
    return db.query(Job).filter(Job.id == job_id).first()

def update_job(db: Session, job_id: int, job_data: JobUpdate):
    db.query(Job).filter(Job.id == job_id).update({
        Job.title: job_data.title,
        Job.status: job_data.status,
        Job.company_name: job_data.company_name,
        Job.company_address: job_data.company_address,
        Job.logo_url: job_data.logo_url,
        Job.description: job_data.description,
    })
    db.commit()

    db_job = db.query(Job).filter(Job.id == job_id).first()
    return db_job

def delete_job(db: Session, job_id: int):
    db_job = db.query(Job).filter(Job.id == job_id).first()
    if db_job:
        db.delete(db_job)
        db.commit()
        return db_job
    return None
