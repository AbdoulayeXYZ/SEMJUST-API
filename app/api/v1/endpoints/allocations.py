from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app import schemas
from app.api import deps
from app.crud import crud_allocation
from app.models.user import User
from app.models.allocation import TypeSemence

router = APIRouter()

@router.get("/", response_model=schemas.AllocationList)
def read_allocations(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    annee: int = None,
    type_semence: TypeSemence = None,
    region_id: int = None,
    departement_id: int = None,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Récupérer toutes les allocations avec filtres optionnels.
    """
    filters = {}
    if annee:
        filters["annee"] = annee
    if type_semence:
        filters["type_semence"] = type_semence
    if region_id:
        filters["region_id"] = region_id
    if departement_id:
        filters["departement_id"] = departement_id

    allocations = crud_allocation.get_multi(
        db, skip=skip, limit=limit, filters=filters
    )
    total = crud_allocation.count(db, filters=filters)
    return {"items": allocations, "total": total}

@router.post("/", response_model=schemas.Allocation)
def create_allocation(
    *,
    db: Session = Depends(deps.get_db),
    allocation_in: schemas.AllocationCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Créer une nouvelle allocation.
    """
    allocation = crud_allocation.create(
        db, obj_in=allocation_in, created_by=current_user.email
    )
    return allocation

@router.get("/{allocation_id}", response_model=schemas.Allocation)
def read_allocation(
    *,
    db: Session = Depends(deps.get_db),
    allocation_id: int,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Récupérer une allocation par son ID.
    """
    allocation = crud_allocation.get(db, id=allocation_id)
    if not allocation:
        raise HTTPException(
            status_code=404,
            detail="Allocation non trouvée",
        )
    return allocation

@router.put("/{allocation_id}", response_model=schemas.Allocation)
def update_allocation(
    *,
    db: Session = Depends(deps.get_db),
    allocation_id: int,
    allocation_in: schemas.AllocationUpdate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Mettre à jour une allocation.
    """
    allocation = crud_allocation.get(db, id=allocation_id)
    if not allocation:
        raise HTTPException(
            status_code=404,
            detail="Allocation non trouvée",
        )
    allocation = crud_allocation.update(
        db, db_obj=allocation, obj_in=allocation_in, updated_by=current_user.email
    )
    return allocation

@router.delete("/{allocation_id}", response_model=schemas.Allocation)
def delete_allocation(
    *,
    db: Session = Depends(deps.get_db),
    allocation_id: int,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Supprimer une allocation.
    """
    allocation = crud_allocation.get(db, id=allocation_id)
    if not allocation:
        raise HTTPException(
            status_code=404,
            detail="Allocation non trouvée",
        )
    allocation = crud_allocation.remove(db, id=allocation_id)
    return allocation

@router.get("/summary/{annee}", response_model=schemas.AllocationSummary)
def get_allocation_summary(
    *,
    db: Session = Depends(deps.get_db),
    annee: int,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Obtenir un résumé des allocations pour une année donnée.
    """
    return crud_allocation.get_summary(db, annee=annee)

@router.post("/optimize", response_model=List[schemas.Allocation])
def optimize_allocations(
    *,
    db: Session = Depends(deps.get_db),
    annee: int,
    type_semence: TypeSemence,
    quantite_totale: float,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Optimiser les allocations pour une année et un type de semence donnés.
    """
    return crud_allocation.optimize_allocations(
        db,
        annee=annee,
        type_semence=type_semence,
        quantite_totale=quantite_totale,
        created_by=current_user.email
    ) 