# Matcha — Documentation du Frontend

## 1. Présentation du projet

**Matcha** est une application web développée avec Vue.js 3 et TypeScript. Elle permet aux utilisateurs de consulter des profils et d'interagir avec d'autres utilisateurs.

Ce document présente l'organisation du frontend, les différents écrans de l'application et les composants réutilisables.



> La commande `type-check` est à vérifier dans le fichier `package.json` du projet.

## 2. Architecture du frontend

### Organisation des fichiers

| Dossier / fichier | Rôle | Chemin |
|---|---|---|
| `src/vues/` | Écrans et pages de l'application | `front-matcha/src/vues/` |
| `src/components/` | Composants Vue réutilisables | `front-matcha/src/components/` |
| `src/services/` | Appels API et logique de communication | `front-matcha/src/services/` |
| `src/types/` | Interfaces et types TypeScript | `front-matcha/src/types/` |
| `src/router/` | Définition des routes | `front-matcha/src/router/`
| `src/assets/` | Images, icônes et ressources statiques | `front-matcha/src/assets/` |
| `src/App.vue` | Composant racine de l'application | `front-matcha/src/App.vue` |
| `src/main.ts` | Point d'entrée du frontend | `front-matcha/src/main.ts` |

### Fonctionnement général

1. `main.ts` initialise l'application Vue.
2. `App.vue` constitue le composant racine.
3. Le routeur permet de naviguer entre les écrans.
4. Les vues assemblent les composants nécessaires à chaque écran.
5. Les composants gèrent l'affichage et les interactions réutilisables.
6. Les services communiquent avec l'API.
7. Les types TypeScript décrivent les données utilisées par le frontend.

## 3. Écrans de l'application


### 3.1 Écran d'accueil

