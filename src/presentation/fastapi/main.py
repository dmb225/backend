import logging
from collections.abc import Iterator
from typing import Annotated, Any

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from src.logging_config import setup_logging
from src.presentation.fastapi import crud, schemas
from src.presentation.fastapi.database import SessionLocal

setup_logging()

logger = logging.getLogger(__name__)
app = FastAPI()
logger.info("FastAPI app initialization..")


def get_db() -> Iterator[Session]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def docs_redirect() -> RedirectResponse:
    return RedirectResponse(url="/docs")


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/users/", response_model=list[schemas.User])
def read_users(
    db: Annotated[Session, Depends(get_db)],
    skip: int = 0,
    limit: int = 100,
) -> Any:
    return crud.get_users(db, skip=skip, limit=limit)


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Annotated[Session, Depends(get_db)]) -> Any:
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.get("/users/email/{user_email}", response_model=schemas.User)
def read_user_by_email(user_email: str, db: Annotated[Session, Depends(get_db)]) -> Any | None:
    db_user = crud.get_user_by_email(db, email=user_email)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Annotated[Session, Depends(get_db)]) -> Any:
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.put("/users/", response_model=schemas.User)
def update_user(user: schemas.UserCreate, db: Annotated[Session, Depends(get_db)]) -> Any:
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        return crud.update_user(db=db, user=user)
    raise HTTPException(status_code=400, detail="User not Found")


@app.delete("/users/{user_id}", response_model=schemas.User)
def delete_user(user_id: int, db: Annotated[Session, Depends(get_db)]) -> Any:
    db_user = crud.delete_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
