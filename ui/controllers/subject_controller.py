from entity.subject import Subject

class SubjectController:
    def __init__(self):
        self.subjects = []

    def create_subject(self, name, priority, credits) -> str:
        if not name:
            return f"El nombre de la materia no puede estar vacío."
        if any(s.name == name for s in self.subjects):
            return f"Materia '{name}' ya existe."
        new_subject = Subject(len(self.subjects) + 1, name, priority, credits)
        self.subjects.append(new_subject)
        return f"Materia '{name}' agregada correctamente."

    def get_all_subjects(self):
        return self.subjects
    
    def delete_subject(self, subject_name):
        """Delete a subject by its name."""
        self.subjects = [subject for subject in self.subjects if subject.name != subject_name]
