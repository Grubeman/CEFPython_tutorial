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

class MyApp(CEFApp):
    def __init__(self):
        CEFApp.__init__(self, "file://"+os.path.join(S_CURRENT_DIR, "index.html") ,window_title="MyApp", jinja_env = JINJA_ENV)

    def onNavigate(self):
        t = self.jinja_env.get_template("helloworld.jinja2")
        self.browser.ExecuteFunction("set_inner_html","body",t.render({"color":"blue", "name":"Grubeman"}))

if __name__ == "__main__":
    MyApp().run()
