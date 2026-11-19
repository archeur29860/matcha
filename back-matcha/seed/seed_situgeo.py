
import random
import math
import uuid
import csv

import psycopg


# ============================================================
# EMPLACEMENTS DE TEST
# ============================================================

FRENCH_LOCATIONS = [
    # PARIS
    {
        "city": "Paris",
        "postcode": "75001",
        "department": "Paris",
        "lat": 48.864716,
        "long": 2.349014,
        "street": "Rue Montorgueil",
        "district": "Les Halles",
    },
    {
        "city": "Paris",
        "postcode": "75004",
        "department": "Paris",
        "lat": 48.857500,
        "long": 2.359000,
        "street": "Rue des Rosiers",
        "district": "Le Marais",
    },
    {
        "city": "Paris",
        "postcode": "75005",
        "department": "Paris",
        "lat": 48.842200,
        "long": 2.350800,
        "street": "Rue Mouffetard",
        "district": "Quartier Latin",
    },
    {
        "city": "Paris",
        "postcode": "75006",
        "department": "Paris",
        "lat": 48.853400,
        "long": 2.333300,
        "street": "Boulevard Saint-Germain",
        "district": "Saint-Germain",
    },
    {
        "city": "Paris",
        "postcode": "75018",
        "department": "Paris",
        "lat": 48.886700,
        "long": 2.343100,
        "street": "Rue des Martyrs",
        "district": "Montmartre",
    },
    {
        "city": "Paris",
        "postcode": "75011",
        "department": "Paris",
        "lat": 48.853000,
        "long": 2.370000,
        "street": "Rue de la Roquette",
        "district": "Bastille",
    },
    {
        "city": "Paris",
        "postcode": "75018",
        "department": "Paris",
        "lat": 48.889000,
        "long": 2.334000,
        "street": "Rue Lepic",
        "district": "Montmartre",
    },

    # LYON
    {
        "city": "Lyon",
        "postcode": "69001",
        "department": "Rhône",
        "lat": 45.770000,
        "long": 4.830000,
        "street": "Montée de la Grande-Côte",
        "district": "Pentes de la Croix-Rousse",
    },
    {
        "city": "Lyon",
        "postcode": "69002",
        "department": "Rhône",
        "lat": 45.757800,
        "long": 4.832000,
        "street": "Rue Victor Hugo",
        "district": "Bellecour",
    },
    {
        "city": "Lyon",
        "postcode": "69003",
        "department": "Rhône",
        "lat": 45.760000,
        "long": 4.860000,
        "street": "Rue de la Villette",
        "district": "Part-Dieu",
    },
    {
        "city": "Lyon",
        "postcode": "69004",
        "department": "Rhône",
        "lat": 45.780000,
        "long": 4.830000,
        "street": "Boulevard de la Croix-Rousse",
        "district": "Croix-Rousse",
    },
    {
        "city": "Lyon",
        "postcode": "69005",
        "department": "Rhône",
        "lat": 45.762000,
        "long": 4.827000,
        "street": "Rue Saint-Jean",
        "district": "Vieux Lyon",
    },
    {
        "city": "Lyon",
        "postcode": "69007",
        "department": "Rhône",
        "lat": 45.750000,
        "long": 4.840000,
        "street": "Grande Rue de la Guillotière",
        "district": "Guillotière",
    },

    # MARSEILLE
    {
        "city": "Marseille",
        "postcode": "13001",
        "department": "Bouches-du-Rhône",
        "lat": 43.296500,
        "long": 5.381100,
        "street": "Rue d'Aubagne",
        "district": "Noailles",
    },
    {
        "city": "Marseille",
        "postcode": "13002",
        "department": "Bouches-du-Rhône",
        "lat": 43.300000,
        "long": 5.367000,
        "street": "Rue du Panier",
        "district": "Le Panier",
    },
    {
        "city": "Marseille",
        "postcode": "13006",
        "department": "Bouches-du-Rhône",
        "lat": 43.287000,
        "long": 5.382000,
        "street": "Rue de Rome",
        "district": "Castellane",
    },
    {
        "city": "Marseille",
        "postcode": "13007",
        "department": "Bouches-du-Rhône",
        "lat": 43.283000,
        "long": 5.355000,
        "street": "Rue d'Endoume",
        "district": "Endoume",
    },

    # TOULOUSE
    {
        "city": "Toulouse",
        "postcode": "31000",
        "department": "Haute-Garonne",
        "lat": 43.604500,
        "long": 1.444000,
        "street": "Rue du Taur",
        "district": "Capitole",
    },
    {
        "city": "Toulouse",
        "postcode": "31300",
        "department": "Haute-Garonne",
        "lat": 43.598000,
        "long": 1.428000,
        "street": "Rue de la République",
        "district": "Saint-Cyprien",
    },
    {
        "city": "Toulouse",
        "postcode": "31500",
        "department": "Haute-Garonne",
        "lat": 43.600000,
        "long": 1.465000,
        "street": "Avenue Jean Rieux",
        "district": "Côte Pavée",
    },

    # BORDEAUX
    {
        "city": "Bordeaux",
        "postcode": "33000",
        "department": "Gironde",
        "lat": 44.837800,
        "long": -0.572000,
        "street": "Rue du Parlement Saint-Pierre",
        "district": "Saint-Pierre",
    },
    {
        "city": "Bordeaux",
        "postcode": "33000",
        "department": "Gironde",
        "lat": 44.849000,
        "long": -0.571000,
        "street": "Rue Notre-Dame",
        "district": "Chartrons",
    },
    {
        "city": "Bordeaux",
        "postcode": "33800",
        "department": "Gironde",
        "lat": 44.830000,
        "long": -0.566000,
        "street": "Rue des Faures",
        "district": "Saint-Michel",
    },

    # NANTES
    {
        "city": "Nantes",
        "postcode": "44000",
        "department": "Loire-Atlantique",
        "lat": 47.215000,
        "long": -1.553000,
        "street": "Rue de la Juiverie",
        "district": "Bouffay",
    },
    {
        "city": "Nantes",
        "postcode": "44200",
        "department": "Loire-Atlantique",
        "lat": 47.207000,
        "long": -1.555000,
        "street": "Boulevard de la Prairie au Duc",
        "district": "Île de Nantes",
    },
    {
        "city": "Nantes",
        "postcode": "44000",
        "department": "Loire-Atlantique",
        "lat": 47.226000,
        "long": -1.565000,
        "street": "Rue des Hauts-Pavés",
        "district": "Hauts-Pavés",
    },
]


