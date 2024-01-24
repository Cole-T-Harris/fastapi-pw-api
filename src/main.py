from fastapi import FastAPI #, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
# from sqlalchemy.orm import Session

from . import models #, schemas, crud
from .database import engine
# from .dependencies import get_db

models.Base.metadata.create_all(bind=engine)

from src.api.api import api_router

app = FastAPI()

# Configure CORS
origins = [
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

# Not needed for productions
# @app.post("/thumbnails/", response_model=schemas.Thumbnail)
# def create_thumbnail(thumbnail: schemas.ThumbnailCreate, db: Session = Depends(get_db)):
#     db_thumbnail = crud.get_thumbnails_by_branch(db, branch=thumbnail.branch)
#     if db_thumbnail:
#         raise HTTPException(status_code=400, detail="Thumbnail already exists")
#     return crud.create_thumbnail(db=db, thumbnail=thumbnail)


# @app.get("/thumbnails/{branch}", response_model=schemas.Thumbnail)
# def read_thumbnail(branch: str, db: Session = Depends(get_db)):
#     db_thumbnail = crud.get_thumbnails_by_branch(db, branch=branch)
#     if db_thumbnail is None:
#         raise HTTPException(status_code=404, detail="Thumbnail not found")
#     return db_thumbnail