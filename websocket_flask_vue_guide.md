# WebSockets : comprendre, implémenter et utiliser

## 1. Objectif

Ce guide explique comment utiliser les WebSockets dans une application
web avec :

-   **Backend :** Flask (Python)
-   **Frontend :** Vue.js
-   **Temps réel :** Flask-SocketIO et Socket.IO côté navigateur
-   **Authentification :** JWT transmis avec un Bearer token pour les
    routes HTTP, et dans `auth` lors de la connexion Socket.IO
-   **Cas d'usage :** messagerie privée et notifications

> Important : WebSocket est un protocole. Socket.IO est une bibliothèque
> qui fournit une couche d'événements au-dessus de transports comme
> WebSocket, avec des mécanismes de reconnexion et de repli. Le client
> Socket.IO ne communique pas directement avec un serveur WebSocket brut
> : les deux côtés doivent parler le même protocole.

------------------------------------------------------------------------

## 2. Qu'est-ce qu'un WebSocket ?

Avec HTTP classique, le navigateur envoie une requête et le serveur
renvoie une réponse. Pour savoir si quelque chose de nouveau est arrivé,
le navigateur doit souvent refaire des requêtes périodiques.

Un WebSocket ouvre une connexion persistante entre le navigateur et le
serveur. Une fois la connexion établie, les deux côtés peuvent envoyer
des données sans recommencer une requête HTTP pour chaque événement.

### HTTP classique et WebSocket

  -----------------------------------------------------------------------
  HTTP classique                      WebSocket
  ----------------------------------- -----------------------------------
  Requête puis réponse                Connexion persistante et
                                      bidirectionnelle

  Le client demande généralement les  Le serveur peut pousser un
  nouvelles données                   événement au client

  Très adapté aux opérations CRUD et  Très adapté au chat, aux
  aux chargements                     notifications et aux mises à jour
                                      en direct

  Les appels sont indépendants        Plusieurs événements peuvent passer
                                      sur la même connexion
  -----------------------------------------------------------------------

### Exemple de messagerie

1.  Alice ouvre une conversation.
2.  Son navigateur envoie un message à Flask.
3.  Flask vérifie son identité et son droit d'écrire dans cette
    conversation.
4.  Flask enregistre le message en base de données.
5.  Flask émet un événement vers la salle Socket.IO du destinataire.
6.  Le navigateur de Bob reçoit `new_message` et met à jour l'interface
    sans recharger la page.

**À retenir :** la base de données reste la source de vérité. Le
WebSocket sert à notifier les clients en temps réel ; il ne remplace ni
la persistance, ni les vérifications d'autorisation.

------------------------------------------------------------------------

## 3. Architecture recommandée

``` text
Vue.js
  ├── HTTP + Bearer JWT ───────────────> Flask REST API
  │                                       ├── Vérification JWT
  │                                       ├── Vérification des droits
  │                                       └── Base de données
  │
  └── Socket.IO + JWT à la connexion ──> Flask-SocketIO
                                          └── Événements vers user:<id>
```

Utilise **HTTP** pour les opérations qui doivent retourner un résultat
explicite, par exemple : - créer une conversation ; - charger
l'historique ; - envoyer un message et obtenir son identifiant ; -
charger les notifications ; - marquer une notification comme lue.

Utilise **Socket.IO** pour : - avertir qu'un nouveau message est arrivé
; - avertir qu'une nouvelle notification est disponible ; -
éventuellement, plus tard, ajouter les événements « en train d'écrire »
ou « message lu ».

Pour une première version, envoyer le message par HTTP puis diffuser
l'événement via Socket.IO est une architecture simple et robuste.

------------------------------------------------------------------------

## 4. Installation

Dans l'environnement Python du backend :

``` bash
pip install Flask-SocketIO simple-websocket PyJWT
```

Dans le projet Vue.js :

``` bash
npm install socket.io-client
```