# ============================================================
# GÉNÉRATION DES COORDONNÉES
# ============================================================

def generate_coordinates(location, radius_meters=150):
    """
    Génère des coordonnées aléatoires autour d'un point de référence.

    radius_meters représente le rayon maximal autour du point.
    """

    distance = random.uniform(0, radius_meters)
    angle = random.uniform(0, 2 * math.pi)

    lat_offset = (
        distance * math.cos(angle) / 111320
    )

    lon_offset = (
        distance * math.sin(angle)
        / (111320 * math.cos(math.radians(location["lat"])))
    )

    return {
        "lat": location["lat"] + lat_offset,
        "long": location["long"] + lon_offset,
    }


# ============================================================
# GÉNÉRATION D'UNE SITUATION GÉOGRAPHIQUE
# ============================================================

def generate_situgeo(
    user_id,
    location=None,
    radius_meters=150,
    gps_consent=None
):
    """
    Génère une situation géographique pour un utilisateur.
    """

    if location is None:
        location = random.choice(FRENCH_LOCATIONS)

    # Consentement GPS aléatoire si aucune valeur n'est imposée.
    if gps_consent is None:
        gps_consent = random.choice([True, False])

    coordinates = generate_coordinates(
        location,
        radius_meters
    )

    return {
        "user_id": str(user_id),
        "city": location["city"],
        "postcode": location["postcode"],
        "department": location["department"],
        "lat": coordinates["lat"],
        "long": coordinates["long"],
        "gps_consent": gps_consent,
        "street": location["street"],
        "district": location["district"],
    }


# ============================================================
# INSERTION EN BASE DE DONNÉES
# ============================================================

