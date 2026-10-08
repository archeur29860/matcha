# Input

## Nom et import

**Composant :** `Input`

```ts
import Input from '@/components/Input.vue'
```

## Props definition

| Prop | Type | Requis | Défaut | Description |
|---|---|---:|---|---|
| `type` | `string` | Non | `"text"` | Type du champ (`text`, `email`, `password`, etc.) |
| `placeholder` | `string` | Non | `""` | Texte indicatif du champ |
| `disabled` | `boolean` | Non | `false` | Désactive le champ |

### Model

Le composant utilise `defineModel` pour gérer sa valeur :

```ts
const model = defineModel<string>({ default: '' })
```

Utilisation :

```vue
<Input v-model="value" />
```

## Emit definition

Aucun `emit` personnalisé.

La valeur est synchronisée avec le parent via `v-model`.

## Fonctionnement global

Le composant fournit un champ `<input>` générique et réutilisable.

- La valeur est gérée via `v-model`.
- Le `type`, `placeholder` et l'état `disabled` sont configurables.
- Le champ possède des styles pour les états `hover`, `focus` et `disabled`.
- La hauteur et la taille du texte sont adaptées sur mobile (`< 600px`).
- Aucun appel API ou traitement métier n'est effectué par le composant.