Si ton application utilise déjà une bibliothèque JWT ou une fonction de
validation de token, réutilise-la. Évite de créer un second système
d'authentification qui interpréterait les tokens différemment.

------------------------------------------------------------------------

## 5. Configurer Flask-SocketIO

Exemple de point d'entrée `app.py` :

``` python
import os
from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO

from database.connection import close_db
from routes.tags_bp import tags_bp
from routes.blocked_bp import blocked_bp
from routes.users_bp import users_bp
from routes.interaction_bp import interaction_bp
from routes.userProfile_bp import userProfile_bp
from routes.pictures_bp import pictures_bp

FRONTEND_ORIGIN = os.getenv(
    "FRONTEND_ORIGIN",
    "http://localhost:5174",
)

app = Flask(__name__)
CORS(app, origins=[FRONTEND_ORIGIN])

app.teardown_appcontext(close_db)

app.register_blueprint(tags_bp)
app.register_blueprint(blocked_bp)
app.register_blueprint(users_bp)
app.register_blueprint(interaction_bp)
app.register_blueprint(userProfile_bp)
app.register_blueprint(pictures_bp)

socketio = SocketIO(
    app,
    cors_allowed_origins=[FRONTEND_ORIGIN],
    async_mode="threading",
)

app.extensions["socketio"] = socketio

# Importer après la création de socketio pour éviter certains imports circulaires.
from sockets.events import register_socket_events
register_socket_events(socketio)

if __name__ == "__main__":
    socketio.run(
        app,
        host="0.0.0.0",
        port=5000,
        debug=True,
    )
```

Adapte les imports à ton projet. Quand Socket.IO est utilisé, démarre
l'application avec `socketio.run(app, ...)`, pas avec `app.run(...)`.

En production, configure correctement le serveur WSGI/ASGI et le mode de
déploiement pris en charge par ta version de Flask-SocketIO. Le mode
`threading` convient souvent au développement et aux déploiements
simples, mais les besoins de montée en charge peuvent nécessiter une
configuration différente.

------------------------------------------------------------------------

## 6. Authentifier une connexion Socket.IO avec JWT

### 6.1 Principe

Les requêtes REST peuvent envoyer le token dans l'en-tête :

``` http
Authorization: Bearer <token>
```

Pour Socket.IO dans le navigateur, il est courant de transmettre le
token lors de la connexion :

``` javascript
io("http://localhost:5000", {
  auth: { token: jwtToken }
});
```

Le serveur doit **valider le token côté serveur** : signature,
expiration et claims attendus. Ne fais jamais confiance à un identifiant
utilisateur envoyé seul par le client.

### 6.2 Exemple d'événements Socket.IO

Crée `sockets/events.py` :

``` python
from flask import request
from flask_socketio import join_room
import jwt

# IMPORTANT :
# Remplace cette fonction par la logique JWT déjà utilisée dans ton backend.
# La clé, l'algorithme et le nom du claim doivent être identiques à ton système.
def decode_access_token(token):
    # Exemple uniquement : adapte SECRET_KEY et les claims à ton application.
    import os

    return jwt.decode(
        token,
        os.environ["SECRET_KEY"],
        algorithms=["HS256"],
        options={"require": ["exp", "sub"]},
    )


def register_socket_events(socketio):
    @socketio.on("connect")
    def on_connect(auth=None):
        auth = auth or {}
        token = auth.get("token")

        if not token:
            return False  # Refuse la connexion.

        try:
            claims = decode_access_token(token)
            user_id = int(claims["sub"])
        except (jwt.InvalidTokenError, KeyError, TypeError, ValueError):
            return False

        # Une salle privée par utilisateur.
        join_room(f"user:{user_id}")

        # Ne pas accepter un user_id fourni séparément par le client.
        print(f"Utilisateur {user_id} connecté à Socket.IO")

    @socketio.on("disconnect")
    def on_disconnect(reason=None):
        # Les salles sont quittées automatiquement à la déconnexion.
        pass
```

