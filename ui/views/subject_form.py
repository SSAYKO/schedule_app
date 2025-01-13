from PyQt6.QtWidgets import (
     QPushButton, QLabel, QVBoxLayout, QWidget, QLineEdit, QSpinBox, QHBoxLayout, QComboBox, QListWidget, QMessageBox, QMenu
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QAction
from ui.controllers.subject_controller import SubjectController
from ui.views.group_management import GroupManagement

class SubjectForm(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack
        self.subject_controller = SubjectController()

        # Main Layout Configuration
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        main_layout.setSpacing(20)

        self.add_label(main_layout, "\nLista de materias", 14)
        # List widget for subjects
        self.subjects_list = QListWidget()
        self.subjects_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.subjects_list.customContextMenuRequested.connect(self.show_context_menu)
        self.subjects_list.itemDoubleClicked.connect(self.view_subject_groups)
        main_layout.addWidget(self.subjects_list)

        # Layout for subject name input
        layout1 = QHBoxLayout()
        self.add_label(layout1, "Nombre de la Materia:")
        self.name_input = self.add_line_edit(layout1, "ej. Calculo Diferencial")

        # Layout for priority and credits input
        layout2 = QHBoxLayout()
        self.add_label(layout2, "Prioridad:")
        self.priority_input = self.add_spin_box(layout2, 1, 5)
        self.add_label(layout2, "Créditos:")
        self.credits_input = self.add_spin_box(layout2, 1, 4)

        # Layout for buttons
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_button("Agregar Materia", self.send_create_subject))
        button_layout.addWidget(self.add_button("Limpiar Campos", self.clear_subjects_page_values))

        main_layout.addLayout(layout1)
        main_layout.addLayout(layout2)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.add_button("Crear Horarios",  lambda: print("Crear Horario")))
        self.setLayout(main_layout)
        self.stack.addWidget(self)

        # Load current subjects
        self.update_subject_list()

    def send_create_subject(self):
        name = self.name_input.text().strip()
        priority = self.priority_input.value()
        credits = self.credits_input.value()
        message = self.subject_controller.create_subject(name, priority, credits)
        self.update_subject_list()
        self.show_message("Schedule App", message)

    def update_subject_list(self):
        self.subjects_list.clear()
        for subject in self.subject_controller.get_all_subjects():
            self.subjects_list.addItem(subject.name)

    def clear_subjects_page_values(self):
        """Clear the input fields for subjects."""
        self.name_input.clear()
        self.priority_input.setValue(1)
        self.credits_input.setValue(1)

    def add_label(self, layout, text, font_size=11):
        """Add a label to a layout."""
        label = QLabel(text)
        label.setFont(QFont("Arial", font_size))
        layout.addWidget(label)

    def add_line_edit(self, layout, placeholder=""):
        """Add a line edit to a layout."""
        line_edit = QLineEdit()
        line_edit.setFixedHeight(30)
        line_edit.setPlaceholderText(placeholder)
        layout.addWidget(line_edit)
        return line_edit

    def add_spin_box(self, layout, minimum, maximum):
        """Add a spin box to a layout."""
        spin_box = QSpinBox()
        spin_box.setFixedHeight(30)
        spin_box.setMinimum(minimum)
        spin_box.setMaximum(maximum)
        layout.addWidget(spin_box)
        return spin_box

    def add_combo_box(self, layout, items):
        """Add a combo box to a layout."""
        combo_box = QComboBox()
        combo_box.addItems(items)
        layout.addWidget(combo_box)
        return combo_box

    def add_button(self, text, callback, color=None):
        """Add a button to a layout."""
        button = QPushButton(text)
        button.setFixedHeight(40)
        button.clicked.connect(callback)
        if color:
            button.setStyleSheet(f"background-color: {color}; color: white;")
        return button

    def show_message(self, title, text, icon=QMessageBox.Icon.Information):
        """Show a message box."""
        QMessageBox(icon, title, text).exec()

    def show_context_menu(self, position):
        """Show context menu for deleting subjects."""
        menu = QMenu()
        delete_action = QAction("Eliminar Elementos", self)
        delete_action.triggered.connect(self.delete_selected_items)
        menu.addAction(delete_action)
        menu.exec(self.subjects_list.viewport().mapToGlobal(position))

    def delete_selected_items(self):
        """Delete selected subjects from the list and notify the controller."""
        selected_items = self.subjects_list.selectedItems()
        if not selected_items:
            return

        # Obtener los nombres de las materias seleccionadas
        selected_subject_names = [item.text() for item in selected_items]

        # Notificar al controlador para eliminar las materias
        for subject_name in selected_subject_names:
            self.subject_controller.delete_subject(subject_name)

        # Actualizar la lista visual después de la eliminación
        self.update_subject_list()

    def find_selected_subject(self, subject_name):
        """Find the selected subject by name."""
        selected_subject = next((subject for subject in self.subject_controller.get_all_subjects() if subject.name == subject_name.text()), None)
        return selected_subject

    def view_subject_groups(self, item):
        """Navega al formulario de gestión de grupos y actualiza su contenido."""
        self.clear_subjects_page_values()

        selected_subject = self.find_selected_subject(item)

        if hasattr(self, 'group_form'):
            self.group_form.update_content(selected_subject)
        else:
            self.group_form = GroupManagement(self.stack, selected_subject)
            self.stack.addWidget(self.group_form)

        self.stack.setCurrentWidget(self.group_form)
