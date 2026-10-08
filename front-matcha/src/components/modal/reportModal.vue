<script setup lang="ts">
import { ref } from 'vue'

type ReportReason = 'fake_account' | 'scam' | 'problematic'

defineProps<{
  open: boolean
}>()

const emit = defineEmits<{
  close: []
  report: [reason: ReportReason]
}>()

const selectedReason = ref<ReportReason | null>(null)

const reasons = [
  {
    value: 'fake_account' as ReportReason,
    title: 'Faux compte',
    description: 'Ce profil semble être un faux compte ou usurper une identité.',
    icon: '👤',
  },
  {
    value: 'scam' as ReportReason,
    title: 'Scam',
    description: 'Cet utilisateur semble essayer de m’arnaquer ou de me soutirer de l’argent.',
    icon: '⚠️',
  },
  {
    value: 'problematic' as ReportReason,
    title: 'Problématique',
    description: 'Le comportement ou le contenu de cet utilisateur pose problème.',
    icon: '🚩',
  },
]

function selectReason(reason: ReportReason) {
  selectedReason.value = reason
}

function close() {
  selectedReason.value = null
  emit('close')
}

function submitReport() {
  if (!selectedReason.value) return

  emit('report', selectedReason.value)

  selectedReason.value = null
}
</script>

<template>
  <Teleport to="body">
    <Transition name="report-modal">
      <div
        v-if="open"
        class="report-modal"
        @click.self="close"
      >
        <div
          class="report-modal__content"
          role="dialog"
          aria-modal="true"
          aria-labelledby="report-title"
        >
          <!-- Header -->
          <header class="report-modal__header">
            <div>
              <h2 id="report-title">
                Signaler cet utilisateur
              </h2>

              <p>
                Pourquoi souhaitez-vous signaler ce profil ?
              </p>
            </div>

            <button
              type="button"
              class="report-modal__close"
              aria-label="Fermer"
              @click="close"
            >
              ×
            </button>
          </header>

          <!-- Reasons -->
          <div class="report-modal__reasons">
            <button
              v-for="reason in reasons"
              :key="reason.value"
              type="button"
              class="report-modal__reason"
              :class="{
                'report-modal__reason--selected':
                  selectedReason === reason.value
              }"
              @click="selectReason(reason.value)"
            >
              <span class="report-modal__reason-icon">
                {{ reason.icon }}
              </span>

              <span class="report-modal__reason-content">
                <strong>
                  {{ reason.title }}
                </strong>

                <small>
                  {{ reason.description }}
                </small>
              </span>

              <span class="report-modal__radio">
                <span
                  v-if="selectedReason === reason.value"
                />
              </span>
            </button>
          </div>

          <!-- Actions -->
          <footer class="report-modal__actions">
            <button
              type="button"
              class="report-modal__cancel"
              @click="close"
            >
              Annuler
            </button>

            <button
              type="button"
              class="report-modal__submit"
              :disabled="!selectedReason"
              @click="submitReport"
            >
              Signaler
            </button>
          </footer>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<style scoped>
.report-modal {
  position: fixed;
  inset: 0;
  z-index: 1000;

  display: flex;
  align-items: center;
  justify-content: center;

  padding: 20px;

  background: rgba(48, 35, 41, 0.45);
  backdrop-filter: blur(4px);
}

.report-modal__content {
  width: 100%;
  max-width: 520px;
  max-height: calc(100vh - 40px);

  overflow-y: auto;

  background: #ffffff;
  border: 1px solid #f1e5e5;
  border-radius: 24px;

  box-shadow: 0 20px 60px rgba(60, 30, 40, 0.2);
}

/* =========================
   HEADER
   ========================= */

.report-modal__header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;

  gap: 20px;
  padding: 28px 28px 20px;
}

.report-modal__header h2 {
  margin: 0;

  color: #302329;
  font-size: 23px;
  line-height: 1.2;
}

.report-modal__header p {
  margin: 8px 0 0;

  color: #8b777d;
  font-size: 14px;
}

.report-modal__close {
  flex-shrink: 0;

  width: 36px;
  height: 36px;

  border: 0;
  border-radius: 50%;

  color: #8b777d;
  background: #f8f1f3;

  font-size: 26px;
  line-height: 1;

  cursor: pointer;

  transition:
    background 0.2s ease,
    color 0.2s ease;
}

