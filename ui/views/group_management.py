from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QLabel, QPushButton, QComboBox, QMessageBox
from PyQt6.QtGui import QFont
from ui.controllers.group_controller import GroupController

class GroupManagement(QWidget):
    MAX_SCHEDULES = 3  # Límite máximo de horarios dinámicos

    def __init__(self, stack, selected_subject):
        super().__init__()
        self.stack = stack
        self.selected_subject = selected_subject
        self.group_controller = GroupController()
        self.schedule_inputs = []  # Lista para almacenar los horarios dinámicos

        # Configurar layout principal
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Etiqueta de título
        title_label = QLabel(f"Grupos de: {self.selected_subject.name}")
        title_label.setFont(QFont("Arial", 14))
        main_layout.addWidget(title_label)

        # Lista de grupos
        self.group_list = QListWidget()
        main_layout.addWidget(self.group_list)

        # Layout para inputs dinámicos
        self.layout_inputs = QVBoxLayout()
        main_layout.addLayout(self.layout_inputs)

        # Agregar un horario inicial
        self.add_schedule_input()

        # Botón para agregar más horarios
        self.add_schedule_button = QPushButton("Agregar horario")
        self.add_schedule_button.clicked.connect(self.add_schedule_input)
        main_layout.addWidget(self.add_schedule_button)

        # Botones de acciones principales
        button_layout = QHBoxLayout()
        main_layout.addLayout(button_layout)
        button_layout.addWidget(self.add_button("Guardar Grupo", self.save_group))
        button_layout.addWidget(self.add_button("Eliminar Grupo", self.delete_selected_group))
        button_layout.addWidget(self.add_button("Regresar", self.return_to_subject_form))

    def add_schedule_input(self):
        """Agrega un nuevo conjunto de inputs para un horario."""
        if len(self.schedule_inputs) >= self.MAX_SCHEDULES:
            self.show_message("Límite alcanzado", f"Solo puedes agregar hasta {self.MAX_SCHEDULES} horarios.")
            return

        # Bloquear horarios anteriores
        for day_input, hour_start_input, hour_end_input in self.schedule_inputs:
            day_input.setEnabled(False)
            hour_start_input.setEnabled(False)
            hour_end_input.setEnabled(False)

        # Calcular la hora mínima para el nuevo horario
        min_start_time = 360  # 6:00 AM en minutos desde medianoche
        if self.schedule_inputs:
            last_day = self.schedule_inputs[-1][0].currentText()
            last_end_time = self.schedule_inputs[-1][2].currentData()
            min_start_time = last_end_time if last_day == "Lunes" else 360

        layout_schedule = QHBoxLayout()
        self.layout_inputs.addLayout(layout_schedule)

        # Crear y agregar widgets
        day_input = self.add_combo_box(layout_schedule, ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"])
        hour_start_input = self.add_time_combo_box(layout_schedule, min_start_time, 1260)  # Hasta las 9:00 PM
        hour_end_input = self.add_time_combo_box(layout_schedule, min_start_time + 60, min(min_start_time + 180, 1320))  # Hasta las 10:00 PM

        # Actualizar el rango del horario final al cambiar el inicio
        hour_start_input.currentIndexChanged.connect(lambda: self.update_hour_end_limits(hour_start_input, hour_end_input))
        day_input.currentIndexChanged.connect(lambda: self.update_day_limits(day_input, hour_start_input, hour_end_input))

        # Almacenar el conjunto de inputs
        self.schedule_inputs.append((day_input, hour_start_input, hour_end_input))

        # Oculta el botón si ya alcanzó el límite
        if len(self.schedule_inputs) >= self.MAX_SCHEDULES:
            self.add_schedule_button.setEnabled(False)

    def update_hour_end_limits(self, hour_start_input, hour_end_input):
        """Actualiza los límites del horario final en función del horario inicial."""
        start_time = hour_start_input.currentData()
        hour_end_input.clear()
        for time in range(start_time + 60, min(start_time + 180, 1320) + 1, 30):
            hour_end_input.addItem(self.minutes_to_ampm(time), time)

    def update_day_limits(self, day_input, hour_start_input, hour_end_input):
        """Actualiza los límites para los horarios según el día seleccionado."""
        selected_day = day_input.currentText()
        min_start_time = 360  # Por defecto 6:00 AM

        # Si el día es el mismo que el último, ajustar según el último horario
        if self.schedule_inputs:
            last_day = self.schedule_inputs[-1][0].currentText()
            last_end_time = self.schedule_inputs[-1][2].currentData()
            if selected_day == last_day:
                min_start_time = last_end_time

        hour_start_input.clear()
        for time in range(min_start_time, 1260 + 1, 30):
            hour_start_input.addItem(self.minutes_to_ampm(time), time)

        # Actualizar el rango del horario final
        self.update_hour_end_limits(hour_start_input, hour_end_input)

    def reset_schedule_inputs(self):
        """Reinicia los inputs de horarios a su estado por defecto."""
        for layout_index in reversed(range(self.layout_inputs.count())):
            layout_item = self.layout_inputs.itemAt(layout_index)
            if layout_item:
                layout_widget = layout_item.layout()
                while layout_widget.count():
                    widget = layout_widget.takeAt(0).widget()
                    if widget:
                        widget.deleteLater()
                layout_widget.deleteLater()

        self.schedule_inputs.clear()
        self.add_schedule_button.setEnabled(True)  # Habilitar el botón de nuevo
        self.add_schedule_input()  # Agregar el horario inicial por defecto

    def save_group(self):
        """Guarda un nuevo grupo para la materia seleccionada."""
        schedules = []
        for day_input, hour_start_input, hour_end_input in self.schedule_inputs:
            schedules.append({
                'day': day_input.currentText(),
                'start': hour_start_input.currentData(),
                'end': hour_end_input.currentData(),
            })

        group_id = len(self.selected_subject.groups) + 1
        success, message = self.group_controller.create_group(self.selected_subject, group_id, schedules)
        self.update_group_list()
        self.show_message("Resultado", message)

    def delete_selected_group(self):
        """Elimina el grupo seleccionado."""
        selected_item = self.group_list.currentItem()
        if selected_item:
            group_id = int(selected_item.text().split()[1])  # Obtener el ID del grupo
            message = self.group_controller.delete_group(self.selected_subject, group_id)
            self.update_group_list()
            self.show_message("Resultado", message)

    def update_group_list(self):
        """Actualiza la lista de grupos."""
        self.group_list.clear()
        groups = self.group_controller.get_groups(self.selected_subject)
        for group in groups:
            schedule_texts = [
                f"{schedule['day']} {self.minutes_to_ampm(schedule['start'])}-{self.minutes_to_ampm(schedule['end'])}"
                for schedule in group.schedules
            ]
            self.group_list.addItem(f"Grupo {group.id}: {', '.join(schedule_texts)}")

    def return_to_subject_form(self):
        """Regresa al formulario de materias y reinicia el formulario."""
        self.reset_schedule_inputs()  # Reinicia los inputs dinámicos
        self.stack.setCurrentIndex(0)

    def add_combo_box(self, layout, items):
        """Crea y agrega un combo box."""
        combo_box = QComboBox()
        combo_box.addItems(items)
        layout.addWidget(combo_box)
        return combo_box

    def add_time_combo_box(self, layout, minimum, maximum):
        """Crea y agrega un combo box para horarios en formato AM/PM."""
        combo_box = QComboBox()
        for time in range(minimum, maximum + 1, 30):
            combo_box.addItem(self.minutes_to_ampm(time), time)
        layout.addWidget(combo_box)
        return combo_box

    def add_button(self, text, callback):
        """Crea y agrega un botón."""
        button = QPushButton(text)
        button.clicked.connect(callback)
        return button

    def show_message(self, title, text):
        """Muestra un mensaje al usuario."""
        QMessageBox(QMessageBox.Icon.Information, title, text).exec()

    def minutes_to_ampm(self, minutes):
        """Convierte minutos desde medianoche a formato AM/PM."""
        hours = minutes // 60
        mins = minutes % 60
        period = "AM" if hours < 12 else "PM"
        hours = hours % 12
        hours = 12 if hours == 0 else hours  # Manejar 12 AM/PM
        return f"{hours}:{mins:02d} {period}"


    def update_content(self, selected_subject):
        """Actualiza el formulario con los datos de la nueva materia seleccionada."""
        self.selected_subject = selected_subject  # Actualiza la materia seleccionada
        
        # Actualiza el título del formulario
        self.layout().itemAt(0).widget().setText(f"Grupos de: {self.selected_subject.name}")
        
        # Actualiza la lista de grupos
        #self.update_group_list()
