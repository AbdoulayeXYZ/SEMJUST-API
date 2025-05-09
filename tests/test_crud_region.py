import pytest
from sqlalchemy.orm import Session

from app.crud.crud_region import region
from app.models.region import Region
from app.schemas.region import RegionCreate, RegionUpdate

def test_create_region(db: Session, region_data: dict):
    region_in = RegionCreate(**region_data)
    region_obj = region.create(db, obj_in=region_in)
    assert region_obj.code == region_data["code"]
    assert region_obj.nom == region_data["nom"]
    assert region_obj.population == region_data["population"]
    assert region_obj.superficie == region_data["superficie"]
    assert region_obj.pluviometrie_moyenne == region_data["pluviometrie_moyenne"]
    assert region_obj.temperature_moyenne == region_data["temperature_moyenne"]
    assert region_obj.type_sol == region_data["type_sol"]
    assert region_obj.irrigation == region_data["irrigation"]
    assert region_obj.facteurs_influence == region_data["facteurs_influence"]

def test_get_region(db: Session, region: Region):
    region_obj = region.get(db, id=region.id)
    assert region_obj is not None
    assert region_obj.id == region.id
    assert region_obj.code == region.code

def test_get_region_by_code(db: Session, region: Region):
    region_obj = region.get_by_code(db, code=region.code)
    assert region_obj is not None
    assert region_obj.id == region.id
    assert region_obj.code == region.code

def test_get_multi_region(db: Session, region: Region):
    regions = region.get_multi(db)
    assert len(regions) > 0
    assert any(r.id == region.id for r in regions)

def test_get_multi_by_population(db: Session, region: Region):
    regions = region.get_multi_by_population(db, min_population=region.population - 1)
    assert len(regions) > 0
    assert any(r.id == region.id for r in regions)

def test_get_multi_by_superficie(db: Session, region: Region):
    regions = region.get_multi_by_superficie(db, min_superficie=region.superficie - 1)
    assert len(regions) > 0
    assert any(r.id == region.id for r in regions)

def test_get_multi_by_pluviometrie(db: Session, region: Region):
    regions = region.get_multi_by_pluviometrie(db, min_pluviometrie=region.pluviometrie_moyenne - 1)
    assert len(regions) > 0
    assert any(r.id == region.id for r in regions)

def test_get_multi_by_temperature(db: Session, region: Region):
    regions = region.get_multi_by_temperature(db, min_temperature=region.temperature_moyenne - 1)
    assert len(regions) > 0
    assert any(r.id == region.id for r in regions)

def test_get_multi_by_irrigation(db: Session, region: Region):
    regions = region.get_multi_by_irrigation(db, irrigation=region.irrigation)
    assert len(regions) > 0
    assert any(r.id == region.id for r in regions)

def test_get_multi_by_type_sol(db: Session, region: Region):
    regions = region.get_multi_by_type_sol(db, type_sol=region.type_sol)
    assert len(regions) > 0
    assert any(r.id == region.id for r in regions)

def test_update_region(db: Session, region: Region):
    new_nom = "Nouveau Dakar"
    region_in = RegionUpdate(nom=new_nom)
    region_obj = region.update(db, db_obj=region, obj_in=region_in)
    assert region_obj.nom == new_nom
    assert region_obj.id == region.id

def test_remove_region(db: Session, region: Region):
    region_obj = region.remove(db, id=region.id)
    assert region_obj.id == region.id
    region_obj = region.get(db, id=region.id)
    assert region_obj is None

def test_count_region(db: Session, region: Region):
    count = region.count(db)
    assert count > 0 