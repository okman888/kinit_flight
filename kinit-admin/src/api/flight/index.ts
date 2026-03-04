import request from '@/config/axios'

export const getFlightTaskListApi = (params: any): Promise<IResponse> => {
  return request.get({ url: '/flight/tasks', params })
}

export const getFlightTaskApi = (taskId: string): Promise<IResponse> => {
  return request.get({ url: `/flight/tasks/${taskId}` })
}

export const addFlightTaskApi = (data: any): Promise<IResponse> => {
  return request.post({ url: '/flight/tasks', data })
}

export const runFlightTaskApi = (taskId: string): Promise<IResponse> => {
  return request.post({ url: `/flight/tasks/${taskId}/run` })
}

export const delFlightTaskApi = (data: any): Promise<IResponse> => {
  return request.delete({ url: '/flight/tasks', data })
}

export const exportFlightTaskApi = (taskId: string): Promise<IResponse> => {
  return request.get({ url: `/flight/tasks/${taskId}/export` })
}

export const getFlightResultListApi = (params: any): Promise<IResponse> => {
  return request.get({ url: '/flight/results', params })
}
