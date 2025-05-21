from prometheus_client import Gauge
import random
from app.db.session import SessionLocal
from app.models.region import Region
from app.models.departement import Departement
from app.models.allocation import Allocation, TypeSemence
from sqlalchemy.exc import IntegrityError

# Gauge pour la quantité allouée par région/département/type_semence
ALLOCATION_GAUGE = Gauge(
    "allocation_quantity",
    "Quantité de semences allouée",
    ["region", "departement", "lat", "lon", "type_semence"]
)

def populate_allocation_metrics():
    regions_departements = [
        {"region": "Dakar", "departements": [
            {"name": "Dakar", "lat": 14.6928, "lon": -17.4467},
            {"name": "Guediawaye", "lat": 14.7841, "lon": -17.4065},
            {"name": "Pikine", "lat": 14.7645, "lon": -17.3907},
            {"name": "Rufisque", "lat": 14.7156, "lon": -17.2736}
        ]},
        {"region": "Thiès", "departements": [
            {"name": "Thiès", "lat": 14.7910, "lon": -16.9256},
            {"name": "Mbour", "lat": 14.4205, "lon": -16.9644},
            {"name": "Tivaouane", "lat": 15.1500, "lon": -16.8167}
        ]},
        {"region": "Saint-Louis", "departements": [
            {"name": "Saint-Louis", "lat": 16.0179, "lon": -16.4896},
            {"name": "Dagana", "lat": 16.6092, "lon": -15.6076},
            {"name": "Podor", "lat": 16.6556, "lon": -14.9722}
        ]},
        {"region": "Kaolack", "departements": [
            {"name": "Kaolack", "lat": 14.1460, "lon": -16.0726},
            {"name": "Guinguinéo", "lat": 14.2611, "lon": -15.9500},
            {"name": "Nioro du Rip", "lat": 13.7500, "lon": -15.8000}
        ]},
        {"region": "Ziguinchor", "departements": [
            {"name": "Ziguinchor", "lat": 12.5833, "lon": -16.2719},
            {"name": "Bignona", "lat": 12.8081, "lon": -16.2264},
            {"name": "Oussouye", "lat": 12.4856, "lon": -16.5461}
        ]},
        {"region": "Fatick", "departements": [
            {"name": "Fatick", "lat": 14.3396, "lon": -16.4160},
            {"name": "Foundiougne", "lat": 14.1333, "lon": -16.4667},
            {"name": "Gossas", "lat": 14.6500, "lon": -16.0667}
        ]},
        {"region": "Kolda", "departements": [
            {"name": "Kolda", "lat": 12.8833, "lon": -14.9500},
            {"name": "Velingara", "lat": 13.1500, "lon": -14.1167},
            {"name": "Medina Yoro Foulah", "lat": 13.2167, "lon": -14.0833}
        ]},
        {"region": "Tambacounda", "departements": [
            {"name": "Tambacounda", "lat": 13.7707, "lon": -13.6673},
            {"name": "Bakel", "lat": 14.9000, "lon": -12.4667},
            {"name": "Goudiry", "lat": 14.1833, "lon": -12.8833},
            {"name": "Koumpentoum", "lat": 13.9833, "lon": -13.1167}
        ]},
        {"region": "Louga", "departements": [
            {"name": "Louga", "lat": 15.6144, "lon": -16.2244},
            {"name": "Kebemer", "lat": 15.3333, "lon": -16.4167},
            {"name": "Linguere", "lat": 15.3833, "lon": -15.1167}
        ]},
        {"region": "Matam", "departements": [
            {"name": "Matam", "lat": 15.6559, "lon": -13.2554},
            {"name": "Kanel", "lat": 15.5000, "lon": -13.1833},
            {"name": "Ranerou", "lat": 15.6333, "lon": -13.4167}
        ]},
        {"region": "Diourbel", "departements": [
            {"name": "Diourbel", "lat": 14.6556, "lon": -16.2342},
            {"name": "Bambey", "lat": 14.7000, "lon": -16.4667},
            {"name": "Mbacke", "lat": 14.9900, "lon": -15.6800}
        ]},
        {"region": "Kaffrine", "departements": [
            {"name": "Kaffrine", "lat": 14.1050, "lon": -15.5500},
            {"name": "Birkilane", "lat": 14.2833, "lon": -15.4167},
            {"name": "Koungheul", "lat": 13.9833, "lon": -14.8167},
            {"name": "Malem Hodar", "lat": 14.1833, "lon": -15.1167}
        ]},
        {"region": "Sédhiou", "departements": [
            {"name": "Sedhiou", "lat": 12.7081, "lon": -15.5569},
            {"name": "Bounkiling", "lat": 12.8000, "lon": -15.2333},
            {"name": "Goudomp", "lat": 12.5167, "lon": -15.3667}
        ]},
        {"region": "Kédougou", "departements": [
            {"name": "Kedougou", "lat": 12.5556, "lon": -12.1744},
            {"name": "Salemata", "lat": 12.7000, "lon": -12.7000},
            {"name": "Saraya", "lat": 12.8833, "lon": -12.5333}
        ]}
    ]

    types_semence = ["mil", "maïs", "arachide", "riz"]
    for region in regions_departements:
        for dep in region["departements"]:
            for type_semence in types_semence:
                quantite = random.randint(50, 500)
                ALLOCATION_GAUGE.labels(
                    region=region["region"],
                    departement=dep["name"],
                    lat=str(dep["lat"]),
                    lon=str(dep["lon"]),
                    type_semence=type_semence
                ).set(quantite)

