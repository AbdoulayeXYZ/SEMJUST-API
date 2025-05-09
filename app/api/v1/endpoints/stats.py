from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, and_

from app import crud, models, schemas
from app.api import deps
from app.models.allocation import Allocation
from app.models.region import Region
from app.models.departement import Departement

router = APIRouter()

@router.get("/allocations/summary", response_model=schemas.AllocationSummary)
def get_allocation_summary(
    *,
    db: Session = Depends(deps.get_db),
    annee: Optional[int] = None,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Obtenir un résumé des allocations pour une année donnée.
    """
    query = db.query(Allocation)
    if annee:
        query = query.filter(Allocation.annee == annee)

    total_quantite = query.with_entities(func.sum(Allocation.quantite)).scalar() or 0
    nombre_allocations = query.count()

    # Répartition par type de semence
    repartition_type = (
        db.query(
            Allocation.type_semence,
            func.sum(Allocation.quantite).label("total")
        )
        .filter(Allocation.annee == annee if annee else True)
        .group_by(Allocation.type_semence)
        .all()
    )

    # Répartition par région
    repartition_region = (
        db.query(
            Region.nom,
            func.sum(Allocation.quantite).label("total")
        )
        .join(Allocation, Allocation.region_id == Region.id)
        .filter(Allocation.annee == annee if annee else True)
        .group_by(Region.nom)
        .all()
    )

    # Répartition par département
    repartition_departement = (
        db.query(
            Departement.nom,
            func.sum(Allocation.quantite).label("total")
        )
        .join(Allocation, Allocation.departement_id == Departement.id)
        .filter(Allocation.annee == annee if annee else True)
        .group_by(Departement.nom)
        .all()
    )

    return {
        "total_quantite": total_quantite,
        "nombre_allocations": nombre_allocations,
        "repartition_type_semence": [
            {"type": t[0], "total": t[1]} for t in repartition_type
        ],
        "repartition_region": [
            {"region": r[0], "total": r[1]} for r in repartition_region
        ],
        "repartition_departement": [
            {"departement": d[0], "total": d[1]} for d in repartition_departement
        ]
    }

@router.get("/allocations/trends", response_model=List[schemas.AllocationTrend])
def get_allocation_trends(
    *,
    db: Session = Depends(deps.get_db),
    type_semence: Optional[str] = None,
    region_id: Optional[int] = None,
    departement_id: Optional[int] = None,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Obtenir les tendances d'allocations sur plusieurs années.
    """
    query = db.query(
        Allocation.annee,
        func.sum(Allocation.quantite).label("total")
    ).group_by(Allocation.annee)

    if type_semence:
        query = query.filter(Allocation.type_semence == type_semence)
    if region_id:
        query = query.filter(Allocation.region_id == region_id)
    if departement_id:
        query = query.filter(Allocation.departement_id == departement_id)

    trends = query.order_by(Allocation.annee).all()
    return [{"annee": t[0], "total": t[1]} for t in trends]

@router.get("/allocations/distribution", response_model=List[schemas.AllocationDistribution])
def get_allocation_distribution(
    *,
    db: Session = Depends(deps.get_db),
    annee: int,
    niveau: str = Query(..., description="Niveau de distribution: 'region' ou 'departement'"),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Obtenir la distribution géographique des allocations.
    """
    if niveau == "region":
        query = (
            db.query(
                Region.nom,
                Region.code,
                func.sum(Allocation.quantite).label("total")
            )
            .join(Allocation, Allocation.region_id == Region.id)
            .filter(Allocation.annee == annee)
            .group_by(Region.nom, Region.code)
        )
    else:  # departement
        query = (
            db.query(
                Departement.nom,
                Departement.code,
                func.sum(Allocation.quantite).label("total")
            )
            .join(Allocation, Allocation.departement_id == Departement.id)
            .filter(Allocation.annee == annee)
            .group_by(Departement.nom, Departement.code)
        )

    distribution = query.all()
    return [
        {
            "nom": d[0],
            "code": d[1],
            "total": d[2]
        }
        for d in distribution
    ]

@router.get("/allocations/comparison", response_model=List[schemas.AllocationComparison])
def get_allocation_comparison(
    *,
    db: Session = Depends(deps.get_db),
    annee1: int,
    annee2: int,
    type_semence: Optional[str] = None,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Comparer les allocations entre deux années.
    """
    query = db.query(
        Allocation.region_id,
        Region.nom.label("region_nom"),
        func.sum(Allocation.quantite).label("total_annee1")
    ).join(
        Region, Allocation.region_id == Region.id
    ).filter(
        Allocation.annee == annee1
    )

    if type_semence:
        query = query.filter(Allocation.type_semence == type_semence)

    annee1_data = query.group_by(Allocation.region_id, Region.nom).all()

    # Requête pour l'année 2
    query2 = db.query(
        Allocation.region_id,
        Region.nom.label("region_nom"),
        func.sum(Allocation.quantite).label("total_annee2")
    ).join(
        Region, Allocation.region_id == Region.id
    ).filter(
        Allocation.annee == annee2
    )

    if type_semence:
        query2 = query2.filter(Allocation.type_semence == type_semence)

    annee2_data = query2.group_by(Allocation.region_id, Region.nom).all()

    # Combiner les résultats
    comparison = []
    for a1 in annee1_data:
        a2 = next((a for a in annee2_data if a[0] == a1[0]), None)
        comparison.append({
            "region_id": a1[0],
            "region_nom": a1[1],
            "total_annee1": a1[2],
            "total_annee2": a2[2] if a2 else 0,
            "variation": ((a2[2] if a2 else 0) - a1[2]) / a1[2] * 100 if a1[2] != 0 else 0
        })

    return comparison 