import pygame
import sys
import random
import os
import time
from player import Player
from strain import Strain
from constants import *

from items import Fertilizer, Equipment

CLICKS_TO_GROW = 15  # Number of clicks required to fully grow a plant
GROW_INCREMENT = 1 / CLICKS_TO_GROW  # Progress increment per click

pygame.init()

# Get the screen info
screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h

# Calculate the position to center the window
x = (screen_width - WIDTH) // 2
y = (screen_height - HEIGHT) // 2

# Set the initial position of the window
os.environ['SDL_VIDEO_WINDOW_POS'] = f"{x},{y}"

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Doggyland ChronicChronicles")

from ui import (
    draw_button, draw_menu, draw_loading_bar, draw_game, draw_shop, draw_inventory,
    start_button, grow_button, shop_button, back_button,
    create_strain_buttons, fertilize_button, water_button,
    FONT_SMALL, FONT_MEDIUM, FONT_LARGE  # Add these font imports
)

player = Player("John Doe")
strains = [
    Strain("OG Kush", 20.0, 0.1, 60, 400, "A classic strain with a strong, relaxing high.", 
           ["images/og_kush_stage1.png", "images/og_kush_stage2.png", "images/og_kush_stage3.png"], max_height=80, typical_potency=20.0, price=100),
    Strain("Blue Dream", 18.0, 0.2, 55, 450, "A balanced hybrid with a sweet berry aroma.", 
           ["images/blue_dream_stage1.png", "images/blue_dream_stage2.png", "images/blue_dream_stage3.png"], max_height=100, typical_potency=18.0, price=90),
    Strain("Sour Diesel", 22.0, 0.2, 65, 380, "An energizing sativa with a pungent diesel smell.", 
           ["images/sour_diesel_stage1.png", "images/sour_diesel_stage2.png", "images/sour_diesel_stage3.png"], max_height=120, typical_potency=22.0, price=110)
]
current_strain = None

strain_buttons = create_strain_buttons(len(strains))

grow_progress = 0
harvest_ready = False
grow_button_held = False
current_state = MENU
growing_rate = 0.1
watered_time = 0
grow_increment = 0

# Add some sample items
fertilizers = [
    Fertilizer("Basic Nutrients", 50, 0.01),
    Fertilizer("Advanced Nutrients", 100, 0.02),
    Fertilizer("Super Grow", 200, 0.05),
]

equipment = [
    Equipment("Basic Grow Light", 200, "Increases growth speed by 10%"),
    Equipment("Hydroponic System", 500, "Increases yield by 20%"),
    Equipment("Climate Control", 1000, "Reduces chance of plant diseases"),
]

