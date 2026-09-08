import { reactive } from 'vue'

const USER_KEY = 'pku-askedu-user'

function readUser() {
  try {
    return JSON.parse(sessionStorage.getItem(USER_KEY) || 'null')
  } catch {
    return null
  }
}

export const authState = reactive({
  ready: false,
  user: readUser(),
  config: {
    auth_mode: 'local',
    registration_enabled: true,
    invite_required: false,
    pku_sso_ready: false,
    password_min_length: 8,
  },
})

export function getUser() {
  return authState.user
}

export function setUser(user) {
  authState.user = user || null
  if (user) sessionStorage.setItem(USER_KEY, JSON.stringify(user))
  else sessionStorage.removeItem(USER_KEY)
}

export function clearAuth() {
  setUser(null)
}

export function setAuthConfig(config) {
  authState.config = { ...authState.config, ...(config || {}) }
}

export function markAuthReady() {
  authState.ready = true
}

export function isAdmin(user = authState.user) {
  return Boolean(user && user.role === 'admin' && user.status === 'active')
}
