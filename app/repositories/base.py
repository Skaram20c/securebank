from sqlalchemy.orm import Session

class BaseRepository:
    def __init__(self, model):
        self.model = model

    def get_by_id(self, db: Session, id: int):
        return db.query(self.model).get(id)

    def get_all(self, db: Session):
        return db.query(self.model).all()
