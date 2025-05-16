# Nebulosa – Backend (Django) README

> **Last updated:** 14 May 2025
> This document is the single source of truth for the Nebulosa backend. It explains *why* each component exists, *how* everything fits together, and *what* to do when you return to the project after a break.

---

## 1 · What is Nebulosa ?

Nebulosa est une application mobile communautaire où les utilisateurs partagent et découvrent des **lieux** liés à des **thèmes** (tags).

*Exemple :* Un supporter du FC Barcelone en séjour à Londres recherche le tag « Barça » → l’app lui affiche les bars, associations et points de rendez‑vous pertinents sur une carte et dans une liste triée par pertinence.

---

## 2 · High‑Level Architecture

```
┌────────────┐        HTTPS/JSON         ┌───────────────┐
│ React Native│  ⇆  API (DRF + JWT)  ⇆  │  Django 5.1.5 │
└────────────┘                          │  Python 3.11  │
                    │                   │   Apps:       │
                    ▼                   │   • users     │
                 PostgreSQL 15 ◄────────┤   • places    │
                                        │   • tags      │
                     (docker)           └───────────────┘
```

* **Front‑end :** React Native (repo séparé).
* **Back‑end :** Django + DRF + SimpleJWT.
* **DB :** PostgreSQL 15, lat/lng stockés en `FloatField`.
* **Docker :** un conteneur `web`, un conteneur `db` (voir `docker-compose.yml`).

---

## 3 · Tech Stack

| Layer     | Tech                          | Version / Remarque               |
| --------- | ----------------------------- | -------------------------------- |
| language  | Python                        | 3.11‑slim (Docker)               |
| framework | Django                        | 5.1.5                            |
| API       | Django REST Framework         | 3.15.2                           |
| Auth      | djangorestframework‑simplejwt | 5.4.0 (access 24 h, refresh 7 j) |
| DB        | PostgreSQL                    | 15 (image officielle)            |
| Container | Docker Compose                | v3.8                             |
| Tests     | Django test runner            | (pytest plus tard possible)      |
| Env vars  | python‑dotenv                 | `.env.dev`, etc.                 |
| Misc      | asgiref 3.8.1, sqlparse 0.5.3 |                                  |
| NLP       | spaCy                         | fr_core_news_md pour la recherche sémantique |

---

## 4 · Local Development Setup

```bash
# Pré‑requis : Docker & Docker Compose installés

cp .env.example .env.dev        # renseigner les variables si besoin

docker compose up --build       # lance web:8000 et db:5432

# App accessible sur http://localhost:8000/
# API root: http://localhost:8000/api/
```

**Hot reload :** le volume `.:/app` dans `docker-compose.yml` permet le rechargement auto de Django lors des modifications.

> *Tip :* pour ouvrir un shell Django dans le conteneur :
> `docker compose exec web python manage.py shell`.

---

## 5 · Project Structure

```
nebulosa-back/
├─ places/           # app Django pour les lieux
│  ├─ models.py
│  ├─ serializers.py
│  ├─ views.py
│  └─ urls.py
├─ users/            # app Django pour les profils
│  ├─ models.py
│  ├─ serializers.py
│  ├─ services.py
│  ├─ signals.py
│  └─ urls.py
├─ tags/             # app Django pour les tags
│  ├─ models.py
│  ├─ serializers.py
│  ├─ services.py
│  ├─ views.py
│  └─ urls.py
├─ nebulosa_back/    # config Django
│  ├─ settings/
│  │   ├─ base.py
│  │   ├─ dev.py
│  │   ├─ preprod.py
│  │   └─ prod.py
│  ├─ urls.py
│  └─ wsgi.py
└─ docker-compose.yml / Dockerfile
```

---

## 6 · Apps & Domain Logic

### 6.1 places

