from typing import List, Optional
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.region import Region
from app.schemas.region import RegionCreate, RegionUpdate

class CRUDRegion(CRUDBase[Region, RegionCreate, RegionUpdate]):
    def get_by_code(self, db: Session, *, code: str) -> Optional[Region]:
        return db.query(Region).filter(Region.code == code).first()

    def get_multi_by_population(
        self, db: Session, *, min_population: int = 0, skip: int = 0, limit: int = 100
    ) -> List[Region]:
        return (
            db.query(Region)
            .filter(Region.population >= min_population)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_multi_by_superficie(
        self, db: Session, *, min_superficie: float = 0, skip: int = 0, limit: int = 100
    ) -> List[Region]:
        return (
            db.query(Region)
            .filter(Region.superficie >= min_superficie)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_multi_by_pluviometrie(
        self, db: Session, *, min_pluviometrie: float = 0, skip: int = 0, limit: int = 100
    ) -> List[Region]:
        return (
            db.query(Region)
            .filter(Region.pluviometrie_moyenne >= min_pluviometrie)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_multi_by_temperature(
        self, db: Session, *, min_temperature: float = 0, skip: int = 0, limit: int = 100
    ) -> List[Region]:
        return (
            db.query(Region)
            .filter(Region.temperature_moyenne >= min_temperature)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_multi_by_irrigation(
        self, db: Session, *, irrigation: bool, skip: int = 0, limit: int = 100
    ) -> List[Region]:
        return (
            db.query(Region)
            .filter(Region.irrigation == irrigation)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_multi_by_type_sol(
        self, db: Session, *, type_sol: str, skip: int = 0, limit: int = 100
    ) -> List[Region]:
        return (
            db.query(Region)
            .filter(Region.type_sol == type_sol)
            .offset(skip)
            .limit(limit)
            .all()
        )

region = CRUDRegion(Region) 