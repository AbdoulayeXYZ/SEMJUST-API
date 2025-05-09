from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field, confloat, conint
from .base import BaseSchema
from .region import Region
from .departement import Departement
from app.models.allocation import TypeSemence

class AllocationBase(BaseModel):
    """Schéma de base pour les allocations"""
    annee: int
    type_semence: TypeSemence
    quantite: confloat(gt=0)  # en tonnes
    niveau: str  # 'region' ou 'departement'
    region_id: Optional[int] = None
    departement_id: Optional[int] = None
    facteurs_influence: Dict[str, Any] = Field(default_factory=dict)

class AllocationCreate(AllocationBase):
    """Schéma pour la création d'une allocation"""
    pass

class AllocationUpdate(AllocationBase):
    """Schéma pour la mise à jour d'une allocation"""
    annee: Optional[int] = None
    type_semence: Optional[TypeSemence] = None
    quantite: Optional[confloat(gt=0)] = None
    niveau: Optional[str] = None
    facteurs_influence: Optional[Dict[str, Any]] = None

class AllocationInDB(AllocationBase, BaseSchema):
    """Schéma pour une allocation en base de données"""
    created_by: Optional[str] = None
    updated_by: Optional[str] = None

class Allocation(AllocationInDB):
    """Schéma pour l'exposition d'une allocation"""
    region: Optional[Region] = None
    departement: Optional[Departement] = None

    class Config:
        from_attributes = True

class AllocationList(BaseModel):
    """Schéma pour la liste des allocations"""
    items: List[Allocation]
    total: int

class AllocationSummary(BaseModel):
    """Schéma pour le résumé des allocations"""
    total_quantite: float
    nombre_allocations: int
    par_type_semence: Dict[str, float]
    par_region: Dict[str, float]
    par_departement: Dict[str, float] 