Si ton JWT contient l'identifiant dans `user_id` plutôt que dans `sub`,
adapte l'extraction. Si tu utilises une autre clé, un autre algorithme
ou une autre bibliothèque, garde la logique déjà présente dans ton
projet.

> Sécurité : une connexion Socket.IO authentifiée au moment du handshake
> ne garantit pas automatiquement qu'un token révoqué reste valide ou
> qu'un utilisateur a toujours accès à une conversation. Pour les
> actions sensibles, vérifie aussi les droits côté serveur. Si
> nécessaire, limite la durée des connexions ou réauthentifie
> périodiquement.

------------------------------------------------------------------------

## 7. Les salles Socket.IO (rooms)

Une **room** est un groupe de connexions auquel le serveur peut envoyer
un événement.

Pour une messagerie privée, on peut utiliser une salle par utilisateur :

``` python
join_room(f"user:{user_id}")
```

Puis émettre un événement uniquement vers cet utilisateur :

``` python
socketio.emit(
    "new_message",
    message_data,
    to=f"user:{recipient_id}",
)
```

Le destinataire peut être connecté sur plusieurs onglets ou appareils :
toutes ses connexions ayant rejoint sa salle peuvent recevoir
l'événement.

**Ne laisse pas le navigateur rejoindre arbitrairement une salle
privée.** Le serveur doit déduire l'identifiant de l'utilisateur depuis
le JWT validé et vérifier les autorisations avant de diffuser un
message.

------------------------------------------------------------------------

## 8. Enregistrer et diffuser un message

Le flux recommandé côté serveur est :

1.  authentifier l'utilisateur ;
2.  vérifier qu'il est membre de la conversation ;
3.  valider et limiter le contenu ;
4.  enregistrer le message en base ;
5.  enregistrer les notifications dans la même transaction, si possible
    ;
6.  valider la transaction (`commit`) ;
7.  diffuser les événements Socket.IO après le commit.

Le point 6 est important : ne diffuse pas un message avant que la
transaction ait été validée. Sinon, un destinataire pourrait voir un
message qui a finalement été annulé en base.

Exemple de principe pour un service :

``` python
def publish_new_message(socketio, recipient_ids, message_data):
    for recipient_id in recipient_ids:
        socketio.emit(
            "new_message",
            message_data,
            to=f"user:{recipient_id}",
        )
```

Ce code illustre seulement la diffusion. La vérification d'accès,
l'insertion SQL, la transaction et la création de notifications doivent
être faites dans les services/routes adaptés à ta base de données.

### Exemple de contenu d'événement

``` json
{
  "id": 481,
  "conversation_id": 27,
  "sender_id": 12,
  "content": "Salut !",
  "created_at": "2026-10-16T14:10:00Z"
}
```

N'envoie que les données nécessaires. Ne diffuse pas d'informations
privées inutiles dans les événements.

------------------------------------------------------------------------

## 9. Connecter Vue.js à Socket.IO

Crée, par exemple, `src/composables/useSocket.js` :

``` javascript
import { ref, onMounted, onUnmounted } from "vue";
import { io } from "socket.io-client";

export function useSocket(getToken) {
  const connected = ref(false);
  const lastMessage = ref(null);
  const lastNotification = ref(null);

  let socket = null;

  function connect() {
    const token = getToken();

    if (!token) return;

    socket = io("http://localhost:5000", {
      auth: { token },
      transports: ["websocket"],
      reconnection: true,
    });

    socket.on("connect", () => {
      connected.value = true;
    });

    socket.on("disconnect", () => {
      connected.value = false;
    });

    socket.on("connect_error", (error) => {
      console.error("Échec de connexion Socket.IO :", error.message);
    });

    socket.on("new_message", (message) => {
      lastMessage.value = message;
    });

    socket.on("new_notification", (notification) => {
      lastNotification.value = notification;
    });
  }

  function disconnect() {
    if (socket) {
      socket.removeAllListeners();
      socket.disconnect();
      socket = null;
    }

    connected.value = false;
  }

  onMounted(connect);
  onUnmounted(disconnect);

  return {
    connected,
    lastMessage,
    lastNotification,
    connect,
    disconnect,
  };
}
```

