class Group:
    def __init__(self, id: int):
        self.id = id
        self.schedules = []  # List to store schedules as dictionaries

    def add_schedule(self, day: str, start_time: int, end_time: int):
        """
        Adds a new schedule for the group.
        
        Args:
            day (str): The day of the schedule (e.g., 'Monday', 'Tuesday').
            start_time (int): The start time in minutes from midnight (e.g., 510 for 8:30 AM).
            end_time (int): The end time in minutes from midnight (e.g., 1020 for 5:00 PM).
        
        Raises:
            ValueError: If start_time is greater than or equal to end_time.
        """
        if start_time >= end_time:
            raise ValueError("Start time must be earlier than end time.")
        self.schedules.append({
            'day': day,
            'start_time': start_time,
            'end_time': end_time
        })

    def minutes_to_ampm(self, minutes: int) -> str:
        """
        Converts minutes since midnight to a time in AM/PM format.
        
        Args:
            minutes (int): The time in minutes since midnight (e.g., 510 for 8:30 AM).
        
        Returns:
            str: The time in AM/PM format (e.g., "8:30 AM").
        """
        hours = minutes // 60
        mins = minutes % 60
        period = "AM" if hours < 12 else "PM"
        hours = hours % 12
        hours = 12 if hours == 0 else hours  # Handle 12 AM/PM
        return f"{hours}:{mins:02d} {period}"

    def get_schedules_in_ampm(self):
        """
        Returns the schedules with times converted to AM/PM format.
        
        Returns:
            list[dict]: List of schedules with start_time and end_time in AM/PM format.
        """
        return [
            {
                'day': schedule['day'],
                'start_time': self.minutes_to_ampm(schedule['start_time']),
                'end_time': self.minutes_to_ampm(schedule['end_time'])
            }
            for schedule in self.schedules
        ]

    def get_schedules(self):
        """
        Returns the list of schedules.
        
        Returns:
            list[dict]: List of schedules, each represented as a dictionary with day, start_time, and end_time.
        """
        return self.schedules
