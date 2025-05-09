from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
import pandas as pd
import io

from app import crud, models, schemas
from app.api import deps
from app.models.allocation import Allocation
from app.models.region import Region
from app.models.departement import Departement

router = APIRouter()

@router.get("/allocations/csv")
def export_allocations_csv(
    *,
    db: Session = Depends(deps.get_db),
    annee: int = None,
    type_semence: str = None,
    region_id: int = None,
    departement_id: int = None,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Exporter les allocations en CSV.
    """
    query = db.query(
        Allocation,
        Region.nom.label("region_nom"),
        Departement.nom.label("departement_nom")
    ).join(
        Region, Allocation.region_id == Region.id
    ).join(
        Departement, Allocation.departement_id == Departement.id
    )

    if annee:
        query = query.filter(Allocation.annee == annee)
    if type_semence:
        query = query.filter(Allocation.type_semence == type_semence)
    if region_id:
        query = query.filter(Allocation.region_id == region_id)
    if departement_id:
        query = query.filter(Allocation.departement_id == departement_id)

    results = query.all()

    # Créer un DataFrame pandas
    data = []
    for r in results:
        data.append({
            "ID": r.Allocation.id,
            "Année": r.Allocation.annee,
            "Type de semence": r.Allocation.type_semence,
            "Quantité": r.Allocation.quantite,
            "Niveau": r.Allocation.niveau,
            "Région": r.region_nom,
            "Département": r.departement_nom,
            "Date de création": r.Allocation.created_at,
            "Date de mise à jour": r.Allocation.updated_at
        })

    df = pd.DataFrame(data)

    # Créer un buffer pour le CSV
    buffer = io.StringIO()
    df.to_csv(buffer, index=False, encoding='utf-8-sig')
    buffer.seek(0)

    # Retourner le fichier CSV
    return StreamingResponse(
        iter([buffer.getvalue()]),
        media_type="text/csv",
        headers={
            "Content-Disposition": f"attachment; filename=allocations_{annee if annee else 'all'}.csv"
        }
    )

@router.get("/allocations/excel")
def export_allocations_excel(
    *,
    db: Session = Depends(deps.get_db),
    annee: int = None,
    type_semence: str = None,
    region_id: int = None,
    departement_id: int = None,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Exporter les allocations en Excel.
    """
    query = db.query(
        Allocation,
        Region.nom.label("region_nom"),
        Departement.nom.label("departement_nom")
    ).join(
        Region, Allocation.region_id == Region.id
    ).join(
        Departement, Allocation.departement_id == Departement.id
    )

    if annee:
        query = query.filter(Allocation.annee == annee)
    if type_semence:
        query = query.filter(Allocation.type_semence == type_semence)
    if region_id:
        query = query.filter(Allocation.region_id == region_id)
    if departement_id:
        query = query.filter(Allocation.departement_id == departement_id)

    results = query.all()

    # Créer un DataFrame pandas
    data = []
    for r in results:
        data.append({
            "ID": r.Allocation.id,
            "Année": r.Allocation.annee,
            "Type de semence": r.Allocation.type_semence,
            "Quantité": r.Allocation.quantite,
            "Niveau": r.Allocation.niveau,
            "Région": r.region_nom,
            "Département": r.departement_nom,
            "Date de création": r.Allocation.created_at,
            "Date de mise à jour": r.Allocation.updated_at
        })

    df = pd.DataFrame(data)

    # Créer un buffer pour le fichier Excel
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Allocations', index=False)
        
        # Obtenir le workbook et le worksheet
        workbook = writer.book
        worksheet = writer.sheets['Allocations']
        
        # Ajouter des formats
        header_format = workbook.add_format({
            'bold': True,
            'text_wrap': True,
            'valign': 'top',
            'fg_color': '#D7E4BC',
            'border': 1
        })
        
        # Appliquer le format aux en-têtes
        for col_num, value in enumerate(df.columns.values):
            worksheet.write(0, col_num, value, header_format)
            worksheet.set_column(col_num, col_num, 15)

    buffer.seek(0)

    # Retourner le fichier Excel
    return StreamingResponse(
        iter([buffer.getvalue()]),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": f"attachment; filename=allocations_{annee if annee else 'all'}.xlsx"
        }
    ) 