# ProfileCard

## Nom et import

**Composant :** `ProfileCard`

```ts
import ProfileCard from '@/components/ProfileCard.vue'
```

## Props definition

| Prop | Type | Requis | Description |
|---|---|---:|---|
| `profile` | `ProfileCard` | Oui | Données du profil à afficher |

Le type `ProfileCard` est importé depuis :

```ts
import type { ProfileCard } from '@/types/profile'
```

Le profil contient notamment les informations suivantes :

```ts
interface ProfileCard {
  user_id: string
  username: string
  age: number
  image: string
  location: string
  tags: string[]
  bio: string
  online: boolean
  popularity: number
}
```

## Emit definition

| Event | Payload | Description |
|---|---|---|
| `like` | `string` (`user_id`) | Déclenché lors du clic sur le bouton "J'aime" |
| `clickOnProfile` | `string` (`user_id`) | Déclenché lors du clic sur le nom du profil |

```ts
emit('like', profile.user_id)
emit('clickOnProfile', profile.user_id)
```

## Fonctionnement global

Le composant affiche une carte de profil contenant :

- la photo du profil ;
- le statut **En ligne** si `online` est à `true` ;
- le niveau de popularité et sa progression ;
- le nom et l'âge ;
- la localisation ;
- les tags ;
- la biographie ;
- un bouton pour liker le profil.

La popularité est automatiquement catégorisée :

| Score | Label |
|---:|---|
| `>= 90` | Ultra populaire |
| `>= 70` | Très populaire |
| `>= 40` | Populaire |
| `< 40` | Nouveau |

Le composant est responsive et adapte sa taille sur les écrans de moins de `600px`.