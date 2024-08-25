import pygame
from strain import Strain

# Initialize Pygame
pygame.init()

# Set up some constants
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Doggyland ChronicChronicles")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
LIGHT_GRAY = (200, 200, 200)

# Define colors for different strains
STRAIN_COLORS = {
    "OG Kush": (0, 100, 0),  # Dark Green
    "Blue Dream": (0, 0, 255),  # Blue
    "Sour Diesel": (255, 255, 0)  # Yellow
}

MENU, PLAYING, SHOP = 0, 1, 2
current_state = MENU

font = pygame.font.Font(None, 36)
button_font = pygame.font.Font(None, 24)

# Set up buttons
grow_button = pygame.Rect(10, HEIGHT - 40, 80, 30)
shop_button = pygame.Rect(100, HEIGHT - 40, 80, 30)
back_button = pygame.Rect(WIDTH // 2 - 50, HEIGHT - 60, 100, 40)
start_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50)
harvest_button = pygame.Rect(WIDTH // 2 - 75, HEIGHT - 100, 150, 40)
water_button = pygame.Rect(440, HEIGHT - 80, 120, 50)
fertilizer_button = pygame.Rect(580, HEIGHT - 80, 120, 50)

def create_strain_buttons(num_strains):
    return [pygame.Rect(40, 100 + i * 60, WIDTH - 80, 50) for i in range(num_strains)]

def draw_button(screen, rect, text, hover):
    color = LIGHT_GRAY if hover else WHITE
    pygame.draw.rect(screen, color, rect)
    pygame.draw.rect(screen, BLACK, rect, 2)
    text_surf = button_font.render(text, True, BLACK)
    text_rect = text_surf.get_rect(center=rect.center)
    screen.blit(text_surf, text_rect)

def draw_menu(screen):
    screen.fill(BLACK)
    title = font.render("Doggyland ChronicChronicles", True, WHITE)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 50))
    draw_button(screen, start_button, "Start Game", False)

def draw_loading_bar(x, y, width, height, progress):
    border_color = WHITE
    fill_color = GREEN
    pygame.draw.rect(screen, border_color, (x, y, width, height), 2)
    fill_width = int(width * progress)
    pygame.draw.rect(screen, fill_color, (x, y, fill_width, height))

def draw_game(screen, player, current_strain, grow_progress, harvest_ready, water_button, fertilizer_button, growing_rate):
    screen.fill(BLACK)
    
    # Left column for text information
    left_margin = 20
    top_margin = 20
    line_height = 40
    
    info_texts = [
        f"Money: ${player.inventory.money}",
        f"Current Strain: {current_strain.name}",
        f"Growth Progress: {grow_progress:.1f}/{current_strain.growth_time}",
        f"Potency: {current_strain.calculate_potency():.1f}%",
        current_strain.get_potency_comparison(),
        f"Yield: {current_strain.yield_amount}g",
        current_strain.get_worth_description()
    ]
    
    for i, text in enumerate(info_texts):
        text_surface = font.render(text, True, WHITE)
        screen.blit(text_surface, (left_margin, top_margin + i * line_height))

    # Draw growth progress bar
    bar_width = 300
    bar_height = 20
    bar_x = left_margin
    bar_y = top_margin + len(info_texts) * line_height + 10
    growth_percentage = grow_progress / current_strain.growth_time
    draw_loading_bar(bar_x, bar_y, bar_width, bar_height, growth_percentage)

    # Right column for plant image
    plant_image = current_strain.get_current_image(grow_progress)
    max_height = HEIGHT - 150  # Leave space for buttons and formula
    max_width = WIDTH // 2  # Use half of the screen width
    scale_factor = min(max_height / plant_image.get_height(), max_width / plant_image.get_width())
    new_width = int(plant_image.get_width() * scale_factor)
    new_height = int(plant_image.get_height() * scale_factor)
    plant_image = pygame.transform.scale(plant_image, (new_width, new_height))
    plant_rect = plant_image.get_rect(midright=(WIDTH - 20, HEIGHT // 2))
    screen.blit(plant_image, plant_rect)

    # Bottom row for buttons
    mouse_pos = pygame.mouse.get_pos()
    draw_button(screen, grow_button, "Grow (G)", grow_button.collidepoint(mouse_pos))
    draw_button(screen, shop_button, "Shop (S)", shop_button.collidepoint(mouse_pos))
    draw_button(screen, water_button, "Water", water_button.collidepoint(mouse_pos))
    draw_button(screen, fertilizer_button, f"Fertilize (x{growing_rate})", fertilizer_button.collidepoint(mouse_pos))

    if harvest_ready:
        draw_button(screen, harvest_button, "Harvest (H)", harvest_button.collidepoint(mouse_pos))

    # Bottom center for formula
    formula_text = font.render("Price = Base Price * Yield * (1 + Potency%)", True, WHITE)
    formula_rect = formula_text.get_rect(centerx=WIDTH // 2, bottom=HEIGHT - 20)
    screen.blit(formula_text, formula_rect)

def draw_shop(screen, strains, strain_buttons):
    screen.fill(BLACK)
    title = font.render("Strain Shop", True, WHITE)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 20))
    for i, strain in enumerate(strains):
        button_rect = strain_buttons[i]
        hover = button_rect.collidepoint(pygame.mouse.get_pos())
        draw_button(screen, button_rect, f"{strain.name} - ${strain.yield_amount}", hover)
    draw_button(screen, back_button, "Back (B)", back_button.collidepoint(pygame.mouse.get_pos()))

strains = [
    Strain("OG Kush", 20.0, 0.1, 60, 400, "A classic strain with a strong, relaxing high.", 
           ["images/og_kush_stage1.png", "images/og_kush_stage2.png", "images/og_kush_stage3.png"], max_height=80, typical_potency=20.0),
    Strain("Blue Dream", 18.0, 0.2, 55, 450, "A balanced hybrid with a sweet berry aroma.", 
           ["images/blue_dream_stage1.png", "images/blue_dream_stage2.png", "images/blue_dream_stage3.png"], max_height=100, typical_potency=18.0),
    Strain("Sour Diesel", 22.0, 0.2, 65, 380, "An energizing sativa with a pungent diesel smell.", 
           ["images/sour_diesel_stage1.png", "images/sour_diesel_stage2.png", "images/sour_diesel_stage3.png"], max_height=120, typical_potency=22.0)
]

strain_buttons = create_strain_buttons(len(strains))

def main():
    global current_state, grow_progress, harvest_ready, current_strain, grow_button_held, growing_rate
    pygame.init()
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
                    elif water_button.collidepoint(event.pos):
                        grow_progress = min(grow_progress + 20, current_strain.growth_time)
                        if grow_progress >= current_strain.growth_time:
                            harvest_ready = True
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
            draw_game(screen, player, current_strain, grow_progress, harvest_ready, water_button, fertilizer_button, growing_rate)
        elif current_state == SHOP:
            draw_shop(screen, strains, strain_buttons)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()