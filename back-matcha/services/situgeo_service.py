from psycopg.errors import (
    IntegrityError,
    ForeignKeyViolation,
    CheckViolation,
    NotNullViolation,
    UniqueViolation,
)
import requests

from database.connection import get_db
from utils.exceptions import AppError



def upsert_user_location(
    user_id: str,
    city: str,
    postcode: str,
    department: str,
    lat: float,
    long: float,
    gps_consent: bool,
    street: str = None,
    district: str = None
) -> dict:
    db = get_db()

    try:
        with db.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO localisation (
                    user_id,
                    street,
                    district,
                    city,
                    postcode,
                    department,
                    lat,
                    long,
                    gps_consent
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (user_id)
                DO UPDATE SET
                    street = EXCLUDED.street,
                    district = EXCLUDED.district,
                    city = EXCLUDED.city,
                    postcode = EXCLUDED.postcode,
                    department = EXCLUDED.department,
                    lat = EXCLUDED.lat,
                    long = EXCLUDED.long,
                    gps_consent = EXCLUDED.gps_consent,
                    updated_at = CURRENT_TIMESTAMP
                RETURNING *
                """,
                (
                    user_id,
                    street,
                    district,
                    city,
                    postcode,
                    department,
                    lat,
                    long,
                    gps_consent
                ),
            )

            location = cursor.fetchone()

        db.commit()
        return location

    except ForeignKeyViolation as e:
        db.rollback()

        if e.diag.constraint_name == "fk_user":
            raise AppError(
                code="USER_NOT_FOUND",
                message="The user does not exist",
                status_code=404,
            )

        raise AppError(
            code="FOREIGN_KEY_VIOLATION",
            message="A referenced resource does not exist",
            status_code=409,
        )

    except CheckViolation as e:
        db.rollback()

        constraint = e.diag.constraint_name

        if constraint == "chk_user_latitude":
            raise AppError(
                code="INVALID_LATITUDE",
                message="Latitude must be between -90 and 90",
                status_code=400,
            )

        if constraint == "chk_user_longitude":
            raise AppError(
                code="INVALID_LONGITUDE",
                message="Longitude must be between -180 and 180",
                status_code=400,
            )

        raise AppError(
            code="CHECK_VIOLATION",
            message="The location contains invalid values",
            status_code=400,
        )

    except NotNullViolation as e:
        db.rollback()

        raise AppError(
            code="MISSING_REQUIRED_FIELD",
            message="A required location field is missing",
            status_code=400,
        )

    except UniqueViolation as e:
        db.rollback()

        raise AppError(
            code="LOCATION_ALREADY_EXISTS",
            message="The location already exists",
            status_code=409,
        )

    except IntegrityError:
        db.rollback()

        raise AppError(
            code="INTEGRITY_ERROR",
            message="The location could not be saved",
            status_code=409,
        )

    except Exception:
        db.rollback()
        raise


BASE_URL_API_SITUGEO = "https://data.geopf.fr/geocodage"

def extract_location(feature: dict) -> dict:
    properties = feature.get("properties") or {}
    geometry = feature.get("geometry") or {}
    coordinates = geometry.get("coordinates") or []

    if len(coordinates) < 2:
        raise ValueError("Coordonnées géographiques invalides.")

    lon, lat = coordinates[:2]

    return {
        "street": properties.get("street"),
        "district": properties.get("district"),
        "city": properties.get("city"),
        "postcode": properties.get("postcode"),
        "department": properties.get("context"),
        "latitude": lat,
        "longitude": lon,
    }


def geocode_city(city_name: str) -> dict | None:
    """
    Géocodage direct :
    Accepte une ville, un quartier, une rue ou une adresse complète.
    Retourne le résultat le plus pertinent.
    """

    endpoint = f"{BASE_URL_API_SITUGEO}/search"

    city_name = city_name.strip()

    if not city_name:
        raise AppError(
            code="SITUGEO_ERROR_INVALID_QUERY",
            message="Location cannot be empty",
            status_code=400,
        )

    params = {
        "q": city_name,
        "limit": 5,
    }

    try:
        response = requests.get(
            endpoint,
            params=params,
            timeout=10,
        )

        response.raise_for_status()

        data = response.json()
        features = data.get("features", [])

        if not features:
            raise AppError(
                code="SITUGEO_ERROR_NOT_FOUND",
                message="Location not found",
                status_code=404,
            )

        best_match = features[0]

        return extract_location(best_match)

    except requests.exceptions.Timeout:
        raise AppError(
            code="SITUGEO_ERROR_TIMEOUT",
            message="Geocoding service timeout",
            status_code=504,
        )

    except requests.exceptions.HTTPError as e:
        status = e.response.status_code if e.response is not None else 502

        print(
            f"Erreur API IGN : {status} - "
            f"{e.response.text if e.response is not None else str(e)}"
        )

        raise AppError(
            code="SITUGEO_ERROR_API",
            message=f"Geocoding API returned HTTP {status}",
            status_code=502,
        )

    except requests.exceptions.RequestException as e:
        raise AppError(
            code="SITUGEO_ERROR_REQUEST",
            message=f"Geocoding request failed: {str(e)}",
            status_code=502,
        )

    except (KeyError, IndexError, TypeError, ValueError) as e:
        raise AppError(
            code="SITUGEO_ERROR_RESULT",
            message=f"Invalid geocoding result: {str(e)}",
            status_code=422,
        )


def reverse_geocode(lat: float, lon: float) -> dict | None:
    """
    Géocodage inverse :
    Convertit des coordonnées GPS en adresse ou lieu le plus proche.
    """

    endpoint = f"{BASE_URL_API_SITUGEO}/reverse"

    params = {
        "lat": lat,
        "lon": lon,
        "limit": 5,
    }

    try:
        response = requests.get(
            endpoint,
            params=params,
            timeout=10,
        )

        response.raise_for_status()

        data = response.json()
        features = data.get("features", [])

        if not features:
            return None

        best_match = features[0]

        return extract_location(best_match)

    except requests.exceptions.Timeout:
        raise AppError(
            code="SITUGEO_ERROR_TIMEOUT",
            message="Reverse geocoding service timeout",
            status_code=504,
        )

    except requests.exceptions.HTTPError as e:
        status = e.response.status_code if e.response is not None else 502

        print(f"Erreur API IGN reverse : {status}")

        raise AppError(
            code="SITUGEO_ERROR_API",
            message=f"Reverse geocoding API returned HTTP {status}",
            status_code=502,
        )

    except requests.exceptions.RequestException as e:
        raise AppError(
            code="SITUGEO_ERROR_REQUEST",
            message=f"Reverse geocoding request failed: {str(e)}",
            status_code=502,
        )

    except (KeyError, IndexError, TypeError, ValueError) as e:
        raise AppError(
            code="SITUGEO_ERROR_RESULT",
            message=f"Invalid reverse geocoding result: {str(e)}",
            status_code=422,
        )
