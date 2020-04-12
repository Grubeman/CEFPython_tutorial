"""Application basique CEFPython
"""
import sys
import os

from cef_app import CEFApp

S_CURRENT_DIR = os.path.dirname(__file__) #repertoire courant

if __name__ == "__main__":
    CEFApp("file://"+os.path.join(S_CURRENT_DIR, "helloworld.html")).run()
