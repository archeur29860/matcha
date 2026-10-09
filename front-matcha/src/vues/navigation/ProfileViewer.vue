<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import ReportModal from '@/components/modal/reportModal.vue';
import { useUserStore } from '@/stores/user';
import { useUserProfileStore } from '@/stores/userProfile';
import { get_userProfile } from '@/services/api_userProfile';

import Notification from '@/components/notification.vue'

const userStore = useUserStore()
const userProfileStore = useUserProfileStore()

onMounted( async () => {
	const userProfileResult = await get_userProfile(userStore.id)
	
	console.log(userProfileResult)
	notificationRef.value?.make_notification(userProfileResult)
	
	if (userProfileResult.success && userProfileResult.data) {
		userProfileStore.id = userProfileResult.data.user_id
		userProfileStore.age = (new Date()).getFullYear() - (new Date(userProfileResult.data.age).getFullYear())
		userProfileStore.gender = userProfileResult.data.gender
		userProfileStore.gender_pref = userProfileResult.data.gender_pref ?? []
		userProfileStore.bio = userProfileResult.data.bio
		userProfileStore.picture_profile_index = userProfileResult.data.picture_profile_index
		userProfileStore.popularity = userProfileResult.data.popularyty
		userProfileStore.location = userProfileResult.data.location ?? ''
		userProfileStore.tags = userProfileResult.data.tags ?? []
		userProfileStore.pictures = userProfileResult.pictures ?? []
	}
	
})

const notificationRef =
ref<InstanceType<typeof Notification> | null>(null)
	
	const props = defineProps<{
		user_id: string
		username: string
		first_name: string
		last_name: string
		age: number
		location: string
		pictures: string[]
		liked: boolean
	}>()
	
	const emit = defineEmits<{
		like: [user_id: string]
		unlike: [user_id: string]
		report: [user_id: string]
		block: [user_id: string]
	}>()
	
	const pictures = computed(() => {
		return props.pictures?.slice(0, 5) ?? []
	})
	
	function handleLike() {
		// emit('like', props.user_id)
	}
	
	function handleUnlike() {
		// emit('unlike', props.user_id)
	}
	
	type ReportReason = 'fake_account' | 'scam' | 'problematic'
	
	const showReportModal = ref(false)
	
	function handleReport() {
		showReportModal.value = true
	}
	
	function handleReportSubmit(reason: ReportReason) {
		showReportModal.value = false
		
		console.log('Utilisateur signalé :', props.user_id)
		console.log('Raison :', reason)
		
		// Appel API ici
	}
	
	function handleBlocked() {
		// emit('block', props.user_id)
	}


const mainPicture = computed(() =>
  (userProfileStore.pictures ?? []).find(
    picture => picture.id === userProfileStore.picture_profile_index
  ) ?? null
)

const secondaryPictures = computed(() =>
  (userProfileStore.pictures ?? []).filter(
    picture => picture.id !== userProfileStore.picture_profile_index
  )
)


</script>

<template>
	<!-- Notification -->
	<Notification
	ref="notificationRef"
	:show="false"
	:duration="5000"
	position="bottom-left"
	:closable="true"
	:show-icon="true"
	width="400px"
	:z-index="10000"
	/>
	
	<main class="profile-viewer">
		<!-- Photos -->
		
		<section class="profile-viewer__photos">
			<!-- Photo principale -->
			<div
			v-if="mainPicture"
			class="profile-viewer__main-photo"
			>
			<img
			:src="mainPicture.url"
			:alt="`Photo de ${userStore.first_name} ${userStore.last_name}`"
			/>
		</div>
		
		<!-- Pas de photo -->
		<div
		v-else
		class="profile-viewer__no-photo"
		>
		<span>📷</span>
		<p>Aucune photo</p>
	</div>
	
	<!-- Photos secondaires -->
	<div
	v-if="secondaryPictures.length > 0"
	class="profile-viewer__gallery"
	>
	<div
	v-for="picture in secondaryPictures"
	:key="picture.index"
	class="profile-viewer__gallery-item"
	>
	<img
	:src="picture.url"
	:alt="`Photo ${picture.index} de ${userStore.first_name} ${userStore.last_name}`"
	/>
</div>
</div>
</section>

<!-- Informations -->
<section class="profile-viewer__info">
	<header class="profile-viewer__header">
		<div>
			<h1>
				{{ userStore.first_name }} {{ userStore.last_name }}
			</h1>
			
			<p class="profile-viewer__username">
				@{{ userStore.username }}
			</p>
		</div>
		
		<span class="profile-viewer__age">
			{{ userProfileStore.age }} ans
		</span>
	</header>
	
	<div class="profile-viewer__location">
		<span>📍</span>
		<span>{{ userProfileStore.location }}</span>
	</div>
	
	<!-- Actions -->
	<div class="profile-viewer__actions">
		<button
		v-if="!liked"
		type="button"
		class="profile-viewer__button profile-viewer__button--like"
		@click="handleLike"
		>
		<span>♥</span>
		Liker
	</button>
	
	<button
	v-else
	type="button"
	class="profile-viewer__button profile-viewer__button--unlike"
	@click="handleUnlike"
	>
	<span>♥</span>
	Retirer le like
</button>
<button
type="button"
class="profile-viewer__button profile-viewer__button--block"
@click="handleBlocked"
>
<span>⚑</span>
Bloquer
</button>
<button
type="button"
class="profile-viewer__button profile-viewer__button--report"
@click="handleReport"
>
<span>⚑</span>
Signaler
</button>
</div>
</section>
<ReportModal
:open="showReportModal"
@close="showReportModal = false"
@report="handleReportSubmit"
/>
</main>
</template>

