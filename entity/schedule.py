from entity.group import Group
from entity.subject import Subject

class Schedule:
    def __init__(self, subjects: list[Subject], preferred_time: str = "morning"):
        self.subjects = subjects
        self.preferred_time = preferred_time

    def add_subject(self, subject: Subject):
        self.subjects.append(subject)

    def is_schedule_conflicting(self, group: Group, scheduled_groups: list[Group]) -> bool:
        """
        Checks if the group's schedule conflicts with already scheduled groups.

        Args:
            group (Group): The group to check.
            scheduled_groups (list[Group]): List of already scheduled groups.

        Returns:
            bool: True if there is a conflict, False otherwise.
        """
        for scheduled_group in scheduled_groups:
            for g_schedule in group.get_schedules():
                for s_schedule in scheduled_group.get_schedules():
                    if g_schedule['day'] == s_schedule['day'] and not (
                        g_schedule['end_time'] <= s_schedule['start_time'] or
                        g_schedule['start_time'] >= s_schedule['end_time']
                    ):
                        return True
        return False

    def is_preferred_time(self, group: Group) -> bool:
        """
        Checks if the group's schedules fall within the preferred time range.

        Args:
            group (Group): The group to check.

        Returns:
            bool: True if the group's schedules match the preferred time, False otherwise.
        """
        time_ranges = {
            "morning": (6 * 60, 12 * 60),  # 6:00 AM to 12:00 PM
            "afternoon": (12 * 60, 22 * 60)  # 12:00 PM to 10:00 PM
        }
        start, end = time_ranges.get(self.preferred_time, (0, 24 * 60))
        for schedule in group.get_schedules():
            if not (start <= schedule['start_time'] < end and start <= schedule['end_time'] <= end):
                return False
        return True

    def generate_variations(self):
        """
        Generates a schedule based on subject priorities, credits, and preferences.

        Returns:
            Schedule: A new Schedule instance with selected subjects and groups.
        """
        # Sort subjects by priority, credits, hours, and id
        def calculate_group_hours(group: Group) -> int:
            return sum(schedule['end_time'] - schedule['start_time'] for schedule in group.get_schedules())

        subjects_sorted = sorted(
            self.subjects,
            key=lambda s: (
                -s.priority,
                -s.credits,
                -max(calculate_group_hours(g) for g in s.groups),  # Use max hours among groups
                s.id
            )
        )

        schedule = Schedule([], self.preferred_time)
        scheduled_groups = []

        for subject in subjects_sorted:
            # Sort groups by preferred time and availability
            subject.groups.sort(key=lambda g: (not self.is_preferred_time(g), g.id))

            for group in subject.groups:
                # Check if group schedule conflicts with already scheduled groups
                if not self.is_schedule_conflicting(group, scheduled_groups):
                    # Add group to the schedule
                    subject.establish_group(group)
                    schedule.add_subject(subject)
                    scheduled_groups.append(group)
                    break  # Move to the next subject if a group is added

        return schedule
