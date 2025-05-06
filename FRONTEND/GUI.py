# gui.py

import sys
import os
from dotenv import dotenv_values
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QStackedWidget, QWidget, QVBoxLayout,
    QPushButton, QLabel, QSizePolicy, QHBoxLayout, QFrame
)
from PyQt5.QtGui import QIcon, QPainter, QMovie, QColor, QTextCharFormat, QFont, QPixmap, QTextBlockFormat
from PyQt5.QtCore import Qt, QSize, QTimer


# Load environment variables
env_vars = dotenv_values(".env")
Assistantname = env_vars.get("Assistantname")
current_dir = os.getcwd()

TempDirPath = os.path.join(current_dir, "FRONTEND", "Files")
GraphicsDirPath = os.path.join(current_dir, "FRONTEND", "Graphics")

old_chat_message = ""

def AnswerModifier(Answer):
    lines = Answer.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    modified_answer = '\n'.join(non_empty_lines)
    return modified_answer

def QueryModifier(Query):
    new_query = Query.lower().strip()
    query_words = new_query.split()
    question_words = ["how", "what", "who", "where", "when", "why", "which", "whose", "whom", "can you", "what's", "where's", "how's"]
    if any(word + " " in new_query for word in question_words):
        if query_words[-1][-1] in ['.', '?', '!']:
            new_query = new_query[:-1] + "?"
        else:
            new_query += "?"
    else:
        if query_words[-1][-1] in ['.', '?', '!']:
            new_query = new_query[:-1] + "."
        else:
            new_query += "."
    return new_query.capitalize()

# ----------- Utility Functions -----------

def GraphicsDirectoryPath(Filename):
    return os.path.join(GraphicsDirPath, Filename)

def TempDirectoryPath(Filename):
    return os.path.join(TempDirPath, Filename)

def SetMicrophoneStatus(Command):
    with open(TempDirectoryPath("Mic.data"), "w", encoding='utf-8') as file:
        file.write(Command)

def GetMicrophoneStatus():
    with open(TempDirectoryPath("Mic.data"), "r", encoding='utf-8') as file:
        return file.read()

def MicButtonInitialed():
    SetMicrophoneStatus("False")

def MicButtonClosed():
    SetMicrophoneStatus("True")

def ShowTextToScreen(Text):
    with open(TempDirectoryPath("Response.data"), "w", encoding='utf-8') as file:
        file.write(Text)

def SetAssistantStatus(Status):
    with open(TempDirectoryPath("Status.data"), "w", encoding='utf-8') as file:
        file.write(Status)

def GetAssistantStatus():
    with open(TempDirectoryPath("Status.data"), "r", encoding='utf-8') as file:
        return file.read()

# ----------- Chat Section -----------

class ChatSection(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(-10, 40, 40, 100)
        layout.setSpacing(-100)

        self.chat_text_edit = QTextEdit()
        self.chat_text_edit.setReadOnly(True)
        self.chat_text_edit.setTextInteractionFlags(Qt.NoTextInteraction)
        self.chat_text_edit.setFrameStyle(QFrame.NoFrame)
        layout.addWidget(self.chat_text_edit)

        font = QFont()
        font.setPointSize(13)
        self.chat_text_edit.setFont(font)

        text_color = QTextCharFormat()
        text_color.setForeground(QColor(Qt.blue))
        self.chat_text_edit.setCurrentCharFormat(text_color)

        self.gif_label = QLabel()
        self.gif_label.setStyleSheet("border: none;")
        self.gif_label.setAlignment(Qt.AlignRight | Qt.AlignBottom)
        self.gif_label.setMovie(QMovie(GraphicsDirectoryPath("Tomi.gif")))
        self.gif_label.movie().start()

        # Mic Icon
        self.icon_label = QLabel()
        self.icon_label.setCursor(Qt.PointingHandCursor)
        self.icon_label.mousePressEvent = self.toggle_icon
        self.toggled = True
        self.load_icon(GraphicsDirectoryPath("Mic_off.png"))

        icon_layout = QHBoxLayout()
        icon_layout.addStretch()
        icon_layout.addWidget(self.icon_label)

        layout.addLayout(icon_layout)
        layout.addWidget(self.gif_label)

        self.label = QLabel("")
        self.label.setStyleSheet("color: white; font-size:16px; margin-right: 195px; border:none; margin-top: -30px;")
        self.label.setAlignment(Qt.AlignRight)
        layout.addWidget(self.label)

        self.setStyleSheet("background-color: black;")
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.loadMessages)
        self.timer.timeout.connect(self.updateStatus)
        self.timer.start(5)

        self.chat_text_edit.viewport().installEventFilter(self)
        self.setScrollBarStyle()

    def load_icon(self, path, width=60, height=60):
        pixmap = QPixmap(path)
        self.icon_label.setPixmap(pixmap.scaled(width, height))

    def toggle_icon(self, event=None):
        if self.toggled:
            self.load_icon(GraphicsDirectoryPath("Mic_on.png"))
            MicButtonInitialed()
        else:
            self.load_icon(GraphicsDirectoryPath("Mic_off.png"))
            MicButtonClosed()
        self.toggled = not self.toggled

    def loadMessages(self):
        global old_chat_message
        with open(TempDirectoryPath("Response.data"), "r", encoding='utf-8') as file:
            messages = file.read()
            if messages and messages != old_chat_message:
                self.addMessage(messages, "white")
                old_chat_message = messages

    def updateStatus(self):
        self.label.setText(GetAssistantStatus())

    def addMessage(self, message, color):
        cursor = self.chat_text_edit.textCursor()
        format_ = QTextCharFormat()
        formatm = QTextBlockFormat()
        formatm.setTopMargin(10)
        formatm.setLeftMargin(10)
        format_.setForeground(QColor(color))
        cursor.setCharFormat(format_)
        cursor.setBlockFormat(formatm)
        cursor.insertText(message + "\n")
        self.chat_text_edit.setTextCursor(cursor)

    def setScrollBarStyle(self):
        self.setStyleSheet("""
            QScrollBar:vertical {
                border: none;
                background: black;
                width: 10px;
                margin: 0;
            }
            QScrollBar::handle:vertical {
                background: white;
                min-height: 20px;
            }
            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                background: black;
                height: 10px;
            }
            QScrollBar::up-arrow:vertical,
            QScrollBar::down-arrow:vertical,
            QScrollBar::add-page:vertical,
            QScrollBar::sub-page:vertical {
                background: none;
            }
        """)

