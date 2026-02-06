import pygame

ORANGE = (255, 159, 15)
BLUE = (21, 96, 130)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (224, 15, 0)
LIGHT_GREY = (200, 200, 200)

running = True

def handle_button_toggles()
    # Toggle button function
    pass

#rename function to something less boring    
def main_ui_function(screen, window_width, window_height, width_scale_factor, height_scale_factor):
    pygame.init()
    global graph_mode

    user_screen_width, user_screen_height = screen.get_size()
    ui_window_width = user_screen_width * 0.8
    ui_window_height = user_screen_height * 0.8

    

    font_title = pygame.font.Font(None, int(36 * height_scale_factor))
    font_label = pygame.font.Font(None, int(24 * height_scale_factor))
    font_regular = pygame.font.Font(None, int(22 * height_scale_factor)) 