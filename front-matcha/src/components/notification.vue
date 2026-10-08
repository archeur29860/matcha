<script setup lang="ts">
import { computed, onBeforeUnmount, ref, watch } from 'vue'


// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

export type NotificationType =
| 'success'
| 'error'
| 'warning'
| 'info'

export type NotificationPosition =
| 'top-left'
| 'top-center'
| 'top-right'
| 'bottom-left'
| 'bottom-center'
| 'bottom-right'


// ---------------------------------------------------------------------------
// Props
// ---------------------------------------------------------------------------

interface Props {
    show: boolean
    
    title?: string
    message?: string
    
    type?: NotificationType
    
    duration?: number
    
    position?: NotificationPosition
    
    closable?: boolean
    
    showIcon?: boolean
    
    width?: string
    
    zIndex?: number
}

const props = withDefaults(defineProps<Props>(), {
    title: '',
    message: '',
    
    type: 'info',
    
    duration: 3000,
    
    position: 'top-right',
    
    closable: true,
    
    showIcon: true,
    
    width: '360px',
    
    zIndex: 9999,
})


// ---------------------------------------------------------------------------
// Emits
// ---------------------------------------------------------------------------

const emit = defineEmits<{
    close: []
}>()


// ---------------------------------------------------------------------------
// State interne
// ---------------------------------------------------------------------------

const visible = ref(false)

let timeout: ReturnType<typeof setTimeout> | null = null
    
    
// ---------------------------------------------------------------------------
// Notification depuis une réponse API
// ---------------------------------------------------------------------------

function make_notification(result: any) {
    
    /*
    * Succès HTTP + succès API
    */
    if (result.success) {
        show_notification(
        'Succès',
        'Opération effectuée avec succès.',
        'success',
        )
        
        return
    }
    
    
    /*
    * Erreur API
    */
    show_notification(
    result.error?.code ?? `Erreur HTTP ${result.status}`,
    result.error?.message ?? 'Une erreur est survenue.',
    'error',
    )
}


// ---------------------------------------------------------------------------
// Affichage d'une notification
// ---------------------------------------------------------------------------

function show_notification(
notificationTitle: string,
notificationMessage: string,
notificationType: NotificationType,
) {
    /*
    * Cette fonction permet de modifier temporairement
    * le contenu de la notification.
    *
    * Comme les props restent inchangées, on utilise
    * des états internes uniquement pour les notifications
    * déclenchées avec make_notification().
    */
    
    internalTitle.value = notificationTitle
    internalMessage.value = notificationMessage
    internalType.value = notificationType
    internalVisible.value = true
    
    startTimer()
}


// ---------------------------------------------------------------------------
// État interne pour make_notification()
// ---------------------------------------------------------------------------

const internalVisible = ref(false)

const internalTitle = ref('')
const internalMessage = ref('')
const internalType = ref<NotificationType>('info')
    
    
// ---------------------------------------------------------------------------
// Valeurs affichées
// ---------------------------------------------------------------------------

const displayedVisible = computed(() => {
    if (internalVisible.value) {
        return true
    }
    
    return visible.value
})

const displayedTitle = computed(() => {
    if (internalVisible.value) {
        return internalTitle.value
    }
    
    return props.title
})

const displayedMessage = computed(() => {
    if (internalVisible.value) {
        return internalMessage.value
    }
    
    return props.message
})

const displayedType = computed<NotificationType>(() => {
    if (internalVisible.value) {
        return internalType.value
    }
    
    return props.type
})


// ---------------------------------------------------------------------------
// Icons
// ---------------------------------------------------------------------------

const icon = computed(() => {
    if (!props.showIcon) {
        return ''
    }
    
    switch (displayedType.value) {
        case 'success':
        return '✓'
        
        case 'error':
        return '✕'
        
        case 'warning':
        return '⚠'
        
        case 'info':
        return 'ⓘ'
        
        default:
        return 'ⓘ'
    }
})


