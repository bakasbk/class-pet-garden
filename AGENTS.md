# AGENTS.md - ClassPetGarden (班级宠物园)

> Guide for AI coding agents working in this repository.

## Project Overview

A gamified class management system combining points tracking with virtual pet adoption. Built for teachers to manage student behavior through positive reinforcement.

**Tech Stack:**
- Frontend: Vue 3 + TypeScript + Vite + Tailwind CSS + Pinia + Vue Router
- Backend: Node.js + Express + SQLite (better-sqlite3)
- Language: TypeScript (frontend), JavaScript ES Modules (backend)

---

## Build / Dev / Test Commands

```bash
# Development
npm run dev          # Start frontend dev server (port 3001)
npm run server       # Start backend API server (port 3002)
npm run start        # Start both frontend + backend concurrently

# Production
npm run build        # Type-check + build frontend (vue-tsc && vite build)
npm run preview      # Preview production build

# Backend only (from server/ directory)
cd server && npm start
```

**No test framework configured.** If adding tests, recommend Vitest for consistency with Vite ecosystem.

**No linter configured.** If adding linting, recommend ESLint + @typescript-eslint + Vue plugin.

---

## Project Structure

```
class-pet-garden/
├── src/                      # Frontend source
│   ├── main.ts              # App entry point
│   ├── App.vue              # Root component
│   ├── style.css            # Global styles (Tailwind imports)
│   ├── router/index.ts      # Vue Router config
│   ├── data/pets.ts         # Pet types & level calculations
│   ├── pages/Home.vue       # Main page (all UI logic)
│   ├── components/          # Reusable components (layout/, modals/, pet/, student/)
│   ├── stores/              # Pinia stores (currently empty)
│   └── utils/               # Utility functions (currently empty)
├── server/
│   ├── index.js             # Express API + SQLite schema
│   └── pet-garden.db        # SQLite database file
├── public/images/pets/      # Pet images (normal/ & mythical/)
├── vite.config.ts           # Vite configuration
├── tsconfig.json            # TypeScript config (strict mode)
└── tailwind.config.js       # Tailwind theme (custom colors)
```

---

## Code Style Guidelines

### TypeScript / Vue

**Vue SFC Structure:**
```vue
<script setup lang="ts">
// 1. Imports (Vue, external, internal)
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import { helperFunction } from '@/utils/helpers'

// 2. Types/Interfaces
interface Student {
  id: string
  name: string
  // ...
}

// 3. State (refs, reactives)
const students = ref<Student[]>([])
const showModal = ref(false)

// 4. Computed properties
const filteredStudents = computed(() => ...)

// 5. Functions (async API calls, handlers)
async function loadStudents() { ... }

// 6. Lifecycle hooks
onMounted(() => { ... })
</script>

<template>
  <!-- Template with Tailwind classes -->
</template>
```

**Imports Order:**
1. Vue APIs (`vue`, `vue-router`, `pinia`)
2. External libraries (`axios`)
3. Internal modules with `@/` alias
4. Types (if separate)

**Path Aliases:**
- Use `@/` for src imports: `import { PET_TYPES } from '@/data/pets'`

**TypeScript Settings:**
- Strict mode enabled (`strict: true`)
- `noUnusedLocals: true`, `noUnusedParameters: true`
- Target: ES2020

### Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Vue components | PascalCase | `StudentCard.vue` |
| TypeScript files | camelCase | `pets.ts`, `storage.ts` |
| Variables/refs | camelCase | `const students = ref([])` |
| Functions | camelCase | `async function loadStudents()` |
| Interfaces | PascalCase | `interface Student { ... }` |
| Constants | SCREAMING_SNAKE_CASE | `export const PET_TYPES` |

### Styling

- **Tailwind CSS** for all styling
- Custom colors defined in `tailwind.config.js`:
  - `primary`: `#FF9F43` (orange)
  - `secondary`: `#26DE81` (green)
  - `danger`: `#EF4444` (red)
  - `warning`: `#F59E0B` (amber)
- Use Tailwind utility classes inline in templates
- Responsive prefixes: `md:`, `lg:`, `xl:`
- Hover states: `hover:bg-orange-500`

### API Layer

**Frontend API calls (axios):**
```typescript
// Create axios instance with baseURL
const api = axios.create({
  baseURL: '/pet-garden/api'
})

// Async/await pattern
async function loadData() {
  try {
    const res = await api.get('/classes')
    classes.value = res.data.classes
  } catch (error) {
    console.error('加载失败:', error)
  }
}
```

**Backend routes (Express):**
```javascript
// ES Modules syntax
import express from 'express'

// Route handlers
app.get('/api/classes', (req, res) => {
  const classes = db.prepare('SELECT * FROM classes').all()
  res.json({ classes })
})
```

### Error Handling

**Frontend:**
- Always use try/catch with async API calls
- Log errors with `console.error()`
- Show user-friendly alerts: `alert('操作失败，请重试')`

**Backend:**
- Return `{ error: 'message' }` for failures
- Use appropriate HTTP status codes (400, 404, 500)
- Log server errors: `console.error('Error:', error)`

---

## Backend API Reference

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/classes` | GET, POST | List/create classes |
| `/api/classes/:id` | PUT, DELETE | Update/delete class |
| `/api/classes/:id/students` | GET | Get students in class |
| `/api/students` | POST | Add student |
| `/api/students/:id` | PUT, DELETE | Update/delete student |
| `/api/students/import` | POST | Batch import students |
| `/api/students/:id/pet` | PUT | Select/change pet |
| `/api/rules` | GET, POST | Get/add evaluation rules |
| `/api/evaluations` | GET, POST | Evaluation records |
| `/api/evaluations/latest` | DELETE | Undo last evaluation |
| `/api/backup` | GET | Export JSON backup |
| `/api/restore` | POST | Restore from backup |

---

## Key Domain Concepts

**Pet System:**
- 25 pet types: 18 normal + 7 mythical
- 8 levels total (Lv.1 start, Lv.8 = graduation)
- Level-up thresholds: `[40, 60, 80, 100, 120, 140, 160]` exp each
- Graduated pets earn badges

**Points System:**
- Categories: 学习 (Learning), 行为 (Behavior), 健康 (Health), 其他 (Other)
- Positive = add points, Negative = subtract points
- Points contribute to pet experience

**Data Persistence:**
- SQLite database at `server/pet-garden.db`
- All data in single `.db` file (easy backup/restore)

---

## Development Notes

1. **Comments are in Chinese** - Match this style for consistency
2. **No tests currently** - Verify manually with `npm run dev` + `npm run server`
3. **Run both servers** for full functionality: `npm run start`
4. **Proxy configured** in Vite: `/pet-garden/api` → `http://localhost:3002`
5. **Type checking** before build: `vue-tsc` runs automatically with `npm run build`