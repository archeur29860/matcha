# listProfileCard

## Nom et import

**Composant :** `listProfileCard`


**Import :**

```ts
import ListProfileCard from '@/components/listProfileCard.vue'
```

## Props definition

| Prop | Type | Requis | Description |
|---|---|---:|---|
| `profiles` | `ProfileCardType[]` | Oui | Liste des profils à afficher |

```ts
interface Props {
  profiles: ProfileCardType[]
}
```
```ts
export interface ProfileCard {
  user_id: string
  username: string
  age: number
  location: string
  online: boolean
  tags: string[]
  bio: string
  image: string
  popularity: number
}
```

## Emit definition

| Event | Payload | Description |
|---|---|---|
| `like` | `string` (`user_id`) | Relaye le like du profil |
| `clickOnProfile` | `string` (`user_id`) | Relaye le clic sur le profil |

```ts
emit('like', user_id)
emit('clickOnProfile', user_id)
```

## Fonctionnement global

Le composant affiche une liste de `ProfileCard` sous forme de grille.

- Parcourt la liste `profiles` avec `v-for`.
- Utilise `user_id` comme clé unique.
- Transmet chaque profil au composant `ProfileCard`.
- Récupère les événements `like` et `clickOnProfile`.
- Relaye ces événements au composant parent.
- La grille est responsive : plusieurs colonnes sur desktop et une colonne sur mobile.