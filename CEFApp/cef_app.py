"""
Base CEF Python Application
"""
import sys
from cefpython3 import cefpython as cef

class CEFApp:
    def __init__(self, start_url, window_title = "CEFApp"):
        """Initialize a new base CEF app
        
        :param start_url: Load url on browser startup
        :type start_url: str
        :param window_title: Top CEF browser title, defaults to "CEFApp"
        :type window_title: str, optional
        """
        sys.excepthook = cef.ExceptHook
        cef.Initialize()
        self.browser = cef.CreateBrowserSync(url=start_url, window_title=window_title)
        self.bindings = cef.JavascriptBindings(
                    bindToFrames=False, bindToPopups=False)
        self.set_javascript_bindings()

    def set_javascript_bindings(self):
        """Sets javscript bindings
        """
        self.bindings.SetProperty("py_print", print)
        self.browser.SetJavascriptBindings(self.bindings)

    def run(self):
        cef.MessageLoop()
        cef.Shutdown()