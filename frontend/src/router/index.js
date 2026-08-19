import { createRouter, createWebHashHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    component: () => import('../views/Layout.vue'),
    children: [
      { path: '', redirect: '/evaluation' },
      {
        path: 'evaluation',
        component: () => import('../views/Evaluation.vue'),
        meta: { title: '教学视频质量评估' },
      },
      {
        path: 'syllabus',
        component: () => import('../views/Syllabus.vue'),
        meta: { title: '教学大纲优化' },
      },
      {
        path: 'qa',
        component: () => import('../views/QA.vue'),
        meta: { title: '教学智能问答' },
      },
    ],
  },
]

export default createRouter({
  history: createWebHashHistory(),
  routes,
})
