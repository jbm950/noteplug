import yaml

from constants import PROD_DIR
from model import Task, TaskList


def load_tasks():
    task_list = TaskList()
    for markdown_file_path in PROD_DIR.rglob("*.md"):
        with open(markdown_file_path, encoding="utf8") as markdown_file:
            first_line = markdown_file.readline()
            if first_line != "---\n":
                task_list.append(Task(markdown_file_path))
                continue

            yaml_list = []
            for next_line in markdown_file.readlines():
                if next_line == "---\n":
                    break
                yaml_list.append(next_line)

        yaml_string = "\n".join(yaml_list)
        yaml_dict = yaml.load(yaml_string, Loader=yaml.Loader)

        task_list.append(Task(markdown_file_path, projects=yaml_dict["projects"]))

    return task_list
