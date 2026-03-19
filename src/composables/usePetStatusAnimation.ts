import { ref } from 'vue'
import { getPetLevelImage } from '@/data/pets'

type PetStatus = 'alive' | 'injured' | 'dead'
type AnimationType = 'injured' | 'death' | 'revive' | 'heal'

interface PetStatusAnimation {
  type: AnimationType
  name: string
  petType: string
  petLevel: number
  fromStatus: PetStatus
  toStatus: PetStatus
}

// 全局状态（单例模式）
const showAnimation = ref(false)
const animationInfo = ref<PetStatusAnimation>({
  type: 'injured',
  name: '',
  petType: '',
  petLevel: 1,
  fromStatus: 'alive',
  toStatus: 'injured'
})
const animationPhase = ref<'start' | 'effect' | 'end'>('start')

export function usePetStatusAnimation() {
  function triggerAnimation(
    type: AnimationType,
    name: string,
    petType: string,
    petLevel: number,
    fromStatus: PetStatus,
    toStatus: PetStatus
  ) {
    animationInfo.value = { type, name, petType, petLevel, fromStatus, toStatus }
    animationPhase.value = 'start'
    showAnimation.value = true

    // 动画时序
    setTimeout(() => { animationPhase.value = 'effect' }, 300)
    setTimeout(() => { animationPhase.value = 'end' }, 1500)
    setTimeout(() => { showAnimation.value = false }, 2500)
  }

  function getPetImage() {
    if (!animationInfo.value.petType) return ''
    return getPetLevelImage(animationInfo.value.petType, animationInfo.value.petLevel)
  }

  function getAnimationConfig() {
    const configs: Record<AnimationType, { emoji: string; title: string; colorClass: string; bgColor: string }> = {
      injured: {
        emoji: '🩹',
        title: '宠物受伤了',
        colorClass: 'text-orange-500',
        bgColor: 'bg-gradient-to-br from-orange-100 to-red-100'
      },
      death: {
        emoji: '💀',
        title: '宠物死亡',
        colorClass: 'text-gray-600',
        bgColor: 'bg-gradient-to-br from-gray-200 to-gray-300'
      },
      revive: {
        emoji: '✨',
        title: '宠物复活了！',
        colorClass: 'text-green-500',
        bgColor: 'bg-gradient-to-br from-green-100 to-emerald-100'
      },
      heal: {
        emoji: '💚',
        title: '恢复健康！',
        colorClass: 'text-green-500',
        bgColor: 'bg-gradient-to-br from-green-100 to-teal-100'
      }
    }
    return configs[animationInfo.value.type]
  }

  return {
    showAnimation,
    animationInfo,
    animationPhase,
    triggerAnimation,
    getPetImage,
    getAnimationConfig
  }
}