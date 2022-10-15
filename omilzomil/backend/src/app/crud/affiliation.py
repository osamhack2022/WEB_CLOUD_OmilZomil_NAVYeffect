from sqlalchemy.orm import Session
from app.models.affiliation import Affiliation


def create_affiliation(db: Session, affiliation_id: int, affiliation: str):
    affiliation = Affiliation(affiliation_id=affiliation_id, affiliation=affiliation)
    db.add(affiliation)
    db.commit()
    db.refresh(affiliation)
    return affiliation
