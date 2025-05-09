import pytest
from typing import Generator, Dict
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.db.base import Base
from app.db.session import get_db
from app.core.config import settings
from app.models.region import Region
from app.models.departement import Departement
from app.models.allocation import Allocation, TypeSemence

# Créer une base de données SQLite en mémoire pour les tests
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session")
def db() -> Generator:
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="module")
def client(db: TestingSessionLocal) -> Generator:
    def override_get_db():
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c

@pytest.fixture
def region_data() -> Dict:
    return {
        "code": "DK",
        "nom": "Dakar",
        "population": 3500000,
        "superficie": 550.0,
        "pluviometrie_moyenne": 500.0,
        "temperature_moyenne": 27.0,
        "type_sol": "sableux",
        "irrigation": True,
        "facteurs_influence": {
            "population": 0.3,
            "superficie": 0.2,
            "pluviometrie": 0.2,
            "temperature": 0.1,
            "type_sol": 0.1,
            "irrigation": 0.1
        }
    }

@pytest.fixture
def departement_data() -> Dict:
    return {
        "code": "DK-01",
        "nom": "Dakar Ville",
        "region_id": 1,
        "population": 1000000,
        "superficie": 100.0,
        "pluviometrie_moyenne": 450.0,
        "temperature_moyenne": 28.0,
        "type_sol": "sableux",
        "irrigation": True,
        "facteurs_influence": {
            "population": 0.3,
            "superficie": 0.2,
            "pluviometrie": 0.2,
            "temperature": 0.1,
            "type_sol": 0.1,
            "irrigation": 0.1
        }
    }

@pytest.fixture
def allocation_data() -> Dict:
    return {
        "annee": 2024,
        "type_semence": TypeSemence.MAIS,
        "quantite": 1000.0,
        "niveau": "departement",
        "region_id": 1,
        "departement_id": 1,
        "facteurs_influence": {
            "population": 0.3,
            "superficie": 0.2,
            "pluviometrie": 0.2,
            "temperature": 0.1,
            "type_sol": 0.1,
            "irrigation": 0.1
        }
    }

@pytest.fixture
def region(db: TestingSessionLocal, region_data: Dict) -> Region:
    region = Region(**region_data)
    db.add(region)
    db.commit()
    db.refresh(region)
    return region

@pytest.fixture
def departement(db: TestingSessionLocal, departement_data: Dict) -> Departement:
    departement = Departement(**departement_data)
    db.add(departement)
    db.commit()
    db.refresh(departement)
    return departement

@pytest.fixture
def allocation(db: TestingSessionLocal, allocation_data: Dict) -> Allocation:
    allocation = Allocation(**allocation_data)
    db.add(allocation)
    db.commit()
    db.refresh(allocation)
    return allocation 