def _insert_situgeo(cursor, generated):
    """
    Insère ou met à jour la situation géographique d'un utilisateur.
    """

    cursor.execute(
        """
        INSERT INTO localisation (
            user_id,
            city,
            postcode,
            department,
            lat,
            long,
            gps_consent,
            street,
            district
        )
        VALUES (
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s
        )
        ON CONFLICT (user_id)
        DO UPDATE SET
            city = EXCLUDED.city,
            postcode = EXCLUDED.postcode,
            department = EXCLUDED.department,
            lat = EXCLUDED.lat,
            long = EXCLUDED.long,
            gps_consent = EXCLUDED.gps_consent,
            street = EXCLUDED.street,
            district = EXCLUDED.district;
        """,
        (
            generated["user_id"],
            generated["city"],
            generated["postcode"],
            generated["department"],
            generated["lat"],
            generated["long"],
            generated["gps_consent"],
            generated["street"],
            generated["district"],
        )
    )


# ============================================================
# SEED CLASSIQUE
# ============================================================

def situgeo(
    db_conf,
    user_ids,
    radius_meters=150,
    city=None
):
    """
    Génère les situations géographiques uniquement
    pour les utilisateurs transmis dans user_ids.

    Si city est renseignée, les utilisateurs seront
    répartis dans les quartiers de cette ville.
    """

    if not user_ids:
        print("Aucun utilisateur à géolocaliser.")
        return []

    # Évite de traiter deux fois le même utilisateur.
    user_ids = list(dict.fromkeys(user_ids))

    locations = FRENCH_LOCATIONS

    if city:
        locations = [
            location
            for location in FRENCH_LOCATIONS
            if location["city"].lower() == city.lower()
        ]

        if not locations:
            raise ValueError(
                f"Aucun emplacement trouvé pour la ville : {city}"
            )

    generated_locations = []

    try:
        with psycopg.connect(**db_conf) as connection:
            with connection.cursor() as cursor:

                for user_id in user_ids:
                    location = random.choice(locations)

                    generated = generate_situgeo(
                        user_id=user_id,
                        location=location,
                        radius_meters=radius_meters
                    )

                    _insert_situgeo(cursor, generated)
                    generated_locations.append(generated)

        print(
            f"{len(generated_locations)} situations géographiques "
            f"créées ou mises à jour."
        )

    except Exception:
        print("Erreur lors de la création des situations géographiques.")
        raise

    return generated_locations


# ============================================================
# SEED DE PROXIMITÉ : UN SEUL QUARTIER
# ============================================================

def situgeo_nearby(
    db_conf,
    user_ids,
    city="Paris",
    district="Le Marais",
    radius_meters=500
):
    """
    Place tous les utilisateurs transmis autour d'un même quartier.

    Pratique pour tester :
    - les recherches d'utilisateurs proches ;
    - les distances entre utilisateurs ;
    - les filtres géographiques ;
    - les résultats dans un rayon donné.
    """

    if not user_ids:
        print("Aucun utilisateur à géolocaliser.")
        return []

    locations = [
        location
        for location in FRENCH_LOCATIONS
        if (
            location["city"].lower() == city.lower()
            and location["district"].lower() == district.lower()
        )
    ]

    if not locations:
        raise ValueError(
            f"Quartier introuvable : {district}, {city}"
        )

    location = locations[0]
    user_ids = list(dict.fromkeys(user_ids))

    generated_locations = []

    try:
        with psycopg.connect(**db_conf) as connection:
            with connection.cursor() as cursor:

                for user_id in user_ids:
                    generated = generate_situgeo(
                        user_id=user_id,
                        location=location,
                        radius_meters=radius_meters
                    )

                    _insert_situgeo(cursor, generated)
                    generated_locations.append(generated)

        print(
            f"{len(generated_locations)} utilisateurs placés "
            f"autour de {district}, {city} "
            f"(rayon : {radius_meters} m)."
        )

    except Exception:
        print("Erreur lors du seed de proximité.")
        raise

    return generated_locations


# ============================================================
# EXPORT CSV
# ============================================================

def generate_csv(
    situgeo_list,
    filename="fake_situgeo.csv"
):
    """
    Exporte les situations géographiques générées dans un CSV.
    """

    if not situgeo_list:
        print("Aucune donnée à exporter.")
        return

    fieldnames = [
        "user_id",
        "city",
        "postcode",
        "department",
        "lat",
        "long",
        "gps_consent",
        "street",
        "district",
    ]

    with open(
        filename,
        mode="w",
        newline="",
        encoding="utf-8"
    ) as csv_file:

        writer = csv.DictWriter(
            csv_file,
            fieldnames=fieldnames,
            delimiter=";"
        )

        writer.writeheader()
        writer.writerows(situgeo_list)

    print(f"Fichier CSV généré : {filename}")
