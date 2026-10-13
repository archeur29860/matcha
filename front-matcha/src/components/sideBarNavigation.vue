<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useUserStore } from '@/stores/user'
import router from '@/router'
import { useRoute } from 'vue-router'

const route = useRoute()
const activeItem = ref('')

const userStore = useUserStore()

onMounted(() => {
  if (route.path === '/home') {
    activeItem.value = 'discover'
  } else if (route.path === '/') {
    activeItem.value = 'likes'
  } else if (route.path === '/') {
    activeItem.value = 'matches'
  } else if (route.path === '/') {
    activeItem.value = 'messages'
  } else if (route.path === `/profile/${userStore.id}`) {
    activeItem.value = 'profile'
  }
})

const navigation = [
  {
    id: 'discover',
    label: 'Découvrir',
    icon: '⌂',
    path: '/home'
  },
  {
    id: 'likes',
    label: 'Likes',
    icon: '♡',
    path: '/',
    badge: 8
  },
  {
    id: 'matches',
    label: 'Matchs',
    icon: '♥',
    path: '/',
    badge: 3
  },
  {
    id: 'messages',
    label: 'Messages',
    icon: '◌',
    path: '/',
    badge: 5
  },
  {
    id: 'profile',
    label: 'Mon profil',
    icon: '♙',
    path: `/profile/${userStore.id}/`
  }
]

const selectItem = (id:string, path:string) => {
  activeItem.value = id
  router.push(path)
}
</script>

<template>
  <aside class="sidebar">

    <!-- Logo -->
    <div class="logo">
      <div class="logo-heart">
        ♥
      </div>

      <span class="logo-text">
        Heartly
      </span>
    </div>

    <!-- Navigation -->
    <nav class="navigation">

      <p class="navigation-title">
        Navigation
      </p>

      <button
        v-for="item in navigation"
        :key="item.id"
        type="button"
        class="nav-item"
        :class="{ active: activeItem === item.id }"
        @click="selectItem(item.id, item.path)"
      >
        <span class="nav-icon">
          {{ item.icon }}
        </span>

        <span class="nav-label">
          {{ item.label }}
        </span>

        <span
          v-if="item.badge"
          class="badge"
        >
          {{ item.badge }}
        </span>
      </button>

    </nav>

    <!-- User -->
    <div class="user-card">

      <div class="avatar">
        {{ userStore.first_name[0] }}
      </div>

      <div class="user-info">
        <strong>{{ userStore.first_name }} {{ userStore.last_name }}</strong>

        <span>
          <i class="online-dot"></i>
          En ligne
        </span>
      </div>

      <button
        type="button"
        class="more-button"
        aria-label="Plus d'options"
      >
        ⋯
      </button>

    </div>

  </aside>
</template>

<style scoped>
/* =================================
   SIDEBAR
================================= */

.sidebar {
  position: fixed;
  inset: 0 auto 0 0;

  width: 250px;
  box-sizing: border-box;

  padding: 28px 18px;

  display: flex;
  flex-direction: column;

  background: #fffdfc;
  border-right: 1px solid #f1e5e5;

  z-index: 100;
}

/* =================================
   LOGO
================================= */

.logo {
  display: flex;
  align-items: center;
  gap: 10px;

  padding: 0 12px;
  margin-bottom: 42px;

  color: #e86f8d;

  font-size: 23px;
  font-weight: 700;
}

.logo-heart {
  width: 36px;
  height: 36px;

  display: flex;
  align-items: center;
  justify-content: center;

  border-radius: 12px;

  background: #ffe1e7;

  font-size: 18px;
}

/* =================================
   NAVIGATION
================================= */

.navigation {
  display: flex;
  flex-direction: column;
  gap: 7px;
}

