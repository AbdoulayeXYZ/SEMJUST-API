from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry

from app.db.base_class import Base

class Departement(Base):
    __tablename__ = "departements"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True, nullable=False)
    nom = Column(String, nullable=False)
    region_id = Column(Integer, ForeignKey("regions.id"), nullable=False)
    population = Column(Integer)
    superficie = Column(Float)  # en hectares
    geom = Column(Geometry('MULTIPOLYGON', srid=4326))
    
    # Facteurs agro-écologiques
    pluviometrie_moyenne = Column(Float)  # en mm/an
    temperature_moyenne = Column(Float)  # en °C
    type_sol = Column(String)
    irrigation = Column(Float)  # pourcentage de surface irriguée
    
    # Métadonnées
    department_metadata = Column(JSONB)
    
    # Historique des allocations
    historique_allocations = Column(JSONB, default={})
    
    # Relations
    region = relationship("Region", back_populates="departements")
    
    def __repr__(self):
        return f"<Departement {self.nom}>" 