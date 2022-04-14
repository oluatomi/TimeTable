from classes_periods import TimeTable


class Prime:
    
    def __init__(self):
        self.comment = "Eggs and bacon"

    def change(self):
        Prime().comment = "Eggs and NO bacon"
        return Prime().comment


c = Prime()
print(c.comment)

print(c.change())
