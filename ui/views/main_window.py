from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget

from ui.views.subject_form import SubjectForm

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Schedule Planner")
        self.setFixedSize(400, 400)

        # Inicializar el stack y la primera vista
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # Agregar vistas
        self.subject_form = SubjectForm(self.stack)
        self.stack.addWidget(self.subject_form)
