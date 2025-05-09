from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app import schemas
from app.api import deps
from app.crud import crud_region
from app.models.user import User

router = APIRouter()

@router.get("/", response_model=schemas.RegionList)
def read_regions(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Récupérer toutes les régions.
    """
    regions = crud_region.get_multi(db, skip=skip, limit=limit)
    total = crud_region.count(db)
    return {"items": regions, "total": total}

@router.post("/", response_model=schemas.Region)
def create_region(
    *,
    db: Session = Depends(deps.get_db),
    region_in: schemas.RegionCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Créer une nouvelle région.
    """
    region = crud_region.get_by_code(db, code=region_in.code)
    if region:
        raise HTTPException(
            status_code=400,
            detail="Une région avec ce code existe déjà",
        )
    region = crud_region.create(db, obj_in=region_in)
    return region

@router.get("/{region_id}", response_model=schemas.Region)
def read_region(
    *,
    db: Session = Depends(deps.get_db),
    region_id: int,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Récupérer une région par son ID.
    """
    region = crud_region.get(db, id=region_id)
    if not region:
        raise HTTPException(
            status_code=404,
            detail="Région non trouvée",
        )
    return region

@router.put("/{region_id}", response_model=schemas.Region)
def update_region(
    *,
    db: Session = Depends(deps.get_db),
    region_id: int,
    region_in: schemas.RegionUpdate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Mettre à jour une région.
    """
    region = crud_region.get(db, id=region_id)
    if not region:
        raise HTTPException(
            status_code=404,
            detail="Région non trouvée",
        )
    region = crud_region.update(db, db_obj=region, obj_in=region_in)
    return region

@router.delete("/{region_id}", response_model=schemas.Region)
def delete_region(
    *,
    db: Session = Depends(deps.get_db),
    region_id: int,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Supprimer une région.
    """
    region = crud_region.get(db, id=region_id)
    if not region:
        raise HTTPException(
            status_code=404,
            detail="Région non trouvée",
        )
    region = crud_region.remove(db, id=region_id)
    return region

@router.get("/{region_id}/departements", response_model=List[schemas.Departement])
def read_region_departements(
    *,
    db: Session = Depends(deps.get_db),
    region_id: int,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Récupérer tous les départements d'une région.
    """
    region = crud_region.get(db, id=region_id)
    if not region:
        raise HTTPException(
            status_code=404,
            detail="Région non trouvée",
        )
    return region.departements 