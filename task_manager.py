tasks = []

def add_task(task):
    tasks.append({"task": task, "done": False})

def list_tasks():
    for i, t in enumerate(tasks, 1):
        status = "✓" if t["done"] else "✗"
        print(f"{i}. {t['task']} [{status}]")

def mark_done(index):
    if 0 <= index < len(tasks):
        tasks[index]["done"] = True
