from prompt_toolkit import Application
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.document import Document
from prompt_toolkit.formatted_text import fragment_list_to_text, HTML, to_formatted_text
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout.containers import VSplit, Window
from prompt_toolkit.layout.controls import BufferControl, FormattedTextControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.styles import Style
from prompt_toolkit.layout.processors import Processor, Transformation
from prompt_toolkit.widgets import Frame


class App:
    def __init__(self, task_list):
        self.dashboard_screen = DashboardScreen(task_list, self)
        self.kanban_screen = KanbanScreen(task_list)

        kb = KeyBindings()

        @kb.add('c-q')
        def exit_(event):
            event.app.reset()
            event.app.exit()

        @kb.add('c-d')
        def switch_to_dashboard_(event):
            event.app.layout = self.dashboard_screen.layout

        style = Style.from_dict({"frame.border": '#008080',
                                 "frame": "#ffffff"})  # Handles frame title text

        self.app = Application(layout=self.dashboard_screen.layout,
                               key_bindings=kb,
                               style=style,
                               full_screen=True)

    def run(self):
        self.app.run()

    def switch_to_kanban(self, project):
        self.kanban_screen.update(project)
        self.app.layout = self.kanban_screen.layout


class DashboardScreen:
    def __init__(self, task_list, top_app):
        self._task_list = task_list
        self._project_list = task_list.projects

        proj_list_kb = KeyBindings()

        @proj_list_kb.add('enter')
        def enter_(event):
            selection = self._project_list[self.project_list_buffer.document.cursor_position_row]
            top_app.switch_to_kanban(selection)

        initial_doc = Document(text=self._format_project_list(), cursor_position=0)
        self.project_list_buffer = Buffer(document=initial_doc, read_only=True)
        self.layout = Layout(Frame(Window(content=BufferControl(self.project_list_buffer,
                                                                input_processors=[FormatText()],
                                                                key_bindings=proj_list_kb))))

    def _format_project_list(self):
        return "\n".join([f"<ansiwhite>{project}</ansiwhite>" for project in self._project_list])


class KanbanScreen:
    def __init__(self, task_list):
        self._task_list = task_list

        self._backlog_control = FormattedTextControl(text="")
        self._active_control = FormattedTextControl(text="")
        self._completed_control = FormattedTextControl(text="")

        self.layout = Layout(
            VSplit([Frame(Window(content=self._backlog_control), title="Backlog"),
                    Frame(Window(content=self._active_control), title="Active"),
                    Frame(Window(content=self._completed_control), title="Completed")]))

    def update(self, project):
        project_tasks = self._task_list.task_status_for_project(project)
        self._backlog_control.text = HTML(self.format_task_column(
            [task.name for task in project_tasks["Backlog"]]
            ))
        self._active_control.text = HTML(self.format_task_column(
            [task.name for task in project_tasks["Active"]]
            ))
        self._completed_control.text = HTML(self.format_task_column(
            [task.name for task in project_tasks["Completed"]]
            ))

    @staticmethod
    def format_task_column(tasks):
        return "\n".join([f"<ansiwhite>{task}</ansiwhite>" for task in tasks])



class FormatText(Processor):
    def apply_transformation(self, transformation_input):
        fragments = to_formatted_text(HTML(fragment_list_to_text(transformation_input.fragments)))
        return Transformation(fragments)
