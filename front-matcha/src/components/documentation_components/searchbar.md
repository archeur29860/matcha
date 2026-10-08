# SearchBar

## Nom et import

**Composant :** `SearchBarWithOption`

```ts
import SearchBarWithOption from '@/components/searchBarWithOption.vue'
```

## Props definition

| Prop | Type | Requis | Défaut | Description |
|---|---|---:|---|---|
| `options` | `SearchOption[]` | Oui | — | Liste des options à rechercher |
| `placeholder` | `string` | Non | `"Rechercher..."` | Texte du champ de recherche |

```ts
interface SearchOption {
  id: number | string
  label: string
  subtitle?: string
  image?: string
}
```

## Emit definition

| Event | Payload | Description |
|---|---|---|
| `select` | `SearchOption` | Émis lorsqu'une option est sélectionnée |

```ts
emit('select', option)
```

## Fonctionnement global

Le composant fournit une barre de recherche avec suggestions dynamiques.

- La recherche s'effectue sur `label` et `subtitle`.
- La recherche est insensible à la casse.
- Les résultats sont limités à **8 options**.
- Les suggestions apparaissent lorsque le champ est focus et contient du texte.
- Une image est affichée si `image` est définie, sinon la première lettre du `label` est utilisée.
- Le bouton `×` permet de vider la recherche.
- La sélection d'une option renseigne le champ et déclenche `select`.
- La liste des résultats possède une animation d'apparition/disparition.
- Le composant est responsive pour les écrans de moins de `600px`.

### Exemple

```vue
<SearchBarWithOption
  :options="options"
  placeholder="Rechercher un utilisateur..."
  @select="handleSelect"
/>
```