Exemple de composant Vue :

``` vue
<script setup>
import { watch } from "vue";
import { useSocket } from "@/composables/useSocket";

// Remplace cette fonction par la façon dont ton application stocke le JWT.
const getToken = () => localStorage.getItem("access_token");

const { connected, lastMessage, lastNotification } = useSocket(getToken);

watch(lastMessage, (message) => {
  if (!message) return;

  // Ajouter le message à la conversation affichée,
  // en évitant les doublons si l'API l'a déjà retourné.
  console.log("Nouveau message :", message);
});

watch(lastNotification, (notification) => {
  if (!notification) return;

  // Mettre à jour le badge de notifications ou afficher un toast.
  console.log("Nouvelle notification :", notification);
});
</script>

<template>
  <div>
    <span>{{ connected ? "Connecté" : "Déconnecté" }}</span>
  </div>
</template>
```

Notes : - `getToken()` doit retourner le token courant. Si le token
change après un rafraîchissement, déconnecte puis reconnecte Socket.IO
avec le nouveau token. - Si tu as un store Pinia ou un composable
d'authentification, préfère-le à `localStorage` directement. -
`transports: ["websocket"]` force le transport WebSocket. Pour permettre
le repli automatique vers d'autres transports Socket.IO, tu peux retirer
cette option. - N'ouvre pas plusieurs connexions Socket.IO à chaque
rendu. Garde une connexion partagée au niveau approprié de l'application
si plusieurs composants en ont besoin.

------------------------------------------------------------------------

## 10. Charger et envoyer les messages avec HTTP

Socket.IO ne remplace pas l'API REST. Un flux simple consiste à charger
l'historique et envoyer les messages en HTTP, puis à recevoir les
nouveaux messages en temps réel.

### Charger l'historique

