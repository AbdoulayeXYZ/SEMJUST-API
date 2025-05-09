from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
import numpy as np
from pulp import *

from app.models.allocation import Allocation
from app.models.region import Region
from app.models.departement import Departement
from app.schemas.allocation import AllocationCreate
from app.services.notification_service import NotificationService
from app.models.notification import NotificationType

class OptimizationService:
    @staticmethod
    def optimize_allocations(
        db: Session,
        *,
        annee: int,
        type_semence: str,
        quantite_totale: float,
        user_id: int,
        considerer_historique: bool = True,
        considerer_superficie: bool = True,
        considerer_rendement: bool = True,
        considerer_population: bool = True
    ) -> List[AllocationCreate]:
        """
        Optimise les allocations en utilisant la programmation linéaire.
        """
        # Récupérer les données historiques
        historique = db.query(
            Departement.id,
            func.avg(Allocation.quantite).label('moyenne_historique'),
            func.sum(Allocation.quantite).label('total_historique')
        ).join(
            Allocation, Allocation.departement_id == Departement.id
        ).filter(
            Allocation.type_semence == type_semence,
            Allocation.annee < annee
        ).group_by(Departement.id).all()

        # Créer le problème d'optimisation
        prob = LpProblem(f"Optimisation_Allocations_{annee}", LpMinimize)

        # Variables de décision
        departements = db.query(Departement).all()
        x = LpVariable.dicts("allocation",
                           ((d.id) for d in departements),
                           lowBound=0)

        # Fonction objectif
        prob += lpSum([x[d.id] for d in departements])

        # Contraintes
        # 1. Quantité totale disponible
        prob += lpSum([x[d.id] for d in departements]) == quantite_totale

        # 2. Contraintes basées sur l'historique
        if considerer_historique:
            for h in historique:
                if h.moyenne_historique:
                    prob += x[h.id] >= h.moyenne_historique * 0.8  # Minimum 80% de la moyenne historique
                    prob += x[h.id] <= h.moyenne_historique * 1.2  # Maximum 120% de la moyenne historique

        # 3. Contraintes basées sur la superficie
        if considerer_superficie:
            for d in departements:
                if d.superficie:
                    prob += x[d.id] <= d.superficie * 0.1  # Maximum 10% de la superficie

        # 4. Contraintes basées sur le rendement
        if considerer_rendement:
            for d in departements:
                if d.rendement_moyen:
                    prob += x[d.id] >= d.rendement_moyen * 0.5  # Minimum 50% du rendement moyen

        # 5. Contraintes basées sur la population
        if considerer_population:
            for d in departements:
                if d.population:
                    prob += x[d.id] >= d.population * 0.01  # Minimum 1% de la population

        # Résoudre le problème
        prob.solve()

        # Créer les allocations optimisées
        allocations = []
        for d in departements:
            if value(x[d.id]) > 0:
                allocation = AllocationCreate(
                    annee=annee,
                    type_semence=type_semence,
                    quantite=value(x[d.id]),
                    region_id=d.region_id,
                    departement_id=d.id,
                    niveau="optimise"
                )
                allocations.append(allocation)

        # Créer une notification pour l'utilisateur
        NotificationService.create_notification(
            db=db,
            user_id=user_id,
            type=NotificationType.SYSTEM_ALERT,
            title="Optimisation des allocations terminée",
            message=f"L'optimisation des allocations pour {type_semence} en {annee} a été effectuée avec succès."
        )

        return allocations

    @staticmethod
    def calculate_metrics(
        db: Session,
        *,
        annee: int,
        type_semence: str
    ) -> Dict:
        """
        Calcule des métriques pour évaluer la qualité des allocations.
        """
        allocations = db.query(Allocation).filter(
            Allocation.annee == annee,
            Allocation.type_semence == type_semence
        ).all()

        if not allocations:
            return {}

        quantites = [a.quantite for a in allocations]
        
        return {
            "moyenne": np.mean(quantites),
            "mediane": np.median(quantites),
            "ecart_type": np.std(quantites),
            "minimum": min(quantites),
            "maximum": max(quantites),
            "nombre_allocations": len(allocations),
            "total_quantite": sum(quantites)
        }

    @staticmethod
    def validate_optimization(
        db: Session,
        *,
        allocations: List[AllocationCreate],
        annee: int,
        type_semence: str
    ) -> Dict:
        """
        Valide les allocations optimisées en vérifiant les contraintes.
        """
        validation = {
            "valid": True,
            "warnings": [],
            "errors": []
        }

        # Vérifier la cohérence des quantités
        total_quantite = sum(a.quantite for a in allocations)
        if total_quantite <= 0:
            validation["valid"] = False
            validation["errors"].append("La quantité totale doit être positive")

        # Vérifier la distribution
        quantites = [a.quantite for a in allocations]
        if len(quantites) > 1:
            cv = np.std(quantites) / np.mean(quantites)  # Coefficient de variation
            if cv > 0.5:  # Si la variation est trop importante
                validation["warnings"].append(
                    f"La distribution des allocations est très inégale (CV = {cv:.2f})"
                )

        # Vérifier les doublons
        departements = set()
        for a in allocations:
            if a.departement_id in departements:
                validation["errors"].append(
                    f"Doublon détecté pour le département {a.departement_id}"
                )
            departements.add(a.departement_id)

        return validation 