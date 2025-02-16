# **🚀 How The Code Works with Celery & Redis**

Project uses **Celery for background task execution** and **Redis as a message queue**. This allows tasks to run asynchronously without blocking your main Flask application.

---

## **✅ Step 1: How Celery & Redis Work Together**
### **📌 What Happens When You Run Your Code?**
1️⃣ **Flask or Celery Beat sends a task**  
   - When a trigger is scheduled, Flask or Celery Beat **adds a task to Redis (queue)**.

2️⃣ **Redis stores the task in a queue**  
   - Redis **temporarily holds the task** until a worker picks it up.

3️⃣ **Celery Worker fetches and executes the task**  
   - The worker pulls the task from Redis and **runs the function in the background**.  
   - After execution, it **removes the task from Redis**.

---

## **✅ Step 2: How Your Code Uses Celery**
### **🔹 1️⃣ You Define Celery in `celery_worker.py`**
```python
celery = Celery('celery_config.celery_worker', broker='redis://localhost:6379/0')
```
- **Creates a Celery app** and tells it to use **Redis (`redis://localhost:6379/0`) as a queue**.  
- **Every Celery task will now be managed by Redis.**

---

### **🔹 2️⃣ Celery Beat Schedules Tasks Automatically**
```python
celery.conf.beat_schedule = {
    'execute_scheduled_triggers_task': {
        'task': 'celery_config.celery_worker.execute_scheduled_triggers_helper',
        'schedule': 60.0  # Runs every 1 minute
    },
    'update_event_states_task': {
        'task': 'celery_config.celery_worker.update_event_states_helper',
        'schedule': crontab(minute='*/30')  # Runs every 30 minutes
    }
}
```
- **Celery Beat automatically schedules tasks** at set intervals.
- **Every 1 minute** → `execute_scheduled_triggers_helper` runs.
- **Every 30 minutes** → `update_event_states_helper` runs.
- These scheduled tasks are **stored in Redis until a worker processes them**.

---

### **🔹 3️⃣ Celery Worker Executes the Task**
```python
@celery.task(name="celery_config.celery_worker.execute_scheduled_triggers_helper")
def execute_scheduled_triggers_helper():
    logging.info("🚀 Task `execute_scheduled_triggers_helper` is running!")
    execute_scheduled_triggers()  # ✅ Runs the trigger execution logic
    logging.info("✅ Task `execute_scheduled_triggers_helper` completed execution.")
```
- **Runs in the background** when Celery Worker picks up the task.
- The **worker reads the task from Redis and executes it asynchronously**.
- Once done, Celery removes it from the queue.

---

### **🔹 4️⃣ Redis Handles Message Passing**
```plaintext
[Flask] → Sends task to Redis  
[Redis] → Stores task in queue  
[Celery Worker] → Pulls task from queue  
[Celery Worker] → Runs the function  
[Redis] → Removes completed task  
```

---

## **✅ Step 3: How to Verify Everything is Working**
### **Check Redis Queue for Pending Tasks**
```sh
redis-cli
```
Then check pending tasks:
```sh
LRANGE celery 0 -1
```
If the queue is empty, all tasks have been processed.

---

### **Check Celery Worker Logs**
```sh
celery -A celery_config.celery_worker worker --loglevel=info
```
If tasks are running, you should see logs like:
```plaintext
[2025-02-15 18:49:54,826: INFO/MainProcess] Task execute_scheduled_triggers_helper received
[2025-02-15 18:49:54,858: INFO/ForkPoolWorker-8] Task execute_scheduled_triggers_helper succeeded
```
✅ **This confirms Celery is picking up and executing tasks.**

---

## **🔹 Summary: What Happens When Your Code Runs?**
1️⃣ **Flask or Celery Beat sends a task → Redis stores it.**  
2️⃣ **Celery Worker picks up the task → Runs the function.**  
3️⃣ **After execution, Redis removes the task.**  
4️⃣ **Celery Beat continues scheduling tasks periodically.**  

🚀 **This allows your app to execute background tasks without blocking the main process!**

---

## **🎯 Next Steps**
- **Want to monitor Celery tasks with a dashboard?** → Install **Flower (`pip install flower`)**  
- **Want to retry failed tasks automatically?** → Use **Celery retry policies**  
- **Want to scale to multiple workers?** → Run more Celery workers  

Let me know if you need more explanations! 🚀😊

