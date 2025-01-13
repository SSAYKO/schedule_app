from entity.group import Group

class Subject:
    def __init__(self, id: int, name: str, priority: int, credits: int):
            self.id = id
            self.name = name
            self.priority = priority
            self.credits = credits
    
    def establish_group(self, group: Group):
         self.group = group

    def establish_groups(self, groups: list[Group]):
          self.groups = groups