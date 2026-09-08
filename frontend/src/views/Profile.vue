<template>
  <div class="profile">
    <el-card shadow="never" class="hero">
      <div class="hero-inner">
        <div class="avatar-wrap">
          <el-avatar :size="88" :src="form.avatar || undefined" class="avatar">
            {{ initials }}
          </el-avatar>
          <el-upload
            :auto-upload="false"
            :show-file-list="false"
            accept="image/png,image/jpeg,image/webp"
            :on-change="onAvatarChange"
          >
            <el-button size="small" text type="primary">更换头像</el-button>
          </el-upload>
        </div>
        <div class="hero-text">
          <h2>{{ form.name || '未填写姓名' }}</h2>
          <p>{{ headline || '完善个人信息后，将显示职称与院系' }}</p>
        </div>
      </div>
    </el-card>

    <el-card shadow="never" class="card">
      <template #header>
        <div class="card-header">
          <span class="card-title">基本资料</span>
          <span class="hint">保存在服务端，登录后可在各设备查看</span>
        </div>
      </template>

      <el-form :model="form" label-width="88px" class="form" v-loading="loading">
        <el-row :gutter="20">
          <el-col :xs="24" :sm="12">
            <el-form-item label="姓名">
              <el-input v-model="form.name" maxlength="40" placeholder="例如：张明" />
            </el-form-item>
          </el-col>
          <el-col :xs="24" :sm="12">
            <el-form-item label="工号">
              <el-input :model-value="staffIdDisplay" disabled placeholder="登录工号" />
            </el-form-item>
          </el-col>
          <el-col :xs="24" :sm="12">
            <el-form-item label="职称">
              <el-select v-model="form.title" placeholder="请选择" clearable style="width: 100%">
                <el-option v-for="t in TITLES" :key="t" :label="t" :value="t" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :xs="24" :sm="12">
            <el-form-item label="院系">
              <el-input v-model="form.department" maxlength="80" placeholder="例如：教育学院" />
            </el-form-item>
          </el-col>
          <el-col :xs="24" :sm="12">
            <el-form-item label="邮箱">
              <el-input v-model="form.email" maxlength="80" placeholder="name@pku.edu.cn" />
            </el-form-item>
          </el-col>
          <el-col :xs="24" :sm="12">
            <el-form-item label="手机">
              <el-input v-model="form.phone" maxlength="20" placeholder="选填" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item label="授课课程">
          <el-input
            v-model="form.courses"
            type="textarea"
            :rows="2"
            maxlength="200"
            show-word-limit
            placeholder="例如：教育学原理、课堂教学设计"
          />
        </el-form-item>
        <el-form-item label="个人简介">
          <el-input
            v-model="form.bio"
            type="textarea"
            :rows="4"
            maxlength="400"
            show-word-limit
            placeholder="简要介绍教学方向、研究兴趣或使用本系统的目标"
          />
        </el-form-item>

        <el-form-item>
          <el-button type="primary" :loading="saving" @click="save">保存</el-button>
          <el-button @click="reload">重新加载</el-button>
          <el-button
            v-if="authState.config.auth_mode === 'local'"
            @click="showPassword = true"
          >
            修改密码
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-dialog v-model="showPassword" title="修改密码" width="400px">
      <el-form label-position="top">
        <el-form-item label="原密码">
          <el-input v-model="passwordForm.old_password" type="password" show-password />
        </el-form-item>
        <el-form-item label="新密码">
          <el-input v-model="passwordForm.new_password" type="password" show-password />
        </el-form-item>
        <el-form-item label="确认新密码">
          <el-input v-model="passwordForm.confirm_password" type="password" show-password />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showPassword = false">取消</el-button>
        <el-button type="primary" :loading="savingPassword" @click="changePassword">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { authApi } from '../api/client'
import { authState, setUser } from '../authStore'

const TITLES = ['教授', '副教授', '讲师', '助教', '研究员', '副研究员', '其他']

const loading = ref(false)
const saving = ref(false)
const showPassword = ref(false)
const savingPassword = ref(false)
const form = reactive(emptyForm())
const passwordForm = reactive({
  old_password: '',
  new_password: '',
  confirm_password: '',
})

const initials = computed(() => {
  const name = (form.name || '').trim()
  return name ? name.slice(0, 1) : '教'
})

const headline = computed(() => {
  return [form.title, form.department].filter(Boolean).join(' · ')
})

const staffIdDisplay = computed(() => {
  return (form.username || form.staff_id || '').trim()
})

function emptyForm() {
  return {
    name: '',
    username: '',
    staff_id: '',
    title: '',
    department: '',
    email: '',
    phone: '',
    courses: '',
    bio: '',
    avatar: '',
  }
}

function applyUser(user) {
  Object.assign(form, emptyForm(), user || {})
}

async function reload() {
  loading.value = true
  try {
    const user = await authApi.me()
    applyUser(user)
    setUser(user)
  } catch {
    /* 401 时拦截器会跳登录 */
  } finally {
    loading.value = false
  }
}

async function onAvatarChange(file) {
  const raw = file.raw
  if (!raw) return
  if (raw.size > 2 * 1024 * 1024) {
    ElMessage.warning('头像请小于 2MB')
    return
  }
  try {
    const user = await authApi.uploadAvatar(raw)
    applyUser(user)
    setUser(user)
    ElMessage.success('头像已更新')
  } catch {
    /* 错误已由 axios 拦截器提示 */
  }
}

async function save() {
  if (!form.name.trim()) {
    ElMessage.warning('请填写姓名')
    return
  }
  saving.value = true
  try {
    const user = await authApi.updateMe({
      name: form.name.trim(),
      department: form.department.trim(),
      email: form.email.trim(),
      phone: form.phone.trim(),
      title: form.title || '',
      courses: form.courses || '',
      bio: form.bio || '',
    })
    applyUser(user)
    setUser(user)
    ElMessage.success('已保存')
  } catch {
    /* 错误已由 axios 拦截器提示 */
  } finally {
    saving.value = false
  }
}

async function changePassword() {
  if (passwordForm.new_password !== passwordForm.confirm_password) {
    ElMessage.warning('两次输入的密码不一致')
    return
  }
  savingPassword.value = true
  try {
    await authApi.changePassword({ ...passwordForm })
    ElMessage.success('密码已更新')
    showPassword.value = false
    passwordForm.old_password = ''
    passwordForm.new_password = ''
    passwordForm.confirm_password = ''
  } catch {
    /* 错误已由 axios 拦截器提示 */
  } finally {
    savingPassword.value = false
  }
}

onMounted(reload)
</script>

<style scoped>
.profile {
  max-width: 860px;
  margin: 0 auto;
}

.hero,
.card {
  border: 1px solid #e8eaed;
  margin-bottom: 16px;
}

.hero-inner {
  display: flex;
  align-items: center;
  gap: 20px;
}

.avatar-wrap {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}

.avatar {
  background: #a61b1b;
  color: #fff;
  font-size: 32px;
  font-weight: 600;
}

.hero-text h2 {
  margin: 0;
  font-size: 22px;
  color: #303133;
}

.hero-text p {
  margin: 8px 0 0;
  font-size: 14px;
  color: #909399;
}

.card-header {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 12px;
}

.card-title {
  font-size: 14px;
  font-weight: 600;
}

.hint {
  font-size: 12px;
  color: #909399;
}

.form {
  max-width: 720px;
}
</style>
