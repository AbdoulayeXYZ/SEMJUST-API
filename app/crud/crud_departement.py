from typing import List, Optional
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.departement import Departement
from app.schemas.departement import DepartementCreate, DepartementUpdate

class CRUDDepartement(CRUDBase[Departement, DepartementCreate, DepartementUpdate]):
    def get_by_code(self, db: Session, *, code: str) -> Optional[Departement]:
        return db.query(Departement).filter(Departement.code == code).first()

    def get_multi_by_region(
        self, db: Session, *, region_id: int, skip: int = 0, limit: int = 100
    ) -> List[Departement]:
        return (
            db.query(Departement)
            .filter(Departement.region_id == region_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def count_by_region(self, db: Session, *, region_id: int) -> int:
        return db.query(Departement).filter(Departement.region_id == region_id).count()

    def get_multi_by_population(
        self, db: Session, *, min_population: int = 0, skip: int = 0, limit: int = 100
    ) -> List[Departement]:
        return (
            db.query(Departement)
            .filter(Departement.population >= min_population)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_multi_by_superficie(
        self, db: Session, *, min_superficie: float = 0, skip: int = 0, limit: int = 100
    ) -> List[Departement]:
        return (
            db.query(Departement)
            .filter(Departement.superficie >= min_superficie)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_multi_by_pluviometrie(
        self, db: Session, *, min_pluviometrie: float = 0, skip: int = 0, limit: int = 100
    ) -> List[Departement]:
        return (
            db.query(Departement)
            .filter(Departement.pluviometrie_moyenne >= min_pluviometrie)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_multi_by_temperature(
        self, db: Session, *, min_temperature: float = 0, skip: int = 0, limit: int = 100
    ) -> List[Departement]:
        return (
            db.query(Departement)
            .filter(Departement.temperature_moyenne >= min_temperature)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_multi_by_irrigation(
        self, db: Session, *, irrigation: bool, skip: int = 0, limit: int = 100
    ) -> List[Departement]:
        return (
            db.query(Departement)
            .filter(Departement.irrigation == irrigation)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_multi_by_type_sol(
        self, db: Session, *, type_sol: str, skip: int = 0, limit: int = 100
    ) -> List[Departement]:
        return (
            db.query(Departement)
            .filter(Departement.type_sol == type_sol)
            .offset(skip)
            .limit(limit)
            .all()
        )

departement = CRUDDepartement(Departement) 