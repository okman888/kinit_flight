<script setup lang="tsx">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ContentWrap } from '@/components/ContentWrap'
import { ElMessage, ElTable, ElTableColumn } from 'element-plus'
import { BaseButton } from '@/components/Button'
import { getFlightTaskApi } from '@/api/flight'

const route = useRoute()
const router = useRouter()
const taskId = route.query.task_id as string
const loading = ref(false)
const taskDetail = ref<any>(null)

const fetchTaskDetail = async () => {
  if (!taskId) {
    ElMessage.error('任务ID不存在')
    return
  }
  loading.value = true
  try {
    const res = await getFlightTaskApi(taskId)
    if (res?.code === 200) {
      taskDetail.value = res.data
      // 解析 task_payload 为 JSON 对象
      if (taskDetail.value?.task_payload) {
        try {
          taskDetail.value.task_payload = JSON.parse(taskDetail.value.task_payload)
        } catch (e) {
          console.error('解析 task_payload 失败:', e)
        }
      }
    } else {
      ElMessage.error('获取任务详情失败')
    }
  } catch (error) {
    ElMessage.error('获取任务详情失败')
  } finally {
    loading.value = false
  }
}

const goBack = () => {
  router.push('/flight/task')
}

onMounted(() => {
  fetchTaskDetail()
})
</script>

<template>
  <ContentWrap>
    <div class="flex items-center justify-between mb-12px">
      <h1 class="text-xl font-bold">任务详情</h1>
      <BaseButton @click="goBack">返回列表</BaseButton>
    </div>
    <div v-if="loading" class="text-center py-20"> 加载中... </div>
    <div v-else-if="taskDetail" class="bg-white p-8px rounded-md">
      <div class="grid grid-cols-3 gap-8px mb-12px">
        <div>
          <div class="text-gray-500 mb-4px">任务ID</div>
          <div class="font-medium">{{ taskDetail.task_id }}</div>
        </div>
        <div>
          <div class="text-gray-500 mb-4px">任务名称</div>
          <div class="font-medium">{{ taskDetail.task_name }}</div>
        </div>
        <div>
          <div class="text-gray-500 mb-4px">渠道</div>
          <div class="font-medium">{{ taskDetail.channel }}</div>
        </div>
        <div>
          <div class="text-gray-500 mb-4px">渠道账号</div>
          <div class="font-medium">{{ taskDetail.channel_account || '无' }}</div>
        </div>
        <div>
          <div class="text-gray-500 mb-4px">代理IP</div>
          <div class="font-medium">{{ taskDetail.http_proxy || '无' }}</div>
        </div>
        <div>
          <div class="text-gray-500 mb-4px">状态</div>
          <div class="font-medium">{{ taskDetail.status }}</div>
        </div>
      </div>
      <div class="mb-8px">
        <h3 class="font-bold mb-4px">采集项</h3>
        <ElTable :data="taskDetail.task_payload?.items || []" border style="width: 100%">
          <ElTableColumn label="出发城市代码" prop="departure_city" min-width="120" />
          <ElTableColumn label="出发城市名称" prop="departure_city_name" min-width="120" />
          <ElTableColumn label="到达城市代码" prop="arrival_city" min-width="120" />
          <ElTableColumn label="到达城市名称" prop="arrival_city_name" min-width="120" />
          <ElTableColumn label="开始日期" prop="start_date" min-width="150" />
          <ElTableColumn label="结束日期" prop="end_date" min-width="150" />
        </ElTable>
      </div>
    </div>
    <div v-else class="text-center py-20"> 未找到任务详情 </div>
  </ContentWrap>
</template>
