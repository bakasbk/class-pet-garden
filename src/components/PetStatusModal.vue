<script setup lang="ts">
import { computed } from 'vue'

// 使用全局状态（通过 provide/inject 或直接导入）
import { usePetStatusAnimation } from '@/composables/usePetStatusAnimation'

// 直接使用共享的状态
const { showAnimation, animationInfo, animationPhase, getPetImage, getAnimationConfig } = usePetStatusAnimation()

const config = computed(() => getAnimationConfig())

// 动画类名
const containerClass = computed(() => {
  if (animationPhase.value === 'effect') {
    return 'animate-shake'
  }
  return ''
})

const petClass = computed(() => {
  if (animationInfo.value.type === 'death' && animationPhase.value !== 'start') {
    return 'grayscale opacity-50'
  }
  if (animationInfo.value.type === 'injured') {
    return 'hue-rotate-[-10deg]'
  }
  return ''
})
</script>

<template>
  <Teleport to="body">
    <Transition name="modal-fade">
      <div
        v-if="showAnimation"
        class="fixed inset-0 z-[100] flex items-center justify-center"
      >
        <!-- 背景遮罩 -->
        <div class="absolute inset-0 bg-black/40 backdrop-blur-sm"></div>

        <!-- 动画容器 -->
        <div
          class="relative z-10 flex flex-col items-center"
          :class="containerClass"
        >
          <!-- 背景光效 -->
          <div
            class="absolute inset-0 rounded-full blur-3xl opacity-50 scale-150"
            :class="config?.bgColor"
          ></div>

          <!-- 宠物图片 -->
          <div class="relative">
            <Transition name="pet-bounce" mode="out-in">
              <img
                :key="animationPhase"
                :src="getPetImage()"
                :alt="animationInfo.name"
                class="w-48 h-48 object-contain transition-all duration-500"
                :class="petClass"
              />
            </Transition>

            <!-- 状态图标 -->
            <Transition name="emoji-pop">
              <div
                v-if="animationPhase !== 'start'"
                class="absolute -top-4 -right-4 text-6xl animate-bounce"
              >
                {{ config?.emoji }}
              </div>
            </Transition>
          </div>

          <!-- 文字提示 -->
          <Transition name="text-fade">
            <div v-if="animationPhase !== 'start'" class="mt-6 text-center">
              <div class="text-2xl font-bold mb-2" :class="config?.colorClass">
                {{ animationInfo.name }}
              </div>
              <div class="text-xl font-medium text-gray-700">
                {{ config?.title }}
              </div>
            </div>
          </Transition>

          <!-- 粒子效果 -->
          <div v-if="animationInfo.type === 'revive'" class="absolute inset-0 pointer-events-none overflow-hidden">
            <span
              v-for="i in 12"
              :key="i"
              class="absolute text-2xl animate-sparkle"
              :style="{
                left: `${Math.random() * 100}%`,
                top: `${Math.random() * 100}%`,
                animationDelay: `${i * 100}ms`
              }"
            >
              ✨
            </span>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<style scoped>
.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: opacity 0.3s ease;
}
.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
}

.pet-bounce-enter-active {
  animation: petBounce 0.5s ease-out;
}
.pet-bounce-leave-active {
  transition: all 0.3s ease;
}
.pet-bounce-leave-to {
  opacity: 0;
  transform: scale(0.8);
}

@keyframes petBounce {
  0% { transform: scale(0.8); opacity: 0; }
  50% { transform: scale(1.1); }
  100% { transform: scale(1); opacity: 1; }
}

.emoji-pop-enter-active {
  animation: emojiPop 0.4s ease-out;
}
.emoji-pop-leave-active {
  transition: opacity 0.2s ease;
}
.emoji-pop-leave-to {
  opacity: 0;
}

@keyframes emojiPop {
  0% { transform: scale(0); opacity: 0; }
  50% { transform: scale(1.3); }
  100% { transform: scale(1); opacity: 1; }
}

.text-fade-enter-active {
  animation: textFade 0.4s ease-out;
}
.text-fade-leave-active {
  transition: opacity 0.2s ease;
}
.text-fade-leave-to {
  opacity: 0;
}

@keyframes textFade {
  0% { opacity: 0; transform: translateY(10px); }
  100% { opacity: 1; transform: translateY(0); }
}

.animate-shake {
  animation: shake 0.5s ease-in-out;
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  20% { transform: translateX(-10px); }
  40% { transform: translateX(10px); }
  60% { transform: translateX(-5px); }
  80% { transform: translateX(5px); }
}
</style>