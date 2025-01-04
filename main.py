from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QLineEdit, QSpinBox, QHBoxLayout, QComboBox, QListWidget, QMessageBox, QStackedWidget, QListWidgetItem, QMenu, QDialog
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor, QAction, QIcon
from entity.group import Group
from entity.subject import Subject
from datetime import datetime
from datetime import datetime, timedelta

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Schedule Planner")
        self.setWindowIcon(QIcon("icons/image.png"))
        self.setFixedSize(400, 400)

        self.subjects = []
        self.selected_subject = None

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.setup_subject_form()

    def setup_subject_form(self):
        self.subject_form_widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)

        layout1 = QHBoxLayout()
        self.add_label(main_layout, "\nLista de materias", 14)
        self.add_label(layout1, "Nombre de la Materia:")
        self.name_input = self.add_line_edit(layout1, "ej. Calculo Diferencial")

        layout2 = QHBoxLayout()
        self.add_label(layout2, "Prioridad:")
        self.priority_input = self.add_spin_box(layout2, 1, 5)
        self.add_label(layout2, "Créditos:")
        self.credits_input = self.add_spin_box(layout2, 1, 4)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_button("Agregar Materia", self.create_subject))
        button_layout.addWidget(self.add_button("Limpiar Campos", self.reset_subject_form))

        self.subjects_list = QListWidget()
        self.subjects_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.subjects_list.customContextMenuRequested.connect(self.show_context_menu)
        self.subjects_list.itemDoubleClicked.connect(self.view_subject_groups)

        main_layout.addWidget(self.subjects_list)
        main_layout.addLayout(layout1)
        main_layout.addLayout(layout2)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.add_button("Crear Horarios", lambda: print("Creando Variaciones...")))
        self.subject_form_widget.setLayout(main_layout)
        self.stack.addWidget(self.subject_form_widget)

    def show_context_menu(self, position):
        menu = QMenu()
        delete_action = QAction("Eliminar Elementos", self)
        delete_action.triggered.connect(self.delete_selected_items)
        menu.addAction(delete_action)
        menu.exec(self.subjects_list.viewport().mapToGlobal(position))

    def delete_selected_items(self):
        selected_items = self.subjects_list.selectedItems()
        if not selected_items:
            return
        for item in selected_items:
            self.subjects_list.takeItem(self.subjects_list.row(item))
            self.subjects = [subject for subject in self.subjects if subject.name != item.text()]

    def verify_subject_exists(self, subject_name):
        return any(subject.name == subject_name for subject in self.subjects)

    def add_subject_to_list(self, subject, icon_path):
        if self.verify_subject_exists(subject.name):
            self.show_message("Falla", f"Materia '{subject.name}' ya existe.", QMessageBox.Icon.Warning)
            return
        self.subjects.append(subject)
        self.update_subject_list()
        self.show_message("Exito", f"Materia '{subject.name}' Agregada Correctamente", QMessageBox.Icon.Information)

    def stylize_list_item(self, subject):
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
        self.selected_subject = next((subject for subject in self.subjects if subject.name == subject_name), None)

    def create_subject(self):
        name = self.name_input.text().strip()
        if not name:
            self.show_message("Error", "El nombre de la materia no puede estar vacío.", QMessageBox.Icon.Warning)
            return
        priority = self.priority_input.value()
        credits = self.credits_input.value()
        new_subject = Subject(len(self.subjects) + 1, name, priority, credits, [])
        self.add_subject_to_list(new_subject, "icon.png")

    def clear_subjects_page_values(self):
        self.name_input.clear()
        self.priority_input.setValue(1)
        self.credits_input.setValue(1)

    def view_subject_groups(self, item):
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
        self.schedule_hour1_input = self.add_combo_box(page3_layout2, [f"{hour}:{minute:02d} {'AM' if hour < 12 else 'PM'}" for hour in range(6, 21) for minute in (0, 30)])
        self.schedule_hour2_input = self.add_combo_box(page3_layout2, [f"{hour}:{minute:02d} {'AM' if hour < 12 else 'PM'}" for hour in range(6, 21) for minute in (0, 30)])
        page3_layout3 = QHBoxLayout()
        self.schedule_date2_input = self.add_combo_box(page3_layout3, ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"])
        self.schedule2_hour1_input = self.add_combo_box(page3_layout3, [f"{hour}:{minute:02d} {'AM' if hour < 12 else 'PM'}" for hour in range(6, 21) for minute in (0, 30)])
        self.schedule2_hour2_input = self.add_combo_box(page3_layout3, [f"{hour}:{minute:02d} {'AM' if hour < 12 else 'PM'}" for hour in range(6, 21) for minute in (0, 30)])

        self.page3_layout.addLayout(page3_layout2)
        self.page3_layout.addLayout(page3_layout3)
        self.page3_layout.addWidget(self.add_button("Guardar Grupo", self.save_group))
        self.page3_layout.addWidget(self.add_button("Regresar", self.return_and_clean))
        self.update_subject_groups_view()

    def update_subject_groups_view(self):
        self.subject_label.setText(f"Grupos de: {self.selected_subject.name}")
        self.group_id_input.setValue(1)
        self.schedule_date1_input.setCurrentIndex(0)
        self.schedule_hour1_input.setCurrentIndex(0)
        self.schedule_hour2_input.setCurrentIndex(0)
        self.schedule_date2_input.setCurrentIndex(0)
        self.schedule2_hour1_input.setCurrentIndex(0)
        self.schedule2_hour2_input.setCurrentIndex(0)
        self.group_list.clear()
        self.update_group_list()

    def return_and_clean(self):
        self.selected_subject = None
        self.stack.setCurrentIndex(0)

    def save_group(self):
        try:
            group_id = self.group_id_input.value()
            schedule1_date = self.schedule_date1_input.currentText()
            schedule1_hour1_date = self.schedule_hour1_input.currentText()
            schedule1_hour2_date = self.schedule_hour2_input.currentText()
            schedule2_date = self.schedule_date2_input.currentText()
            schedule2_hour1_date = self.schedule2_hour1_input.currentText()
            schedule2_hour2_date = self.schedule2_hour2_input.currentText()

            def convert_to_24_hour(time_str):
                return datetime.strptime(time_str, "%I:%M %p").time()

            schedule1_hour1_time = convert_to_24_hour(schedule1_hour1_date)
            schedule1_hour2_time = convert_to_24_hour(schedule1_hour2_date)
            schedule2_hour1_time = convert_to_24_hour(schedule2_hour1_date)
            schedule2_hour2_time = convert_to_24_hour(schedule2_hour2_date)


            if schedule2_hour2_time == schedule1_hour2_time or schedule2_hour1_time == schedule1_hour1_time:
                
                 self.show_message("Error", "Verifica si cambiaste correctamente las horas.", QMessageBox.Icon.Warning)
                 return

            if datetime.combine(datetime.today(), schedule1_hour2_time) - datetime.combine(datetime.today(), schedule1_hour1_time) < timedelta(hours=1):
                self.show_message("Error", "La diferencia entre las horas del primer horario debe ser al menos de 1 hora.", QMessageBox.Icon.Warning)
                return
            
            if datetime.combine(datetime.today(), schedule2_hour2_time) - datetime.combine(datetime.today(), schedule2_hour1_time) < timedelta(hours=1):
                self.show_message("Error", "La diferencia entre las horas del segundo horario debe ser al menos de 1 hora.", QMessageBox.Icon.Warning)
                return

            group = Group(group_id, schedule1_date, schedule1_hour1_date, schedule1_hour2_date, schedule2_date, schedule2_hour1_date, schedule2_hour2_date)

            if any(existing_group.id == group_id for existing_group in self.selected_subject.groups):
                self.show_message("Error", f"El grupo con ID {group_id} ya existe.", QMessageBox.Icon.Warning)
                return

            self.selected_subject.groups.append(group)
            self.show_message("Éxito", f"Grupo {group_id} creado para materia '{self.selected_subject.name}'.")
            self.update_group_list()

        except ValueError:
            self.show_message("Error", "El ID del grupo es numerico", QMessageBox.Icon.Warning)

    def update_subject_list(self):
        self.subjects_list.clear()
        for subject in self.subjects:
            self.subjects_list.addItem(self.stylize_list_item(subject))

    def update_group_list(self):
        self.group_list.clear()
        for group in self.selected_subject.groups:
            self.group_list.addItem(f"Grupo {group.id}: ({group.schedule_date1_input} {group.schedule1_hour1_date}-{group.schedule1_hour2_date}), ({group.schedule_date2_input} {group.schedule2_hour1_date}-{group.schedule2_hour2_date})")

    def reset_subject_form(self):
        self.name_input.clear()
        self.priority_input.setValue(1)
        self.credits_input.setValue(1)

    def add_label(self, layout, text, font_size=11):
        label = QLabel(text)
        label.setFont(QFont("Arial", font_size))
        layout.addWidget(label)

    def add_line_edit(self, layout, placeholder=""):
        line_edit = QLineEdit()
        line_edit.setFixedHeight(30)
        line_edit.setPlaceholderText(placeholder)
        layout.addWidget(line_edit)
        return line_edit

    def add_spin_box(self, layout, minimum, maximum):
        spin_box = QSpinBox()
        spin_box.setFixedHeight(30)
        spin_box.setMinimum(minimum)
        spin_box.setMaximum(maximum)
        layout.addWidget(spin_box)
        return spin_box

    def add_combo_box(self, layout, items):
        combo_box = QComboBox()
        combo_box.addItems(items)
        layout.addWidget(combo_box)
        return combo_box

    def add_button(self, text, callback, color=None):
        button = QPushButton(text)
        button.setFixedHeight(40)
        button.clicked.connect(callback)
        if color:
            button.setStyleSheet(f"background-color: {color}; color: white;")
        return button

    def show_message(self, title, text, icon=QMessageBox.Icon.Information):
        QMessageBox(icon, title, text).exec()

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()