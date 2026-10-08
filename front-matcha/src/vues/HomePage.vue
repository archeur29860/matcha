<script setup lang="ts">
import ListProfileCard from '@/components/listProfileCard.vue';
import SearchBarWithOption from '@/components/searchBarWithOption.vue';
import type { ProfileCard as ProfileCardType } from '@/types/profile';
import { ref } from 'vue';

const profiles: ProfileCardType[] = [
  {
    user_id: 1,
    username: 'alex_dev',
    age: 27,
    location: 'Paris, France',
    online: true,
    popularity: 87,
    tags: ['Vue.js', 'TypeScript', 'Gaming'],
    bio: 'Développeur passionné par le web, les jeux vidéo et les nouvelles technologies.',
    image: 'https://i.pravatar.cc/300?img=12'
  },
  {
    user_id: 2,
    username: 'sophie_design',
    age: 25,
    location: 'Lyon, France',
    online: false,
    popularity: 72,
    tags: ['Design', 'Voyage', 'Photographie'],
    bio: 'Designer UI/UX qui adore voyager et découvrir de nouveaux endroits.',
    image: 'https://i.pravatar.cc/300?img=47'
  },
  {
    user_id: 3,
    username: 'thomas_music',
    age: 30,
    location: 'Bordeaux, France',
    online: true,
    popularity: 94,
    tags: ['Guitare', 'Rock', 'Concerts'],
    bio: 'Musicien amateur, fan de rock et toujours partant pour un concert.',
    image: 'https://i.pravatar.cc/300?img=11'
  },
  {
    user_id: 4,
    username: 'emma_travel',
    age: 24,
    location: 'Marseille, France',
    online: true,
    popularity: 81,
    tags: ['Voyage', 'Randonnée', 'Nature'],
    bio: 'Je préfère les montagnes, les randonnées et les couchers de soleil.',
    image: 'https://i.pravatar.cc/300?img=44'
  },
  {
    user_id: 5,
    username: 'lucas_fit',
    age: 29,
    location: 'Toulouse, France',
    online: false,
    popularity: 63,
    tags: ['Fitness', 'Running', 'Nutrition'],
    bio: 'Sportif dans l’âme, je prépare actuellement mon premier marathon.',
    image: 'https://i.pravatar.cc/300?img=13'
  },
  {
    user_id: 6,
    username: 'clara_books',
    age: 26,
    location: 'Nantes, France',
    online: true,
    popularity: 46,
    tags: ['Lecture', 'Cinéma', 'Écriture'],
    bio: 'Grande lectrice, passionnée de cinéma et d’histoires en tout genre.',
    image: 'https://i.pravatar.cc/300?img=32'
  },
  {
    user_id: 7,
    username: 'antoine_food',
    age: 31,
    location: 'Lille, France',
    online: false,
    popularity: 76,
    tags: ['Cuisine', 'Restaurants', 'Voyage'],
    bio: 'Toujours à la recherche du meilleur restaurant et de nouvelles saveurs.',
    image: 'https://i.pravatar.cc/300?img=14'
  },
  {
    user_id: 8,
    username: 'lea_art',
    age: 23,
    location: 'Nice, France',
    online: true,
    popularity: 91,
    tags: ['Peinture', 'Art', 'Musique'],
    bio: 'Artiste indépendante, j’aime peindre, écouter de la musique et créer.',
    image: 'https://i.pravatar.cc/300?img=45'
  },
  {
    user_id: 9,
    username: 'max_gamer',
    age: 28,
    location: 'Strasbourg, France',
    online: true,
    popularity: 68,
    tags: ['Gaming', 'PC', 'Esport'],
    bio: 'Gamer depuis toujours, principalement FPS et jeux compétitifs.',
    image: 'https://i.pravatar.cc/300?img=15'
  },
  {
    user_id: 10,
    username: 'chloe_photo',
    age: 27,
    location: 'Montpellier, France',
    online: false,
    popularity: 38,
    tags: ['Photographie', 'Mode', 'Voyage'],
    bio: 'Photographe amateur avec une passion pour la mode et les voyages.',
    image: 'https://i.pravatar.cc/300?img=49'
  },
  {
    user_id: 11,
    username: 'julien_coffee',
    age: 32,
    location: 'Paris, France',
    online: true,
    popularity: 55,
    tags: ['Café', 'Cuisine', 'Musique'],
    bio: 'Amateur de bons cafés, de cuisine maison et de playlists interminables.',
    image: 'https://i.pravatar.cc/300?img=3'
  },
  {
    user_id: 12,
    username: 'camille_yoga',
    age: 26,
    location: 'Rennes, France',
    online: true,
    popularity: 97,
    tags: ['Yoga', 'Bien-être', 'Voyage'],
    bio: 'Passionnée de yoga et de voyages, toujours à la recherche de nouvelles expériences.',
    image: 'https://i.pravatar.cc/300?img=5'
  }
]

const profile = ref({
  user_id: 1,
  username: 'alex_dev',
  first_name: 'Alex',
  last_name: 'Martin',
  age: 27,
  location: 'Paris, France',
  liked: false,

  pictures: [
    'https://i.pravatar.cc/800?img=12',
    'https://i.pravatar.cc/800?img=13',
    'https://i.pravatar.cc/800?img=14',
    'https://i.pravatar.cc/800?img=15',
    'https://i.pravatar.cc/800?img=16',
  ],
})

const searchOptions = profiles.map((profile) => ({
  id: profile.user_id,
  label: profile.username,
  image: profile.image,
}))

function handleProfileSelected(option: {
  id: number | string
  label: string
  subtitle?: string
  image?: string
}) {
  console.log('Profil sélectionné :', option.id)

  // Par exemple :
  // router.push(`/profile/${option.id}`)
}

function handleLike(user_id: string) {
  console.log('Liked', user_id)
}

function handleClickOnProfile(user_id: string) {
  console.log('Click on profile', user_id)
}
</script>

<template>
    <SearchBarWithOption
    :options="searchOptions"
    placeholder="Rechercher un utilisateur..."
    @select="handleProfileSelected"
    />

    <ListProfileCard :profiles="profiles"
    @like="handleLike"
    @clickOnProfile="handleClickOnProfile"
    />
</template>
