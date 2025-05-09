from typing import List, Optional
from pydantic import BaseModel

class TypeSemenceStats(BaseModel):
    type: str
    total: float

class RegionStats(BaseModel):
    region: str
    total: float

class DepartementStats(BaseModel):
    departement: str
    total: float

class AllocationSummary(BaseModel):
    total_quantite: float
    nombre_allocations: int
    repartition_type_semence: List[TypeSemenceStats]
    repartition_region: List[RegionStats]
    repartition_departement: List[DepartementStats]

class AllocationTrend(BaseModel):
    annee: int
    total: float

class AllocationDistribution(BaseModel):
    nom: str
    code: str
    total: float

class AllocationComparison(BaseModel):
    region_id: int
    region_nom: str
    total_annee1: float
    total_annee2: float
    variation: float  # Pourcentage de variation

class AllocationMetrics(BaseModel):
    moyenne_quantite: float
    mediane_quantite: float
    ecart_type_quantite: float
    quantite_min: float
    quantite_max: float
    nombre_allocations: int
    nombre_regions: int
    nombre_departements: int
    nombre_types_semence: int 