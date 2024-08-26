from items import Fertilizer, Equipment
from strain import Strain  # Add this import

class Player:
    def __init__(self, name):
        self.name = name
        self.money = 1000
        self.inventory = Inventory()
        self.current_strain = None
        self.passive_multiplier = 1.0  # Add this line

    def purchase(self, item, price):
        if self.money >= price:
            self.money -= price
            self.inventory.add_item(item)
            return True
        return False

    def select_strain(self, strain):
        # We'll use a string comparison instead of isinstance
        if hasattr(strain, 'name'):  # Check if the object has a 'name' attribute
            self.current_strain = strain
            return True
        return False

    def use_item(self, item):
        if item in self.inventory.fertilizers:
            self.inventory.fertilizers.remove(item)
            return "fertilizer", item.boost
        elif item in self.inventory.equipment:
            # Equipment is not consumed, so we don't remove it
            return "equipment", item.effect
        elif item in self.inventory.strains:
            self.current_strain = item
            return "strain", None
        else:
            return None, None

class Inventory:
    def __init__(self):
        self.strains = []
        self.fertilizers = []
        self.equipment = []

    def add_item(self, item):
        if isinstance(item, Strain):
            self.strains.append(item)
        elif isinstance(item, Fertilizer):
            self.fertilizers.append(item)
        elif isinstance(item, Equipment):
            self.equipment.append(item)