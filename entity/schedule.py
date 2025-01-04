from entity.subject import Subject

class Schedule:
    def __init__(self, id: int, subjects: list[Subject]):
        self.id = id
        self.subjects = subjects

    def add_subject(self, subject: Subject):
        self.subjects.append(subject)

    def generate_variations(self):
        variations = []
        while variations.count() < 5:
            schedule = Schedule()
            # search the subject with the highest priority and add it to the schedule    
            # if two or more subjects has the same priority, add the one with the highest credits
            # if two or more subjects has the same priority and credits, add the one with the highest hours
            # if two or more subjects has the same priority, credits and hours, add the one with the lowest id
            subjects_sorted = sorted(self.subjects, key=lambda s: (-s.priority, -s.credits, -s.hours, s.id))
            for subject in subjects_sorted:
                if subject not in schedule.subjects:
                    schedule.add_subject(subject)
                    break
            variations.append(schedule)
        return variations