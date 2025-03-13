import logging
from fastapi import APIRouter, Depends, HTTPException, Form
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
    summary="Создание вакансии",
    description="""Создаёт новую вакансию в системе, с возможностью парсинга данных с hh.ru.  
    Если вакансия с таким названием уже существует, возвращает ошибку.
    """,
    responses={
        201: {"description": "Вакансия успешно создана"},
        400: {"description": "Вакансия уже существует"}
    },
)
async def create_vacancy(
        title: str = Form(..., description="Название вакансии"),
        status: str = Form(..., description="Статус вакансии"),
        company_name: str = Form(..., description="Название компании"),
        company_address: str = Form(..., description="Адрес компании"),
        logo_url: str = Form(..., description="Логотип компании"),
        description: str = Form(..., description="Описание вакансии"),
        db: Session = Depends(get_db)
):
    """
    **Создание вакансии**
    - ❌ Возвращает ошибку, если вакансия с таким названием уже существует.
    """

    logging.info(f"✅ Попытка создать вакансию: {title}")

    # Проверяем, существует ли уже вакансия с таким названием
    if get_job_by_title(db, title):
        logging.warning(f"❌ Вакансия с названием {title} уже существует")
        raise HTTPException(status_code=400, detail="Vacancy already exists")

    # Создаем объект JobCreate перед передачей в create_job
    job_data = JobCreate(
        title=title,
        status=status,
        company_name=company_name,
        company_address=company_address,
        logo_url=logo_url,
        description=description
    )

    new_job = create_job(db, job_data)
    logging.info(f"✅ Вакансия {title} успешно создана")

    return new_job


@router.put(
    "/update/{job_id}",
    response_model=JobOut,
    summary="Обновление вакансии",
    description="Обновляет информацию о вакансии по заданному id",
)
async def update_vacancy(
    job_id: int,
    title: str = Form(..., description="Название вакансии"),
    status: str = Form(..., description="Статус вакансии"),
    company_name: str = Form(..., description="Название компании"),
    company_address: str = Form(..., description="Адрес компании"),
    logo_url: str = Form(..., description="Логотип компании"),
    description: str = Form(..., description="Описание вакансии"),
    db: Session = Depends(get_db)
):
    """
    **Обновление вакансии**
    - 🔄 Обновляет информацию о вакансии.
    """

    logging.info(f"✅ Попытка обновить вакансию с id: {job_id}")

    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        logging.warning(f"❌ Вакансия с id {job_id} не найдена")
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
    logging.info(f"✅ Вакансия с id {job_id} успешно обновлена")

    return updated_job


@router.get(
    "/get/{job_id}",
    response_model=JobOut,
    summary="Получение вакансии",
    description="Получает информацию о вакансии по id из внутренней БД",
)
async def get_vacancy(
        job_id: int,
        db: Session = Depends(get_db)
):
    """
    **Получение вакансии**
    - 📄 Получает информацию о вакансии по её id.
    """

    logging.info(f"✅ Попытка получить вакансию с id: {job_id}")

    job = get_job_by_id(db, job_id)
    if not job:
        logging.warning(f"❌ Вакансия с id {job_id} не найдена")
        raise HTTPException(status_code=404, detail="Vacancy not found")

    return job


@router.delete(
    "/delete/{job_id}",
    summary="Удаление вакансии",
    description="Удаляет вакансию по заданному id",
)
async def delete_vacancy(
        job_id: int,
        db: Session = Depends(get_db)
):
    """
    **Удаление вакансии**
    - ❌ Удаляет вакансию по id.
    """

    logging.info(f"✅ Попытка удалить вакансию с id: {job_id}")

    job = get_job_by_id(db, job_id)
    if not job:
        logging.warning(f"❌ Вакансия с id {job_id} не найдена")
        raise HTTPException(status_code=404, detail="Vacancy not found")

    delete_job(db, job_id)
    logging.info(f"✅ Вакансия с id {job_id} успешно удалена")

    return {"message": "Vacancy successfully deleted"}


