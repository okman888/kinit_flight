import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'kinit-api')))

from core.database import session_factory
from apps.flight import crud

async def check_task_status():
    task_id = '131045adb684478fa8ff'
    
    print(f"查询任务状态，任务ID: {task_id}")
    
    try:
        async with session_factory() as db:
            task = await crud.FlightTaskDal(db).get_data(task_id=task_id)
            print('任务状态:', task.status)
            print('任务消息:', task.message)
            print('成功请求数:', task.success_requests)
            print('失败请求数:', task.failed_requests)
            print('结果数量:', task.result_count)
            print('开始时间:', task.started_at)
            print('结束时间:', task.finished_at)
    except Exception as e:
        print(f"查询失败: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    import asyncio
    asyncio.run(check_task_status())
