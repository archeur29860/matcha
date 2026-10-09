# Sommaire des composants

Ce document répertorie les composants réutilisables du frontend Matcha et donne accès à leur documentation détaillée.

> [Retour à la documentation front](/front-matcha/front-readme.md)

## Liste des composants

| Composant | Description | Documentation |
|---|---|---|
| `SearchBarWithOption` | Barre de recherche avec suggestions | [Voir la documentation](./searchbar.md) |
| `Input` | Champ de saisie réutilisable | [Voir la documentation](./input.md) |
| `ProfileCard` | Carte affichant les informations d'un profil utilisateur | [Voir la documentation](./profileCard.md) |
| `listProfileCard` | Liste de cartes de profils utilisateurs | [Voir la documentation](./listProfileCard.md) |
| `Notification` | Notification de succès, d'erreur, d'avertissement ou d'information | [Voir la documentation](./notification.md) |

## Organisation

Chaque documentation de composant présente :

1. **Nom et import**
2. **Props definition**
3. **Emit definition**
4. **Fonctionnement global**

## Ajouter un composant

Lorsqu'un nouveau composant est ajouté au projet :

1. Créer son fichier Vue dans `src/components/`.
2. Rédiger sa documentation dans `src/components/documentation_components`.
3. Ajouter une ligne dans le tableau ci-dessus.
4. Vérifier que le lien vers sa documentation fonctionne.
