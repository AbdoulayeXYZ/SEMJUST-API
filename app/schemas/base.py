from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field

class BaseSchema(BaseModel):
    """Schéma de base avec les champs communs"""
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class BaseMetadataSchema(BaseModel):
    """Schéma pour les métadonnées"""
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)

class BaseGeoSchema(BaseModel):
    """Schéma de base pour les entités géographiques"""
    code: str
    nom: str
    population: Optional[int] = None
    superficie: Optional[float] = None  # en hectares
    
    # Facteurs agro-écologiques
    pluviometrie_moyenne: Optional[float] = None  # en mm/an
    temperature_moyenne: Optional[float] = None  # en °C
    type_sol: Optional[str] = None
    irrigation: Optional[float] = None  # pourcentage de surface irriguée 

class Msg(BaseModel):
    """Simple message response schema"""
    msg: str