| Information | Valeur |
|---|---|
| Nom de l'écran | Accueil |
| Fichier Vue | [HomePage](src/vues/navigation/HomePage.vue#homepage) |
| Route | `[/] (quand log); [/home]` |
| Objectif | Présenter l'application et orienter l'utilisateur |
| [Composants utilisés](src/components/documentation_components/sommaire_components.md) | `[AppLayout, SearchBarWithOption, ListProfileCard]` |
| Services API | `[À renseigner]` |

**Fonctionnement :**
- Présentation initiale de l'application.
- Navigation vers les fonctionnalités principales.

### 3.2 Écran de connexion

| Information | Valeur |
|---|---|
| Nom de l'écran | Connexion |
| Fichier Vue | `[À renseigner : chemin du fichier .vue]` |
| Route | `[À renseigner : URL de la route]` |
| Objectif | Permettre à un utilisateur de se connecter |
| [Composants utilisés](src/components/documentation_components/sommaire_components.md) | `[À renseigner]` |
| Services API | `[À renseigner]` |

**Fonctionnement :**
- Saisie des informations d'identification.
- Validation des champs.
- Envoi de la requête de connexion.
- Affichage des erreurs ou confirmation du succès.

### 3.3 Écran d'inscription

| Information | Valeur |
|---|---|
| Nom de l'écran | Inscription |
| Fichier Vue | `[À renseigner : chemin du fichier .vue]` |
| Route | `[À renseigner : URL de la route]` |
| Objectif | Créer un compte utilisateur |
| [Composants utilisés](src/components/documentation_components/sommaire_components.md) `[À renseigner]` |
| Services API | `[À renseigner]` |

**Fonctionnement :**
- Saisie des informations nécessaires à la création du compte.
- Vérification des champs.
- Envoi des données à l'API.
- Affichage du résultat de l'inscription.

### 3.4 Écran de recherche de profils

| Information | Valeur |
|---|---|
| Nom de l'écran | Recherche de profils |
| Fichier Vue | `[À renseigner : chemin du fichier .vue]` |
| Route | `[À renseigner : URL de la route]` |
| Objectif | Rechercher et consulter des profils |
| Composants utilisés | `SearchBar`, `ProfileCard`, `listProfileCard` — à confirmer |
| Services API | `[À renseigner]` |

**Fonctionnement :**
- Recherche à partir de critères ou de termes saisis.
- Affichage des profils correspondants.
- Consultation d'un profil et interactions disponibles.

### 3.5 Écran de profil utilisateur

| Information | Valeur |
|---|---|
| Nom de l'écran | Profil utilisateur |
| Fichier Vue | `[À renseigner : chemin du fichier .vue]` |
| Route | `[À renseigner : URL de la route]` |
| Objectif | Afficher les informations d'un utilisateur |
| Composants utilisés | `[À renseigner]` |
| Services API | `[À renseigner]` |

**Fonctionnement :**
- Affichage des informations du profil.
- Présentation des photos, descriptions et caractéristiques disponibles.
- Accès aux interactions proposées par l'application.

### 3.6 Écran de gestion des utilisateurs bloqués

| Information | Valeur |
|---|---|
| Nom de l'écran | Utilisateurs bloqués |
| Fichier Vue | `[À renseigner : chemin du fichier .vue]` |
| Route | `[À renseigner : URL de la route]` |
| Objectif | Gérer les relations de blocage entre utilisateurs |
| Composants utilisés | `Notification` |
| Services API | `@/services/api_blocked.ts` |

**Fonctionnement :**
- Blocage d'un utilisateur à partir de deux identifiants.
- Suppression d'une relation de blocage.
- Récupération de la liste des utilisateurs bloqués par un utilisateur.
- Mise à jour de la liste à partir des données renvoyées par l'API.
- Affichage du résultat de chaque requête à l'aide du composant `Notification`.

### 3.7 Écran de paramètres

| Information | Valeur |
|---|---|
| Nom de l'écran | Paramètres |
| Fichier Vue | `[À renseigner : chemin du fichier .vue]` |
| Route | `[À renseigner : URL de la route]` |
| Objectif | Gérer les préférences du compte |
| Composants utilisés | `[À renseigner]` |
| Services API | `[À renseigner]` |

**Fonctionnement :**
- Consultation et modification des paramètres disponibles.
- Enregistrement des modifications via l'API, si nécessaire.
- Affichage du résultat des opérations.

### 3.8 Autres écrans

Ajouter une section par écran supplémentaire en reprenant le modèle suivant :

| Information | Valeur |
|---|---|
| Nom de l'écran | `[Nom de l'écran]` |
| Fichier Vue | `[Chemin du fichier .vue]` |
| Route | `[URL de la route]` |
| Objectif | `[Rôle de l'écran]` |
| Composants utilisés | `[Noms des composants]` |
| Services API | `[Services utilisés]` |

**Fonctionnement :**
- `[Décrire les principales actions et interactions]`

## 6. Services API

Les services regroupent les fonctions permettant au frontend de communiquer avec le backend.

| Service | Fonction | Chemin |
|---|---|---|
| Gestion des utilisateurs bloqués | Blocage, suppression et récupération des relations de blocage | `src/services/api_blocked.ts` |
| Authentification | `[À renseigner]` | `[À renseigner]` |
| Profils utilisateurs | `[À renseigner]` | `[À renseigner]` |
| Recherche | `[À renseigner]` | `[À renseigner]` |
| Interaction | Création de l'intéraction, récupérations en fonction du type | `src/services/api_interactions.ts` |

Les services doivent retourner des résultats exploitables par les vues et les composants. Les opérations peuvent notamment utiliser le composant `Notification` pour informer l'utilisateur du succès ou de l'échec d'une requête.

## 7. Conventions de développement

- Utiliser Vue 3 avec la Composition API et `<script setup lang="ts">`.
- Définir les types et interfaces dans les fichiers TypeScript adaptés.
- Réutiliser les composants communs plutôt que dupliquer leur code.
- Centraliser les appels backend dans les services.
- Gérer les états de chargement, les erreurs et les retours utilisateur.
- Maintenir à jour la documentation des écrans et des composants.

## 8. Informations restant à compléter

- [*] Liste exacte des écrans et de leurs routes.
- [ ] Chemin réel des fichiers `.vue` de chaque écran.
- [*] Emplacement définitif du dossier `docs/`.
- [ ] Liste complète des composants réutilisables.
- [ ] Liste complète des services API.
