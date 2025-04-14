from app.models.place import Place
from app import db
from app.persistence.repository import SQLAlchemyRepository

class PlaceRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Place)

    def get_place_by_latitude(self, latitude):
        return self.model.query.filter_by(latitude=latitude).first()

    def get_place_by_longitude(self, longitude):
        return self.model.query.filter_by(longitude=longitude).first()

