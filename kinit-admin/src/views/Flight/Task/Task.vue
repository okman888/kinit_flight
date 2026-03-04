<script setup lang="tsx">
import { reactive, ref, unref } from 'vue'
import { useRouter } from 'vue-router'
import { Search } from '@/components/Search'
import { FormSchema } from '@/components/Form'
import { ContentWrap } from '@/components/ContentWrap'
import { Table, TableColumn } from '@/components/Table'
import { Dialog } from '@/components/Dialog'
import {
  ElMessage,
  ElMessageBox,
  ElRow,
  ElCol,
  ElInput,
  ElDatePicker,
  ElTable,
  ElTableColumn,
  ElUpload
} from 'element-plus'
import { BaseButton } from '@/components/Button'
import { useTable } from '@/hooks/web/useTable'
import {
  getFlightTaskListApi,
  addFlightTaskApi,
  runFlightTaskApi,
  exportFlightTaskApi,
  delFlightTaskApi
} from '@/api/flight'
import * as XLSX from 'xlsx'

defineOptions({
  name: 'FlightTask'
})

const { push } = useRouter()

const { tableRegister, tableState, tableMethods } = useTable({
  fetchDataApi: async () => {
    const { pageSize, currentPage } = tableState
    const res = await getFlightTaskListApi({
      page: unref(currentPage),
      limit: unref(pageSize),
      ...unref(searchParams)
    })
    return {
      list: res.data || [],
      total: res.count || 0
    }
  },
  fetchDelApi: async (value) => {
    const res = await delFlightTaskApi({ ids: value })
    return res?.code === 200
  }
})

const { dataList, loading, total, pageSize, currentPage } = tableState
const { getList, delList } = tableMethods

const tableColumns = reactive<TableColumn[]>([
  { field: 'task_id', label: '任务ID', show: true, width: '180px' },
  { field: 'task_name', label: '任务名称', show: true, minWidth: '180px' },
  { field: 'channel', label: '渠道', show: true, width: '120px' },
  { field: 'status', label: '状态', show: true, width: '120px' },
  { field: 'success_requests', label: '成功请求', show: true, width: '100px' },
  { field: 'failed_requests', label: '失败请求', show: true, width: '100px' },
  { field: 'result_count', label: '结果条数', show: true, width: '100px' },
  { field: 'message', label: '说明', show: true, minWidth: '200px' },
  { field: 'create_datetime', label: '创建时间', show: true, width: '180px' },
  {
    field: 'action',
    label: '操作',
    show: true,
    width: '280px',
    slots: {
      default: (data: any) => {
        const row = data.row
        return (
          <>
            <BaseButton type="primary" link size="small" onClick={() => toResult(row)}>
              查看结果
            </BaseButton>
            <BaseButton type="primary" link size="small" onClick={() => rerunTask(row)}>
              重新执行
            </BaseButton>
            <BaseButton type="primary" link size="small" onClick={() => exportTask(row)}>
              下载Excel
            </BaseButton>
            <BaseButton type="danger" link size="small" onClick={() => delData(row)}>
              删除
            </BaseButton>
          </>
        )
      }
    }
  }
])

const searchSchema = reactive<FormSchema[]>([
  {
    field: 'task_id',
    label: '任务ID',
    component: 'Input',
    componentProps: { clearable: true, style: { width: '214px' } }
  },
  {
    field: 'status',
    label: '状态',
    component: 'Select',
    componentProps: {
      style: { width: '214px' },
      clearable: true,
      options: [
        { label: 'pending', value: 'pending' },
        { label: 'running', value: 'running' },
        { label: 'success', value: 'success' },
        { label: 'partial_success', value: 'partial_success' },
        { label: 'failed', value: 'failed' }
      ]
    }
  }
])

const searchParams = ref({})
const setSearchParams = (data: any) => {
  currentPage.value = 1
  searchParams.value = data
  getList()
}

const delData = async (row: any) => {
  const deleteId = row?.id ?? row?.task_id
  if (deleteId === undefined || deleteId === null || deleteId === '') {
    ElMessage.warning('删除失败：未找到任务ID')
    return
  }
  await delList(true, [deleteId], false)
}

const toResult = (row: any) => {
  push(`/flight/result?task_id=${row.task_id}`)
}

const rerunTask = async (row: any) => {
  await runFlightTaskApi(row.task_id)
  ElMessage.success('任务已重新提交')
  getList()
}

const exportTask = async (row: any) => {
  const res = await exportFlightTaskApi(row.task_id)
  if (res?.data?.url) {
    window.open(res.data.url, '_blank')
  }
}

interface TaskItem {
  departure_city: string
  departure_city_name: string
  arrival_city: string
  arrival_city_name: string
  start_date: string
  end_date: string
}

const dialogVisible = ref(false)
const saveLoading = ref(false)
const formData = reactive({
  task_name: '',
  channel: 'hk.trip.com',
  channel_account: '',
  channel_password: '',
  proxy: '',
  http_proxy: '',
  https_proxy: ''
})

