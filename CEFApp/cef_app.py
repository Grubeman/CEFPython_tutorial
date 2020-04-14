"""
Base CEF Python Application
"""
import sys
import os
from cefpython3 import cefpython as cef
from urllib.parse import urlparse

class LoadHandler(object):
    def __init__(self, app=None):
        self.app = app

    def OnLoadStart(self, browser, frame, **_):
        print("On load start")

    def OnLoadError(self, browser, frame, error_code, error_text_out, failed_url, **_):
        parsed_url = urlparse(failed_url)
        root_path = parsed_url.netloc+parsed_url.path
        raw_query = parsed_url.query
        query_data = dict([parsed_url.query.split("=")])
        if 'ERR_UNKNOWN_URL_SCHEME' in error_text_out and parsed_url.scheme == "jinja":
            try:
                t = self.app.jinja_env.get_template(root_path)
                self.app.LoadJinjaUrl(root_path, context=query_data)
            except Exception as e:
                print("Template not found",path)
                pass
            return
        if 'ERR_FILE_NOT_FOUND' in error_text_out:
            root_path = os.path.relpath(root_path, self.app.cef_temp_dir).replace(os.path.sep, "/")
            try:
                t = self.app.jinja_env.get_template(root_path)
                self.app.LoadJinjaUrl(root_path, context=query_data)
            except Exception as e:
                print("Template not found",root_path)
                pass
            return
        
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
    def __init__(self, start_url, window_title = "CEFApp", jinja_env=None, cef_temp_dir=None):
        """Initialize a new base CEF app
        
        :param start_url: Load url on browser startup
        :type start_url: str
        :param window_title: Top CEF browser title, defaults to "CEFApp"
        :type window_title: str, optional
        """
        sys.excepthook = cef.ExceptHook
        cef.Initialize()
        self.jinja_env = jinja_env
        if cef_temp_dir is None:
            self.cef_temp_dir = os.path.join(os.path.dirname(__file__), ".cef_temp")
        else:
            self.cef_temp_dir = cef_temp_dir
        self.browser = cef.CreateBrowserSync(url=start_url, window_title=window_title)
        self.bindings = cef.JavascriptBindings(
                    bindToFrames=False, bindToPopups=False)

        #Ajout des clients handler
        self.set_client_handlers()

    def set_client_handlers(self):
        client_handlers = [LoadHandler(self)]
        for handler in client_handlers:
            self.browser.SetClientHandler(handler)

    def set_javascript_bindings(self):
        """Sets javscript bindings
        """
        self.bindings.SetProperty("py_print", print)
        self.browser.SetJavascriptBindings(self.bindings)

    def LoadJinjaUrl(self, template_url, context=None, **kwargs):
        if context is None:
            context = {}
        t = self.jinja_env.get_template(template_url)
        if not os.path.exists(self.cef_temp_dir):
            os.makedirs(self.cef_temp_dir)
        with open(os.path.join(self.cef_temp_dir, "temp.html"), "w") as f:
            f.write(t.render(context))

        template_url = os.path.join(self.cef_temp_dir, "temp.html")
        return self.browser.LoadUrl(template_url, **kwargs)

    def run(self):
        cef.MessageLoop()
        cef.Shutdown()