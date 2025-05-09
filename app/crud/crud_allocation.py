from typing import List, Optional, Dict, Any, Union
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime

from app.crud.base import CRUDBase
from app.models.allocation import Allocation, TypeSemence
from app.schemas.allocation import AllocationCreate, AllocationUpdate, AllocationSummary

class CRUDAllocation(CRUDBase[Allocation, AllocationCreate, AllocationUpdate]):
    def create_with_metadata(
        self, db: Session, *, obj_in: AllocationCreate, created_by: str
    ) -> Allocation:
        obj_in_data = obj_in.dict()
        obj_in_data["created_by"] = created_by
        obj_in_data["updated_by"] = created_by
        db_obj = Allocation(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update_with_metadata(
        self,
        db: Session,
        *,
        db_obj: Allocation,
        obj_in: Union[AllocationUpdate, Dict[str, Any]],
        updated_by: str
    ) -> Allocation:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        update_data["updated_by"] = updated_by
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def get_multi_by_annee(
        self, db: Session, *, annee: int, skip: int = 0, limit: int = 100
    ) -> List[Allocation]:
        return (
            db.query(Allocation)
            .filter(Allocation.annee == annee)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_multi_by_type_semence(
        self, db: Session, *, type_semence: TypeSemence, skip: int = 0, limit: int = 100
    ) -> List[Allocation]:
        return (
            db.query(Allocation)
            .filter(Allocation.type_semence == type_semence)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_multi_by_region(
        self, db: Session, *, region_id: int, skip: int = 0, limit: int = 100
    ) -> List[Allocation]:
        return (
            db.query(Allocation)
            .filter(Allocation.region_id == region_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_multi_by_departement(
        self, db: Session, *, departement_id: int, skip: int = 0, limit: int = 100
    ) -> List[Allocation]:
        return (
            db.query(Allocation)
            .filter(Allocation.departement_id == departement_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_summary(self, db: Session, *, annee: int) -> AllocationSummary:
        # Calculer les totaux
        total_quantite = db.query(func.sum(Allocation.quantite)).filter(
            Allocation.annee == annee
        ).scalar() or 0

        nombre_allocations = db.query(func.count(Allocation.id)).filter(
            Allocation.annee == annee
        ).scalar() or 0

        # Répartition par type de semence
        repartition_type_semence = {}
        for type_sem in TypeSemence:
            quantite = db.query(func.sum(Allocation.quantite)).filter(
                Allocation.annee == annee,
                Allocation.type_semence == type_sem
            ).scalar() or 0
            repartition_type_semence[type_sem.value] = quantite

        # Répartition par région
        repartition_region = {}
        regions = db.query(Allocation.region_id, func.sum(Allocation.quantite)).filter(
            Allocation.annee == annee
        ).group_by(Allocation.region_id).all()
        for region_id, quantite in regions:
            repartition_region[region_id] = quantite

        # Répartition par département
        repartition_departement = {}
        departements = db.query(Allocation.departement_id, func.sum(Allocation.quantite)).filter(
            Allocation.annee == annee
        ).group_by(Allocation.departement_id).all()
        for departement_id, quantite in departements:
            repartition_departement[departement_id] = quantite

        return AllocationSummary(
            annee=annee,
            total_quantite=total_quantite,
            nombre_allocations=nombre_allocations,
            repartition_type_semence=repartition_type_semence,
            repartition_region=repartition_region,
            repartition_departement=repartition_departement
        )

    def optimize_allocations(
        self,
        db: Session,
        *,
        annee: int,
        type_semence: TypeSemence,
        quantite_totale: float,
        created_by: str
    ) -> List[Allocation]:
        """
        Optimise les allocations en fonction des facteurs d'influence.
        Cette méthode utilise un algorithme simple basé sur les facteurs d'influence
        pour distribuer les semences de manière équitable.
        """
        # Récupérer tous les départements avec leurs facteurs d'influence
        departements = db.query(Departement).all()
        
        # Calculer le score total pour la normalisation
        total_score = sum(
            sum(dept.facteurs_influence.values()) for dept in departements
        )
        
        # Créer les allocations optimisées
        allocations = []
        for dept in departements:
            # Calculer le score du département
            dept_score = sum(dept.facteurs_influence.values())
            
            # Calculer la quantité allouée proportionnellement au score
            quantite = (dept_score / total_score) * quantite_totale
            
            # Créer l'allocation
            allocation = Allocation(
                annee=annee,
                type_semence=type_semence,
                quantite=quantite,
                niveau="departement",
                region_id=dept.region_id,
                departement_id=dept.id,
                facteurs_influence=dept.facteurs_influence,
                created_by=created_by,
                updated_by=created_by
            )
            allocations.append(allocation)
        
        # Sauvegarder les allocations
        for allocation in allocations:
            db.add(allocation)
        db.commit()
        
        # Rafraîchir les objets pour obtenir les IDs
        for allocation in allocations:
            db.refresh(allocation)
        
        return allocations

allocation = CRUDAllocation(Allocation) 