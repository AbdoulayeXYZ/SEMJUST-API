import pytest
from sqlalchemy.orm import Session

from app.crud.crud_departement import departement
from app.models.departement import Departement
from app.schemas.departement import DepartementCreate, DepartementUpdate

def test_create_departement(db: Session, departement_data: dict):
    departement_in = DepartementCreate(**departement_data)
    departement_obj = departement.create(db, obj_in=departement_in)
    assert departement_obj.code == departement_data["code"]
    assert departement_obj.nom == departement_data["nom"]
    assert departement_obj.region_id == departement_data["region_id"]
    assert departement_obj.population == departement_data["population"]
    assert departement_obj.superficie == departement_data["superficie"]
    assert departement_obj.pluviometrie_moyenne == departement_data["pluviometrie_moyenne"]
    assert departement_obj.temperature_moyenne == departement_data["temperature_moyenne"]
    assert departement_obj.type_sol == departement_data["type_sol"]
    assert departement_obj.irrigation == departement_data["irrigation"]
    assert departement_obj.facteurs_influence == departement_data["facteurs_influence"]

def test_get_departement(db: Session, departement: Departement):
    departement_obj = departement.get(db, id=departement.id)
    assert departement_obj is not None
    assert departement_obj.id == departement.id
    assert departement_obj.code == departement.code

def test_get_departement_by_code(db: Session, departement: Departement):
    departement_obj = departement.get_by_code(db, code=departement.code)
    assert departement_obj is not None
    assert departement_obj.id == departement.id
    assert departement_obj.code == departement.code

def test_get_multi_departement(db: Session, departement: Departement):
    departements = departement.get_multi(db)
    assert len(departements) > 0
    assert any(d.id == departement.id for d in departements)

def test_get_multi_by_region(db: Session, departement: Departement):
    departements = departement.get_multi_by_region(db, region_id=departement.region_id)
    assert len(departements) > 0
    assert any(d.id == departement.id for d in departements)

def test_count_by_region(db: Session, departement: Departement):
    count = departement.count_by_region(db, region_id=departement.region_id)
    assert count > 0

def test_get_multi_by_population(db: Session, departement: Departement):
    departements = departement.get_multi_by_population(db, min_population=departement.population - 1)
    assert len(departements) > 0
    assert any(d.id == departement.id for d in departements)

def test_get_multi_by_superficie(db: Session, departement: Departement):
    departements = departement.get_multi_by_superficie(db, min_superficie=departement.superficie - 1)
    assert len(departements) > 0
    assert any(d.id == departement.id for d in departements)

def test_get_multi_by_pluviometrie(db: Session, departement: Departement):
    departements = departement.get_multi_by_pluviometrie(db, min_pluviometrie=departement.pluviometrie_moyenne - 1)
    assert len(departements) > 0
    assert any(d.id == departement.id for d in departements)

def test_get_multi_by_temperature(db: Session, departement: Departement):
    departements = departement.get_multi_by_temperature(db, min_temperature=departement.temperature_moyenne - 1)
    assert len(departements) > 0
    assert any(d.id == departement.id for d in departements)

def test_get_multi_by_irrigation(db: Session, departement: Departement):
    departements = departement.get_multi_by_irrigation(db, irrigation=departement.irrigation)
    assert len(departements) > 0
    assert any(d.id == departement.id for d in departements)

def test_get_multi_by_type_sol(db: Session, departement: Departement):
    departements = departement.get_multi_by_type_sol(db, type_sol=departement.type_sol)
    assert len(departements) > 0
    assert any(d.id == departement.id for d in departements)

def test_update_departement(db: Session, departement: Departement):
    new_nom = "Nouveau Dakar Ville"
    departement_in = DepartementUpdate(nom=new_nom)
    departement_obj = departement.update(db, db_obj=departement, obj_in=departement_in)
    assert departement_obj.nom == new_nom
    assert departement_obj.id == departement.id

def test_remove_departement(db: Session, departement: Departement):
    departement_obj = departement.remove(db, id=departement.id)
    assert departement_obj.id == departement.id
    departement_obj = departement.get(db, id=departement.id)
    assert departement_obj is None

def test_count_departement(db: Session, departement: Departement):
    count = departement.count(db)
    assert count > 0 