# ----------- Initial Screen (Home) -----------

class InitialScreen(QWidget):
    def __init__(self):
        super().__init__()

        screen = QApplication.primaryScreen().geometry()
        screen_width = screen.width()
        screen_height = screen.height()

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 60)  # Add some bottom padding
        layout.setSpacing(0)

        # Tomi GIF in center
        gif_label = QLabel()
        movie = QMovie(GraphicsDirectoryPath("Tomi.gif"))
        movie.setScaledSize(QSize(int(screen_width * 0.5), int(screen_height * 0.7)))
        gif_label.setMovie(movie)
        gif_label.setAlignment(Qt.AlignCenter)
        movie.start()

        # Mic icon in center-bottom
        self.icon_label = QLabel()
        self.icon_label.setCursor(Qt.PointingHandCursor)
        self.icon_label.mousePressEvent = self.toggle_icon
        self.toggled = True
        self.load_icon(GraphicsDirectoryPath("Mic_off.png"))

        mic_layout = QHBoxLayout()
        mic_layout.addStretch()
        mic_layout.addWidget(self.icon_label)
        mic_layout.addStretch()

        layout.addWidget(gif_label, stretch=1, alignment=Qt.AlignCenter)
        layout.addLayout(mic_layout, stretch=0)

        self.setLayout(layout)
        self.setStyleSheet("background-color: black;")
        self.setFixedSize(screen_width, screen_height)

    def load_icon(self, path, width=60, height=60):
        pixmap = QPixmap(path)
        self.icon_label.setPixmap(pixmap.scaled(width, height))

    def toggle_icon(self, event=None):
        if self.toggled:
            self.load_icon(GraphicsDirectoryPath("Mic_on.png"))
            MicButtonInitialed()
        else:
            self.load_icon(GraphicsDirectoryPath("Mic_off.png"))
            MicButtonClosed()
        self.toggled = not self.toggled

# ----------- Message Screen -----------

class MessageScreen(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel(""))
        layout.addWidget(ChatSection())
        self.setLayout(layout)
        self.setStyleSheet("background-color: black;")

# ----------- Top Bar -----------

class CustomTopBar(QWidget):
    def __init__(self, parent, stacked_widget):
        super().__init__(parent)
        self.stacked_widget = stacked_widget
        self.maximized = False
        self.initUI()

    def initUI(self):
        self.setFixedHeight(50)
        layout = QHBoxLayout(self)
        layout.setAlignment(Qt.AlignRight)

        title = QLabel(f" {str(Assistantname).capitalize()} AI     ")
        title.setStyleSheet("background-color:white; color:black; font-size: 18px")

        home_btn = QPushButton(" Home", icon=QIcon(GraphicsDirectoryPath("Home.png")))
        home_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))

        chat_btn = QPushButton(" Chat", icon=QIcon(GraphicsDirectoryPath("Chats.png")))
        chat_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))

        minimize_btn = QPushButton(icon=QIcon(GraphicsDirectoryPath("Minimize2.png")))
        minimize_btn.clicked.connect(self.parent().showMinimized)

        self.max_btn = QPushButton(icon=QIcon(GraphicsDirectoryPath("Maximize.png")))
        self.max_btn.clicked.connect(self.toggleMaximize)

        close_btn = QPushButton(icon=QIcon(GraphicsDirectoryPath("Close.png")))
        close_btn.clicked.connect(self.parent().close)

        for btn in [home_btn, chat_btn, minimize_btn, self.max_btn, close_btn]:
            btn.setStyleSheet("background-color:white")

        layout.addWidget(title)
        layout.addStretch()
        layout.addWidget(home_btn)
        layout.addWidget(chat_btn)
        layout.addStretch()
        layout.addWidget(minimize_btn)
        layout.addWidget(self.max_btn)
        layout.addWidget(close_btn)

    def toggleMaximize(self):
        if self.maximized:
            self.parent().showNormal()
            self.max_btn.setIcon(QIcon(GraphicsDirectoryPath("Maximize.png")))
        else:
            self.parent().showMaximized()
            self.max_btn.setIcon(QIcon(GraphicsDirectoryPath("Restore.png")))
        self.maximized = not self.maximized

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), Qt.white)
        super().paintEvent(event)

# ----------- Main Window -----------

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.initUI()

    def initUI(self):
        screen = QApplication.primaryScreen().geometry()
        self.setGeometry(0, 0, screen.width(), screen.height())

        self.stack = QStackedWidget(self)
        self.stack.addWidget(InitialScreen())
        self.stack.addWidget(MessageScreen())

        top_bar = CustomTopBar(self, self.stack)
        self.setMenuWidget(top_bar)
        self.setCentralWidget(self.stack)
        self.setStyleSheet("background-color: black;")

# ----------- Launch -----------

def GraphicalUserInterface():
    print("Lunching GUI...")
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    GraphicalUserInterface()
