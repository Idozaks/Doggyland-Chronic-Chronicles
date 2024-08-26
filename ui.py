import pygame

import time

from constants import WIDTH, HEIGHT, GREEN, YELLOW, RED, BLACK, GRAY, WHITE, BLUE, LIGHT_GREEN, LIGHT_RED

# Font initialization
pygame.font.init()
FONT_SMALL = pygame.font.Font(None, 24)
FONT_MEDIUM = pygame.font.Font(None, 32)
FONT_LARGE = pygame.font.Font(None, 48)

# Button dimensions
BUTTON_WIDTH = 120
BUTTON_HEIGHT = 50

# Button definitions
start_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 50)
grow_button = pygame.Rect(WIDTH // 2 - 180, HEIGHT - 100, BUTTON_WIDTH, BUTTON_HEIGHT)
water_button = pygame.Rect(WIDTH // 2 - 60, HEIGHT - 100, BUTTON_WIDTH, BUTTON_HEIGHT)
fertilize_button = pygame.Rect(WIDTH // 2 + 60, HEIGHT - 100, BUTTON_WIDTH, BUTTON_HEIGHT)
shop_button = pygame.Rect(WIDTH // 2 + 180, HEIGHT - 100, BUTTON_WIDTH, BUTTON_HEIGHT)
back_button = pygame.Rect(WIDTH - 130, HEIGHT - 60, 100, 40)

def draw_button(screen, button, text, font, color, hover_color):
    mouse_pos = pygame.mouse.get_pos()
    if button.collidepoint(mouse_pos):
        pygame.draw.rect(screen, hover_color, button)
    else:
        pygame.draw.rect(screen, color, button)
    text_surf = font.render(text, True, BLACK)
    text_rect = text_surf.get_rect(center=button.center)
    screen.blit(text_surf, text_rect)

def draw_menu(screen):
    screen.fill((0, 100, 0))  # Green background
    title_font = pygame.font.Font(None, 64)
    title_text = title_font.render("Doggyland ChronicChronicles", True, (255, 255, 255))
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 100))
    
    # Update this line to include all required arguments
    draw_button(screen, start_button, "Start Game", FONT_MEDIUM, (0, 200, 0), (0, 255, 0))

def draw_loading_bar(screen, progress):
    bar_width = 400
    bar_height = 40
    bar_x = (WIDTH - bar_width) // 2
    bar_y = HEIGHT // 2 + 100
    pygame.draw.rect(screen, WHITE, (bar_x, bar_y, bar_width, bar_height), 2)
    pygame.draw.rect(screen, WHITE, (bar_x, bar_y, bar_width * progress, bar_height))

def draw_game(screen, player, current_strain, grow_progress, harvest_ready, grow_increment, watered_time):
    screen.fill(BLACK)
    
    # Draw strain info
    font = pygame.font.Font(None, 24)
    strain_info = [
        f"Strain: {current_strain.name}",
        f"THC: {current_strain.thc_content:.1f}%",
        f"Grow Increment: {grow_increment:.2f}",
        f"Typical Potency: {current_strain.typical_potency:.1f}%"
    ]
    for i, info in enumerate(strain_info):
        text = font.render(info, True, WHITE)
        screen.blit(text, (10, 10 + i * 30))

    # Calculate image size and position
    image_height = HEIGHT - 150
    image_width = int(image_height * 0.6)
    image_x = (WIDTH - image_width) // 2
    image_y = 10

    # Load and draw the plant image
    stage = min(int(grow_progress * 3), 2)
    plant_image = pygame.image.load(current_strain.image_paths[stage])
    plant_image = pygame.transform.scale(plant_image, (image_width, image_height))
    screen.blit(plant_image, (image_x, image_y))

    # Define button dimensions and positions
    button_width = 100
    button_height = 40
    button_y = HEIGHT - 50
    grow_button = pygame.Rect(WIDTH // 5 - button_width // 2, button_y, button_width, button_height)
    water_button = pygame.Rect(2 * WIDTH // 5 - button_width // 2, button_y, button_width, button_height)
    fertilize_button = pygame.Rect(3 * WIDTH // 5 - button_width // 2, button_y, button_width, button_height)
    shop_button = pygame.Rect(4 * WIDTH // 5 - button_width // 2, button_y, button_width, button_height)

    # Draw buttons
    pygame.draw.rect(screen, GREEN, grow_button)
    pygame.draw.rect(screen, BLUE, water_button)
    pygame.draw.rect(screen, YELLOW, fertilize_button)
    pygame.draw.rect(screen, RED, shop_button)

    font = pygame.font.Font(None, 28)
    grow_text = font.render("Grow", True, BLACK)
    water_text = font.render("Water", True, BLACK)
    fertilize_text = font.render("Fertilize", True, BLACK)
    shop_text = font.render("Shop", True, BLACK)

    screen.blit(grow_text, (grow_button.x + 25, grow_button.y + 10))
    screen.blit(water_text, (water_button.x + 20, water_button.y + 10))
    screen.blit(fertilize_text, (fertilize_button.x + 10, fertilize_button.y + 10))
    screen.blit(shop_text, (shop_button.x + 25, shop_button.y + 10))

    # Draw progress bar
    draw_loading_bar(screen, grow_progress)

    return grow_button, water_button, fertilize_button, shop_button

def draw_shop(screen, player, strains, fertilizers, equipment):
    screen.fill((200, 200, 200))
    font = pygame.font.Font(None, 36)
    small_font = pygame.font.Font(None, 24)
    
    # Draw player's money
    money_text = font.render(f"Money: ${player.money}", True, (0, 0, 0))
    screen.blit(money_text, (20, 20))

    # Define column widths and positions
    col_width = WIDTH // 3
    col1_x = 20
    col2_x = col_width + 20
    col3_x = 2 * col_width + 20

    # Draw strains
    draw_shop_section(screen, "Strains", strains, col1_x, 80, (0, 100, 0), font, small_font)

    # Draw fertilizers
    draw_shop_section(screen, "Fertilizers", fertilizers, col2_x, 80, (139, 69, 19), font, small_font)

    # Draw equipment
    draw_shop_section(screen, "Equipment", equipment, col3_x, 80, (70, 130, 180), font, small_font)

    # Draw back button
    back_button = pygame.Rect(WIDTH - 120, HEIGHT - 60, 100, 40)
    pygame.draw.rect(screen, (100, 100, 100), back_button)
    back_text = font.render("Back", True, (255, 255, 255))
    screen.blit(back_text, (back_button.x + 25, back_button.y + 10))

    return back_button

def draw_shop_section(screen, title, items, x, y, color, font, small_font):
    title_text = font.render(title, True, (0, 0, 0))
    screen.blit(title_text, (x, y))

    buttons = []
    for i, item in enumerate(items):
        button = pygame.Rect(x, y + 40 + i * 100, 280, 80)
        pygame.draw.rect(screen, color, button)
        item_text = font.render(f"{item.name} - ${item.price}", True, (255, 255, 255))
        screen.blit(item_text, (button.x + 10, button.y + 10))
        
        # Add item description
        if hasattr(item, 'description'):
            desc = item.description
        elif hasattr(item, 'boost'):
            desc = f"Boost: {item.boost}"
        elif hasattr(item, 'effect'):
            desc = item.effect
        else:
            desc = "No description available"
        
        desc_text = small_font.render(desc, True, (255, 255, 255))
        screen.blit(desc_text, (button.x + 10, button.y + 45))
        
        buttons.append(button)

    return buttons

def create_strain_buttons(num_strains):
    buttons = []
    for i in range(num_strains):
        x = 50 + (i % 3) * (BUTTON_WIDTH + 20)
        y = 100 + (i // 3) * (BUTTON_HEIGHT + 60)
        buttons.append(pygame.Rect(x, y, BUTTON_WIDTH, BUTTON_HEIGHT))
    return buttons

def draw_inventory(screen, player):
    screen.fill((200, 200, 200))
    font = pygame.font.Font(None, 36)
    small_font = pygame.font.Font(None, 24)
    
    # Draw player's money
    money_text = font.render(f"Money: ${player.money}", True, (0, 0, 0))
    screen.blit(money_text, (20, 20))

    # Draw inventory sections
    draw_inventory_section(screen, "Strains (Click to plant)", player.inventory.strains, 20, 80, (0, 100, 0), font, small_font)
    draw_inventory_section(screen, "Fertilizers", player.inventory.fertilizers, 20, 300, (139, 69, 19), font, small_font)
    draw_inventory_section(screen, "Equipment", player.inventory.equipment, 20, 520, (70, 130, 180), font, small_font)

    # Draw back button
    back_button = pygame.Rect(WIDTH - 120, HEIGHT - 60, 100, 40)
    pygame.draw.rect(screen, (100, 100, 100), back_button)
    back_text = font.render("Back", True, (255, 255, 255))
    screen.blit(back_text, (back_button.x + 25, back_button.y + 10))

    return back_button

def draw_inventory_section(screen, title, items, x, y, color, font, small_font):
    title_text = font.render(title, True, (0, 0, 0))
    screen.blit(title_text, (x, y))

    for i, item in enumerate(items):
        item_rect = pygame.Rect(x, y + 40 + i * 60, 280, 50)
        pygame.draw.rect(screen, color, item_rect)
        item_text = font.render(item.name, True, (255, 255, 255))
        screen.blit(item_text, (item_rect.x + 10, item_rect.y + 10))
        
        if hasattr(item, 'description'):
            desc = item.description
        elif hasattr(item, 'boost'):
            desc = f"Boost: {item.boost}"
        elif hasattr(item, 'effect'):
            desc = item.effect
        else:
            desc = "No description available"
        
        desc_text = small_font.render(desc, True, (255, 255, 255))
        screen.blit(desc_text, (item_rect.x + 10, item_rect.y + 35))