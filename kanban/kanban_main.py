from load_tasks import load_tasks
from tui import App

task_list = load_tasks()
app = App(task_list)
app.run()
