from entity.group import Group

class Subject:
    def __init__(self, id: int, name: str, priority: int, credits: int, groups: list[Group]):
        self.id = id
        self.name = name
        self.priority = priority
        self.credits = credits
        self.groups = groups