``` javascript
async function loadMessages(conversationId, token) {
  const response = await fetch(
    `http://localhost:5000/api/conversations/${conversationId}/messages`,
    {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  );

  if (!response.ok) {
    throw new Error("Impossible de charger les messages");
  }

  return response.json();
}
```

### Envoyer un message

``` javascript
async function sendMessage(conversationId, content, token) {
  const response = await fetch(
    `http://localhost:5000/api/conversations/${conversationId}/messages`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ content }),
    }
  );

  if (!response.ok) {
    const detail = await response.text();
    throw new Error(`Échec de l'envoi : ${detail}`);
  }

  return response.json();
}
```

Les URL sont des exemples : elles doivent correspondre aux routes
réellement enregistrées dans ton application.

### Éviter les doublons

Après l'envoi HTTP, le client reçoit normalement le message dans la
réponse. Il peut aussi recevoir un événement Socket.IO. Avant d'ajouter
un message à la liste, vérifie son `id` pour ne pas l'afficher deux
fois.

------------------------------------------------------------------------

## 11. Notifications

Une notification doit être persistée en base pour que l'utilisateur
puisse la retrouver même s'il était hors ligne.

Flux recommandé :

1.  le message est enregistré ;
2.  une notification est enregistrée pour chaque destinataire concerné ;
3.  après le commit, le serveur émet `new_notification` ;
4.  si l'utilisateur est hors ligne, la notification reste dans la base
    ;
5.  à la prochaine ouverture de l'application, Vue charge les
    notifications via une route HTTP.

Exemple de charge utile :

``` json
{
  "id": 902,
  "type": "new_message",
  "conversation_id": 27,
  "message_id": 481,
  "content": "Tu as reçu un nouveau message.",
  "is_read": false,
  "created_at": "2026-10-16T14:10:00Z"
}
```

Événements possibles : - `new_message` - `new_notification` -
`notification_read` (si l'application diffuse aussi les changements
d'état)

Les noms d'événements sont à définir une fois et à réutiliser à
l'identique côté serveur et côté client.

------------------------------------------------------------------------

## 12. Sécurité : points indispensables

-   **Authentification :** vérifier le JWT côté serveur, y compris sa
    signature et son expiration.
-   **Autorisation :** avant de lire ou d'envoyer un message, vérifier
    que l'utilisateur est membre de la conversation.
-   **Isolation :** envoyer les événements privés uniquement aux salles
    des utilisateurs autorisés.
-   **Validation :** rejeter les contenus vides, trop longs ou mal
    formés.
-   **CORS / origine :** autoriser uniquement les origines de frontend
    nécessaires. CORS n'est pas un remplacement de l'authentification.
-   **HTTPS/WSS :** utiliser HTTPS et WebSocket sécurisé en production.
-   **Limitation de débit :** protéger les endpoints et événements
    contre le spam.
-   **Secrets :** conserver la clé JWT dans une variable
    d'environnement, jamais dans le dépôt Git.
-   **Erreurs :** ne pas exposer les tokens, secrets, requêtes SQL ou
    détails internes dans les messages d'erreur.
-   **Déconnexion :** gérer les tokens expirés et reconnecter seulement
    après avoir obtenu un token valide.
-   **Persistance :** enregistrer les messages et notifications avant de
    les diffuser.
-   **Multi-instance :** si plusieurs processus/serveurs Flask-SocketIO
    sont utilisés, prévoir une file de messages compatible (par exemple
    Redis) et une configuration de déploiement appropriée.

------------------------------------------------------------------------

## 13. Tester le fonctionnement

### Vérifications côté backend

1.  Démarrer Flask via `socketio.run(...)`.
2.  Vérifier que les routes REST fonctionnent toujours.
3.  Se connecter avec un token valide.
4.  Essayer un token absent, invalide ou expiré : la connexion doit être
    refusée.
5.  Vérifier qu'un utilisateur non membre d'une conversation ne peut ni
    lire ni envoyer de messages.
6.  Envoyer un message et vérifier qu'il est enregistré avant sa
    diffusion.
7.  Vérifier qu'un utilisateur non destinataire ne reçoit pas
    l'événement.
8.  Tester le comportement quand le destinataire est hors ligne : il
    doit retrouver le message et la notification en rechargeant les
    données via HTTP.

### Vérifications côté frontend

1.  Se connecter à l'application.
2.  Vérifier l'état `connected`.
3.  Ouvrir deux sessions avec deux comptes de test différents.
4.  Envoyer un message depuis le premier compte.
5.  Vérifier que le second reçoit `new_message` sans recharger la page.
6.  Vérifier que `new_notification` actualise le badge ou l'interface.
7.  Tester la perte de réseau, la reconnexion et l'expiration du token.

### Diagnostic rapide

  -----------------------------------------------------------------------
  Symptôme                            Causes possibles
  ----------------------------------- -----------------------------------
  `connect_error`                     URL/port incorrect, serveur non
                                      démarré, origine refusée, token
                                      invalide

  Connexion établie mais aucun        Nom d'événement différent, mauvaise
  événement                           room, émission non exécutée

  Message visible chez le mauvais     Erreur de contrôle d'accès ou de
  utilisateur                         ciblage des rooms : corriger avant
                                      mise en production

  Événements dupliqués                Plusieurs connexions, listeners
                                      enregistrés plusieurs fois ou
                                      doublon entre réponse HTTP et
                                      événement

  Fonctionne en local mais pas en     Proxy WebSocket, configuration TLS,
  production                          serveur de déploiement ou
                                      multi-instance
  -----------------------------------------------------------------------

------------------------------------------------------------------------

## 14. Erreurs fréquentes

### Utiliser `app.run()` au lieu de `socketio.run()`

Quand Flask-SocketIO est intégré, démarre le serveur avec la méthode
prévue par Flask-SocketIO.

### Faire confiance à `sender_id` envoyé par Vue

Le serveur doit dériver l'identité depuis le token validé, jamais depuis
un champ libre du corps de la requête.

### Envoyer un message sans vérifier la conversation

Un utilisateur ne doit pouvoir lire ou envoyer des messages que dans les
conversations auxquelles il appartient.

### Diffuser avant d'enregistrer

Persiste les données et valide la transaction avant d'émettre
l'événement.

### Penser que Socket.IO stocke les messages

Socket.IO transmet des événements. Il ne remplace pas une base de
données ni une API de récupération d'historique.

### Mélanger WebSocket natif et Socket.IO

Le client `socket.io-client` doit se connecter à un serveur Socket.IO,
comme Flask-SocketIO. Il n'est pas interchangeable avec une
implémentation WebSocket brute.

------------------------------------------------------------------------

## 15. Particularités à adapter à ton projet

Le code d'exemple ne peut pas être considéré comme directement
exécutable sans vérifier ces éléments :

1.  **JWT existant :** nom du claim contenant l'identifiant utilisateur,
    clé et algorithme.
2.  **Base de données :** moteur utilisé, syntaxe SQL, marqueurs de
    paramètres (`?`, `%s`, etc.), gestion des transactions et
    récupération de l'identifiant créé.
3.  **Connexion DB :** nom et comportement des fonctions présentes dans
    `database/connection.py`.
4.  **Schéma :** tables et colonnes réellement présentes pour les
    utilisateurs, conversations, messages et notifications.
5.  **Blueprints :** préfixes d'URL et conventions de réponse JSON.
6.  **Frontend :** emplacement réel du token et gestion de la session
    utilisateur.

En particulier, les exemples SQL utilisant `?`, `lastrowid` et
`INTEGER PRIMARY KEY AUTOINCREMENT` correspondent à certains usages de
SQLite ; ils ne sont pas universels.

Avant d'intégrer les routes de messagerie, adapte-les au schéma réel et
à la connexion de base de données existante. Ne crée pas un système JWT
parallèle si ton backend en possède déjà un.

------------------------------------------------------------------------

## 16. Checklist de mise en œuvre

-   [ ] Installer `Flask-SocketIO` et `socket.io-client`.
-   [ ] Initialiser `SocketIO` dans le point d'entrée Flask.
-   [ ] Démarrer le backend avec `socketio.run`.
-   [ ] Réutiliser le système JWT existant pour authentifier la
    connexion.
-   [ ] Faire rejoindre chaque utilisateur à sa salle privée après
    authentification.
-   [ ] Créer les tables ou modèles nécessaires pour conversations,
    messages et notifications.
-   [ ] Vérifier les membres d'une conversation sur chaque endpoint.
-   [ ] Enregistrer le message et les notifications dans une
    transaction.
-   [ ] Diffuser `new_message` et `new_notification` après le commit.
-   [ ] Connecter Vue avec `socket.io-client`.
-   [ ] Charger l'historique et les notifications via HTTP.
-   [ ] Éviter les doublons dans la liste des messages.
-   [ ] Tester tokens invalides, utilisateurs non autorisés, reconnexion
    et destinataires hors ligne.
-   [ ] Configurer HTTPS/WSS, CORS, secrets et déploiement pour la
    production.

## Conclusion

Les WebSockets permettent de rendre l'interface réactive, mais la
sécurité et la fiabilité reposent toujours sur le backend : validation
JWT, autorisation par conversation, persistance en base et diffusion
ciblée. Pour une messagerie Flask/Vue, une bonne approche consiste à
utiliser **HTTP pour lire et envoyer les données**, puis **Socket.IO
pour notifier instantanément les autres utilisateurs**.
