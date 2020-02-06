from PySide2.QtWidgets import *
from PySide2.QtGui import QKeySequence

class MainWindow(QMainWindow):
    def closeEvent(self, e):
        if not text.document().isModified():
            return
        answer = QMessageBox.question(
            window, None,
            "You have unsaved changes. Save before closing?",
            QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel
        )
        if answer & QMessageBox.Save:
            save()
        elif answer & QMessageBox.Cancel:
            e.ignore()

app = QApplication([])
app.setApplicationName("Text Editor")
text = QPlainTextEdit()
window = MainWindow()
window.setWindowTitle("Text Editor")
window.setCentralWidget(text)
file_path = None

# Add menu bar
menu = window.menuBar().addMenu("&File")
save_action = QAction("&Save")
# Set up menu action to save files
save_as_action = QAction("Save &As...")
def save_as():
    # Execute save as from menu bar or shortcut
    global file_path
    path = QFileDialog.getSaveFileName(window, "Save As")[0]
    if path:
        file_path = path
        save()
def save():
    if file_path is None:
        save_as()
    else:
        with open(file_path, "w") as f:
            f.write(text.toPlainText())
save_action.triggered.connect(save)
save_action.setShortcut(QKeySequence.Save)
save_as_action.triggered.connect(save_as)
menu.addAction(save_as_action)
menu.addAction(save_action)

# Set up menu action to open files
open_action = QAction("&Open")
def open_file():
    # Set up function to open files
    global file_path
    path = QFileDialog.getOpenFileName(window, "Open")[0]
    if path:
        text.setPlainText(open(path).read())
        file_path = path
# Set up signal and slot for open_action
open_action.triggered.connect(open_file)
# Set hotkey for 'Ctrl+O'
open_action.setShortcut(QKeySequence.Open)
menu.addAction(open_action)

# Add menu action to close application
close = QAction("&Close")
close.triggered.connect(window.close)
menu.addAction(close)

# Set up menu action to open information about the app
help_menu = window.menuBar().addMenu("&Help")
about_action = QAction("&About")
help_menu.addAction(about_action)
def show_about_dialog():
    # Show "About App" dialog
    text = "<center>" \
        "<h1>Text Editor</h1>" \
        "&#8291;" \
        "<img src=icon.svg>" \
        "</center>" \
        "<p>Version 31.4.159.265358<br/>" \
        "Copyright &copy; LogoSec Inc.</p>"
    QMessageBox.about(window, "About Text Editor", text)

about_action.triggered.connect(show_about_dialog)
window.show()
app.exec_()
