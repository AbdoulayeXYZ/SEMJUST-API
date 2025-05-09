from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app import schemas
from app.api import deps
from app.crud import crud_departement
from app.models.user import User

router = APIRouter()

@router.get("/", response_model=schemas.DepartementList)
def read_departements(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    region_id: int = None,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Récupérer tous les départements.
    """
    if region_id:
        departements = crud_departement.get_multi_by_region(
            db, region_id=region_id, skip=skip, limit=limit
        )
        total = crud_departement.count_by_region(db, region_id=region_id)
    else:
        departements = crud_departement.get_multi(db, skip=skip, limit=limit)
        total = crud_departement.count(db)
    return {"items": departements, "total": total}

@router.post("/", response_model=schemas.Departement)
def create_departement(
    *,
    db: Session = Depends(deps.get_db),
    departement_in: schemas.DepartementCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Créer un nouveau département.
    """
    departement = crud_departement.get_by_code(db, code=departement_in.code)
    if departement:
        raise HTTPException(
            status_code=400,
            detail="Un département avec ce code existe déjà",
        )
    departement = crud_departement.create(db, obj_in=departement_in)
    return departement

@router.get("/{departement_id}", response_model=schemas.Departement)
def read_departement(
    *,
    db: Session = Depends(deps.get_db),
    departement_id: int,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Récupérer un département par son ID.
    """
    departement = crud_departement.get(db, id=departement_id)
    if not departement:
        raise HTTPException(
            status_code=404,
            detail="Département non trouvé",
        )
    return departement

@router.put("/{departement_id}", response_model=schemas.Departement)
def update_departement(
    *,
    db: Session = Depends(deps.get_db),
    departement_id: int,
    departement_in: schemas.DepartementUpdate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Mettre à jour un département.
    """
    departement = crud_departement.get(db, id=departement_id)
    if not departement:
        raise HTTPException(
            status_code=404,
            detail="Département non trouvé",
        )
    departement = crud_departement.update(db, db_obj=departement, obj_in=departement_in)
    return departement

@router.delete("/{departement_id}", response_model=schemas.Departement)
def delete_departement(
    *,
    db: Session = Depends(deps.get_db),
    departement_id: int,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Supprimer un département.
    """
    departement = crud_departement.get(db, id=departement_id)
    if not departement:
        raise HTTPException(
            status_code=404,
            detail="Département non trouvé",
        )
    departement = crud_departement.remove(db, id=departement_id)
    return departement

@router.get("/{departement_id}/allocations", response_model=List[schemas.Allocation])
def read_departement_allocations(
    *,
    db: Session = Depends(deps.get_db),
    departement_id: int,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Récupérer toutes les allocations d'un département.
    """
    departement = crud_departement.get(db, id=departement_id)
    if not departement:
        raise HTTPException(
            status_code=404,
            detail="Département non trouvé",
        )
    return departement.allocations 