.navigation-title {
  margin: 0 0 10px;
  padding: 0 13px;

  color: #b3a7ac;

  font-size: 11px;
  font-weight: 600;

  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.nav-item {
  position: relative;

  width: 100%;
  height: 48px;

  padding: 0 14px;

  display: flex;
  align-items: center;
  gap: 13px;

  border: 0;
  border-radius: 14px;

  background: transparent;

  color: #81767c;

  font-family: inherit;
  font-size: 14px;
  font-weight: 500;

  text-align: left;

  cursor: pointer;

  transition:
    background 0.2s ease,
    color 0.2s ease,
    transform 0.2s ease;
}

.nav-item:hover {
  background: #fff1f3;
  color: #e86f8d;
}

.nav-item:active {
  transform: scale(0.98);
}

.nav-item.active {
  background: #ffe7eb;
  color: #e85f80;
  font-weight: 600;
}

.nav-item.active::before {
  content: '';

  position: absolute;
  left: 0;
  top: 12px;

  width: 3px;
  height: 24px;

  border-radius: 0 4px 4px 0;

  background: #e86f8d;
}

.nav-icon {
  width: 21px;
  height: 21px;

  flex-shrink: 0;

  display: flex;
  align-items: center;
  justify-content: center;

  font-size: 18px;
}

.nav-label {
  white-space: nowrap;
}

.badge {
  min-width: 21px;
  height: 21px;

  margin-left: auto;
  padding: 0 6px;

  display: flex;
  align-items: center;
  justify-content: center;

  border-radius: 20px;

  background: #ef7895;
  color: white;

  font-size: 10px;
  font-weight: 700;
}

/* =================================
   USER
================================= */

.user-card {
  margin-top: auto;

  min-height: 67px;

  padding: 12px;

  display: flex;
  align-items: center;
  gap: 11px;

  border: 1px solid #f1e5e5;
  border-radius: 17px;

  background: #fff8f7;
}

.avatar {
  width: 40px;
  height: 40px;

  flex-shrink: 0;

  display: flex;
  align-items: center;
  justify-content: center;

  border-radius: 50%;

  background: linear-gradient(
    135deg,
    #ffd9df,
    #c9e9ed
  );

  color: #6d5960;

  font-size: 14px;
  font-weight: 700;
}

.user-info {
  min-width: 0;

  display: flex;
  flex-direction: column;
  gap: 3px;
}

.user-info strong {
  overflow: hidden;

  color: #4d4248;

  font-size: 13px;

  white-space: nowrap;
  text-overflow: ellipsis;
}

.user-info span {
  display: flex;
  align-items: center;

  color: #a59a9f;

  font-size: 11px;
}

.online-dot {
  width: 6px;
  height: 6px;

  margin-right: 5px;

  border-radius: 50%;

  background: #73d4b0;
}
.more-button {
  margin-left: auto;

  width: 36px;
  height: 36px;

  display: flex;
  align-items: center;
  justify-content: center;

  border: 0;
  border-radius: 999px;

  background: transparent;
  color: #a99da2;

  font-size: 18px;
  line-height: 1;

  cursor: pointer;

  transition:
    background-color 0.25s ease,
    color 0.25s ease,
    transform 0.2s ease,
    box-shadow 0.25s ease;
}

.more-button:hover {
  cursor: url('/cursor.cur'), auto;

  background: #ffd9df;
  color: #e86f8d;

  transform: scale(1.08);

  box-shadow: 0 4px 12px rgba(232, 111, 141, 0.15);
}
/* =================================
   TABLET
================================= */

@media (max-width: 900px) {
  .sidebar {
    width: 76px;
    padding: 22px 12px;
  }

  .logo {
    justify-content: center;

    padding: 0;
  }

  .logo-text,
  .navigation-title,
  .nav-label,
  .user-info,
  .more-button {
    display: none;
  }

  .nav-item {
    justify-content: center;
    padding: 0;
  }

  .nav-item.active::before {
    display: none;
  }

  .badge {
    position: absolute;

    top: 3px;
    right: 3px;

    min-width: 17px;
    height: 17px;

    padding: 0;

    font-size: 9px;
  }

  .user-card {
    justify-content: center;
    padding: 8px;
  }
}

/* =================================
   MOBILE
================================= */

@media (max-width: 600px) {
  .sidebar {
    position: fixed;

    top: auto;
    bottom: 0;
    left: 0;

    width: 100%;
    height: 72px;

    padding: 8px 12px;

    border-right: 0;
    border-top: 1px solid #f1e5e5;
  }

  .logo,
  .navigation-title,
  .user-card {
    display: none;
  }

  .navigation {
    width: 100%;
    height: 100%;

    flex-direction: row;

    justify-content: space-around;
    align-items: center;
  }

  .nav-item {
    width: 52px;
    height: 52px;

    padding: 0;

    justify-content: center;
  }

  .nav-item.active {
    background: #ffe7eb;
  }

  .nav-item.active::before {
    display: none;
  }

  .nav-icon {
    font-size: 19px;
  }
}
</style>