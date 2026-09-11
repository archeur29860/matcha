# Normes API — Flask / Vue

## 1. Architecture

Chaque fonctionnalité doit respecter cette séparation :

```text
models/
    └── feature_m.py

routes/
    └── feature_bp.py

services/
    └── feature_service.py

utils/
    ├── exceptions.py
    ├── error_handler.py
    ├── response.py
    └── validate.py
```

Responsabilités :

* `models/` : table dans postgre.
* `routes/` : HTTP, récupération des données et validation des entrées.
* `services/` : logique métier et accès à la base de données.
* `utils/exceptions.py` : exceptions applicatives.
* `utils/error_handler.py` : transformation des exceptions en réponses HTTP.
* `utils/response.py` : format standard des réponses.
* `utils/validate.py` : validations réutilisables.

---

# 2. Routes

Une route doit uniquement :

1. récupérer les données ;
2. vérifier leur présence ;
3. valider leur format ;
4. appeler le service ;
5. retourner une réponse standardisée.

Structure :

```python
@blueprint.route("/", methods=["POST"])
def create_resource():

    data = request.get_json()

    if not data:
        raise ValidationError("JSON body required")

    if "field" not in data:
        raise ValidationError("field is required")

    field = validate_xxx(
        data["field"],
        "field"
    )

    result = service.create_resource(field)

    return success(result, 201)
```

La route ne doit pas :

* contenir de SQL ;
* gérer `try/except Exception` ;
* faire de `print()` pour les erreurs ;
* construire manuellement les réponses JSON ;
* contenir de logique métier complexe.

---

# 3. Services

Le service contient la logique métier et les opérations SQL.

Structure :

```python
def create_resource(...):

    try:
        result = db.session.execute(
            text("""
                ...
            """),
            {
                ...
            }
        )

        result = result.mappings().one()

        db.session.commit()

        return dict(result)

    except IntegrityError:
        db.session.rollback()

        raise ConflictError(
            "Resource already exists"
        )

    except Exception:
        db.session.rollback()
        raise
```

## Règles

Toute transaction SQL doit respecter :

```text
try
 ├── execute
 ├── récupération résultat
 └── commit

except erreur connue
 ├── rollback
 └── raise AppError

except erreur inconnue
 ├── rollback
 └── raise
```

Ne jamais masquer une exception avec :

```python
except Exception:
    return None
```

Une erreur doit remonter jusqu'au `error_handler`.

---

# 4. Exceptions

Toutes les erreurs applicatives doivent hériter de `AppError`.

```python
class AppError(Exception):

    def __init__(
        self,
        code,
        message,
        status_code=400,
        details=None
    ):
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details

        super().__init__(message)
```

Exemples exceptions spécialisées :

```python
class ValidationError(AppError)
```

```python
class NotFoundError(AppError)
```

```python
class ConflictError(AppError)
```

---

# 5. Codes HTTP

| HTTP  | Code               | Utilisation                      |
| ----- | ------------------ | -------------------------------- |
| `200` | —                  | Requête réussie                  |
| `201` | —                  | Ressource créée                  |
| `204` | —                  | Succès sans contenu              |
| `400` | `VALIDATION_ERROR` | Données invalides                |
| `401` | `UNAUTHORIZED`     | Authentification requise         |
| `403` | `FORBIDDEN`        | Permission refusée               |
| `404` | `NOT_FOUND`        | Ressource inexistante            |
| `409` | `CONFLICT`         | Conflit / doublon                |
| `422` | `INVALID_DATA`     | Données sémantiquement invalides |
| `500` | `INTERNAL_ERROR`   | Erreur serveur                   |

Les codes métier doivent être écrits en `UPPER_SNAKE_CASE`.

```text
VALIDATION_ERROR
NOT_FOUND
CONFLICT
BLOCK_ALREADY_EXISTS
UNAUTHORIZED
FORBIDDEN
INTERNAL_ERROR
```