// ---------------------------------------------------------------------------
// Position
// ---------------------------------------------------------------------------

const positionClass = computed(() => {
    return `notification-${props.position}`
})


// ---------------------------------------------------------------------------
// Close
// ---------------------------------------------------------------------------

function close() {
    visible.value = false
    internalVisible.value = false
    
    if (timeout) {
        clearTimeout(timeout)
        timeout = null
    }
    
    emit('close')
}


// ---------------------------------------------------------------------------
// Auto close
// ---------------------------------------------------------------------------

function startTimer() {
    if (timeout) {
        clearTimeout(timeout)
        timeout = null
    }
    
    if (props.duration <= 0) {
        return
    }
    
    timeout = setTimeout(() => {
        close()
    }, props.duration)
}


// ---------------------------------------------------------------------------
// Watch show
// ---------------------------------------------------------------------------

watch(
() => props.show,
(show) => {
    if (show) {
        visible.value = true
        startTimer()
    } else {
        visible.value = false
        
        if (timeout) {
            clearTimeout(timeout)
            timeout = null
        }
    }
},
{
    immediate: true,
},
)


// ---------------------------------------------------------------------------
// Expose
// ---------------------------------------------------------------------------

defineExpose({
    make_notification,
})


// ---------------------------------------------------------------------------
// Cleanup
// ---------------------------------------------------------------------------

onBeforeUnmount(() => {
    if (timeout) {
        clearTimeout(timeout)
    }
})
    </script>
    
    
    <template>
        <Teleport to="body">
            
            <Transition name="notification">
                
                <div
                v-if="displayedVisible"
                class="notification-wrapper"
                :class="positionClass"
                :style="{
                    zIndex,
                }"
                >
                
                <div
                class="notification"
                :class="`notification-${displayedType}`"
                :style="{
                    width,
                }"
                >
                
                <!-- Icon -->
                <div
                v-if="showIcon"
                class="notification-icon"
                >
                {{ icon }}
            </div>
            
            
            <!-- Content -->
            <div class="notification-content">
                
                <div
                v-if="displayedTitle"
                class="notification-title"
                >
                {{ displayedTitle }}
            </div>
            
            <div
            v-if="displayedMessage"
            class="notification-message"
            >
            {{ displayedMessage }}
        </div>
        
    </div>
    
    
    <!-- Close -->
    <button
    v-if="closable"
    type="button"
    class="notification-close"
    aria-label="Fermer"
    @click="close"
    >
    ×
</button>

</div>

</div>

</Transition>

</Teleport>
</template>


<style scoped>

/*
|--------------------------------------------------------------------------
| Wrapper
|--------------------------------------------------------------------------
*/

.notification-wrapper {
    position: fixed;
    
    display: flex;
    
    padding: 20px;
    
    pointer-events: none;
}


/*
|--------------------------------------------------------------------------
| Positions
|--------------------------------------------------------------------------
*/

.notification-top-left {
    top: 0;
    left: 0;
    
    justify-content: flex-start;
}

.notification-top-center {
    top: 0;
    left: 50%;
    
    transform: translateX(-50%);
    
    justify-content: center;
}

.notification-top-right {
    top: 0;
    right: 0;
    
    justify-content: flex-end;
}


.notification-bottom-left {
    bottom: 0;
    left: 0;
    
    justify-content: flex-start;
}

.notification-bottom-center {
    bottom: 0;
    left: 50%;
    
    transform: translateX(-50%);
    
    justify-content: center;
}

.notification-bottom-right {
    right: 0;
    bottom: 0;
    
    justify-content: flex-end;
}


/*
|--------------------------------------------------------------------------
| Notification
|--------------------------------------------------------------------------
*/

.notification {
    display: flex;
    align-items: flex-start;
    
    gap: 12px;
    
    padding: 14px 16px;
    
    border-radius: 10px;
    
    background: white;
    
    box-shadow:
    0 10px 30px rgba(0, 0, 0, 0.15);
    
    pointer-events: auto;
}


