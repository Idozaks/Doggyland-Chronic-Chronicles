import pygame
import sys
import random
import os
import time
from player import Player
from strain import Strain
from constants import *

CLICKS_TO_GROW = 15  # Number of clicks required to fully grow a plant
GROW_INCREMENT = 1 / CLICKS_TO_GROW  # Progress increment per click

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Doggyland ChronicChronicles")

from ui import (
    draw_button, draw_menu, draw_loading_bar, draw_game, draw_shop,
    start_button, grow_button, shop_button, back_button,
    create_strain_buttons, fertilize_button, water_button
)

player = Player("John Doe")
strains = [
    Strain("OG Kush", 20.0, 0.1, 60, 400, "A classic strain with a strong, relaxing high.", 
           ["images/og_kush_stage1.png", "images/og_kush_stage2.png", "images/og_kush_stage3.png"], max_height=80, typical_potency=20.0),
    Strain("Blue Dream", 18.0, 0.2, 55, 450, "A balanced hybrid with a sweet berry aroma.", 
           ["images/blue_dream_stage1.png", "images/blue_dream_stage2.png", "images/blue_dream_stage3.png"], max_height=100, typical_potency=18.0),
    Strain("Sour Diesel", 22.0, 0.2, 65, 380, "An energizing sativa with a pungent diesel smell.", 
           ["images/sour_diesel_stage1.png", "images/sour_diesel_stage2.png", "images/sour_diesel_stage3.png"], max_height=120, typical_potency=22.0)
]
current_strain = random.choice(strains)

strain_buttons = create_strain_buttons(len(strains))

grow_progress = 0
harvest_ready = False
grow_button_held = False
current_state = MENU
growing_rate = 0.1
watered_time = 0
grow_increment = 0

def main():
    global current_state, grow_progress, harvest_ready, current_strain, grow_button_held, growing_rate, watered_time, grow_increment
    clock = pygame.time.Clock()
    last_state = None  # Keep track of the last state

    # Initialize grow_progress and clicks_to_grow at the start
    grow_progress = 0
    harvest_ready = False
    clicks_to_grow = random.randint(10, 15)
    grow_increment = 1 / clicks_to_grow

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
        SHOP: "SHOP"
    }

    harvest_popup = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 - 100, 300, 200)
    harvest_button = pygame.Rect(WIDTH // 2 - 75, HEIGHT // 2 + 25, 150, 50)

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
                            grow_progress = 0
                            harvest_ready = False
                    elif current_state == PLAYING:
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
                    elif current_state == SHOP:
                        if back_button.collidepoint(mouse_pos):
                            print("Button clicked: Back")
                            current_state = PLAYING
                        for button, strain in zip(strain_buttons, strains):
                            if button.collidepoint(mouse_pos):
                                print(f"Button clicked: Strain - {strain.name}")  # For now, just print the strain name
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
                elif current_state == SHOP:
                    if event.key == pygame.K_b:
                        current_state = PLAYING

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Left mouse button
                    grow_button_held = False

        # Update grow progress if the grow button is being held down
        if current_state == PLAYING and grow_button_held:
            grow_progress += growing_rate
            if grow_progress >= current_strain.growth_time:
                grow_progress = current_strain.growth_time
                harvest_ready = True

        # Apply water boost if recently watered
        if time.time() - watered_time < WATER_EFFECT_DURATION:
            current_growth_rate = growing_rate + WATER_GROWTH_BOOST
        else:
            current_growth_rate = growing_rate

        if current_state == MENU:
            draw_menu(screen)
        elif current_state == PLAYING:
            grow_button, water_button, fertilize_button, shop_button = draw_game(screen, player, current_strain, grow_progress, harvest_ready, growing_rate, watered_time)
            if harvest_ready:
                draw_harvest_popup(screen, harvest_popup, harvest_button)
        elif current_state == SHOP:
            back_button, strain_buttons = draw_shop(screen, strains, strain_buttons)

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
    if grow_progress >= 1:
        grow_progress = 1
        harvest_ready = True
    print(f"Grow progress: {grow_progress:.2f}")

def water_plant():
    global watered_time
    print("Watering plant")
    watered_time = time.time()

def fertilize_plant():
    global growing_rate
    print("Fertilizing plant")
    growing_rate += FERTILIZER_BOOST

def harvest_plant():
    global grow_progress, harvest_ready, current_strain, grow_increment
    print("Plant harvested!")
    grow_progress = 0
    harvest_ready = False
    clicks_to_grow = random.randint(10, 15)
    grow_increment = 1 / clicks_to_grow
    current_strain = random.choice(strains)
    print(f"New plant started: {current_strain.name}. Clicks to grow: {clicks_to_grow}")

def draw_harvest_popup(screen, popup_rect, button_rect):
    pygame.draw.rect(screen, (200, 200, 200), popup_rect)
    pygame.draw.rect(screen, (100, 100, 100), button_rect)
    font = pygame.font.Font(None, 32)
    text = font.render("Harvest Ready!", True, (0, 0, 0))
    screen.blit(text, (popup_rect.centerx - text.get_width() // 2, popup_rect.y + 20))
    button_text = font.render("Harvest", True, (255, 255, 255))
    screen.blit(button_text, (button_rect.centerx - button_text.get_width() // 2, button_rect.centery - button_text.get_height() // 2))

if __name__ == "__main__":
    main()