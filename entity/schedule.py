from entity.subject import Subject

class Schedule:
    def __init__(self, subjects: list[Subject]):
        self.subjects = subjects

    def add_subject(self, subject: Subject):
        self.subjects.append(subject)

    def generate_variations(self):
        subjects_sorted = sorted(self.subjects, key=lambda s: (-s.priority, -s.credits, s.id))
        schedule = Schedule([])
        subjects_added = 0
        for subject in subjects_sorted:
            # check if the subject is already in the schedule
            if subject not in schedule.subjects:
                # check if the subject has groups
                group_added = False
                for group in subject.groups:
                    # check if the group is available
                    if subjects_added == 0:
                        subject.group = subject.groups[0]
                        schedule.add_subject(subject)
                        subjects_added += 1
                        break

                    for s in schedule.subjects:
                        if group_added:
                            break
                        # Check if the group schedule does not conflict with the other subjects schedules
                        if (group.schedule_date1_input == s.group.schedule_date1_input and group.schedule_date2_input == s.group.schedule_date2_input):
                            if (group.schedule1_hour1_date >= s.group.schedule1_hour2_date and group.schedule2_hour1_date >= s.group.schedule2_hour2_date):
                                subject.group = group
                                schedule.add_subject(subject)
                                subjects_added += 1
                                group_added = True
                                break
                            else:
                                break
                        elif (group.schedule_date1_input == s.group.schedule_date1_input):
                            if (group.schedule1_hour1_date >= s.group.schedule1_hour2_date):
                                subject.group = group
                                schedule.add_subject(subject)
                                subjects_added += 1
                                group_added = True
                                break
                            else:
                                break
                        elif (group.schedule_date2_input == s.group.schedule_date2_input):
                            if (group.schedule1_hour1_date >= s.group.schedule1_hour2_date):
                                subject.group = group
                                schedule.add_subject(subject)
                                subjects_added += 1
                                group_added = True
                                break
                            else:
                                break
                        else:
                            subject.group = group
                            schedule.add_subject(subject)
                            subjects_added += 1
                            group_added = True
                            break
                    if group_added:
                        break
        return schedule