from entity.group import Group


class GroupController:
    def __init__(self):
        self.groups = []

    def create_group(self, subject, group_id, schedule1, schedule2):
        """Crea y valida un nuevo grupo para la materia seleccionada."""
        if any(g.id == group_id for g in subject.groups):
            return False, f"El grupo con ID {group_id} ya existe para la materia {subject.name}."

        # Validaciones de horarios
        if schedule1['day'] == schedule2['day']:
            return False, "Los días de los horarios no pueden ser iguales."
        
        if schedule1['end'] - schedule1['start'] < 100 or schedule2['end'] - schedule2['start'] < 100:
            return False, "La diferencia entre las horas debe ser al menos de 1 hora."

        # Crear el grupo y asignarlo a la materia
        new_group = Group(
            group_id,
            schedule1['day'], schedule1['start'], schedule1['end'],
            schedule2['day'], schedule2['start'], schedule2['end']
        )
        subject.groups.append(new_group)
        return True, f"Grupo {group_id} creado exitosamente para {subject.name}."

    def get_groups(self, subject):
        """Obtiene todos los grupos asociados a una materia."""
        return subject.groups

    def delete_group(self, subject, group_id):
        """Elimina un grupo de una materia."""
        subject.groups = [g for g in subject.groups if g.id != group_id]
        return f"Grupo {group_id} eliminado de {subject.name}."
