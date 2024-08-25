class Player:
    def __init__(self, name):
        self.name = name
        self.inventory = Inventory()

class Inventory:
    def __init__(self):
        self.money = 1000
        self.strains = []
        self.products = []