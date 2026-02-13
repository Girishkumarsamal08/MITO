import sys
import threading
import subprocess
from PyQt5.QtWidgets import QApplication
from FRONTEND.GUI import MainWindow  # assuming GUI.py defines a MainWindow class
import os
import traceback

def run_main():
    script_path = os.path.join(os.path.dirname(__file__), "Main.py")
    subprocess.Popen([sys.executable, script_path])


def main():
    # Start backend logic
    threading.Thread(target=run_main, daemon=True).start()

    # Start GUI
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

def log_exception(exc_type, exc_value, exc_traceback):
    with open("error_log.txt", "w") as f:
        traceback.print_exception(exc_type, exc_value, exc_traceback, file=f)

sys.excepthook = log_exception

if __name__ == "__main__":
    main()
