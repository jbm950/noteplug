from constants import PROD_DIR


class Task:
    def __init__(self, file_path, projects=None):
        self.file_path = file_path
        # This gets the name of the first folder after "Productivity" and
        # assume that it represents the state of the task (ex. Backlog,
        # Completed, etc.).
        self.state = file_path.relative_to(PROD_DIR).parents[-2].name
        self.projects: list = projects


class TaskList(list):
    pass