| Model           | Champs clés                                                          | Description                 |
| --------------- | -------------------------------------------------------------------- | --------------------------- |
| **Place**       | name, description, FK address, created\_at, updated\_at              | Lieu géolocalisé.           |
| **PlaceAdress** | street, number, city, state, country, zip\_code, latitude, longitude | Adresse + coords (doubles). |

#### Endpoints

| Method | URL                 | Permission | Notes                                |
| ------ | ------------------- | ---------- | ------------------------------------ |
| GET    | `/api/places/`      | Auth       | Liste paginée des lieux.             |
| GET    | `/api/places/{id}/` | Auth       | Détail du lieu.                      |
| POST   | `/api/places/`      | Auth       | Crée un lieu avec adresse imbriquée. |

### 6.2 users

| Model           | Champs                               | Description              |
| --------------- | ------------------------------------ | ------------------------ |
| **UserProfile** | 1‑to‑1 vers `auth.User`, birth\_date | Métadonnées utilisateur. |

#### Endpoints

| Method | URL                | Permission | Notes                             |
| ------ | ------------------ | ---------- | --------------------------------- |
| POST   | `/api/users/`      | Public     | Inscription : User + UserProfile. |
| GET    | `/api/users/{id}/` | IsOwner    | Récupère son profil.              |

### 6.3 tags

| Model           | Champs clés                                                          | Description                 |
| --------------- | -------------------------------------------------------------------- | --------------------------- |
| **Tag**         | name, creator, created_at, updated_at                              | Tag générique.              |
| **PlaceTag**    | tag, place, description, grade, creator, created_at, updated_at    | Association tag-lieu.       |

#### Endpoints

| Method | URL                          | Permission | Notes                                |
| ------ | ---------------------------- | ---------- | ------------------------------------ |
| POST   | `/api/tags/search_similar/`  | Auth       | Recherche sémantique de tags similaires. |

---

## 7 · Authentication & Permissions

* **JWT** via `djangorestframework_simplejwt` :

  * `/api/token/` → access + refresh.
  * `/api/token/refresh/`.
* `REST_FRAMEWORK.DEFAULT_PERMISSION_CLASSES = [IsAuthenticated]` (défaut global).
* Permissions custom :

  * `IsOwnerUser` : accès à son propre profil.
  * `IsAuthenticated` alias project‑wide.

---

## 8 · Settings & Environments

| Fichier      | Héritage | Usage                                           |
| ------------ | -------- | ----------------------------------------------- |
| `base.py`    | —        | Paramètres communs (DB, JWT, INSTALLED\_APPS…). |
| `dev.py`     | `base`   | DEBUG = True, hosts localhost.                  |
| `preprod.py` | `base`   | Déployé sur *preprod.nebulosa.com*.             |
| `prod.py`    | `base`   | Déploiement prod.                               |

Changement d’environnement : variable `DJANGO_SETTINGS_MODULE` dans `docker-compose.yml` ou via CI.

---

## 9 · Database

* **Schema actuel :** coord lat/lng en `FloatField`.
* Docker Compose expose `5432`.

> **Init DB** : lors du premier démarrage `docker compose up`, Django exécute automatiquement les migrations (voir `entrypoint` futur si besoin).

---

## 10 · Testing

* Runner : `python manage.py test`.
* Couverture minimale : factories + tests unités sur sérializers + vues.

---

## 11 · Deployment

1. **Préproduction** : settings `preprod.py`, image Docker, DB managed.
2. **Production** : idem avec `prod.py`.

   * Variables sensibles (SECRET\_KEY, DB creds) fournies via env vars.

---

## 12 · Coding Style & Conventions

* PEP 8 + isort + black *(add pre‑commit hook).*
* Commits : *Conventional Commits* (`feat:`, `fix:`, `docs:`…).
* Branching : *Git Flow* simplifié (`main`, `dev`, feature branches).

---

## 13 · Contacts

| Rôle         | Nom         | GitHub                                |
| ------------ | ----------- | ------------------------------------- |
| Lead / Admin | **stonoly** | [stonoly](https://github.com/stonoly) |