<template>
  <Transition name="modal">
  <div v-if="modelValue" class="modal-mask" @click.self="close">
    <div class="modal-container" role="dialog" aria-modal="true">
      <div class="modal-head">
        <h3 class="modal-title">{{ title }}</h3>
        <button type="button" class="modal-x" aria-label="关闭" @click="close">
          <i class="fa-solid fa-xmark"></i>
        </button>
      </div>
      <div class="modal-body">
        <slot />
      </div>
      <div class="modal-footer">
        <button class="btn btn-outline-dark" @click="close">{{ cancelText }}</button>
        <button v-if="showConfirm" class="btn btn-primary" @click="confirm">{{ confirmText }}</button>
      </div>
    </div>
  </div>
  </Transition>
</template>

<script setup>
defineProps({
  modelValue: Boolean,
  title: { type: String, default: '提示' },
  cancelText: { type: String, default: '取消' },
  confirmText: { type: String, default: '确认' },
  showConfirm: { type: Boolean, default: true }
})
const emit = defineEmits(['update:modelValue', 'confirm'])

const close = () => emit('update:modelValue', false)
const confirm = () => emit('confirm')

</script>

<style scoped>
.modal-mask {
  position: fixed;
  z-index: 2000;
  inset: 0;
  background: rgba(20, 16, 30, 0.42);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 16px;
  box-sizing: border-box;
}

.modal-container {
  background: var(--c-surface);
  border-radius: var(--radius-lg);
  width: 800px;
  max-width: calc(100vw - 32px);
  padding: 24px;
  box-sizing: border-box;
  box-shadow: var(--shadow-lg);
  max-height: calc(100vh - 32px);
  display: flex;
  flex-direction: column;
}

.modal-head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 16px;
}

.modal-title {
  margin: 0;
  font-size: 19px;
  font-weight: 800;
}

.modal-x {
  flex-shrink: 0;
  width: 34px;
  height: 34px;
  padding: 0;
  border-radius: 10px;
  border: 1px solid var(--c-border);
  background: var(--c-surface);
  color: var(--c-text-2);
}

.modal-x:hover {
  background: var(--c-surface-2);
}

.modal-body {
  max-height: 70vh;
  min-height: 0;
  overflow-y: auto;
  overflow-x: hidden;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
  padding-top: 16px;
  border-top: 1px solid var(--c-border);
}

.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.22s ease;
}

.modal-enter-active .modal-container,
.modal-leave-active .modal-container {
  transition: transform 0.25s cubic-bezier(0.22, 1, 0.36, 1);
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-from .modal-container,
.modal-leave-to .modal-container {
  transform: translateY(12px) scale(0.98);
}

@media (max-width: 768px) {
  .modal-mask {
    align-items: flex-end;
    padding: calc(env(safe-area-inset-top, 0px) + 24px) 0 0;
  }

  .modal-container {
    width: 100%;
    max-width: 100%;
    max-height: 100%;
    border-radius: 24px 24px 0 0;
    padding: 20px 16px calc(env(safe-area-inset-bottom, 0px) + 16px);
  }

  .modal-body {
    max-height: none;
    flex: 1 1 auto;
  }

  .modal-enter-from .modal-container,
  .modal-leave-to .modal-container {
    transform: translateY(40px);
  }
}
</style>