---

# 6. Réponses API

Toutes les réponses doivent utiliser `success()` ou `error()`.

## Succès

```python
return success(data, 200)
```

Format :

```json
{
    "success": true,
    "data": {},
    "error": null
}
```

## Succès sans données

```python
return success(status=204)
```

## Erreur

```python
raise ValidationError(...)
```

ou :

```python
raise ConflictError(...)
```

L'`error_handler` transforme automatiquement l'exception.

Format :

```json
{
    "success": false,
    "data": null,
    "error": {
        "code": "VALIDATION_ERROR",
        "message": "...",
        "details": {}
    }
}
```

Le frontend doit donc toujours pouvoir utiliser :

```javascript
response.success
response.data
response.error
```

---

# 7. Error Handler

Le handler est le point central de gestion des exceptions.

```python
def register_error_handlers(app):

    @app.errorhandler(AppError)
    def handle_app_error(e):

        return error(
            e.code,
            e.message,
            e.status_code,
            e.details
        )

    @app.errorhandler(Exception)
    def handle_unknown_error(e):

        app.logger.exception(
            "Unhandled exception"
        )

        return error(
            "INTERNAL_ERROR",
            "An internal error occurred",
            500
        )
```

## Principe

```text
Route
  │
  ├── ValidationError
  │
  └── Service
        │
        ├── ConflictError
        ├── NotFoundError
        └── Exception
              │
              ▼
        error_handler
              │
              ▼
        réponse JSON standardisée
```

Une route ne doit donc pas gérer individuellement les erreurs applicatives.

---

# 8. Validation

Les validations réutilisables doivent être placées dans :

```text
utils/validate.py
```

Exemple :

```python
def validate_uuid(value, field_name):

    try:
        return UUID(str(value))

    except (ValueError, TypeError, AttributeError):

        raise ValidationError(
            f"{field_name} must be a valid UUID",
            {
                "field": field_name,
                "value": value
            }
        )
```

Utilisation :

```python
user_id = validate_uuid(
    data["user_id"],
    "user_id"
)
```

La validation doit lever une exception, pas retourner `None`.

---

# 9. Frontend Vue

Le frontend doit traiter toutes les réponses avec la même structure.

Structure générale :

```javascript
const response = await fetch(url, options)

const result = await response.json()

if (!response.ok) {

    const error = result.error

    // error.code
    // error.message
    // error.details

    return
}

const data = result.data
```

## Succès

```javascript
if (result.success) {
    const data = result.data
}
```

## Erreur

```javascript
if (!response.ok) {

    const { code, message, details } = result.error

    switch (code) {

        case "VALIDATION_ERROR":
            break

        case "NOT_FOUND":
            break

        case "CONFLICT":
            break

        default:
            break
    }
}
```

---

# 10. Convention frontend recommandée

Créer une fonction centralisée pour les requêtes API.

```text
src/
└── services/
    └── api.ts
```

Toutes les requêtes doivent passer par cette couche.

```typescript
export async function apiFetch(url, options = {}) {

    const response = await fetch(url, options);

    const result = await response.json();

    if (!response.ok) {
        throw result.error;
    }

    return result.data;
}
```

Utilisation :

```typescript
try {

    const data = await apiFetch(
        "http://localhost:5000/api/blocked/",
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                user_id,
                user_id_blocked
            })
        }
    );

} catch (error) {

    console.error(error.code);
    console.error(error.message);
    console.error(error.details);
}
```

Le composant Vue ne doit donc pas connaître la structure HTTP complète.

---

# 11. Règle principale

Une erreur ne doit jamais être silencieuse.

À éviter :

```python
except Exception:
    return None
```

À utiliser :

```python
except Exception:
    db.session.rollback()
    raise
```

Cette convention permet d'avoir **une seule structure de réponse pour toute l'API**, indépendamment de la fonctionnalité concernée.