def main():
    global current_state, grow_progress, harvest_ready, current_strain, grow_button_held, growing_rate, watered_time, grow_increment
    clock = pygame.time.Clock()
    last_state = None  # Keep track of the last state

    # Initialize grow_progress and clicks_to_grow at the start
    grow_progress = 0
    harvest_ready = False
    clicks_to_grow = 0
    grow_increment = 0

    # Initialize buttons
    grow_button = pygame.Rect(0, 0, 1, 1)  # Placeholder, will be updated in draw_game
    water_button = pygame.Rect(0, 0, 1, 1)
    fertilize_button = pygame.Rect(0, 0, 1, 1)
    shop_button = pygame.Rect(0, 0, 1, 1)
    back_button = pygame.Rect(0, 0, 1, 1)  # Initialize back_button

    strain_buttons = [pygame.Rect(50, 100 + i * 60, 200, 50) for i in range(len(strains))]

    # Add this dictionary to map state IDs to names
    state_names = {
        MENU: "MENU",
        PLAYING: "PLAYING",
        SHOP: "SHOP",
        INVENTORY: "INVENTORY"
    }

    harvest_popup = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 - 100, 300, 200)
    harvest_button = pygame.Rect(WIDTH // 2 - 75, HEIGHT // 2 + 25, 150, 50)

    # Add an inventory button
    inventory_button = pygame.Rect(WIDTH - 140, 10, 120, 40)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    mouse_pos = pygame.mouse.get_pos()
                    if current_state == MENU:
                        if start_button.collidepoint(mouse_pos):
                            print("Button clicked: Start Game")
                            current_state = PLAYING
                    elif current_state == PLAYING:
                        if current_strain is None:
                            shop_button = draw_no_plant_screen(screen, player)
                            if shop_button.collidepoint(mouse_pos):
                                current_state = SHOP
                            elif inventory_button.collidepoint(mouse_pos):
                                current_state = INVENTORY
                        else:
                            if grow_button.collidepoint(mouse_pos):
                                if not harvest_ready:
                                    grow_plant()
                            elif water_button.collidepoint(mouse_pos):
                                water_plant()
                            elif fertilize_button.collidepoint(mouse_pos):
                                fertilize_plant()
                            elif shop_button.collidepoint(mouse_pos):
                                current_state = SHOP
                            elif harvest_ready and harvest_button.collidepoint(mouse_pos):
                                harvest_plant()
                                select_strain_from_inventory()
                        if inventory_button.collidepoint(mouse_pos):
                            current_state = INVENTORY
                    elif current_state == SHOP:
                        if back_button.collidepoint(mouse_pos):
                            print("Button clicked: Back")
                            current_state = PLAYING
                        else:
                            handle_shop_purchase(player, mouse_pos, strains, fertilizers, equipment)
                    elif current_state == INVENTORY:
                        if back_button.collidepoint(mouse_pos):
                            current_state = PLAYING
                        else:
                            handle_inventory_selection(player, mouse_pos)
                            if current_strain:
                                current_state = PLAYING
            elif event.type == pygame.KEYDOWN:
                if current_state == PLAYING:
                    if event.key == pygame.K_g:
                        grow_plant()
                    elif event.key == pygame.K_w:
                        water_plant()
                    elif event.key == pygame.K_f:
                        fertilize_plant()
                    elif event.key == pygame.K_s:
                        current_state = SHOP
                    elif event.key == pygame.K_h and harvest_ready:
                        harvest_plant()
                        select_strain_from_inventory()
                    elif event.key == pygame.K_i:
                        current_state = INVENTORY
                elif current_state == SHOP:
                    if event.key == pygame.K_b:
                        current_state = PLAYING
                elif current_state == INVENTORY:
                    if event.key == pygame.K_b:
                        current_state = PLAYING

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Left mouse button
                    grow_button_held = False

        # Update grow progress if the grow button is being held down
        if current_state == PLAYING and grow_button_held:
            grow_plant()

        # Apply water boost if recently watered
        if time.time() - watered_time < WATER_EFFECT_DURATION:
            current_growth_rate = growing_rate + WATER_GROWTH_BOOST
        else:
            current_growth_rate = growing_rate

        if current_state == MENU:
            draw_menu(screen)
        elif current_state == PLAYING:
            if current_strain is None:
                shop_button = draw_no_plant_screen(screen, player)
            else:
                grow_button, water_button, fertilize_button, shop_button = draw_game(screen, player, current_strain, grow_progress, harvest_ready, grow_increment, watered_time)
                if harvest_ready:
                    draw_harvest_popup(screen, harvest_popup, harvest_button)
            # Draw inventory button
            pygame.draw.rect(screen, BLUE, inventory_button)
            inventory_text = FONT_SMALL.render("Inventory", True, WHITE)
            screen.blit(inventory_text, (inventory_button.x + 10, inventory_button.y + 10))
        elif current_state == SHOP:
            back_button = draw_shop(screen, player, strains, fertilizers, equipment)
        elif current_state == INVENTORY:
            back_button = draw_inventory(screen, player)

        # Check if the state has changed
        if current_state != last_state:
            print(f"Current state changed to: {state_names[current_state]}")
            last_state = current_state

        pygame.display.flip()
        clock.tick(60)

def grow_plant():
    global grow_progress, harvest_ready
    print("Growing plant")
    grow_progress += grow_increment
    
    # Check for disease
    if random.random() > current_strain.disease_resistance:
        disease_chance = 0.05  # 5% chance of disease per growth increment
        if random.random() < disease_chance:
            print("Oh no! Your plant got a disease!")
            grow_progress -= grow_increment * 2  # Disease sets back growth
            if grow_progress < 0:
                grow_progress = 0

    if grow_progress >= 1:
        grow_progress = 1
        harvest_ready = True
    print(f"Grow progress: {grow_progress:.2f}")

def water_plant():
    global watered_time
    print("Watering plant")
    watered_time = time.time()

def fertilize_plant():
    global grow_increment
    if player.inventory.fertilizers:
        fertilizer = player.inventory.fertilizers.pop(0)
        print(f"Fertilizing plant with {fertilizer.name}")
        grow_increment += fertilizer.boost
        print(f"Grow increment increased to {grow_increment:.2f}")
    else:
        print("No fertilizers available")

def harvest_plant():
    global grow_progress, harvest_ready, current_strain, grow_increment
    print("Plant harvested!")
    
    # Remove the harvested strain from the player's inventory
    if current_strain in player.inventory.strains:
        player.inventory.strains.remove(current_strain)
        print(f"Removed {current_strain.name} from inventory.")
    else:
        print(f"Warning: {current_strain.name} not found in inventory.")
    
    grow_progress = 0
    harvest_ready = False
    clicks_to_grow = random.randint(10, 15)
    grow_increment = 1 / clicks_to_grow  # Reset grow_increment to its initial value
    
    # Set current_strain to None after harvesting
    current_strain = None
    
    print("Plant harvested. Select a new strain from your inventory to continue growing.")

def select_strain_from_inventory():
    global current_strain, grow_progress, harvest_ready, clicks_to_grow, grow_increment
    if player.inventory.strains:
        current_strain = player.inventory.strains[0]  # Select the first available strain
        grow_progress = 0
        harvest_ready = False
        clicks_to_grow = random.randint(10, 15)
        grow_increment = 1 / clicks_to_grow
        print(f"Selected strain: {current_strain.name}")
    else:
        print("No strains available in inventory. Visit the shop to buy more.")

def draw_harvest_popup(screen, popup_rect, button_rect):
    pygame.draw.rect(screen, (200, 200, 200), popup_rect)
    pygame.draw.rect(screen, (100, 100, 100), button_rect)
    font = pygame.font.Font(None, 32)
    text = font.render("Harvest Ready!", True, (0, 0, 0))
    screen.blit(text, (popup_rect.centerx - text.get_width() // 2, popup_rect.y + 20))
    button_text = font.render("Harvest", True, (255, 255, 255))
    screen.blit(button_text, (button_rect.centerx - button_text.get_width() // 2, button_rect.centery - button_text.get_height() // 2))

def handle_shop_purchase(player, mouse_pos, strains, fertilizers, equipment):
    col_width = WIDTH // 3
    
    for i, strain in enumerate(strains):
        button = pygame.Rect(20, 120 + i * 100, 280, 80)
        if button.collidepoint(mouse_pos):
            if player.purchase(strain, strain.price):
                print(f"Purchased {strain.name}")
                player.inventory.add_item(strain)

    for i, fertilizer in enumerate(fertilizers):
        button = pygame.Rect(col_width + 20, 120 + i * 100, 280, 80)
        if button.collidepoint(mouse_pos):
            if player.purchase(fertilizer, fertilizer.price):
                print(f"Purchased {fertilizer.name}")
                player.inventory.add_item(fertilizer)

    for i, equip in enumerate(equipment):
        button = pygame.Rect(2 * col_width + 20, 120 + i * 100, 280, 80)
        if button.collidepoint(mouse_pos):
            if player.purchase(equip, equip.price):
                print(f"Purchased {equip.name}")
                player.inventory.add_item(equip)
                apply_equipment_effects()  # Apply effects immediately after purchase

def apply_equipment_effects():
    global growing_rate, current_strain
    for equipment in player.inventory.equipment:
        if "growth speed" in equipment.effect.lower():
            growing_rate *= 1.1  # 10% increase in growth speed
        elif "yield" in equipment.effect.lower():
            current_strain.yield_factor *= 1.2  # 20% increase in yield
        elif "climate control" in equipment.effect.lower():
            current_strain.disease_resistance = 0.8  # 80% chance to resist diseases
        # Add more equipment effects as needed

def handle_inventory_selection(player, mouse_pos):
    global current_strain, grow_progress, harvest_ready, clicks_to_grow, grow_increment
    for i, strain in enumerate(player.inventory.strains):
        item_rect = pygame.Rect(20, 120 + i * 60, 280, 50)
        if item_rect.collidepoint(mouse_pos):
            current_strain = strain
            grow_progress = 0
            harvest_ready = False
            clicks_to_grow = random.randint(10, 15)
            grow_increment = 1 / clicks_to_grow
            print(f"Selected strain: {current_strain.name}")
            break

def draw_no_plant_screen(screen, player):
    screen.fill(BLACK)
    font = pygame.font.Font(None, 36)
    text = font.render("No plant selected. Visit the shop to buy a strain!", True, WHITE)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    
    # Draw money
    money_text = font.render(f"Money: ${player.money}", True, WHITE)
    screen.blit(money_text, (20, 20))

    # Draw shop button
    shop_button = pygame.Rect(WIDTH // 2 - 60, HEIGHT // 2 + 50, 120, 40)
    pygame.draw.rect(screen, GREEN, shop_button)
    shop_text = font.render("Shop", True, BLACK)
    screen.blit(shop_text, (shop_button.x + 35, shop_button.y + 10))

    return shop_button

if __name__ == "__main__":
    main()