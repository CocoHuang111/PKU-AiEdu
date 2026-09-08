import { createRouter, createWebHashHistory } from 'vue-router'
import { authApi } from '../api/client'
import { authState, isAdmin, markAuthReady, setAuthConfig, setUser } from '../authStore'
import { resetQa } from '../qaStore'

const routes = [
  {
    path: '/login',
    component: () => import('../views/Login.vue'),
    meta: { public: true, title: '登录' },
  },
  {
    path: '/forbidden',
    component: () => import('../views/Forbidden.vue'),
    meta: { title: '无权限' },
  },
  {
    path: '/admin',
    component: () => import('../views/admin/AdminLayout.vue'),
    meta: { admin: true, title: '管理后台' },
    children: [
      { path: '', redirect: '/admin/overview' },
      {
        path: 'overview',
        component: () => import('../views/admin/Overview.vue'),
        meta: { admin: true, title: '概览' },
      },
      {
        path: 'users',
        component: () => import('../views/admin/Users.vue'),
        meta: { admin: true, title: '用户管理' },
      },
      {
        path: 'tasks',
        component: () => import('../views/admin/Tasks.vue'),
        meta: { admin: true, title: '任务管理' },
      },
      {
        path: 'audit',
        component: () => import('../views/admin/Audit.vue'),
        meta: { admin: true, title: '审计日志' },
      },
    ],
  },
  {
    path: '/',
    component: () => import('../views/Layout.vue'),
    children: [
      { path: '', redirect: '/qa' },
      {
        path: 'qa',
        component: () => import('../views/QA.vue'),
        meta: { title: '智能问答' },
      },
      {
        path: 'evaluation',
        component: () => import('../views/Evaluation.vue'),
        meta: { title: '教学评估' },
      },
      {
        path: 'syllabus',
        component: () => import('../views/Syllabus.vue'),
        meta: { title: '大纲优化' },
      },
      {
        path: 'profile',
        component: () => import('../views/Profile.vue'),
        meta: { title: '我的' },
      },
    ],
  },
]

const router = createRouter({
  history: createWebHashHistory(),
  routes,
})

async function ensureAuth() {
  if (authState.ready) return authState.user
  try {
    setAuthConfig(await authApi.config())
  } catch {
    /* 配置失败时沿用默认 */
  }
  try {
    setUser(await authApi.me())
  } catch {
    setUser(null)
  } finally {
    markAuthReady()
  }
  return authState.user
}

router.beforeEach(async (to) => {
  const user = await ensureAuth()
  const loggedIn = Boolean(user)
  if (to.meta.public) {
    if (loggedIn && to.path === '/login') return '/qa'
    if (!loggedIn) resetQa()
    return true
  }
  if (!loggedIn) {
    resetQa()
    return {
      path: '/login',
      query: { redirect: to.fullPath },
    }
  }
  if (to.meta.admin && !isAdmin(user)) {
    return '/forbidden'
  }
  return true
})

export default router
