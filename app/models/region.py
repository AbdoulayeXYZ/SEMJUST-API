from sqlalchemy import Column, Integer, String, Float, JSON
from sqlalchemy.dialects.postgresql import JSONB
from geoalchemy2 import Geometry
from sqlalchemy.orm import relationship

from app.db.base_class import Base

class Region(Base):
    __tablename__ = "regions"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True, nullable=False)
    nom = Column(String, nullable=False)
    population = Column(Integer)
    superficie = Column(Float)  # en hectares
    geom = Column(Geometry('MULTIPOLYGON', srid=4326))
    
    # Facteurs agro-écologiques
    pluviometrie_moyenne = Column(Float)  # en mm/an
    temperature_moyenne = Column(Float)  # en °C
    type_sol = Column(String)
    irrigation = Column(Float)  # pourcentage de surface irriguée
    
    # Métadonnées
    region_metadata = Column(JSONB)
    
    # Historique des allocations
    historique_allocations = Column(JSONB, default={})
    
    # Relations
    departements = relationship("Departement", back_populates="region")
    allocations = relationship("Allocation", back_populates="region")
    
    def __repr__(self):
        return f"<Region {self.nom}>" 