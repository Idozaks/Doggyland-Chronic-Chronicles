import pygame  # Import the pygame library for game development
import sys  # Import sys for system-specific parameters and functions
from player import Player
import random

# Initialize Pygame
pygame.init()  # Initialize all imported pygame modules

# Set up the display
WIDTH, HEIGHT = 800, 600  # Define the width and height of the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Create the game window
pygame.display.set_caption("Doggyland ChronicChronicles")  # Set the window title

# Define colors
BLACK = (0, 0, 0)  # Define RGB color for black
WHITE = (255, 255, 255)  # Define RGB color for white
GREEN = (0, 255, 0)  # Define RGB color for green
# All color values: Expected range 0 to 255

# Game states
MENU = 0  # Constant for menu state
PLAYING = 1  # Constant for playing state
current_state = MENU  # Set the initial game state to menu
# MENU, PLAYING, current_state: Expected range 0 to 1

# Font setup
font = pygame.font.Font(None, 36)  # Create a font object with default font and size 36
# Font size: Expected range 1 to 100

player = Player("John Doe")  # Create an instance of the Player class

class Strain:
    def __init__(self, name, thc_content, cbd_content, growth_time, yield_amount, description, image_paths, max_height, typical_potency):
        self.name = name
        self.thc_content = thc_content
        self.cbd_content = cbd_content
        self.growth_time = growth_time
        self.yield_amount = yield_amount
        self.description = description
        self.image_paths = image_paths if isinstance(image_paths, list) else [image_paths]
        self.max_height = max_height
        self.typical_potency = typical_potency
        self.images = self.load_images()

    def load_images(self):
        images = []
        for path in self.image_paths:
            if path.startswith("placeholder"):
                # Create a colored surface as a placeholder
                color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                image = pygame.Surface((50, 50))  # Adjust size as needed
                image.fill(color)
            else:
                image = pygame.image.load(path)
            images.append(image)
        return images

    def get_current_image(self, growth_progress):
        stage = min(int(growth_progress / self.growth_time * len(self.images)), len(self.images) - 1)
        return self.images[stage]

    def calculate_potency(self):
        return self.thc_content + self.cbd_content

    def get_potency_description(self):
        potency = self.calculate_potency()
        if potency < 10:
            return "Mild"
        elif potency < 20:
            return "Moderate"
        else:
            return "Strong"

    def calculate_worth(self):
        potency = self.calculate_potency()
        base_price = 10  # Base price per gram
        potency_multiplier = 1 + (potency / 100)  # Increase price by 1% for each potency point
        return round(self.yield_amount * base_price * potency_multiplier, 2)

    def get_worth_description(self):
        worth = self.calculate_worth()
        return f"Worth: ${worth:.2f} (${worth/self.yield_amount:.2f}/g)"

    def get_potency_comparison(self):
        actual_potency = self.calculate_potency()
        difference = actual_potency - self.typical_potency
        if abs(difference) < 0.1:
            return f"Typical potency: {self.typical_potency:.1f}% (As expected)"
        elif difference > 0:
            return f"Typical potency: {self.typical_potency:.1f}% (Better than average!)"
        else:
            return f"Typical potency: {self.typical_potency:.1f}% (Below average)"

# ... (rest of the code remains unchanged)