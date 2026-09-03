import { createRouter, createWebHashHistory } from 'vue-router'

const routes = [
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

export default createRouter({
  history: createWebHashHistory(),
  routes,
})
