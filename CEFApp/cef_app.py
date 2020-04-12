"""
Base CEF Python Application
"""
import sys
from cefpython3 import cefpython as cef


class LoadHandler(object):
    def OnLoadStart(self, browser, frame, **_):
        print("On load start")

    def OnLoadError(self, browser, frame, error_code, error_text_out, failed_url, **_):
        print("On load error")
        
    def OnLoadEnd(self, browser, frame, **_):
        print("On load end")

    def OnLoadingStateChange(self, browser, is_loading, **_):
        """Called when the loading state has changed."""
        if not is_loading:
            # Loading is complete. DOM is ready.
            print("Loading is complete")
        else:
            print("DOM is loading")

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

        #Ajout des clients handler
        self.set_client_handlers()

    def set_client_handlers(self):
        client_handlers = [LoadHandler()]
        for handler in client_handlers:
            self.browser.SetClientHandler(handler)

    def set_javascript_bindings(self):
        """Sets javscript bindings
        """
        self.bindings.SetProperty("py_print", print)
        self.browser.SetJavascriptBindings(self.bindings)

    def run(self):
        cef.MessageLoop()
        cef.Shutdown()