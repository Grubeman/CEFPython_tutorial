"""Application basique CEFPython
"""
import sys
import os
from cefpython3 import cefpython as cef

S_CURRENT_DIR = os.path.dirname(__file__) #repertoire courant

def launch_cef():
    """Lance une application CEF
    """
    sys.excepthook = cef.ExceptHook  # Tue tous les process CEF si erreur
    cef.Initialize()
    cef.CreateBrowserSync(url="file://"+os.path.join(S_CURRENT_DIR, "helloworld.html"), window_title="Helloworld")
    cef.MessageLoop()
    cef.Shutdown()

if __name__ == "__main__":
    launch_cef()
