from datetime import datetime

class Group:
    def __init__(self, id: int, schedule_date1_input: str, schedule1_hour1_date: str, schedule1_hour2_date: str, schedule_date2_input: str, schedule2_hour1_date: str, schedule2_hour2_date: str):
        self.id = id
        self.schedule_date1_input = schedule_date1_input
        self.schedule1_hour1_date = schedule1_hour1_date
        self.schedule1_hour2_date = schedule1_hour2_date
        self.schedule_date2_input = schedule_date2_input
        self.schedule2_hour1_date = schedule2_hour1_date
        self.schedule2_hour2_date = schedule2_hour2_date