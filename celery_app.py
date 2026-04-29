from celery import Celery
from config import settings
import time
from models import SessionLocal, Task

celery_app = Celery(
    "multi_agent_system",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="Asia/Shanghai",
    beat_schedule={
        "periodic-check": {
            "task": "celery_app.periodic_check",
            "schedule": 60.0,
        },
    },
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@celery_app.task(bind=True)
def execute_agent_task(self, task_id: int, task_data: dict):
    db = next(get_db())
    try:
        task = db.query(Task).filter(Task.id == task_id).first()
        task.status = "EXECUTING"
        db.commit()

        # 模拟Agent执行逻辑（替换为你的业务代码）
        time.sleep(5)
        result = f"Agent processed: {task_data}"

        task.status = "COMPLETED"
        task.result = result
        db.commit()

        check_task_result.delay(task_id)
        return result
    except Exception as e:
        task.status = "FAILED"
        task.result = str(e)
        db.commit()
        raise self.retry(exc=e, countdown=10, max_retries=3)

@celery_app.task
def check_task_result(task_id: int):
    db = next(get_db())
    task = db.query(Task).filter(Task.id == task_id).first()
    if task:
        task.check_status = "PASSED" if "processed" in (task.result or "") else "FAILED"
        db.commit()
    return f"Check done for task {task_id}"

@celery_app.task
def periodic_check():
    db = next(get_db())
    pending = db.query(Task).filter(Task.status == "PENDING").all()
    for t in pending:
        execute_agent_task.delay(t.id, t.data)
    return f"Periodic check processed {len(pending)} tasks"