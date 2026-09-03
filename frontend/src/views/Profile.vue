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
          <span class="hint">仅保存在本机浏览器，换设备或清缓存后需重新填写</span>
        </div>
      </template>

      <el-form :model="form" label-width="88px" class="form">
        <el-row :gutter="20">
          <el-col :xs="24" :sm="12">
            <el-form-item label="姓名">
              <el-input v-model="form.name" maxlength="40" placeholder="例如：张明" />
            </el-form-item>
          </el-col>
          <el-col :xs="24" :sm="12">
            <el-form-item label="工号">
              <el-input v-model="form.staffId" maxlength="32" placeholder="选填" />
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
          <el-button type="primary" @click="save">保存</el-button>
          <el-button @click="reset">恢复上次保存</el-button>
          <el-button text type="danger" @click="clearAll">清空</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { computed, reactive } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { loadProfile, saveProfile, emptyProfile } from '../profileStore'

const TITLES = ['教授', '副教授', '讲师', '助教', '研究员', '副研究员', '其他']

const form = reactive(loadProfile())

const initials = computed(() => {
  const name = (form.name || '').trim()
  return name ? name.slice(0, 1) : '教'
})

const headline = computed(() => {
  return [form.title, form.department].filter(Boolean).join(' · ')
})

function onAvatarChange(file) {
  const raw = file.raw
  if (!raw) return
  if (raw.size > 2 * 1024 * 1024) {
    ElMessage.warning('头像请小于 2MB')
    return
  }
  const reader = new FileReader()
  reader.onload = () => {
    form.avatar = String(reader.result || '')
  }
  reader.readAsDataURL(raw)
}

function save() {
  saveProfile(form)
  ElMessage.success('已保存到本机')
}

function reset() {
  Object.assign(form, loadProfile())
  ElMessage.info('已恢复上次保存的内容')
}

async function clearAll() {
  try {
    await ElMessageBox.confirm('确定清空本机保存的个人信息？', '清空确认', {
      type: 'warning',
      confirmButtonText: '清空',
      cancelButtonText: '取消',
    })
  } catch {
    return
  }
  Object.assign(form, emptyProfile())
  saveProfile(form)
  ElMessage.success('已清空')
}
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
