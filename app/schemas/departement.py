from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field
from .base import BaseSchema, BaseGeoSchema, BaseMetadataSchema
from .region import Region

class DepartementBase(BaseGeoSchema, BaseMetadataSchema):
    """Schéma de base pour les départements"""
    region_id: int

class DepartementCreate(DepartementBase):
    """Schéma pour la création d'un département"""
    pass

class DepartementUpdate(DepartementBase):
    """Schéma pour la mise à jour d'un département"""
    code: Optional[str] = None
    nom: Optional[str] = None
    region_id: Optional[int] = None

class DepartementInDB(DepartementBase, BaseSchema):
    """Schéma pour un département en base de données"""
    historique_allocations: Dict[str, Any] = Field(default_factory=dict)

class Departement(DepartementInDB):
    """Schéma pour l'exposition d'un département"""
    region: Optional[Region] = None

    class Config:
        from_attributes = True

class DepartementList(BaseModel):
    """Schéma pour la liste des départements"""
    items: List[Departement]
    total: int 