import logging
from fastapi import APIRouter, Depends, HTTPException, Form, Query
import requests
from sqlalchemy.orm import Session
from app.models.base import get_db
from app.crud.job import create_job, update_job, get_job_by_title, delete_job,get_job_by_id
from app.models.job import Job
from app.schemas.job import JobCreate, JobUpdate, JobOut

router = APIRouter()
logging.basicConfig(level=logging.INFO)


@router.post(
    "/create",
    response_model=JobOut,
    summary="Create a job vacancy",
    description="""Creates a new job vacancy in the system, with the option to parse data from hh.ru.  
    If a vacancy with the same title already exists, it returns an error.
    """,
    responses={
        201: {"description": "Job vacancy successfully created"},
        400: {"description": "Vacancy already exists"}
    },
)
async def create_vacancy(
        title: str = Form(..., description="Job title"),
        status: str = Form(..., description="Vacancy status"),
        company_name: str = Form(..., description="Company name"),
        company_address: str = Form(..., description="Company address"),
        logo_url: str = Form(..., description="Company logo"),
        description: str = Form(..., description="Job description"),
        db: Session = Depends(get_db)
):
    """
    **Create a job vacancy**
    - ❌ Returns an error if a vacancy with the same title already exists.
    """

    logging.info(f"✅ Attempting to create vacancy: {title}")

    # Check if a vacancy with this title already exists
    if get_job_by_title(db, title):
        logging.warning(f"❌ Vacancy with title {title} already exists")
        raise HTTPException(status_code=400, detail="Vacancy already exists")

    # Create a JobCreate object before passing it to create_job
    job_data = JobCreate(
        title=title,
        status=status,
        company_name=company_name,
        company_address=company_address,
        logo_url=logo_url,
        description=description
    )

    new_job = create_job(db, job_data)
    logging.info(f"✅ Вакансия {title} successfully created")

    return new_job


@router.put(
    "/update/{job_id}",
    response_model=JobOut,
    summary="Update a job vacancy",
    description="Updates job vacancy information by the given ID",
)
async def update_vacancy(
    job_id: int,
    title: str = Form(..., description="Job title"),
    status: str = Form(..., description="Vacancy status"),
    company_name: str = Form(..., description="Company name"),
    company_address: str = Form(..., description="Company address"),
    logo_url: str = Form(..., description="Company logo"),
    description: str = Form(..., description="Job description"),
    db: Session = Depends(get_db)
):
    """
    **Update a job vacancy**
    - 🔄 Updates job vacancy information.
    """

    logging.info(f"✅ Attempting to update vacancy with ID: {job_id}")

    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        logging.warning(f"❌ Vacancy with ID {job_id} not found")
        raise HTTPException(status_code=404, detail="Vacancy not found")

    job_data = JobUpdate(
        title=title,
        status=status,
        company_name=company_name,
        company_address=company_address,
        logo_url=logo_url,
        description=description
    )

    updated_job = update_job(db, job_id, job_data)
    logging.info(f"✅ Vacancy with ID {job_id} successfully updated")

    return updated_job


@router.get(
    "/get/{job_id}",
    response_model=JobOut,
    summary="Get a job vacancy",
    description="Retrieves job vacancy information by ID from the internal database",
)
async def get_vacancy(
        job_id: int,
        db: Session = Depends(get_db)
):
    """
    **Get a job vacancy**
    - 📄 Retrieves job vacancy information by its ID.
    """

    logging.info(f"✅ Attempting to retrieve vacancy with ID: {job_id}")

    job = get_job_by_id(db, job_id)
    if not job:
        logging.warning(f"❌ Vacancy with ID {job_id} not found")
        raise HTTPException(status_code=404, detail="Vacancy not found")

    return job


@router.delete(
    "/delete/{job_id}",
    summary="Delete a job vacancy",
    description="Deletes a job vacancy by the given ID",
)
async def delete_vacancy(
        job_id: int,
        db: Session = Depends(get_db)
):
    """
    **Delete a job vacancy**
    - ❌ Deletes a job vacancy by ID.
    """

    logging.info(f"✅ Attempting to delete vacancy with ID: {job_id}")

    job = get_job_by_id(db, job_id)
    if not job:
        logging.warning(f"❌ Vacancy with ID {job_id} not found")
        raise HTTPException(status_code=404, detail="Vacancy not found")

    delete_job(db, job_id)
    logging.info(f"✅ Vacancy with ID {job_id} successfully deleted")

    return {"message": "Vacancy successfully deleted"}



@router.post("/parse")
async def parse_vacancies(
        search_query: str = Query(..., description="Search query"),
        count: int = Query(10, description="Number of vacancies to fetch"),
        db: Session = Depends(get_db)
):
    """
    **Parse job vacancies from hh.ru**
    - 🔍 Retrieves vacancies based on the given search query.
    - 📥 Saves them to the database if they do not already exist.
    """

    hh_api_url = "https://api.hh.ru/vacancies"

    params = {"text": search_query, "per_page": count}
    response = requests.get(hh_api_url, params=params)

    if response.status_code != 200:
        logging.error("❌ API request to hh.ru failed")
        raise HTTPException(status_code=500, detail="Failed to fetch data from hh.ru")

    logging.info(f"✅ API request to hh.ru {hh_api_url} was successful")
    vacancies = response.json().get("items", [])

    added_count = 0
    for vacancy in vacancies:
        if not isinstance(vacancy, dict):
            continue

        employer = vacancy.get("employer")
        address = vacancy.get("address")

        title = vacancy.get("name", "Not specified")
        logo_url = employer["logo_urls"]["original"] if employer and employer.get("logo_urls") else ""
        company_name = employer["name"] if employer and employer.get("name") else "Not specified"
        company_address = address["city"] if address and address.get("city") else "Not specified"
        description = vacancy.get("description", "Description not available")
        status = vacancy["schedule"]["name"] if vacancy.get("schedule") and vacancy["schedule"].get("name") else "Not specified"

        if get_job_by_title(db, title):
            continue

        job_data = JobCreate(
            title=title,
            status=status,
            company_name=company_name,
            company_address=company_address,
            logo_url=logo_url,
            description=description
        )
        create_job(db, job_data)
        added_count += 1

    logging.info(f"✅ Vacancies added: {added_count}")
    return {"message": "Parsing completed", "added": added_count}
