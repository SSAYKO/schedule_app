from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QLineEdit, QSpinBox, QHBoxLayout, QComboBox, QListWidget, QMessageBox, QStackedWidget, QListWidgetItem, QMenu, QDialog
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor, QAction, QIcon
from entity.group import Group
from entity.schedule import Schedule
from entity.subject import Subject

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set window properties
        self.setWindowTitle("Schedule Planner")
        self.setWindowIcon(QIcon("icons/image.png"))
        self.setFixedSize(400, 400)

        # Initialize attributes
        self.subjects = []
        self.selected_subject = None

        # Set up the main stack widget
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # Set up the subject form
        self.setup_subject_form()

    def setup_subject_form(self):
        """Set up the form for adding subjects."""
        self.subject_form_widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)

        # Layout for subject name input
        layout1 = QHBoxLayout()
        self.add_label(main_layout, "\nLista de materias", 14)
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
        button_layout.addWidget(self.add_button("Agregar Materia", self.create_subject))
        button_layout.addWidget(self.add_button("Limpiar Campos", self.reset_subject_form))

        # List widget for subjects
        self.subjects_list = QListWidget()
        self.subjects_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.subjects_list.customContextMenuRequested.connect(self.show_context_menu)
        self.subjects_list.itemDoubleClicked.connect(self.view_subject_groups)

        # Add widgets to the main layout
        main_layout.addWidget(self.subjects_list)
        main_layout.addLayout(layout1)
        main_layout.addLayout(layout2)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.add_button("Crear Horarios", self.create_schedule))
        self.subject_form_widget.setLayout(main_layout)
        self.stack.addWidget(self.subject_form_widget)

    def create_schedule(self):
        """Create the schedule for the selected subjects."""
        if not self.subjects:
            self.show_message("Error", "Agregue materias antes de crear horarios.", QMessageBox.Icon.Warning)
            return
        
        for subject in self.subjects:
            if not subject.groups:
                self.show_message("Error", f"La materia '{subject.name}' no tiene grupos asignados.", QMessageBox.Icon.Warning)
                return
            
        if hasattr(self, 'page4'):
            self.stack.setCurrentWidget(self.page4)
            return
        self.page4 = QWidget()
        self.page4_layout = QVBoxLayout()
        self.page4.setLayout(self.page4_layout)
        self.stack.addWidget(self.page4)
        self.stack.setCurrentIndex(2)
        self.schedule = Schedule(self.subjects).generate_variations()
        print("El horario es...")
        for subject in self.schedule.subjects:
            print(f"La materia es: {subject.name} con grupo {subject.group.id} en horario {subject.group.schedule_date1_input} {subject.group.schedule1_hour1}-{subject.group.schedule1_hour2}, {subject.group.schedule_date2_input} {subject.group.schedule2_hour1}-{subject.group.schedule2_hour2}")

    def show_context_menu(self, position):
        """Show context menu for deleting subjects."""
        menu = QMenu()
        delete_action = QAction("Eliminar Elementos", self)
        delete_action.triggered.connect(self.delete_selected_items)
        menu.addAction(delete_action)
        menu.exec(self.subjects_list.viewport().mapToGlobal(position))

    def delete_selected_items(self):
        """Delete selected subjects from the list."""
        selected_items = self.subjects_list.selectedItems()
        if not selected_items:
            return
        for item in selected_items:
            self.subjects_list.takeItem(self.subjects_list.row(item))
            self.subjects = [subject for subject in self.subjects if subject.name != item.text()]

    def verify_subject_exists(self, subject_name):
        """Check if a subject already exists."""
        return any(subject.name == subject_name for subject in self.subjects)

    def add_subject_to_list(self, subject, icon_path):
        """Add a new subject to the list."""
        if self.verify_subject_exists(subject.name):
            self.show_message("Falla", f"Materia '{subject.name}' ya existe.", QMessageBox.Icon.Warning)
            return
        self.subjects.append(subject)
        self.update_subject_list()
        self.show_message("Exito", f"Materia '{subject.name}' Agregada Correctamente", QMessageBox.Icon.Information)

    def stylize_list_item(self, subject):
        """Stylize the list item for a subject."""
        item = QListWidgetItem(subject.name)
        item.setForeground(QColor(Qt.GlobalColor.black))
        item.setBackground(QColor(Qt.GlobalColor.gray))
        font = item.font()
        font.setPointSize(12)
        font.setBold(True)
        item.setFont(font)
        item.setToolTip(f"Id: {subject.id}\nNombre: {subject.name}\nPrioridad: {subject.priority} \nCréditos: {subject.credits}")
        return item

    def find_selected_subject(self, subject_name):
        """Find the selected subject by name."""
        self.selected_subject = next((subject for subject in self.subjects if subject.name == subject_name), None)

    def create_subject(self):
        """Create a new subject."""
        name = self.name_input.text().strip()
        if not name:
            self.show_message("Error", "El nombre de la materia no puede estar vacío.", QMessageBox.Icon.Warning)
            return
        priority = self.priority_input.value()
        credits = self.credits_input.value()
        new_subject = Subject(len(self.subjects) + 1, name, priority, credits)
        self.add_subject_to_list(new_subject, "icon.png")

    def clear_subjects_page_values(self):
        """Clear the input fields for subjects."""
        self.name_input.clear()
        self.priority_input.setValue(1)
        self.credits_input.setValue(1)

    def view_subject_groups(self, item):
        """View the groups for a selected subject."""
        self.clear_subjects_page_values()
        self.find_selected_subject(item.text())
        if hasattr(self, 'page3'):
            self.update_subject_groups_view()
            self.stack.setCurrentWidget(self.page3)
            return
        self.page3 = QWidget()
        self.page3_layout = QVBoxLayout()
        self.group_list = QListWidget()
        self.subject_label = QLabel("Grupos de: " + self.selected_subject.name)
        self.subject_label.setFont(QFont("Arial", 14))
        self.page3_layout.addWidget(self.subject_label)
        self.page3_layout.addWidget(self.group_list)
        self.page3.setLayout(self.page3_layout)
        self.stack.addWidget(self.page3)
        self.stack.setCurrentIndex(1)

        self.add_label(self.page3_layout, "ID del Grupo:")
        self.group_id_input = self.add_spin_box(self.page3_layout, 1, 5)

        page3_layout2 = QHBoxLayout()
        self.schedule_date1_input = self.add_combo_box(page3_layout2, ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"])
        self.schedule_hour1_input = self.add_spin_box(page3_layout2, 600, 2100)  # Horarios como enteros
        self.schedule_hour2_input = self.add_spin_box(page3_layout2, 600, 2100)

        page3_layout3 = QHBoxLayout()
        self.schedule_date2_input = self.add_combo_box(page3_layout3, ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"])
        self.schedule2_hour1_input = self.add_spin_box(page3_layout3, 600, 2100)
        self.schedule2_hour2_input = self.add_spin_box(page3_layout3, 600, 2100)

        self.page3_layout.addLayout(page3_layout2)
        self.page3_layout.addLayout(page3_layout3)
        self.page3_layout.addWidget(self.add_button("Guardar Grupo", self.save_group))
        self.page3_layout.addWidget(self.add_button("Regresar", self.return_and_clean))
        self.update_subject_groups_view()

    def update_subject_groups_view(self):
        """Update the view for subject groups."""
        self.subject_label.setText(f"Grupos de: {self.selected_subject.name}")
        self.group_id_input.setValue(1)
        self.schedule_hour1_input.setValue(600)
        self.schedule_hour2_input.setValue(600)
        self.schedule2_hour1_input.setValue(600)
        self.schedule2_hour2_input.setValue(600)
        self.group_list.clear()
        self.update_group_list()

    def return_and_clean(self):
        """Return to the main page and clear selections."""
        self.selected_subject = None
        self.stack.setCurrentIndex(0)

    def save_group(self):
        """Save a new group for the selected subject."""
        try:
            group_id = self.group_id_input.value()
            schedule1_date = self.schedule_date1_input.currentText()
            schedule1_hour1 = self.schedule_hour1_input.value()
            schedule1_hour2 = self.schedule_hour2_input.value()
            schedule2_date = self.schedule_date2_input.currentText()
            schedule2_hour1 = self.schedule2_hour1_input.value()
            schedule2_hour2 = self.schedule2_hour2_input.value()

            if schedule1_date == schedule2_date:
                self.show_message("Error", "Los días de los horarios no pueden ser iguales.", QMessageBox.Icon.Warning)
                return

            if schedule1_hour2 - schedule1_hour1 < 100:
                self.show_message("Error", "La diferencia entre las horas del primer horario debe ser al menos de 1 hora.", QMessageBox.Icon.Warning)
                return
            
            if schedule2_hour2 - schedule2_hour1 < 100:
                self.show_message("Error", "La diferencia entre las horas del segundo horario debe ser al menos de 1 hora.", QMessageBox.Icon.Warning)
                return

            group = Group(group_id, schedule1_date, schedule1_hour1, schedule1_hour2, schedule2_date, schedule2_hour1, schedule2_hour2)

            if any(existing_group.id == group_id for existing_group in self.selected_subject.groups):
                self.show_message("Error", f"El grupo con ID {group_id} ya existe.", QMessageBox.Icon.Warning)
                return

            self.selected_subject.groups.append(group)
            self.show_message("Éxito", f"Grupo {group_id} creado para materia '{self.selected_subject.name}'.")
            self.update_group_list()

        except ValueError:
            self.show_message("Error", "El ID del grupo es numerico", QMessageBox.Icon.Warning)

    def update_subject_list(self):
        """Update the list of subjects."""
        self.subjects_list.clear()
        for subject in self.subjects:
            self.subjects_list.addItem(self.stylize_list_item(subject))

    def update_group_list(self):
        """Update the list of groups for the selected subject."""
        self.group_list.clear()
        for group in self.selected_subject.groups:
            self.group_list.addItem(f"Grupo {group.id}: ({group.schedule_date1_input} {group.schedule1_hour1_date}-{group.schedule1_hour2_date}), ({group.schedule_date2_input} {group.schedule2_hour1_date}-{group.schedule2_hour2_date})")

    def reset_subject_form(self):
        """Reset the input fields for subjects."""
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

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()