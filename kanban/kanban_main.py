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

from load_tasks import load_tasks

# GET DATA
task_list = load_tasks()


# TUI
class FormatText(Processor):
    def apply_transformation(self, transformation_input):
        fragments = to_formatted_text(HTML(fragment_list_to_text(transformation_input.fragments)))
        return Transformation(fragments)


wrapped_list = [f"<ansiwhite>{project}</ansiwhite>" for project in task_list.projects]

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

