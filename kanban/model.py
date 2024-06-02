from constants import PROD_DIR


class Task:
    def __init__(self, file_path, projects=None):
        self.name = file_path.name
        self.file_path = file_path
        # This gets the name of the first folder after "Productivity" and
        # assume that it represents the state of the task (ex. Backlog,
        # Completed, etc.).
        self.status = file_path.relative_to(PROD_DIR).parents[-2].name
        self.projects: list = projects


class TaskList(list):
    @property
    def projects(self):
        projects_set = set()
        for task in self:
            projects = task.projects
            if projects is not None:
                for project in projects:
                    projects_set.add(project)

        return sorted(list(projects_set))

    def task_status_for_project(self, project):
        result = {"Active": [], "Archived": [], "Backlog": [], "Completed": []}
        for task in self:
            if task.projects is not None and project in task.projects:
                status = task.status if task.status != "Projects" else "Active"
                result[status].append(task)

        return result

