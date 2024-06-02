import os
import pathlib
import yaml

from prompt_toolkit import Application
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.document import Document
from prompt_toolkit.formatted_text import fragment_list_to_text, HTML, to_formatted_text
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout.containers import VSplit, Window
from prompt_toolkit.layout.controls import BufferControl, FormattedTextControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.layout.processors import Processor, Transformation
from prompt_toolkit.widgets import Frame

# GET DATA
class Task:
    def __init__(self, file_path, projects=None):
        self.file_path = file_path
        # This gets the name of the first folder after "Productivity" and
        # assume that it represents the state of the task (ex. Backlog,
        # Completed, etc.).
        self.state = file_path.relative_to(NOTES_DIR).parents[-3].name
        self.projects: list = projects

class TaskList(list):
    pass

# Probably need a check that Notes Dir exists as an environment variable
NOTES_DIR = pathlib.Path(os.environ["NOTES_DIR"])
PROD_DIR = NOTES_DIR.joinpath("Productivity")

task_list = TaskList()
data = {}
for markdown_file_path in PROD_DIR.rglob("*.md"):
    with open(markdown_file_path) as markdown_file:
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
    data[markdown_file_path] = yaml.load(yaml_string, Loader=yaml.Loader)

projects_set = set()
for item in task_list:
    projects = item.projects
    if projects is not None:
        for project in projects:
            projects_set.add(project)

projects_list = sorted(list(projects_set))

# TUI
class FormatText(Processor):
    def apply_transformation(self, transformation_input):
        fragments = to_formatted_text(HTML(fragment_list_to_text(transformation_input.fragments)))
        return Transformation(fragments)

wrapped_list = [f"<ansiwhite>{project}</ansiwhite>" for project in projects_list]

initial_doc = Document(text="\n".join(wrapped_list), cursor_position=0)
buffer1 = Buffer(document=initial_doc, read_only=True)
screen1 = Layout(Frame(Window(content=BufferControl(buffer1, input_processors=[FormatText()]))))

screen2 = Layout(
    VSplit([Frame(Window(content=FormattedTextControl(text=HTML("<ansiwhite>Screen 2</ansiwhite>"))),
                  title="Backlog"),
           Frame(Window(content=FormattedTextControl(text=HTML("<ansiwhite>Screen 2</ansiwhite>"))),
                  title="Active"),
            Frame(Window(content=FormattedTextControl(text=HTML("<ansiwhite>Screen 2</ansiwhite>"))),
                  title="Completed")]))

kb = KeyBindings()

@kb.add('c-q')
def exit_(event):
    event.app.reset()
    event.app.exit()

@kb.add('2')
def screen2_(event):
    event.app.layout = screen2

@kb.add('1')
def screen2_(event):
    event.app.layout = screen1

app = Application(layout=screen1, key_bindings=kb, full_screen=True)
app.run()