const createEmptyItem = (): TaskItem => ({
  departure_city: '',
  departure_city_name: '',
  arrival_city: '',
  arrival_city_name: '',
  start_date: '',
  end_date: ''
})

const taskItems = ref<TaskItem[]>([createEmptyItem()])

const addTaskItem = () => {
  taskItems.value.push(createEmptyItem())
}

const removeTaskItem = (index: number) => {
  if (taskItems.value.length === 1) {
    ElMessage.warning('至少保留一条采集项')
    return
  }
  taskItems.value.splice(index, 1)
}

const openAddDialog = () => {
  formData.task_name = ''
  formData.channel = 'hk.trip.com'
  formData.channel_account = ''
  formData.channel_password = ''
  formData.proxy = ''
  formData.http_proxy = ''
  formData.https_proxy = ''
  taskItems.value = [createEmptyItem()]
  dialogVisible.value = true
}

const HEADER_MAP: Record<string, keyof TaskItem> = {
  出发城市代码: 'departure_city',
  departure_city: 'departure_city',
  出发城市名称: 'departure_city_name',
  departure_city_name: 'departure_city_name',
  到达城市代码: 'arrival_city',
  arrival_city: 'arrival_city',
  到达城市名称: 'arrival_city_name',
  arrival_city_name: 'arrival_city_name',
  开始日期: 'start_date',
  start_date: 'start_date',
  结束日期: 'end_date',
  end_date: 'end_date'
}

const handleExcelUpload = (options: any) => {
  const file: File = options.file
  const reader = new FileReader()
  reader.onload = (e) => {
    try {
      const data = new Uint8Array(e.target?.result as ArrayBuffer)
      const workbook = XLSX.read(data, { type: 'array' })
      const sheet = workbook.Sheets[workbook.SheetNames[0]]
      const jsonRows: Record<string, any>[] = XLSX.utils.sheet_to_json(sheet, { defval: '' })
      if (!jsonRows.length) {
        ElMessage.warning('Excel 文件中无有效数据')
        return
      }
      const parsed: TaskItem[] = jsonRows.map((row) => {
        const item = createEmptyItem()
        for (const [header, value] of Object.entries(row)) {
          const key = HEADER_MAP[header.trim()]
          if (key) {
            item[key] = String(value).trim()
          }
        }
        return item
      })
      const valid = parsed.filter((r) => r.departure_city && r.arrival_city)
      if (!valid.length) {
        ElMessage.warning('未识别到有效数据行，请检查列名是否匹配')
        return
      }
      taskItems.value = valid
      ElMessage.success(`成功导入 ${valid.length} 条采集项`)
    } catch {
      ElMessage.error('Excel 文件解析失败，请检查文件格式')
    }
  }
  reader.readAsArrayBuffer(file)
}

const downloadTemplate = () => {
  const headers = [
    '出发城市代码',
    '出发城市名称',
    '到达城市代码',
    '到达城市名称',
    '开始日期',
    '结束日期'
  ]
  const sample = [['SIN', '新加坡', 'SYD', '悉尼', '2026-03-01', '2026-03-07']]
  const ws = XLSX.utils.aoa_to_sheet([headers, ...sample])
  const wb = XLSX.utils.book_new()
  XLSX.utils.book_append_sheet(wb, ws, '采集项')
  XLSX.writeFile(wb, '采集项模板.xlsx')
}

const saveTask = async () => {
  const invalid = taskItems.value.some((item) => {
    return !item.departure_city || !item.arrival_city || !item.start_date || !item.end_date
  })
  if (invalid) {
    ElMessage.warning('请完善采集项中的必填字段（出发/到达城市代码、开始/结束日期）')
    return
  }
  saveLoading.value = true
  try {
    const proxy = formData.proxy.trim()
    const httpProxyInput = formData.http_proxy.trim()
    const httpsProxyInput = formData.https_proxy.trim()
    const defaultProxy = proxy || httpProxyInput || httpsProxyInput
    const httpProxy = httpProxyInput || defaultProxy
    const httpsProxy = httpsProxyInput || defaultProxy
    await addFlightTaskApi({
      task_name: formData.task_name,
      channel: formData.channel,
      channel_account: formData.channel_account || undefined,
      channel_password: formData.channel_password || undefined,
      http_proxy: httpProxy || undefined,
      https_proxy: httpsProxy || undefined,
      items: taskItems.value
    })
    ElMessage.success('任务创建成功，已提交后台异步执行')
    dialogVisible.value = false
    getList()
  } finally {
    saveLoading.value = false
  }
}

const refreshConfirm = () => {
  ElMessageBox.confirm('执行中的任务需要手动刷新查看进度，是否立即刷新？', '提示', {
    type: 'warning'
  }).then(() => getList())
}
</script>