<style scoped>
.profile-viewer {
	width: 100%;
	min-height: 100%;
	background: #fff;
}

/* =========================
PHOTOS
========================= */

.profile-viewer__photos {
	width: 100%;
	max-width: 1100px;
	margin: 0 auto;
}

.profile-viewer__main-photo {
	width: 100%;
	height: min(70vh, 700px);
	min-height: 400px;
	overflow: hidden;
	background: #f8eeee;
}

.profile-viewer__main-photo img {
	width: 100%;
	height: 100%;
	display: block;
	object-fit: cover;
}

.profile-viewer__no-photo {
	width: 100%;
	height: 500px;
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;
	gap: 10px;
	background: #f8eeee;
	color: #8b777d;
}

.profile-viewer__no-photo span {
	font-size: 42px;
}

.profile-viewer__no-photo p {
	margin: 0;
}

/* Galerie des 4 photos restantes */
.profile-viewer__gallery {
	display: grid;
	grid-template-columns: repeat(4, 1fr);
	gap: 4px;
	margin-top: 4px;
}

.profile-viewer__gallery-item {
	height: 220px;
	overflow: hidden;
	background: #f8eeee;
}

.profile-viewer__gallery-item img {
	width: 100%;
	height: 100%;
	display: block;
	object-fit: cover;
	transition: transform 0.25s ease;
}

.profile-viewer__gallery-item:hover img {
	transform: scale(1.03);
}

/* =========================
INFORMATIONS
========================= */

.profile-viewer__info {
	width: 100%;
	max-width: 900px;
	margin: 0 auto;
	padding: 36px 24px 48px;
}

.profile-viewer__header {
	display: flex;
	align-items: flex-end;
	justify-content: space-between;
	gap: 20px;
}

.profile-viewer__header h1 {
	margin: 0;
	color: #302329;
	font-size: 34px;
	line-height: 1.15;
	font-weight: 700;
}

.profile-viewer__username {
	margin: 8px 0 0;
	color: #b85570;
	font-size: 16px;
}

.profile-viewer__age {
	color: #8b777d;
	font-size: 20px;
	white-space: nowrap;
}

.profile-viewer__location {
	display: flex;
	align-items: center;
	gap: 8px;
	margin-top: 18px;
	color: #8b777d;
	font-size: 16px;
}

/* =========================
ACTIONS
========================= */

.profile-viewer__actions {
	display: flex;
	gap: 12px;
	margin-top: 32px;
}

.profile-viewer__button {
	min-height: 48px;
	padding: 0 24px;
	border: 0;
	border-radius: 14px;
	font: inherit;
	font-weight: 600;
	cursor: pointer;
	transition:
	transform 0.2s ease,
	box-shadow 0.2s ease,
	background 0.2s ease;
}

.profile-viewer__button:hover {
	transform: translateY(-1px);
}

.profile-viewer__button:active {
	transform: translateY(0);
}

.profile-viewer__button--like {
	flex: 1;
	color: white;
	background: linear-gradient(135deg, #f6a2b5, #ed6284);
	box-shadow: 0 8px 20px rgba(237, 98, 132, 0.22);
}

.profile-viewer__button--like:hover {
	box-shadow: 0 10px 24px rgba(237, 98, 132, 0.3);
}

.profile-viewer__button--unlike {
	flex: 1;
	color: #b85570;
	background: #fff0f3;
	border: 1px solid #f6d5de;
}

.profile-viewer__button--report {
	color: #8b777d;
	background: #f8f1f3;
}

.profile-viewer__button--report:hover {
	color: #b85570;
	background: #fff0f3;
}

.profile-viewer__button--block {
	color: #8b777d;
	background: #f8f1f3;
}

.profile-viewer__button--block:hover {
	color: #b85570;
	background: #fff0f3;
}

.profile-viewer__button span {
	margin-right: 6px;
}

/* =========================
TABLETTE
========================= */

@media (max-width: 800px) {
	.profile-viewer__main-photo {
		height: 60vh;
		min-height: 350px;
	}
	
	.profile-viewer__gallery-item {
		height: 180px;
	}
	
	.profile-viewer__info {
		padding: 28px 20px 40px;
	}
}

/* =========================
MOBILE
========================= */

@media (max-width: 600px) {
	.profile-viewer__main-photo {
		height: 65vh;
		min-height: 320px;
		max-height: 550px;
	}
	
	.profile-viewer__gallery {
		grid-template-columns: repeat(2, 1fr);
	}
	
	.profile-viewer__gallery-item {
		height: 180px;
	}
	
	.profile-viewer__info {
		padding: 24px 16px 32px;
	}
	
	.profile-viewer__header {
		align-items: flex-start;
	}
	
	.profile-viewer__header h1 {
		font-size: 27px;
	}
	
	.profile-viewer__age {
		font-size: 17px;
	}
	
	.profile-viewer__actions {
		flex-direction: column;
		margin-top: 26px;
	}
	
	.profile-viewer__button {
		width: 100%;
	}
}

/* =========================
PETIT MOBILE
========================= */

@media (max-width: 400px) {
	.profile-viewer__main-photo {
		height: 60vh;
		min-height: 280px;
	}
	
	.profile-viewer__gallery-item {
		height: 140px;
	}
	
	.profile-viewer__header h1 {
		font-size: 24px;
	}
}
</style>