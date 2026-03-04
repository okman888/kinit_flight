<script setup lang="tsx">
import { reactive, ref, unref } from 'vue'
import { useRoute } from 'vue-router'
import { Search } from '@/components/Search'
import { FormSchema } from '@/components/Form'
import { ContentWrap } from '@/components/ContentWrap'
import { Table, TableColumn } from '@/components/Table'
import { useTable } from '@/hooks/web/useTable'
import { getFlightResultListApi } from '@/api/flight'

defineOptions({
  name: 'FlightResult'
})

const route = useRoute()
const initialTaskId = (route.query.task_id as string) || ''

const { tableRegister, tableState, tableMethods } = useTable({
  fetchDataApi: async () => {
    const { pageSize, currentPage } = tableState
    const res = await getFlightResultListApi({
      page: unref(currentPage),
      limit: unref(pageSize),
      ...unref(searchParams)
    })
    return {
      list: res.data || [],
      total: res.count || 0
    }
  }
})

const { dataList, loading, total, pageSize, currentPage } = tableState
const { getList } = tableMethods

const tableColumns = reactive<TableColumn[]>([
  { field: 'task_id', label: '任务ID', show: true, width: '180px' },
  { field: 'create_time', label: '采集时间', show: true, width: '180px' },
  { field: 'travel_date', label: '出发日期', show: true, width: '180px' },
  { field: 'departure_city', label: '出发代码', show: true, width: '100px' },
  { field: 'departure_city_name', label: '出发名称', show: true, width: '120px' },
  { field: 'arrival_city', label: '到达代码', show: true, width: '100px' },
  { field: 'arrival_city_name', label: '到达名称', show: true, width: '120px' },
  { field: 'departure_time', label: '起飞时间', show: true, width: '180px' },
  { field: 'arrival_time', label: '到达时间', show: true, width: '180px' },
  { field: 'duration', label: '时长(分钟)', show: true, width: '110px' },
  { field: 'min_price', label: '最低价', show: true, width: '100px' },
  { field: 'min_price_tax', label: '税费', show: true, width: '100px' },
  { field: 'seat_left', label: '余位', show: true, width: '80px' },
  { field: 'default_cabin', label: '舱位', show: true, width: '100px' },
  { field: 'flights_info', label: '航班信息', show: true, minWidth: '220px' },
  { field: 'data_source', label: '来源', show: true, width: '120px' }
])

const searchSchema = reactive<FormSchema[]>([
  {
    field: 'task_id',
    label: '任务ID',
    component: 'Input',
    componentProps: { clearable: true, style: { width: '214px' } }
  },
  {
    field: 'departure_city',
    label: '出发城市',
    component: 'Input',
    componentProps: { clearable: true, style: { width: '214px' } }
  },
  {
    field: 'arrival_city',
    label: '到达城市',
    component: 'Input',
    componentProps: { clearable: true, style: { width: '214px' } }
  },
  {
    field: 'travel_date',
    label: '出发日期',
    component: 'DatePicker',
    componentProps: {
      style: { width: '214px' },
      type: 'date',
      format: 'YYYY-MM-DD',
      valueFormat: 'YYYY-MM-DD'
    }
  }
])

const searchParams = ref<any>({
  task_id: initialTaskId
})

const setSearchParams = (data: any) => {
  currentPage.value = 1
  searchParams.value = data
  getList()
}
</script>

<template>
  <ContentWrap>
    <Search
      :schema="searchSchema"
      :defaultExpand="true"
      @reset="setSearchParams"
      @search="setSearchParams"
    />
    <Table
      v-model:current-page="currentPage"
      v-model:page-size="pageSize"
      :columns="tableColumns"
      :data="dataList"
      :loading="loading"
      :pagination="{ total }"
      @register="tableRegister"
      @refresh="getList"
    />
  </ContentWrap>
</template>
