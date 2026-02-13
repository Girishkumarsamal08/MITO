import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QStyle
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtCore import Qt, QSize

current_dir = os.getcwd()
GraphicsDirPath = os.path.join(current_dir, "FRONTEND", "Graphics")

def GraphicsDirectoryPath(Filename):
    return os.path.join(GraphicsDirPath, Filename)

class SiriStyleOverlay(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 7px;
            }
            QLabel {
                color: black;
                font-size: 20px;
                font-weight: bold;
            }
            QPushButton {
                background-color: transparent;
                border: none;
                border-radius: 5px;            
            }
        """)

        self.resize(300, 72)
        screen_geometry = QApplication.primaryScreen().geometry()
        self.move(screen_geometry.width() - self.width() - 30, 30)

        self.label = QLabel("Hey Darling", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setGeometry(20, 16, self.width() - 90, 40)

        self.mic_button = QPushButton(self)
        mic_icon = QPixmap(GraphicsDirectoryPath("Mic_on.png"))
        self.mic_button.setIcon(QIcon(mic_icon))
        self.mic_button.setIconSize(QSize(36, 36))
        self.mic_button.setFixedSize(48, 48)
        self.mic_button.move(self.width() - 60, 12)

        self.show()

    def update_text(self, new_text):
        self.label.setText(new_text)

    
# Function to update the label of the existing overlay window
def update_label(text):
    if hasattr(QApplication, "instance") and QApplication.instance():
        for widget in QApplication.instance().allWidgets():
            if isinstance(widget, SiriStyleOverlay):
                widget.update_text(text)
                break


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SiriStyleOverlay()
    sys.exit(app.exec_())
