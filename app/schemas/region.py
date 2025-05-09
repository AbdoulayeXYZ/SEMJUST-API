from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field
from .base import BaseSchema, BaseGeoSchema, BaseMetadataSchema

class RegionBase(BaseGeoSchema, BaseMetadataSchema):
    """Schéma de base pour les régions"""
    pass

class RegionCreate(RegionBase):
    """Schéma pour la création d'une région"""
    pass

class RegionUpdate(RegionBase):
    """Schéma pour la mise à jour d'une région"""
    code: Optional[str] = None
    nom: Optional[str] = None

class RegionInDB(RegionBase, BaseSchema):
    """Schéma pour une région en base de données"""
    historique_allocations: Dict[str, Any] = Field(default_factory=dict)

class Region(RegionInDB):
    """Schéma pour l'exposition d'une région"""
    class Config:
        from_attributes = True

class RegionList(BaseModel):
    """Schéma pour la liste des régions"""
    items: List[Region]
    total: int 