<template>
  <ContentWrap>
    <Search :schema="searchSchema" @reset="setSearchParams" @search="setSearchParams" />
    <Table
      v-model:current-page="currentPage"
      v-model:page-size="pageSize"
      showAction
      :columns="tableColumns"
      :data="dataList"
      :loading="loading"
      :pagination="{ total }"
      @register="tableRegister"
      @refresh="getList"
    >
      <template #toolbar>
        <ElRow :gutter="10">
          <ElCol :span="1.5">
            <BaseButton type="primary" @click="openAddDialog">新建采集任务</BaseButton>
          </ElCol>
          <ElCol :span="1.5">
            <BaseButton @click="refreshConfirm">刷新进度</BaseButton>
          </ElCol>
        </ElRow>
      </template>
    </Table>
  </ContentWrap>

  <Dialog v-model="dialogVisible" title="创建航班采集任务" :width="1060">
    <div class="mb-12px">
      <div class="mb-8px">任务名称</div>
      <ElInput v-model="formData.task_name" placeholder="可选，不填则自动生成" />
    </div>
    <div class="mb-12px grid grid-cols-3 gap-12px">
      <div>
        <div class="mb-8px">采集渠道</div>
        <ElInput v-model="formData.channel" />
      </div>
      <div>
        <div class="mb-8px">渠道账号（可选）</div>
        <ElInput v-model="formData.channel_account" />
      </div>
      <div>
        <div class="mb-8px">渠道密码（可选）</div>
        <ElInput v-model="formData.channel_password" type="password" show-password />
      </div>
    </div>
    <div class="mb-12px grid grid-cols-3 gap-12px">
      <div>
        <div class="mb-8px">代理IP（可选，HTTP/HTTPS默认同地址）</div>
        <ElInput v-model="formData.proxy" placeholder="如 http://127.0.0.1:7890" />
      </div>
      <div>
        <div class="mb-8px">HTTP代理（可选）</div>
        <ElInput v-model="formData.http_proxy" placeholder="留空时默认使用上方代理IP" />
      </div>
      <div>
        <div class="mb-8px">HTTPS代理（可选）</div>
        <ElInput v-model="formData.https_proxy" placeholder="留空时默认使用上方代理IP" />
      </div>
    </div>

    <div class="mb-8px flex items-center justify-between">
      <span class="font-bold">采集项（共 {{ taskItems.length }} 条）</span>
      <div class="flex items-center gap-8px">
        <BaseButton type="primary" link @click="downloadTemplate">下载模板</BaseButton>
        <ElUpload
          :show-file-list="false"
          accept=".xlsx,.xls,.csv"
          :auto-upload="true"
          :http-request="handleExcelUpload"
        >
          <BaseButton type="success" link>导入Excel</BaseButton>
        </ElUpload>
        <BaseButton type="primary" link @click="addTaskItem">新增一行</BaseButton>
      </div>
    </div>

    <ElTable :data="taskItems" border size="small" max-height="360" style="width: 100%">
      <ElTableColumn label="#" type="index" width="50" align="center" />
      <ElTableColumn label="出发城市代码" min-width="120">
        <template #default="{ row }">
          <ElInput v-model="row.departure_city" size="small" placeholder="如 SIN" />
        </template>
      </ElTableColumn>
      <ElTableColumn label="出发城市名称" min-width="120">
        <template #default="{ row }">
          <ElInput v-model="row.departure_city_name" size="small" placeholder="如 新加坡" />
        </template>
      </ElTableColumn>
      <ElTableColumn label="到达城市代码" min-width="120">
        <template #default="{ row }">
          <ElInput v-model="row.arrival_city" size="small" placeholder="如 SYD" />
        </template>
      </ElTableColumn>
      <ElTableColumn label="到达城市名称" min-width="120">
        <template #default="{ row }">
          <ElInput v-model="row.arrival_city_name" size="small" placeholder="如 悉尼" />
        </template>
      </ElTableColumn>
      <ElTableColumn label="开始日期" min-width="150">
        <template #default="{ row }">
          <ElDatePicker
            v-model="row.start_date"
            type="date"
            size="small"
            value-format="YYYY-MM-DD"
            format="YYYY-MM-DD"
            placeholder="开始日期"
            style="width: 100%"
          />
        </template>
      </ElTableColumn>
      <ElTableColumn label="结束日期" min-width="150">
        <template #default="{ row }">
          <ElDatePicker
            v-model="row.end_date"
            type="date"
            size="small"
            value-format="YYYY-MM-DD"
            format="YYYY-MM-DD"
            placeholder="结束日期"
            style="width: 100%"
          />
        </template>
      </ElTableColumn>
      <ElTableColumn label="操作" width="70" align="center" fixed="right">
        <template #default="{ $index }">
          <BaseButton type="danger" link size="small" @click="removeTaskItem($index)">
            删除
          </BaseButton>
        </template>
      </ElTableColumn>
    </ElTable>

    <template #footer>
      <BaseButton type="primary" :loading="saveLoading" @click="saveTask">创建并执行</BaseButton>
      <BaseButton @click="dialogVisible = false">关闭</BaseButton>
    </template>
  </Dialog>
</template>
