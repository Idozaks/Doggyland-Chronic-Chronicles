import pygame
import sys
from player import Player
from strain import Strain
import random
from ui import draw_button, draw_menu, draw_loading_bar, draw_game, draw_shop, WIDTH, HEIGHT, MENU, PLAYING, SHOP, start_button, grow_button, shop_button, harvest_button, back_button, create_strain_buttons, fertilizer_button

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Doggyland ChronicChronicles")

player = Player("John Doe")
strains = [
    Strain("OG Kush", 20.0, 0.1, 60, 400, "A classic strain with a strong, relaxing high.", 
           ["images/og_kush_stage1.png", "images/og_kush_stage2.png", "images/og_kush_stage3.png"], max_height=80, typical_potency=20.0),
    Strain("Blue Dream", 18.0, 0.2, 55, 450, "A balanced hybrid with a sweet berry aroma.", 
           ["images/blue_dream_stage1.png", "images/blue_dream_stage2.png", "images/blue_dream_stage3.png"], max_height=100, typical_potency=18.0),
    Strain("Sour Diesel", 22.0, 0.2, 65, 380, "An energizing sativa with a pungent diesel smell.", 
           ["images/sour_diesel_stage1.png", "images/sour_diesel_stage2.png", "images/sour_diesel_stage3.png"], max_height=120, typical_potency=22.0)]
current_strain = random.choice(strains)

strain_buttons = create_strain_buttons(len(strains))

grow_progress = 0
harvest_ready = False
grow_button_held = False
current_state = MENU
growing_rate = 0.1

def main():
    global current_state, grow_progress, harvest_ready, current_strain, grow_button_held, growing_rate
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and current_state == MENU:
                    current_state = PLAYING
                elif current_state == PLAYING:
                    if event.key == pygame.K_g:
                        grow_button_held = True
                    elif event.key == pygame.K_h and harvest_ready:
                        player.inventory.money += current_strain.yield_amount
                        grow_progress = 0
                        harvest_ready = False
                        current_strain = random.choice(strains)
                        growing_rate = 0.1  # Reset growing rate
                    elif event.key == pygame.K_s:
                        current_state = SHOP
                elif current_state == SHOP:
                    if event.key == pygame.K_b:
                        current_state = PLAYING
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_g:
                    grow_button_held = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if current_state == MENU:
                    if start_button.collidepoint(event.pos):
                        current_state = PLAYING
                elif current_state == PLAYING:
                    if grow_button.collidepoint(event.pos):
                        grow_button_held = True
                    elif shop_button.collidepoint(event.pos):
                        current_state = SHOP
                    elif harvest_button.collidepoint(event.pos) and harvest_ready:
                        player.inventory.money += current_strain.yield_amount
                        grow_progress = 0
                        harvest_ready = False
                        current_strain = random.choice(strains)
                        growing_rate = 0.1  # Reset growing rate
                    elif fertilizer_button.collidepoint(event.pos):
                        growing_rate += 0.1
                elif current_state == SHOP:
                    if back_button.collidepoint(event.pos):
                        current_state = PLAYING
                    else:
                        for i, button in enumerate(strain_buttons):
                            if button.collidepoint(event.pos):
                                current_strain = strains[i]
                                current_state = PLAYING
                                growing_rate = 0.1  # Reset growing rate
                                break
            if event.type == pygame.MOUSEBUTTONUP:
                if grow_button.collidepoint(event.pos):
                    grow_button_held = False

        if current_state == PLAYING and grow_button_held:
            grow_progress += growing_rate
            if grow_progress >= current_strain.growth_time:
                grow_progress = current_strain.growth_time
                harvest_ready = True

        if current_state == MENU:
            draw_menu(screen)
        elif current_state == PLAYING:
            draw_game(screen, player, current_strain, grow_progress, harvest_ready, fertilizer_button, growing_rate)
        elif current_state == SHOP:
            draw_shop(screen, strains, strain_buttons)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()