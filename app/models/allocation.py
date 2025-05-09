from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Enum
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
import enum
from datetime import datetime

from app.db.base_class import Base

class TypeSemence(enum.Enum):
    RIZ = "riz"
    MIL = "mil"
    SORGHO = "sorgho"
    MAIS = "mais"
    ARACHIDE = "arachide"
    NIÉBÉ = "niebe"
    AUTRE = "autre"

class Allocation(Base):
    __tablename__ = "allocations"

    id = Column(Integer, primary_key=True, index=True)
    annee = Column(Integer, nullable=False)
    type_semence = Column(Enum(TypeSemence), nullable=False)
    quantite = Column(Float, nullable=False)  # en tonnes
    
    # Niveau d'allocation (région ou département)
    niveau = Column(String, nullable=False)  # 'region' ou 'departement'
    region_id = Column(Integer, ForeignKey("regions.id"))
    departement_id = Column(Integer, ForeignKey("departements.id"))
    
    # Facteurs d'influence
    facteurs_influence = Column(JSONB, default={})
    
    # Métadonnées
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(String)
    updated_by = Column(String)
    
    # Relations
    region = relationship("Region", back_populates="allocations")
    departement = relationship("Departement", back_populates="allocations")
    
    def __repr__(self):
        return f"<Allocation {self.type_semence.value} {self.annee}>" 