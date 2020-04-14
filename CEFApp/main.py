"""Application basique CEFPython
"""
import sys
import os

from cef_app import CEFApp

from jinja2 import Template
from jinja2 import Environment, FileSystemLoader

S_CURRENT_DIR = os.path.dirname(__file__) #repertoire courant

file_loader = FileSystemLoader(os.path.join(S_CURRENT_DIR, "templates"))
JINJA_ENV = Environment(loader=file_loader)
print(JINJA_ENV.list_templates())
class MyApp(CEFApp):
    def __init__(self):
        CEFApp.__init__(self, "jinja://helloworld.jinja2?name=Grubeman" ,window_title="MyApp", jinja_env = JINJA_ENV)

if __name__ == "__main__":
    MyApp().run()
