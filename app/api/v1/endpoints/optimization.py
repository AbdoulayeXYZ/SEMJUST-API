from typing import Any, List, Dict
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app import schemas
from app.models.user import User
from app.api import deps
from app.services.optimization_service import OptimizationService
from app.crud import crud_allocation

router = APIRouter()

@router.post("/optimize", response_model=List[schemas.Allocation])
def optimize_allocations(
    *,
    db: Session = Depends(deps.get_db),
    annee: int,
    type_semence: str,
    quantite_totale: float,
    considerer_historique: bool = True,
    considerer_superficie: bool = True,
    considerer_rendement: bool = True,
    considerer_population: bool = True,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Optimise les allocations pour une année et un type de semence donnés.
    """
    # Vérifier si des allocations existent déjà pour cette année et ce type
    existing_allocations = crud_allocation.get_multi_by_annee(
        db=db,
        annee=annee,
        type_semence=type_semence
    )
    if existing_allocations:
        raise HTTPException(
            status_code=400,
            detail="Des allocations existent déjà pour cette année et ce type de semence"
        )

    # Optimiser les allocations
    optimized_allocations = OptimizationService.optimize_allocations(
        db=db,
        annee=annee,
        type_semence=type_semence,
        quantite_totale=quantite_totale,
        user_id=current_user.id,
        considerer_historique=considerer_historique,
        considerer_superficie=considerer_superficie,
        considerer_rendement=considerer_rendement,
        considerer_population=considerer_population
    )

    # Valider les allocations optimisées
    validation = OptimizationService.validate_optimization(
        db=db,
        allocations=optimized_allocations,
        annee=annee,
        type_semence=type_semence
    )

    if not validation["valid"]:
        raise HTTPException(
            status_code=400,
            detail={
                "message": "Les allocations optimisées ne sont pas valides",
                "errors": validation["errors"],
                "warnings": validation["warnings"]
            }
        )

    # Créer les allocations dans la base de données
    created_allocations = []
    for allocation in optimized_allocations:
        created_allocation = crud_allocation.create(
            db=db,
            obj_in=allocation
        )
        created_allocations.append(created_allocation)

    return created_allocations

@router.get("/metrics", response_model=Dict)
def get_optimization_metrics(
    *,
    db: Session = Depends(deps.get_db),
    annee: int,
    type_semence: str,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Récupère les métriques d'optimisation pour une année et un type de semence donnés.
    """
    metrics = OptimizationService.calculate_metrics(
        db=db,
        annee=annee,
        type_semence=type_semence
    )
    
    if not metrics:
        raise HTTPException(
            status_code=404,
            detail="Aucune allocation trouvée pour cette année et ce type de semence"
        )
        
    return metrics

@router.post("/validate", response_model=Dict)
def validate_allocations(
    *,
    db: Session = Depends(deps.get_db),
    allocations: List[schemas.AllocationCreate],
    annee: int,
    type_semence: str,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Valide un ensemble d'allocations proposées.
    """
    validation = OptimizationService.validate_optimization(
        db=db,
        allocations=allocations,
        annee=annee,
        type_semence=type_semence
    )
    
    return validation 