/*
|--------------------------------------------------------------------------
| Types
|--------------------------------------------------------------------------
*/

.notification-success {
    border-left: 4px solid #22c55e;
}

.notification-error {
    border-left: 4px solid #ef4444;
}

.notification-warning {
    border-left: 4px solid #f59e0b;
}

.notification-info {
    border-left: 4px solid #3b82f6;
}


/*
|--------------------------------------------------------------------------
| Icon
|--------------------------------------------------------------------------
*/

.notification-icon {
    flex-shrink: 0;
    
    display: flex;
    align-items: center;
    justify-content: center;
    
    width: 24px;
    height: 24px;
    
    font-size: 18px;
    font-weight: 700;
}

.notification-success .notification-icon {
    color: #22c55e;
}

.notification-error .notification-icon {
    color: #ef4444;
}

.notification-warning .notification-icon {
    color: #f59e0b;
}

.notification-info .notification-icon {
    color: #3b82f6;
}


/*
|--------------------------------------------------------------------------
| Content
|--------------------------------------------------------------------------
*/

.notification-content {
    flex: 1;
    
    min-width: 0;
}

.notification-title {
    margin-bottom: 3px;
    
    color: #111827;
    
    font-size: 14px;
    font-weight: 700;
}

.notification-message {
    color: #6b7280;
    
    font-size: 13px;
    
    line-height: 1.4;
}


/*
|--------------------------------------------------------------------------
| Close
|--------------------------------------------------------------------------
*/

.notification-close {
    flex-shrink: 0;
    
    width: 24px;
    height: 24px;
    
    padding: 0;
    
    border: none;
    
    background: transparent;
    
    color: #9ca3af;
    
    font-size: 20px;
    
    line-height: 1;
    
    cursor: pointer;
}

.notification-close:hover {
    color: #111827;
}


/*
|--------------------------------------------------------------------------
| Fade + slide
|--------------------------------------------------------------------------
*/

.notification-enter-active,
.notification-leave-active {
    transition:
    opacity 0.3s ease,
    transform 0.3s ease;
}

.notification-enter-from,
.notification-leave-to {
    opacity: 0;
}


/*
|--------------------------------------------------------------------------
| Top
|--------------------------------------------------------------------------
*/

.notification-top-left.notification-enter-from,
.notification-top-left.notification-leave-to {
    transform: translateX(-20px);
}

.notification-top-center.notification-enter-from,
.notification-top-center.notification-leave-to {
    transform: translate(-50%, -20px);
}

.notification-top-right.notification-enter-from,
.notification-top-right.notification-leave-to {
    transform: translateX(20px);
}


/*
|--------------------------------------------------------------------------
| Bottom
|--------------------------------------------------------------------------
*/

.notification-bottom-left.notification-enter-from,
.notification-bottom-left.notification-leave-to {
    transform: translateX(-20px);
}

.notification-bottom-center.notification-enter-from,
.notification-bottom-center.notification-leave-to {
    transform: translate(-50%, 20px);
}

.notification-bottom-right.notification-enter-from,
.notification-bottom-right.notification-leave-to {
    transform: translateX(20px);
}


/*
|--------------------------------------------------------------------------
| Mobile
|--------------------------------------------------------------------------
*/

@media (max-width: 600px) {
    
    .notification-wrapper {
        left: 0;
        right: 0;
        
        padding: 12px;
        
        justify-content: center;
    }
    
    .notification {
        width: 100% !important;
        
        max-width: 100%;
    }
    
    .notification-top-center,
    .notification-bottom-center {
        transform: none;
    }
    
    .notification-top-left,
    .notification-top-right {
        transform: none;
    }
    
    .notification-bottom-left,
    .notification-bottom-right {
        transform: none;
    }
}

</style>