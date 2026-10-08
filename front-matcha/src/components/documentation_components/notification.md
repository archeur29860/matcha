# Notification

## Nom et import

**Composant :** `Notification`

```ts
import Notification from '@/components/notification.vue'
```

## Props definition

| Prop | Type | Requis | Défaut | Description |
|---|---|---:|---|---|
| `show` | `boolean` | Oui | — | Contrôle l'affichage |
| `title` | `string` | Non | `""` | Titre de la notification |
| `message` | `string` | Non | `""` | Message affiché |
| `type` | `NotificationType` | Non | `"info"` | Type de notification |
| `duration` | `number` | Non | `3000` | Durée d'affichage en ms |
| `position` | `NotificationPosition` | Non | `"top-right"` | Position à l'écran |
| `closable` | `boolean` | Non | `true` | Affiche le bouton de fermeture |
| `showIcon` | `boolean` | Non | `true` | Affiche l'icône |
| `width` | `string` | Non | `"360px"` | Largeur de la notification |
| `zIndex` | `number` | Non | `9999` | Niveau de superposition |

### Types disponibles

```ts
type NotificationType =
  | 'success'
  | 'error'
  | 'warning'
  | 'info'

type NotificationPosition =
  | 'top-left'
  | 'top-center'
  | 'top-right'
  | 'bottom-left'
  | 'bottom-center'
  | 'bottom-right'
```

## Emit definition

| Event | Payload | Description |
|---|---|---|
| `close` | Aucun | Émis lorsque la notification est fermée |

```ts
emit('close')
```

Le composant expose également une méthode :

```ts
defineExpose({
  make_notification,
})
```

Elle permet de déclencher une notification directement depuis une réponse API.

## Fonctionnement global

Le composant affiche une notification temporaire avec différents types et positions.

- L'affichage est contrôlé par la prop `show`.
- La notification se ferme automatiquement après `duration` millisecondes.
- Le bouton de fermeture permet de la fermer manuellement.
- Les types disponibles sont `success`, `error`, `warning` et `info`.
- La notification peut être positionnée dans les 6 zones principales de l'écran.
- Elle est injectée dans le `<body>` grâce à `Teleport`.
- Une transition de fondu et de déplacement est appliquée à l'apparition et à la disparition.
- Sur mobile, la notification prend toute la largeur disponible.
- `make_notification()` permet de générer automatiquement une notification de succès ou d'erreur à partir d'une réponse API.
- Le timer est nettoyé lors de la fermeture et de la destruction du composant.