def populate_postgres_test_data():
    db = SessionLocal()
    regions_departements = [
        {"region": "Dakar", "departements": [
            {"name": "Dakar", "lat": 14.6928, "lon": -17.4467},
            {"name": "Guediawaye", "lat": 14.7841, "lon": -17.4065},
            {"name": "Pikine", "lat": 14.7645, "lon": -17.3907},
            {"name": "Rufisque", "lat": 14.7156, "lon": -17.2736}
        ]},
        {"region": "Thiès", "departements": [
            {"name": "Thiès", "lat": 14.7910, "lon": -16.9256},
            {"name": "Mbour", "lat": 14.4205, "lon": -16.9644},
            {"name": "Tivaouane", "lat": 15.1500, "lon": -16.8167}
        ]},
        {"region": "Saint-Louis", "departements": [
            {"name": "Saint-Louis", "lat": 16.0179, "lon": -16.4896},
            {"name": "Dagana", "lat": 16.6092, "lon": -15.6076},
            {"name": "Podor", "lat": 16.6556, "lon": -14.9722}
        ]},
        {"region": "Kaolack", "departements": [
            {"name": "Kaolack", "lat": 14.1460, "lon": -16.0726},
            {"name": "Guinguinéo", "lat": 14.2611, "lon": -15.9500},
            {"name": "Nioro du Rip", "lat": 13.7500, "lon": -15.8000}
        ]},
        {"region": "Ziguinchor", "departements": [
            {"name": "Ziguinchor", "lat": 12.5833, "lon": -16.2719},
            {"name": "Bignona", "lat": 12.8081, "lon": -16.2264},
            {"name": "Oussouye", "lat": 12.4856, "lon": -16.5461}
        ]},
        {"region": "Fatick", "departements": [
            {"name": "Fatick", "lat": 14.3396, "lon": -16.4160},
            {"name": "Foundiougne", "lat": 14.1333, "lon": -16.4667},
            {"name": "Gossas", "lat": 14.6500, "lon": -16.0667}
        ]},
        {"region": "Kolda", "departements": [
            {"name": "Kolda", "lat": 12.8833, "lon": -14.9500},
            {"name": "Velingara", "lat": 13.1500, "lon": -14.1167},
            {"name": "Medina Yoro Foulah", "lat": 13.2167, "lon": -14.0833}
        ]},
        {"region": "Tambacounda", "departements": [
            {"name": "Tambacounda", "lat": 13.7707, "lon": -13.6673},
            {"name": "Bakel", "lat": 14.9000, "lon": -12.4667},
            {"name": "Goudiry", "lat": 14.1833, "lon": -12.8833},
            {"name": "Koumpentoum", "lat": 13.9833, "lon": -13.1167}
        ]},
        {"region": "Louga", "departements": [
            {"name": "Louga", "lat": 15.6144, "lon": -16.2244},
            {"name": "Kebemer", "lat": 15.3333, "lon": -16.4167},
            {"name": "Linguere", "lat": 15.3833, "lon": -15.1167}
        ]},
        {"region": "Matam", "departements": [
            {"name": "Matam", "lat": 15.6559, "lon": -13.2554},
            {"name": "Kanel", "lat": 15.5000, "lon": -13.1833},
            {"name": "Ranerou", "lat": 15.6333, "lon": -13.4167}
        ]},
        {"region": "Diourbel", "departements": [
            {"name": "Diourbel", "lat": 14.6556, "lon": -16.2342},
            {"name": "Bambey", "lat": 14.7000, "lon": -16.4667},
            {"name": "Mbacke", "lat": 14.9900, "lon": -15.6800}
        ]},
        {"region": "Kaffrine", "departements": [
            {"name": "Kaffrine", "lat": 14.1050, "lon": -15.5500},
            {"name": "Birkilane", "lat": 14.2833, "lon": -15.4167},
            {"name": "Koungheul", "lat": 13.9833, "lon": -14.8167},
            {"name": "Malem Hodar", "lat": 14.1833, "lon": -15.1167}
        ]},
        {"region": "Sédhiou", "departements": [
            {"name": "Sedhiou", "lat": 12.7081, "lon": -15.5569},
            {"name": "Bounkiling", "lat": 12.8000, "lon": -15.2333},
            {"name": "Goudomp", "lat": 12.5167, "lon": -15.3667}
        ]},
        {"region": "Kédougou", "departements": [
            {"name": "Kedougou", "lat": 12.5556, "lon": -12.1744},
            {"name": "Salemata", "lat": 12.7000, "lon": -12.7000},
            {"name": "Saraya", "lat": 12.8833, "lon": -12.5333}
        ]}
    ]
    types_semence = ["mil", "maïs", "arachide", "riz"]
    try:
        # Création des régions
        for idx, region in enumerate(regions_departements, start=1):
            reg = Region(
                code=f"R{idx:02d}",
                nom=region["region"],
                population=random.randint(200000, 2000000),
                superficie=random.uniform(100000, 500000),
                geom=None  # À remplacer par une géométrie réelle si besoin
            )
            db.add(reg)
            db.flush()  # Pour obtenir l'ID
            for jdx, dep in enumerate(region["departements"], start=1):
                dep_obj = Departement(
                    code=f"D{idx:02d}{jdx:02d}",
                    nom=dep["name"],
                    region_id=reg.id,
                    population=random.randint(50000, 500000),
                    superficie=random.uniform(10000, 50000),
                    geom=None  # À remplacer par une géométrie réelle si besoin
                )
                db.add(dep_obj)
                db.flush()
                for type_semence in types_semence:
                    alloc = Allocation(
                        annee=2024,
                        type_semence=TypeSemence(type_semence.upper()),
                        quantite=random.randint(50, 500),
                        niveau="departement",
                        region_id=reg.id,
                        departement_id=dep_obj.id,
                        created_by="test_script"
                    )
                    db.add(alloc)
        db.commit()
    except IntegrityError:
        db.rollback()
    finally:
        db.close() 