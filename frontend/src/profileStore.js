const STORAGE_KEY = 'pku-askedu-profile'

export function emptyProfile() {
  return {
    name: '',
    staffId: '',
    title: '',
    department: '',
    email: '',
    phone: '',
    courses: '',
    bio: '',
    avatar: '',
  }
}

export function loadProfile() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    if (!raw) return emptyProfile()
    return { ...emptyProfile(), ...JSON.parse(raw) }
  } catch {
    return emptyProfile()
  }
}

export function saveProfile(profile) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify({ ...emptyProfile(), ...profile }))
}
