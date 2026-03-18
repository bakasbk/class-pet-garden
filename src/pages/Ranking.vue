<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import type { Student } from '@/types'
import { useAuth } from '@/composables/useAuth'
import { getPetLevelImage, calculateLevel } from '@/data/pets'

const { api } = useAuth()

const students = ref<Student[]>([])
const isLoading = ref(true)

// 排序方式
const sortBy = ref<'points' | 'level' | 'name'>('points')

// 排行榜数据
const ranking = computed(() => {
  return [...students.value].sort((a, b) => {
    switch (sortBy.value) {
      case 'points':
        return b.total_points - a.total_points
      case 'level':
        return (b.pet_level || 0) - (a.pet_level || 0) || b.total_points - a.total_points
      case 'name':
        return a.name.localeCompare(b.name)
      default:
        return 0
    }
  })
})

// 前三名
const top3 = computed(() => ranking.value.slice(0, 3))
// 其余学生
const rest = computed(() => ranking.value.slice(3))

function getStudentPetImage(student: Student): string {
  if (!student.pet_type) return ''
  return getPetLevelImage(student.pet_type, student.pet_level)
}

function getDisplayLevel(student: Student): number {
  return calculateLevel(student.pet_exp)
}

async function loadRanking() {
  isLoading.value = true
  try {
    const classRes = await api.get('/classes')
    const classes = classRes.data.classes
    if (classes.length > 0) {
      const res = await api.get(`/classes/${classes[0].id}/students`)
      students.value = res.data.students
    }
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  loadRanking()
})
</script>

<template>
  <div class="min-h-screen bg-gradient-to-br from-orange-50 via-pink-50 to-purple-50 p-6">
    <!-- 头部 -->
    <header class="mb-6">
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-3xl font-bold text-gradient flex items-center gap-3">
            <span class="text-4xl">🏆</span>
            积分排行榜
          </h1>
          <p class="text-gray-500 mt-2">共 {{ students.length }} 名学生</p>
        </div>
        <router-link to="/" class="px-6 py-3 bg-white rounded-xl shadow-md hover:shadow-lg transition-all font-medium text-gray-700">
          ← 返回首页
        </router-link>
      </div>
    </header>

    <!-- 排序按钮 -->
    <div class="flex gap-3 mb-6">
      <button
        @click="sortBy = 'points'"
        class="px-5 py-2.5 rounded-xl font-bold transition-all"
        :class="sortBy === 'points'
          ? 'bg-gradient-to-r from-orange-400 to-pink-500 text-white shadow-lg'
          : 'bg-white text-gray-600 hover:bg-gray-50 shadow-md'"
      >
        ⭐ 按积分
      </button>
      <button
        @click="sortBy = 'level'"
        class="px-5 py-2.5 rounded-xl font-bold transition-all"
        :class="sortBy === 'level'
          ? 'bg-gradient-to-r from-orange-400 to-pink-500 text-white shadow-lg'
          : 'bg-white text-gray-600 hover:bg-gray-50 shadow-md'"
      >
        📈 按等级
      </button>
      <button
        @click="sortBy = 'name'"
        class="px-5 py-2.5 rounded-xl font-bold transition-all"
        :class="sortBy === 'name'
          ? 'bg-gradient-to-r from-orange-400 to-pink-500 text-white shadow-lg'
          : 'bg-white text-gray-600 hover:bg-gray-50 shadow-md'"
      >
        🔤 按姓名
      </button>
    </div>

    <!-- 加载中 -->
    <div v-if="isLoading" class="flex items-center justify-center py-20">
      <div class="text-center">
        <div class="text-6xl animate-bounce mb-4">🐾</div>
        <div class="text-gray-500">加载中...</div>
      </div>
    </div>

    <!-- 无数据 -->
    <div v-else-if="students.length === 0" class="flex items-center justify-center py-20">
      <div class="text-center">
        <div class="text-6xl mb-4">📊</div>
        <div class="text-gray-500">暂无学生数据</div>
      </div>
    </div>

    <!-- 排行榜 -->
    <template v-else>
      <!-- 前三名 - 特殊展示 -->
      <div v-if="top3.length > 0" class="grid grid-cols-3 gap-4 mb-6">
        <div
          v-for="(student, index) in top3"
          :key="student.id"
          class="relative bg-white rounded-2xl p-4 shadow-lg transition-all hover:shadow-xl"
          :class="{ 'transform scale-105': index === 0 }"
        >
          <!-- 排名徽章 -->
          <div class="absolute -top-3 -left-3 w-10 h-10 rounded-full flex items-center justify-center text-2xl shadow-lg"
            :class="{
              'bg-gradient-to-r from-yellow-400 to-amber-400': index === 0,
              'bg-gradient-to-r from-gray-300 to-slate-400': index === 1,
              'bg-gradient-to-r from-orange-300 to-amber-400': index === 2
            }">
            {{ index === 0 ? '🥇' : index === 1 ? '🥈' : '🥉' }}
          </div>

          <!-- 宠物头像 -->
          <div class="w-16 h-16 mx-auto rounded-full flex items-center justify-center overflow-hidden bg-gradient-to-br from-orange-100 to-pink-100 shadow-inner">
            <img
              v-if="student.pet_type"
              :src="getStudentPetImage(student)"
              class="w-14 h-14 object-contain"
            />
            <span v-else class="text-3xl">❓</span>
          </div>

          <!-- 信息 -->
          <div class="text-center mt-3">
            <div class="font-bold text-gray-800 truncate">{{ student.name }}</div>
            <div class="text-xs text-gray-500 mt-1">Lv.{{ getDisplayLevel(student) }}</div>
            <div class="text-lg font-bold mt-1" :class="index === 0 ? 'text-orange-500' : index === 1 ? 'text-gray-500' : 'text-amber-600'">
              ⭐ {{ student.total_points }}
            </div>
          </div>
        </div>
      </div>

      <!-- 其余学生 - 网格布局 -->
      <div v-if="rest.length > 0" class="grid grid-cols-4 md:grid-cols-6 lg:grid-cols-8 gap-3">
        <div
          v-for="(student, index) in rest"
          :key="student.id"
          class="bg-white rounded-xl p-3 shadow-md hover:shadow-lg transition-all"
        >
          <div class="flex items-center gap-2">
            <!-- 排名 -->
            <div class="w-6 h-6 rounded-full bg-gray-100 flex items-center justify-center text-xs font-bold text-gray-500">
              {{ index + 4 }}
            </div>

            <!-- 宠物 -->
            <div class="w-8 h-8 rounded-full flex items-center justify-center overflow-hidden bg-gradient-to-br from-orange-100 to-pink-100">
              <img
                v-if="student.pet_type"
                :src="getStudentPetImage(student)"
                class="w-7 h-7 object-contain"
              />
              <span v-else class="text-lg">❓</span>
            </div>

            <!-- 信息 -->
            <div class="flex-1 min-w-0">
              <div class="font-medium text-sm text-gray-800 truncate">{{ student.name }}</div>
              <div class="text-xs text-gray-400">⭐{{ student.total_points }}</div>
            </div>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<style scoped>
.text-gradient {
  background: linear-gradient(to right, #f97316, #ec4899);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
</style>