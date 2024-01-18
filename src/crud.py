from sqlalchemy.orm import Session

from . import models, schemas

def get_thumbnails_by_branch(db: Session, branch: str):
    return db.query(models.Thumbnail).filter(models.Thumbnail.branch == branch).first()

# Not needed for production
# def create_thumbnail(db: Session, thumbnail: schemas.ThumbnailCreate):
#     db_thumbnail = models.Thumbnail(branch=thumbnail.branch, url=thumbnail.url)
#     db.add(db_thumbnail)
#     db.commit()
#     db.refresh(db_thumbnail)
#     return db_thumbnail