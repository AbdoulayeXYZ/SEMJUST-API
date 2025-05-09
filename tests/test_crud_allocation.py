import pytest
from sqlalchemy.orm import Session

from app.crud.crud_allocation import allocation
from app.models.allocation import Allocation, TypeSemence
from app.schemas.allocation import AllocationCreate, AllocationUpdate

def test_create_allocation(db: Session, allocation_data: dict):
    allocation_in = AllocationCreate(**allocation_data)
    allocation_obj = allocation.create_with_metadata(
        db, obj_in=allocation_in, created_by="test@example.com"
    )
    assert allocation_obj.annee == allocation_data["annee"]
    assert allocation_obj.type_semence == allocation_data["type_semence"]
    assert allocation_obj.quantite == allocation_data["quantite"]
    assert allocation_obj.niveau == allocation_data["niveau"]
    assert allocation_obj.region_id == allocation_data["region_id"]
    assert allocation_obj.departement_id == allocation_data["departement_id"]
    assert allocation_obj.facteurs_influence == allocation_data["facteurs_influence"]
    assert allocation_obj.created_by == "test@example.com"
    assert allocation_obj.updated_by == "test@example.com"

def test_get_allocation(db: Session, allocation: Allocation):
    allocation_obj = allocation.get(db, id=allocation.id)
    assert allocation_obj is not None
    assert allocation_obj.id == allocation.id
    assert allocation_obj.annee == allocation.annee

def test_get_multi_allocation(db: Session, allocation: Allocation):
    allocations = allocation.get_multi(db)
    assert len(allocations) > 0
    assert any(a.id == allocation.id for a in allocations)

def test_get_multi_by_annee(db: Session, allocation: Allocation):
    allocations = allocation.get_multi_by_annee(db, annee=allocation.annee)
    assert len(allocations) > 0
    assert any(a.id == allocation.id for a in allocations)

def test_get_multi_by_type_semence(db: Session, allocation: Allocation):
    allocations = allocation.get_multi_by_type_semence(db, type_semence=allocation.type_semence)
    assert len(allocations) > 0
    assert any(a.id == allocation.id for a in allocations)

def test_get_multi_by_region(db: Session, allocation: Allocation):
    allocations = allocation.get_multi_by_region(db, region_id=allocation.region_id)
    assert len(allocations) > 0
    assert any(a.id == allocation.id for a in allocations)

def test_get_multi_by_departement(db: Session, allocation: Allocation):
    allocations = allocation.get_multi_by_departement(db, departement_id=allocation.departement_id)
    assert len(allocations) > 0
    assert any(a.id == allocation.id for a in allocations)

def test_update_allocation(db: Session, allocation: Allocation):
    new_quantite = 2000.0
    allocation_in = AllocationUpdate(quantite=new_quantite)
    allocation_obj = allocation.update_with_metadata(
        db, db_obj=allocation, obj_in=allocation_in, updated_by="test@example.com"
    )
    assert allocation_obj.quantite == new_quantite
    assert allocation_obj.id == allocation.id
    assert allocation_obj.updated_by == "test@example.com"

def test_remove_allocation(db: Session, allocation: Allocation):
    allocation_obj = allocation.remove(db, id=allocation.id)
    assert allocation_obj.id == allocation.id
    allocation_obj = allocation.get(db, id=allocation.id)
    assert allocation_obj is None

def test_count_allocation(db: Session, allocation: Allocation):
    count = allocation.count(db)
    assert count > 0

def test_get_summary(db: Session, allocation: Allocation):
    summary = allocation.get_summary(db, annee=allocation.annee)
    assert summary.annee == allocation.annee
    assert summary.total_quantite > 0
    assert summary.nombre_allocations > 0
    assert allocation.type_semence.value in summary.repartition_type_semence
    assert allocation.region_id in summary.repartition_region
    assert allocation.departement_id in summary.repartition_departement

def test_optimize_allocations(db: Session, departement: Departement):
    annee = 2024
    type_semence = TypeSemence.MAIS
    quantite_totale = 10000.0
    created_by = "test@example.com"

    allocations = allocation.optimize_allocations(
        db,
        annee=annee,
        type_semence=type_semence,
        quantite_totale=quantite_totale,
        created_by=created_by
    )

    assert len(allocations) > 0
    total_allocated = sum(a.quantite for a in allocations)
    assert abs(total_allocated - quantite_totale) < 0.01  # Tolérance pour les erreurs d'arrondi

    for a in allocations:
        assert a.annee == annee
        assert a.type_semence == type_semence
        assert a.created_by == created_by
        assert a.updated_by == created_by
        assert a.niveau == "departement"
        assert a.region_id is not None
        assert a.departement_id is not None
        assert a.facteurs_influence is not None 