.report-modal__close:hover {
  color: #b85570;
  background: #fff0f3;
}

/* =========================
   REASONS
   ========================= */

.report-modal__reasons {
  display: flex;
  flex-direction: column;
  gap: 10px;

  padding: 8px 28px 24px;
}

.report-modal__reason {
  width: 100%;

  display: flex;
  align-items: center;

  gap: 14px;

  padding: 16px;

  border: 1px solid #f1e5e5;
  border-radius: 16px;

  text-align: left;

  background: #ffffff;

  cursor: pointer;

  transition:
    border-color 0.2s ease,
    background 0.2s ease,
    transform 0.2s ease;
}

.report-modal__reason:hover {
  border-color: #f6c8d4;
  background: #fff8fa;
  transform: translateY(-1px);
}

.report-modal__reason--selected {
  border-color: #ed6284;
  background: #fff0f3;
}

.report-modal__reason-icon {
  width: 42px;
  height: 42px;

  flex-shrink: 0;

  display: flex;
  align-items: center;
  justify-content: center;

  border-radius: 12px;

  background: #f8eeee;

  font-size: 20px;
}

.report-modal__reason-content {
  min-width: 0;

  display: flex;
  flex: 1;
  flex-direction: column;
  gap: 4px;
}

.report-modal__reason-content strong {
  color: #302329;
  font-size: 15px;
}

.report-modal__reason-content small {
  color: #8b777d;
  font-size: 12px;
  line-height: 1.4;
}

/* =========================
   RADIO
   ========================= */

.report-modal__radio {
  width: 20px;
  height: 20px;

  flex-shrink: 0;

  display: flex;
  align-items: center;
  justify-content: center;

  border: 2px solid #d9c7cc;
  border-radius: 50%;
}

.report-modal__reason--selected .report-modal__radio {
  border-color: #ed6284;
}

.report-modal__radio span {
  width: 10px;
  height: 10px;

  border-radius: 50%;
  background: #ed6284;
}

/* =========================
   ACTIONS
   ========================= */

.report-modal__actions {
  display: flex;
  gap: 10px;

  padding: 20px 28px 28px;

  border-top: 1px solid #f1e5e5;
}

.report-modal__actions button {
  min-height: 46px;

  border-radius: 13px;

  font: inherit;
  font-weight: 600;

  cursor: pointer;

  transition:
    transform 0.2s ease,
    background 0.2s ease,
    box-shadow 0.2s ease;
}

.report-modal__cancel {
  flex: 1;

  border: 1px solid #f1e5e5;

  color: #8b777d;
  background: #ffffff;
}

.report-modal__cancel:hover {
  background: #f8f1f3;
}

.report-modal__submit {
  flex: 1;

  border: 0;

  color: #ffffff;
  background: linear-gradient(135deg, #f6a2b5, #ed6284);

  box-shadow: 0 8px 18px rgba(237, 98, 132, 0.2);
}

.report-modal__submit:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 10px 22px rgba(237, 98, 132, 0.28);
}

.report-modal__submit:disabled {
  opacity: 0.45;
  cursor: not-allowed;
  box-shadow: none;
}

/* =========================
   TRANSITION
   ========================= */

.report-modal-enter-active,
.report-modal-leave-active {
  transition: opacity 0.2s ease;
}

.report-modal-enter-active .report-modal__content,
.report-modal-leave-active .report-modal__content {
  transition:
    transform 0.2s ease,
    opacity 0.2s ease;
}

.report-modal-enter-from,
.report-modal-leave-to {
  opacity: 0;
}

.report-modal-enter-from .report-modal__content,
.report-modal-leave-to .report-modal__content {
  opacity: 0;
  transform: translateY(15px) scale(0.98);
}

/* =========================
   MOBILE
   ========================= */

@media (max-width: 600px) {
  .report-modal {
    align-items: flex-end;
    padding: 0;
  }

  .report-modal__content {
    max-height: 90vh;

    border-radius: 24px 24px 0 0;
  }

  .report-modal__header {
    padding: 24px 20px 18px;
  }

  .report-modal__reasons {
    padding: 8px 20px 20px;
  }

  .report-modal__reason {
    padding: 14px;
  }

  .report-modal__reason-content small {
    font-size: 11px;
  }

  .report-modal__actions {
    padding: 16px 20px 24px;
  }
}
</style>